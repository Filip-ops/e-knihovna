from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

'''app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ptokoocanzqqkx:fae86dd94df17029ffb5c3f6009c8ffedb6323fb56cc2e21e53cb6e88d29e0bf@ec2-34-241-19-183.eu-west-1.compute.amazonaws.com:5432/d655itnumnt7dq'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' '''

app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=False)
