from flask import Blueprint,request,make_response
from utils import restful
from utils import cache
from utils.smssender import send_sms
from .forms import SMSCaptchaForm
from io import BytesIO
from utils.captcha import Captcha
bp = Blueprint('common',__name__,url_prefix='/common')

@bp.route('/')
def index():
    return 'commonview'

# @bp.route('/sms_captcha/')
# def sms_captcha():
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(message='请输入手机号码')
#     code = Captcha.gene_text()
#     if send_sms(telphone=telephone,message=code):
#         return restful.success(message='短信发送成功')
#     else:
#         return restful.params_error(message='短信发送失败')

@bp.route('/sms_captcha/',methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        code = Captcha.gene_text()
        if send_sms(telephone=telephone,message=code):
            cache.set(key=telephone, value=code)
            return restful.success(message='短信发送成功')
        else:
            return restful.params_error('短信发送失败')
    else:
        return restful.params_error(message='参数错误')

@bp.route('/captcha/')
def graph_captcha():
    text,image = Captcha.gene_code()
    cache.set(key=text.lower(),value=text.lower())
    out = BytesIO() #数据保存在内存中
    image.save(out,'png')
    out.seek(0) #指针归0
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp
