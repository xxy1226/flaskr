##########
# 蓝图和视图
##########

# 视图是一个应用对请求进行响应的函数。 
# Flask 通过模型把进来的请求 URL 匹配到 对应的处理视图。
# 视图返回数据， Flask 把数据变成出去的响应。 Flask 也可以反 过来，根据视图的名称和参数生成 URL 。

#####
# 创建蓝图
#####

# Blueprint 是一种组织一组相关视图及其他代码的方式。
# 与把视图及其他代码直接注册到应用的方式不同，蓝图方式是把它们注册到蓝图，然后在工厂函数中把蓝图注册到应用。

# Flaskr 有两个蓝图，一个用于认证功能，另一个用于博客帖子管理。
# 每个蓝图的代码 都在一个单独的模块中。
# 使用博客首先需要认证，因此我们先写认证蓝图。

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# 这里创建了一个名称为 'auth' 的 Blueprint 。
# 和应用对象一样， 蓝图需要知道是在哪里定义的，因此把 __name__ 作为函数的第二个参数。 
# url_prefix 会添加到所有与该蓝图关联的 URL 前面。

# --> __init__.py

#####
# 第一个视图：注册
#####

# 当用访问 /auth/register URL 时， register 视图会返回用于填写注册内容的表单的 HTML 。
# 当用户提交表单时，视图会验证表单内容，然后要么 再次显示表单并显示一个出错信息，要么 创建新用户并显示登录页面。

# 这里是视图代码，下一页会写生成 HTML 表单的模板。

@bp.route('/register', methods={'GET', 'POST'})
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    return render_template('auth/register.html')

# 这个 register 视图做了以下工作：

