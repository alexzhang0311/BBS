from flask import (Blueprint,views,render_template,
                   request,session,redirect,url_for,
                   g)
from flask_mail import Message
from .forms import LoginForm,ResetpwdForm,ResetemailForm
from .models import CMSUser,CMSPermission
from .decorates import login_required,permission_required
from exts import db,mail
from utils import restful,cache
import config,string,random,re

from werkzeug.security import check_password_hash
bp = Blueprint('cms',__name__,url_prefix='/cms')

@bp.route('/')
@login_required
def index():
    return render_template('cms/cmd_index.html')

@bp.route('/email_captcha/') #修改邮箱验证码接口
@login_required
def email_captcha():
    email = request.args.get('email')
    email_check = re.compile(r'^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$')
    form = email_check.search(email)
    if not form:
        return restful.params_error(message='请输入正确的邮箱格式')
    else:
        source = list(string.ascii_letters) #产生一个小写a-z&大写A-Z的字符串,转变为列表
        #source.extend([str(i) for i in range(10)])
        #source.extend(map(str,range(10)))
        source.extend(map(lambda x:str(x),range(10)))
        captcha = ''.join(random.sample(source,6)) #source中随机取6位作为验证码,通过join列表转字符串
        body = 'Dear %s,\n\n  Please note your Captcha is: %s \n\nBR,\nCMS Team' % (g.cms_user.username,captcha)
        message = Message(subject='CMS邮箱验证码',recipients=[email],body=body)
        try:
            mail.send(message)
            cache.set(key=email, value=captcha)
            return restful.success(message='邮件发送成功')
        except:
            return restful.server_error(message='邮件发送失败')

@bp.route('/logout/')
@login_required
def logout():
    #session.clear()
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))

@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')

@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    return render_template('cms/cms_posts.html')

@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_coments.html')

@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    return render_template('cms/cms_boards.html')

@bp.route('/frontuser/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def frontuser():
    return render_template('cms/cms_frontuser.html')

@bp.route('/users/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def users():
    return render_template('cms/cms_users.html')

@bp.route('/groups/')
@login_required
@permission_required(CMSPermission.ADMIN)
def groups():
    return render_template('cms/cms_groups.html')


class ResetEmail(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')
    def post(self):
        form = ResetemailForm(request.form)
        #print(request.form)
        if form.validate():
            email = form.email.data
            # existed_email = CMSUser.query.filter_by(email=email).first()
            existed_email = [i.email for i in CMSUser.query.all()]  #保证数据库中至少有一个用户
            # if not existed_email:
            if not (email in existed_email):
                g.cms_user.email = email
                db.session.commit()
                return restful.success('邮箱更改成功')
            else:
                return restful.server_error(message='该邮箱已存在')
        else:
            message = form.get_error()
            return restful.server_error(message)

class ResetPassword(views.MethodView):
    decorators = [login_required]
    def get(self,message=None):
        return render_template('cms/cms_reset.html',message=message)
    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            newpwd = form.newpwd.data
            oldpwd = form.oldpwd.data
            user = g.cms_user
            if newpwd != oldpwd:
                if user.check_password(oldpwd):
                    user.password = newpwd
                    db.session.commit()
                    #{"code":200,message="密码错误"}
                    return restful.success(message="密码修改成功") ###前端ajax,因此要返回json
                else:
                    return restful.params_error(message='现有密码错误') ###400代表参数错误
            else:
                return restful.params_error(message='新密码不可与旧密码相同')
        else:
            # message = form.errors.popitem()[1][0]
            message = form.get_error()
            return restful.server_error(message=message)

class LoginView(views.MethodView):
    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter(CMSUser.email == email).first()
            # print(user._password)
            # print(password)
            # print(check_password_hash(user._password,password))
            if user and user.check_password(raw_password=password):#check_password_hash(user._password,password)
                session[config.CMS_USER_ID] = user.id
                if remember == 1:
                    session.permanent = True #默认31天过期,在config中可以更改
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或密码错误')

        else:
            #print(form.errors)
            #message = form.errors.popitem()[1][0]
            message = form.get_error()
            #return self.get(message=message) #self.get()重新渲染登录模板
            return self.get(message=message)

bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetPassword.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmail.as_view('resetemail'))


#后端与前端交互
##wiki
#url:http://www.xxx.com/resetpwd/
#param {xxx}
#method = POST&GET