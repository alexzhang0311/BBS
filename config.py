import os
from datetime import timedelta
from PIL import Image,ImageDraw,ImageFont
DEBUG = True

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'zlbbs'
USERNAME = 'root'
PASSWORD = 'Zc@2328980'

DB_URL = 'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}?charset=utf8'\
    .format(username=USERNAME,password=PASSWORD,hostname=HOSTNAME,port=PORT,database=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.urandom(24) #项目每次启动会生成一个新的SECRET_KEY，影响session的解析

PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

CMS_USER_ID = 'SDSADAS'
USER_ID='lkjllk'
#邮件配置
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
#MAIL_USE_SSL = True
MAIL_DEBUG = False #默认跟APP的DEBUG状态(app.debug)，APP DEBUG 为True, Mail debug 也为True
MAIL_USERNAME = 'a.l.e.x.03110510@gmail.com'
MAIL_PASSWORD = 'tcoyfsczlryjzicv'
MAIL_DEFAULT_SENDER = MAIL_USERNAME
# MAIL_MAX_EMAILS : default None
# MAIL_SUPPRESS_SEND : default app.testing
# MAIL_ASCII_ATTACHMENTS : default False 附件


