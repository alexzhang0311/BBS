from celery import Celery
# from zlbbs import create_app #出现循环导入问题
from flask import Flask
from flask_mail import Message
from exts import mail
from utils.smssender import send_sms
import config
# celery = Celery("tasks",broker="redis://:Zc@2328980@192.168.110.2:6379/0",backend="redis://:Zc@2328980@192.168.110.2:6379/0")

app = Flask(__name__)
app.config.from_object(config)
mail.init_app(app=app) #需要初始化才可以读取到config中对于email的配置

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app=app)

@celery.task
def send_mail(subject,recipients,body):
    message = Message(subject=subject,recipients=recipients,body=body)
    mail.send(message)


@celery.task
def send_sms_captcha(telephone,message):
    send_sms(telephone,message)

### ImportError: cannot import name 'bp' 报错说明出现了循环导入的问题
### cms,app ==> zlbbs ==> taks ==> cms.app
### 运行worker:celery -A task.celery worker --pool=eventlet --loglevel=INFO