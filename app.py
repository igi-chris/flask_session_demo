import os
from flask import Flask, render_template, session, request
from flask_session import Session
import numpy as np
import pandas as pd
import redis
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
# Check Configuration section for more details
redis_pwd = os.getenv('IGI_ML_REDIS_PWD')
try:
    r = redis.Redis(host="igiml.redis.cache.windows.net", port=6380, 
                    password=redis_pwd, ssl=True)
    SESSION_TYPE = 'redis'
    SESSION_REDIS = r
    r.ping()  # just something to trigger exeception if not connected
except Exception as e:
    print("** Using filesystem session cache as unable to connect to redis **")
    SESSION_TYPE = 'filesystem'

app.config.from_object(__name__)
Session(app)

@app.route("/")
def index() -> str:
    return render_template('index.html', data=session)
        
@app.route('/append/')
def append_session_data():
    for param_name, val in request.args.items():
        if param_name not in session:
            session[param_name] = []
        if val:
            session[param_name].append(val)
    return index()
        
@app.route('/overwrite/')
def overwrite_session_data():
    for param_name, val in request.args.items():
        if val:
            session[param_name] = val
    return index()

@app.route('/create_df_and_model/')
def create_df_and_model():
    ncols = request.args.get("df_n_cols", 5, type=int)
    nrows = request.args.get("df_n_rows", 10, type=int)
    cols = [chr(i+65) for i in range(ncols)]
    
    df = pd.DataFrame(np.random.randint(0,100,size=(nrows, ncols)), columns=cols)
    if 'dfs' not in session:
        session['dfs'] = []
    session[f'dfs'].append(df)

    model = LinearRegression()
    result_func = lambda row: sum([(v * (i%3)) + i for i,v in enumerate(row)])
    results = list(map(result_func, [r.values for _, r in df.iterrows()]))
    model.fit(X=df, y=results)    
    if 'models' not in session:
        session['models'] = []
    session[f'models'].append(model)
    use_models()

    return index()

#@app.route('/predict/')
def use_models():
    # the purpse is just to demonstrate that the objects we get back work, actual numbers are throw away
    # regen all intentially - want the need to get dfs and cache from session and use
    predictions = []
    df: pd.DataFrame
    model: LinearRegression
    for df, model in zip(session["dfs"], session["models"]):
        predictions.append(model.predict(df))
    session["predictions"] = predictions

@app.route('/reset/')
def reset():
    session.clear()
    return index()