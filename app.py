from flask import Flask, render_template, session, request, jsonify
from flask_session import Session
import os
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

@app.route("/", methods=['GET'])
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

@app.route('/get/', methods=['GET'])
def get():
    return jsonify(session)

@app.route('/reset/')
def reset():
    session.clear()
    return index()