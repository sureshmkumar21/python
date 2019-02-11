
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from aliceBlue.controllers import aliceBlue_blueprint
from aliceBlue.trade.trade_controllers import trade_blueprint

from aliceBlue.models import User

application = Flask(__name__)
Bootstrap(application)

application.config.from_object('config.DevelopementConfig')
application.register_blueprint(aliceBlue_blueprint)
application.register_blueprint(trade_blueprint)

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "aliceBlue_home.login"

@login_manager.user_loader
def load_user(userid):
    return User(userid)

application.run(host='localhost', port=7001)
