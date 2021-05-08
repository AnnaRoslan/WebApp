from flask_hal import HAL, document
from flask_hal.link import Link
from flask_hal.document import Document, Embedded
from flask_cors import CORS
from flask import Flask, request, render_template,send_from_directory, make_response, session, flash, url_for, g
from dotenv import load_dotenv
from os import getenv
from bcrypt import hashpw,gensalt, checkpw
from flask_session import Session
from datetime import datetime, timedelta
import secrets
from redis import StrictRedis
from jwt import encode, decode
import json
import uuid
import requests
import constants
from authlib.integrations.flask_client import OAuth
from flask_socketio import SocketIO


load_dotenv()
REDIS_HOST = getenv("REDIS_HOST")
REDIS_PASS = getenv("REDIS_PASS")
JWT_SECRET = getenv("JWT_SECRET")
JWT_EXP = int(getenv("JWT_EXP"))

db = StrictRedis(REDIS_HOST, db=20, password=REDIS_PASS)

SESSION_TYPE = "redis"
SESSION_REDIS = db
app = Flask(__name__, static_url_path="/static")
app.config.from_object(__name__)
app.secret_key = secrets.token_urlsafe(32)
CORS(app)
sess = Session(app)

socket_io = SocketIO(app, cors_allowed_origins="*")
CORS(app, resources={r"/*": {"origins": "*"}})
URL = 'https://peaceful-taiga-72510.herokuapp.com'

from six.moves.urllib.parse import urlencode
from functools import wraps

AUTH0_CALLBACK_URL = getenv("AUTH0_CALLBACK_URL")
AUTH0_CLIENT_ID = getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = getenv("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = getenv("AUTH0_DOMAIN")
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = getenv("AUTH0_AUDIENCE")

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


@app.route('/')
def main():
    resp = make_response(render_template('main.html', login = g.user))
    resp.headers['Access-Control-Allow-Origin'] = "https://sheltered-reaches-07912.herokuapp.com"
    return resp

@app.route('/sender/register', methods=["GET"])
def register():
    return render_template('register.html',login = g.user)

@app.route('/sender/register', methods=["POST"])
def register_post():
    firstname = request.form.get('firstname')
    lastname =  request.form.get('lastname')
    email = request.form.get('email')
    password =  request.form.get('password')
    login =  request.form.get('login')
    if  not firstname:
        flash("No first name provided")
    if  not lastname:
        flash("No lastname name provided")
    if  not email:
        flash("No email name provided")
    if  not password:
        flash("No password name provided")
    if  not login:
        flash("No login name provided")

    if email and login and password: 
        if is_user(login):
            flash("user already registred")
            return redirect(url_for('register'))
        
        success = save_user(firstname, lastname, email, password, login)
        if not success:
            flash("Error while sawing user")
            return redirect(url_for('register_form'))

    return redirect(url_for('login'))
    
@app.route('/sender/login', methods=["GET"])
def login():
    return render_template('login.html',login = g.user)

@app.route('/sender/login', methods=["POST"])
def login_post():

    login = request.form.get("login")
    password = request.form.get("password")

    if not login or not password:
        flash("Missing username and/or password")
        return redirect(url_for("login"))
    
    if not verify_user(login, password):
        flash("Invalid username and/or password")
        return redirect(url_for("login"))

    flash(f"Welcome {login}!")
    session["login"] = login
    session["logged_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('main.html', login = login)

@app.route('/sender/logout', methods=["GET"])
def logout():
    session.clear()
    flash("Logged out!")
    params = {'returnTo': url_for('main', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@app.route('/sender/dashboard', methods=["GET"])
def dashboard():
    if g.user is None:
        return'Not authorized', 401
    
    user = g.user
    token = generate_token(user, 'sender')
    return render_template_with_labels(token)

@app.route('/sender/dashboard', methods=["DELETE"])
def dashboard_delete():
    if g.user is None:
        return'Not authorized', 401
    
    user = g.user
    label_id = request.form.get('id')
    if not label_id:
        flash("Cannot delete package")
    
    token = generate_token(user, 'sender')
    response = requests.delete(f"{URL}/sender/labels/{label_id}",headers={'Authorization': token})
    if response.status_code == 200:
        flash("Pacage Deleted!")
        return render_template_with_labels(token)
    else:
        flash(response.text)
        
    return render_template_with_labels(token)
    

@app.route('/sender/dashboard', methods=["POST"])
def dashboard_post():
    if g.user is None:
        return'Not authorized', 401
    user = g.user

    token = generate_token(user, 'sender')

    response = requests.post(f"{URL}/sender/labels",headers={'Authorization': token})
    if response.status_code == 200:
            flash(f"New Pacage Created!")
    else:
       return  make_response(response.text ,response.status_code )

    return render_template_with_labels(token)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session["login"] = userinfo['email']
    session["logged_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    flash(f"Welcome {userinfo['email']}!")
    return redirect(url_for("main"))

@app.route('/authLogin')
def authLogin():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


def render_template_with_labels(token):
    response = requests.get(f"{URL}/sender/labels",headers={'Authorization': token})
    if response.status_code == 200:
        labels = response.json()['_embedded']['items']
        return render_template('dashboard.html',labels=labels,login = g.user)
    
    return make_response(response.text ,response.status_code )

@app.before_request
def get_logged_username():
    g.user = session.get('login')

def redirect(url, status=301):
    response = make_response("", 301)
    response.headers["Location"] = url
    return response

def is_user(login):
    return db.hexists(f"user:{login}", "password")

def save_user(firstname, lastname, email, password, login):
    hashed_password = hashpw(password.encode('utf-8'), gensalt(4))
    db.hset(f"user:{login}", "firstname", firstname)
    db.hset(f"user:{login}", "lastname", lastname)
    db.hset(f"user:{login}", "email", email)
    db.hset(f"user:{login}", "password", hashed_password)

    db.hset('users', f'login_{login}',f'{login}')
    return True

def verify_user(login, password):
    passwd = password.encode('utf-8')
    hashed = db.hget(f"user:{login}", "password")
    if not hashed:
       
        return False
    return checkpw(passwd, hashed)
    
def generate_token(user,user_role):
    payload = {
        "usr": user,
        "user_role": user_role,
        "aud":"aud",
        "exp": datetime.utcnow() + timedelta(seconds=JWT_EXP)
    }
    token = encode(payload, JWT_SECRET, algorithm='HS256')
    return token

if __name__ == '__main__':
    app.run(threaded=True, port=5001, debug=True)



