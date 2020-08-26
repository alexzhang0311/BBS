from flask import (Blueprint,views,render_template,make_response,request)
from .forms import SignupForm
from utils import restful
from exts import db
from .models import FrontUser
bp = Blueprint('front',__name__,url_prefix='/front')
@bp.route('/')
def index():
    return 'front index'

class SignupView(views.MethodView):
    def get(self):
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