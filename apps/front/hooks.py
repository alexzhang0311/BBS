from flask import session,g,render_template
from .models import FrontUser
from .views import bp
import config

@bp.before_request
def front_before_request():
    if config.USER_ID in session:
        user_tel = session.get(config.USER_ID)
        user = FrontUser.query.filter_by(telephone=user_tel).first()
        if user:
            g.front_user = user

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('front/front_404.html'),404