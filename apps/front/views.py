from flask import (
    Blueprint,views,render_template,
    make_response,request,session,
    redirect,url_for)
from .forms import SignupForm,SigninForm
from utils import restful,safeutils
from exts import db
from .models import FrontUser
from .decorates import login_required
import config
bp = Blueprint('front',__name__,url_prefix='/front')
@bp.route('/')
# @login_required
def index():
    return render_template('front/front_index.html')

# @bp.route('/test/')
# def test():
#     return render_template('front/front_test.html')

class SigninView(views.MethodView):
    def get(self,message=None):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for('front.signup') and safeutils.is_safe_url('front/front_signin.html'):
            return render_template('front/front_signin.html',return_to=return_to)
        else:
            return render_template('front/front_signin.html')
        # return render_template('front/front_signin.html',message=message)
    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            print(remember)
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.USER_ID] = user.telephone
                if remember == 'true' :
                    session.permanent = True
                return restful.success(message='登陆成功')
                # return redirect(url_for('front.index'))
            else:
                return restful.params_error(message='号码或密码错误')
                # return self.get(message='号码或密码错误')
        else:
            message = form.get_error()
            # return self.get(message=message)
            return restful.params_error(message=message)


class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        # print(return_to,request.host_url) http://127.0.0.1:8000/front/ http://127.0.0.1:8000/
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html',return_to=return_to)
        else:
            return render_template('front/front_signup.html')
    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = FrontUser(telephone=telephone,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success(message='注册成功')
        else:
            return restful.params_error(message=form.get_error())


# print(Captcha.gene_code())

bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/',view_func=SigninView.as_view('signin'))