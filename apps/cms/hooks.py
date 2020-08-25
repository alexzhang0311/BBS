import config
from flask import session,g
from .models import CMSUser #只有直接在项目文件夹下的库才可以直接导入，否则同级的也要加个.
from .views import bp
from .models import CMSPermission

@bp.before_request
def before_request():
        if config.CMS_USER_ID in session:
            user_id = session.get(config.CMS_USER_ID)
            user = CMSUser.query.get(user_id)
            if user:
                g.cms_user = user
###上下文钩子函数中的变量，所有模板均可以使用
@bp.context_processor
def cms_context_process():
    return {"CMSPermission":CMSPermission}