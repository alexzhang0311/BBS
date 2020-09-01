from wtforms import StringField,IntegerField,ValidationError
from wtforms.validators import Email,InputRequired,Length,EqualTo
from apps.forms import BaseForm
from utils import cache
from flask import g
from apps.cms.models import  CMSUser
# from ..forms import BaseForm

#BaseForm 为父类，继承自Form

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确邮箱格式'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,20,message='请输入正确格式的密码')])
    remember = IntegerField()

class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message='请输入正确格式的旧密码')])
    newpwd = StringField(validators=[Length(6,20,message='请输入正确格式的新密码')])
    newpwd2 = StringField(validators=[EqualTo("newpwd",message='两次密码输入不同')])

class ResetemailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱'),InputRequired(message='请输入邮箱')])
    captcha = StringField(validators=[Length(min=6,max=6,message='验证码格式错误')])
    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_cache = cache.get(key=email)
        if not (captcha_cache and (captcha_cache.lower() == captcha.lower())):
            raise ValidationError('验证码错误')
        # try:
        #     if not (captcha_cache or (captcha.lower() == captcha_cache.lower())):
        #     # if not captcha:
        #         raise ValidationError('验证码错误')
        #         # raise ValidationError(captcha_cache.lower())
        # except:
        #     raise ValidationError('输入信息有误！请检查')

    def validate_email(self,field):
        email = field.data
        user = g.cms_user
        if email == user.email:
            raise ValidationError('新邮箱不能与现有邮箱一样啦！')

class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级')])

class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图ID')])

class DeleteBannerForm(BaseForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图ID')])