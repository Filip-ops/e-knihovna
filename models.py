from datetime import datetime
from sqlalchemy.orm import backref
#import db, login_manager
from flask_login import UserMixin
from flask_login import current_user

'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)'''