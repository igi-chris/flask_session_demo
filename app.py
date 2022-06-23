import imp
import os
from flask import Flask, render_template, session, request, jsonify
from flask_session import Session
import numpy as np
import pandas as pd
from pyparsing import col
import redis

app = Flask(__name__)
# Check Configuration section for more details
redis_pwd = os.getenv('IGI_ML_REDIS_PWD')
SESSION_TYPE = 'redis'
r = redis.Redis(host="igiml.redis.cache.windows.net", port=6380, 
                password=redis_pwd, ssl=True)
SESSION_REDIS = r
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

@app.route('/create_df/')
def create_df():
    ncols = request.args.get("df_n_cols", 5, type=int)
    nrows = request.args.get("df_n_rows", 10, type=int)
    cols = [chr(i+65) for i in range(ncols)]
    
    ndfs = sum(1 for val in session.values() if isinstance(val, pd.DataFrame))
    df = pd.DataFrame(np.random.randint(0,100,size=(nrows, ncols)), columns=cols)
    session[f'df_{ndfs}'] = df
    return index()

@app.route('/get/', methods=['GET'])
def get():
    return jsonify(session)

@app.route('/reset/')
def reset():
    session.clear()
    return index()