from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from zlbbs import create_app
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
app = create_app()
manager = Manager(app=app)
FrontUser = front_models.FrontUser
CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSRoleUser = cms_models.cms_role_user
CMSPermission = cms_models.CMSPermission
Migrate(app,db)

manager.add_command('db',MigrateCommand)

@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')

def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功')

@manager.option('-e','--email',dest='email')
@manager.option('-r','--role',dest='name')
def add_role2user(email,name):
    user = CMSUser.query.filter(CMSUser.email==email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户添加角色成功')
        else:
            print('%s角色不存在'%name)
    else:
        print('%s该邮箱不存在'%email)


@manager.option('-e','--email',dest='email')
@manager.option('-r','--role',dest='name')
def del_role2user(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        #user_role = user.roles.filter_by(name=name).all()
        user_role = user.roles.filter_by(name=name).first()
        # print(user_role.name) # user_role为list
        #print(user_role[0].name) # user_role为list,对应.all()
        if user_role:
            role = CMSRole.query.filter_by(name=name).first()
            user.roles.remove(role)
            db.session.commit()
            print('%s邮箱%s权限删除成功'%(email,name))
        else:
            print('%s该邮箱不存在%s权限'%(email,name))
    else:
        print('%s该邮箱不存在' % email)

@manager.option('-e','--email',dest='email')
def check_role(email):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        user_roles = user.roles.all()
        if user_roles:
            for user_role in user.roles.all():
                print('%s该邮箱权限为：%s'%(email,user_role.name))
        else:
            print('%s该邮箱不存在任何权限' % email)
    else:
        print('%s该邮箱不存在' % email)


@manager.option('-u','--username',dest='username')
def delete_cms_user(username):
    user =CMSUser.query.filter(CMSUser.username==username).first()
    db.session.delete(user)
    db.session.commit()
    print('cms用户%s删除成功'%user)

@manager.command
def create_role():
    #访问者
    vistor = CMSRole(name='游客',desc='访问权限，无修改权限')
    vistor.permissions = CMSPermission.VISITOR
    #运营角色
    operator = CMSRole(name='运营',desc='管理前台用户，帖子，评论')
    operator.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER
    #管理员角色(拥有大部分权限，不同admin之间不可以修改对方的权限)
    admin = CMSRole(name='管理员',desc='本系统所有权限')
    admin.permissions=CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.BOARDER|CMSPermission.FRONTUSER|CMSPermission.CMSUSER
    #开发者(拥有全部权限)
    developer = CMSRole(name='开发者',desc='本系统所有权限')
    developer.permissions=CMSPermission.ALL_PERMISSION

    db.session.add_all([vistor,operator,admin,developer])
    db.session.commit()

@manager.command
def test_permission():
    user = CMSUser.query.first()
    if user.has_permission(CMSPermission.VISITOR):
        print('该用户有游客权限')
    else:
        print('该用户无游客权限')


###前端用户
@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')

def create_user(telephone,username,password):
    frontuser = FrontUser(username=username,password=password,telephone=telephone)
    db.session.add(frontuser)
    db.session.commit()
    print('添加用户成功')



if __name__ == '__main__':
    manager.run()