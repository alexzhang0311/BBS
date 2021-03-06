from flask import (Blueprint,views,render_template,
                   request,session,redirect,url_for,
                   g)
from flask_mail import Message
from .forms import (LoginForm,ResetpwdForm,ResetemailForm,AddBannerForm,
                    UpdateBannerForm,DeleteBannerForm,AddBoardForm,UpdateBoardForm,DeleteBoardForm)
from .models import CMSUser,CMSPermission
from .decorates import login_required,permission_required
from exts import db,mail
from utils import restful,cache
import config,string,random,re
from ..models import BannerModel,BoardModel,PostModel,HighlightPostModel
from task import send_mail

from werkzeug.security import check_password_hash
bp = Blueprint('cms',__name__,url_prefix='/cms')

@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')

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
        ###Start异步发送邮件
        send_mail.delay(subject='CMS邮箱验证码', recipients=[email], body=body)  # Celery异步发送
        cache.set(key=email, value=captcha)
        return restful.success(message='邮件发送成功')
        ###END异步发送邮件
        # message = Message(subject='CMS邮箱验证码',recipients=[email],body=body) #同步发送
        # try:
        #     # mail.send(message) #同步发送
        #     cache.set(key=email, value=captcha)
        #     return restful.success(message='邮件发送成功')
        # except:
        #     return restful.server_error(message='邮件发送失败')

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
    posts = PostModel.query.all()
    context={
        "posts":posts
    }
    return render_template('cms/cms_posts.html',**context)

@bp.route('/hpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def hpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('请传入帖子ID')
    else:
        post = PostModel.query.get(post_id)
        if not post:
            return restful.params_error('该帖子不存在')
        else:
            highlight = HighlightPostModel()
            highlight.post = post
            db.session.add(highlight)
            db.session.commit()
            return restful.success('该帖子加精成功')

@bp.route('/unhpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def unhpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('请传入帖子ID')
    else:
        post = PostModel.query.get(post_id)
        if not post:
            return restful.params_error('该帖子不存在')
        else:
            highlight = post.highlight_post[0]
            db.session.delete(highlight)
            db.session.commit()
            return restful.success('取消加精成功')

@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_coments.html')

@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    boards_all = BoardModel.query.all()
    context = {
        'boards':boards_all
    }
    return render_template('cms/cms_boards.html',**context)

@bp.route('/aboard/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        message = form.get_error()
        return restful.params_error(message)

@bp.route('/uboard/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success(message='板块修改成功')
        else:
            return restful.params_error(message='没有这个板块')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dboard/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def dboard():
    # board_id = request.form.get('board_id')
    form = DeleteBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        board = BoardModel.query.get(board_id)
        if board:
            db.session.delete(board)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块')
    else:
        return restful.params_error(message=form.get_error())

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

@bp.route('/banner/')
@login_required
@permission_required(CMSPermission.ADMIN)
def banner():
    banners = BannerModel.query.all()
    return render_template('cms/cms_banner.html',banners=banners)

@bp.route('/abanner/',methods=['POST'])
@login_required
@permission_required(CMSPermission.ADMIN)
def abanner():
    # print(request.form)
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner_db = BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner_db)
        db.session.commit()
        return restful.success(message='轮播图添加成功')
    else:
        message = form.get_error()
        return restful.params_error(message=message)

@bp.route('/ubanner/',methods=['POST'])
@login_required
@permission_required(CMSPermission.ADMIN)
def ubanner():
    # print(request.form)
    form = UpdateBannerForm(request.form)
    if form.validate():
        name = form.name.data
        banner_id = form.banner_id.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url= image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success(message='轮播图修改成功')
        else:
            return restful.params_error(message='轮播图不存在')
    else:
        message = form.get_error()
        return restful.params_error(message=message)

@bp.route('/dbanner/',methods=['POST'])
@login_required
@permission_required(CMSPermission.ADMIN)
def dbanner():
    banner_id = request.form.get('banner_id')
    # print(banner_id)
    form = DeleteBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        banner = BannerModel.query.get(banner_id)
        db.session.delete(banner)
        db.session.commit()
        return restful.success('删除成功')
    else:
        message = form.get_error()
        # print(message)
        return restful.params_error(message=message)

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