# ━━━━━━神兽出没━━━━━━ 
# 　　　 ┏┓　　　┏┓
# 　　┏┛┻━━━┛┻┓ 
# 　　┃　　　　　　　┃ 
# 　　┃　　　━　　　┃ 
# 　　┃　┳┛　┗┳　┃ 
# 　　┃　　　　　　　┃ 
# 　　┃　　　┻　　　┃ 
# 　　┃　　　　　　　┃ 
# 　　┗━┓　　　┏━┛Code is far away from bug with the animal protecting 
# 　　　　┃　　　┃    神兽保佑,代码无bug 
# 　　　　┃　　　┃ 
# 　　　　┃　　　┗━━━┓ 
# 　　　　┃　　　　　　　┣┓ 
# 　　　　┃　　　　　　　┏┛ 
# 　　　　┗┓┓┏━┳┓┏┛ 
# 　　　　　┃┫┫　┃┫┫ 
# 　　　　　┗┻┛　┗┻┛ 
# ━━━━━━神兽出没━━━━━━

from flask import Blueprint, request, render_template, flash, redirect
from flask_login import login_user, logout_user, login_required, current_user

from apps.account.models import User
from apps.config import BLUEPRINT_ACCOUNT_KEY
from apps.ext import lm, db

account = Blueprint(BLUEPRINT_ACCOUNT_KEY, __name__, template_folder='templates')


# 插件必须要求实现的方法,session获取用户的对象
@lm.user_loader
def load_user(uid):
    return User.query.get(uid)


"""
login_user
login_out
login_required
current_user
"""
"""
一种直接通过输入/login/
另外一种 通过验证方法调转

"""


# 四个插件
@account.route('/login/', methods=['get', 'post'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.values.get('username')
        password = request.values.get('password')
        users = User.query.filter(User.username == username)
        if users:
            if users.first() and users.first().is_active == 0:
                user = users.first()
                if user.verify_password(password):
                    login_user(user, remember=True)
                    return '登录成功'
                else:
                    return render_template('login.html', msg="用户名或者密码错误")
                # 提示用户名或者密码错误
            else:
                return render_template('login.html', msg="用户未激活,请与管理员联系")
                # 表示用户未激活,请与管理员联系
        else:
            return render_template('login.html', msg="用户名不存在")


@account.route('/register/', methods=['get', 'post'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.values.get('username')
        password = request.values.get('password')
        user = User.query.filter(User.username == username).first()
        if user:
            return render_template('register.html', msg='用户存在,请重新注册')
        else:
            user = User(username=username)
            user.password = password
            db.session.add(user)
            db.session.commit()
    return render_template('register.html', msg='注册成功')


@account.route('/logout/')
@login_required
def logout():
    logout_user()
    return '登出成功'


@account.route('/paginate/')
def paginate():
    page = request.values.get('page')
    size = request.values.get('size')
    pagination = User.query.paginate(page=page, per_page=size, error_out=False)
    return render_template('macro.html', pagination=pagination)
