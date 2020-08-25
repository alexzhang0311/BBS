from functools import wraps
from flask import session,redirect,url_for,g
import config
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        user_id = session.get(config.CMS_USER_ID)
        if user_id: #if config.CMS_USER_ID in session
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))
    return wrapper


def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args,**kwargs):
            cms_user = g.cms_user
            if cms_user.has_permission(permission):
                return func(*args,**kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inner
    return outter
