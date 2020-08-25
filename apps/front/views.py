from flask import (Blueprint,views,render_template,make_response)
bp = Blueprint('front',__name__,url_prefix='/front')
@bp.route('/')
def index():
    return 'front index'

class SignupView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')
    def post(self):
        pass

# print(Captcha.gene_code())

bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))