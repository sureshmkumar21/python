
from flask import Flask, Blueprint, render_template, session, redirect, request, url_for
from flask_login import login_user, logout_user
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
from flask.json import jsonify

from aliceBlue.models import User

application = Flask(__name__)
application.config.from_object('config.DevelopementConfig')

aliceBlue_blueprint = Blueprint('aliceBlue_home', __name__, template_folder='templates', static_folder='static')

redirect_url = ""

@aliceBlue_blueprint.route('/')
def home():
    return render_template("home.html")

@aliceBlue_blueprint.route('/login', methods=["GET", "POST"])
def login():
    aliceBlue = OAuth2Session(application.config['CLIENT_ID'])
    authorization_url, state = aliceBlue.authorization_url(application.config['AUTHORIZATION_BASE_URL'])
    session['oauth_state'] = state
    user = User(application.config['CLIENT_ID'])
    authorization_url = authorization_url + "&redirect_uri=" + application.config['REDIRECT_URI']
    login_user(user)
    
    return redirect(authorization_url)

@aliceBlue_blueprint.route("/callback", methods=["GET"])
def callback():
    aliceBlue = OAuth2Session(application.config['CLIENT_ID'], state=session['oauth_state'])
    
    all_args = request.args.to_dict()
    code = all_args['code']
    headers = {'Accept':'application/json'}
    auth = HTTPBasicAuth(application.config['CLIENT_ID'], application.config['CLIENT_SECRET'])
    
    body = 'grant_type=authorization_code&code=' + code + '&redirect_uri=' + application.config['REDIRECT_URI']
    token = aliceBlue.fetch_token(application.config['TOKEN_URL'], code=code, auth=auth, body=body, headers=headers)
    session['oauth_token'] = token
    
    return redirect(url_for('trade_home.trade'))

@aliceBlue_blueprint.route("/profile", methods=["GET"])
def profile():
    aliceBlue = OAuth2Session(application.config['CLIENT_ID'], token=session['oauth_token'])
    return jsonify(aliceBlue.get('https://ant.aliceblueonline.com/api/v2/profile').json())

@aliceBlue_blueprint.route("/logout")
def logout():
    logout_user()
    return render_template("home.html")
