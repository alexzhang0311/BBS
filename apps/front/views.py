from flask import (
    Blueprint,views,render_template,
    make_response,request,session,
    redirect,url_for,g,abort)
from flask_paginate import Pagination, get_page_parameter
from .forms import SignupForm,SigninForm,AddPostForm,AddCommentForm
from utils import restful,safeutils
from exts import db
from .models import FrontUser
from ..models import BannerModel,BoardModel,PostModel,CommentModel,HighlightPostModel
from .decorates import login_required
from sqlalchemy import func
import config
bp = Blueprint('front',__name__,url_prefix='/front')
@bp.route('/')
# @login_required
def index():
    sort = request.args.get("st",type=int,default=1)
    board_id = request.args.get('bd',type=int,default=None)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    banners = BannerModel.query.order_by(BannerModel.priority.asc()).limit(4)
    boards = BoardModel.query.all()
    # posts = PostModel.query.all()
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    posts = None
    total = 0
    query_obj = None
    if sort == 1:
        # st=1 按照时间倒序排序
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        # st=2 按照加精时间倒序排序
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(HighlightPostModel.create_time.desc(),PostModel.create_time.desc())
    elif sort == 3:
        # st=3 按照点赞数量排序
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        # st=4 按照评论数量排序
        query_obj = db.session.query(PostModel).join(CommentModel).group_by(PostModel.id).order_by(func.count(CommentModel.id).desc(),PostModel.create_time.desc())
    if board_id:
        # query_obj = query_obj.filter_by(board_id=board_id)
        query_obj = query_obj.filter(PostModel.board_id==board_id)
        print(query_obj)
        posts = query_obj.slice(start,end)
        total = query_obj.count()
    else:
        # query_obj = PostModel.query.order_by(PostModel.create_time.desc())
        posts = query_obj.slice(start,end)
        total = query_obj.count()
    pagination = Pagination(bs_version=3,page=page,total=total,outer_window=0)
    # print(boards)
    context = {
        'banners':banners,
        'boards':boards,
        'posts':posts,
        'pagination':pagination,
        'current':board_id,
        'current_sort': sort
    }
    return render_template('front/front_index.html',**context)

# @bp.route('/test/')
# def test():
#     return render_template('front/front_test.html')

@bp.route('/p/<post_id>')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    else:
        if hasattr(g,'front_user'):
            front_user = g.front_user
        else:
            front_user = None
        return render_template('front/front_pdetail.html',post=post,user=front_user)

@bp.route('/acomment/',methods = ['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success('评论添加成功')
    else:
        return restful.params_error(form.get_error())


@bp.route('/logout/')
@login_required
def logout():
    del session[config.USER_ID]
    return redirect(url_for('front.signin'))

@bp.route('/apost/',methods=['GET','POST'])
@login_required
def apost():
    if request.method=='GET':
        boards = BoardModel.query.all()
        context = {
            'boards':boards
        }
        return render_template('front/front_apost.html',**context)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            user_id = session.get(config.USER_ID)
            author = FrontUser.query.filter_by(telephone=user_id).first()
            if not board:
                return restful.params_error(message='板块不存在')
            post = PostModel(title=title,content=content)
            post.board = board
            post.author = author
            db.session.add(post)
            db.session.commit()
            return restful.success(message='帖子添加成功')
        else:
            return restful.params_error(form.get_error())


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
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.USER_ID] = user.telephone
                if remember == 'true':
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