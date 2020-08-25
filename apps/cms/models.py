from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class CMSPermission(object):
    #255 二进制的方式来表示1111 1111 admin 权限
    ALL_PERMISSION = 0b11111111
    #1. 访问者权限
    VISITOR        = 0b00000001
    #2. 管理帖子权限
    POSTER = 0b00000010
    #3. 管理评论权限
    COMMENTER = 0b00000100
    #4. 管理板块权限
    BOARDER = 0b00001000
    #5. 管理前台用户的权限
    FRONTUSER = 0b00010000
    #6. 管理后台用户的权限
    CMSUSER = 0b00100000
    #7. 管理员权限
    ADMIN = 0b01000000

cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    db.Column('cms_user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True),
)

class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50),nullable=False)
    desc = db.Column(db.String(200),nullable=True)
    create_time = db.Column(db.DateTime,default=datetime.now)
    permissions = db.Column(db.Integer,default=CMSPermission.VISITOR)
    users = db.relationship('CMSUser',secondary=cms_role_user,backref=db.backref('roles',lazy='dynamic'))

class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,username,password,email):
        self.username = username
        self.password = password #调用@password.setter方法，将password 传给 raw_passord,加密后传给self._password
        self.email = email

    #get 值
    @property
    def password(self):
        return self._password
    #set 值
    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)#self.password 调用@property get self._password 的值 与  raw_password 进行比较
        return result

    # 密码：对外的字段叫做password; 对内的字段叫做_password

    # 按照执行方法的方式设置password
    # user.password('abc')
    # 添加了@password.setter,按照属性的方式设置password
    # user.password = 'abc'

    @property
    def permissions(self):
        if not self.roles:
            return 0 #0代表无权限
        else:
            all_permissions = 0
            for role in self.roles:
                permissions = role.permissions
                all_permissions |= permissions
            return all_permissions

    def has_permission(self,permission):
        return (self.permissions&permission) == permission

    @property
    def is_developer(self):
        return self.has_permission(CMSPermission.ALL_PERMISSION)