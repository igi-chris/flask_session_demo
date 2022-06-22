from flask import Flask, render_template, session, request, jsonify
from flask_session import Session

app = Flask(__name__)
# Check Configuration section for more details
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/set/')
def set():
    for param_name, val in request.args.items():
        if param_name not in session:
            session[param_name] = []
        if val:
            session[param_name].append(val)
    return index()

@app.route('/get/')
def get():
    return jsonify(
        key1=session.get("key1", []),
        key2=session.get("key2", []),
        key3=session.get("key3", []))

@app.route("/", methods=['GET'])
def index() -> str:
    return render_template('index.html')

@app.route('/reset/')
def reset():
    for param_name in request.args.keys():
        session[param_name] = []
    return get()
