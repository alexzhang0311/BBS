from wtforms import StringField,ValidationError,IntegerField
from wtforms.validators import Regexp,EqualTo,InputRequired
from ..forms import BaseForm
from utils import cache

class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"^9204\d{4}$",message='请输入正确格式的手机号码')])
    sms_captcha = StringField(validators=[Regexp(r"\w{4}",message='请输入正确格式验证码')])
    username = StringField(validators=[Regexp(r".{2,20}",message='请输入正确格式用户名')])
    password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.@]{6,20}",message='请输入正确格式的密码')])
    password2 = StringField(validators=[EqualTo('password1',message='两次输入的密码不一致')])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}",message='请输入正确格式短信验证码')])

    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        telephone = self.telephone.data
        sms_captcha_mem = cache.get(key=telephone)
        #print("sms_captcha",sms_captcha)
        #print("sms_captcha_mem",sms_captcha_mem)
        # if sms_captcha != '1111':
        if not sms_captcha_mem or sms_captcha_mem.lower() != sms_captcha.lower():
            raise ValidationError(message='短信验证码错误')

    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        #print(graph_captcha)
        #print(cache.get(key=graph_captcha.lower()))
        # if graph_captcha != '1111':
        if not cache.get(key=graph_captcha.lower()):
            raise ValidationError(message='图形验证码错误')

class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'^9204\d{4}$',message='请输入正确格式的号码')])
    password = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.@]{6,20}',message='请输入正确格式的密码')])
    remember = StringField()

class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题')])
    content = StringField(validators=[InputRequired(message='请输入内容')])
    board_id = IntegerField(validators=[InputRequired(message='请输入板块ID')])

class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入评论内容')])
    post_id = StringField(validators=[InputRequired(message='请输入帖子ID')])