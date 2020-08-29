from functools import wraps
from flask import session,redirect,url_for,g
import config
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        user_id = session.get(config.USER_ID)
        if user_id: #if config.USER_ID in session
            return func(*args,**kwargs)
        else:
            return redirect(url_for('front.signin'))
    return wrapper
