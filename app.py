from flask import Flask, render_template, session, request, jsonify
from flask_session import Session
import os
import redis
import json

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
    raw_data = get().data.decode('utf-8')
    session_state = json.loads(raw_data)
    return render_template('index.html', data=session_state)

@app.route('/get/', methods=['GET'])
def get():
    return jsonify(
        key1=session.get("key1", []),
        key2=session.get("key2", []),
        key3=session.get("key3", []))
        
@app.route('/set/')
def set():
    for param_name, val in request.args.items():
        if param_name not in session:
            session[param_name] = []
        if val:
            session[param_name].append(val)
    return index()

# @app.route('/reset/')
# def reset():
#     for param_name in request.args.keys():
#         session[param_name] = []
#     return get()
