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


# 当 Flask 收到一个指向 /auth/register 的请求时就会调用 register 视图并把其返回值作为响应。
@bp.route('/register', methods={'GET', 'POST'})
def register():
    
    # 如果用户提交了表单，那么 request.method 将会是 'POST' 。
    # 然后开始验证用户的输入内容。
    if request.method == 'POST':
        
        # request.form 是一个特殊类型的 dict
        # 其映射了提交表单的键和值。表单中，用户将会输入其 username 和 password 。
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # 验证 username 和 password 不为空。
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        # 通过查询数据库，检查是否有查询结果返回来验证 username 是否已被注册
        if error is None:
            try:
                
                # db.execute 使用了带有 ? 占位符 的 SQL 查询语句。
                # 占位符可以代替后面的元组参数中相应的值。
                # 使用占位符的 好处是会自动帮你转义输入值，以抵御 SQL 注入攻击 。
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    # 为了安全起见，永远不要将密码直接存储在数据库中。
                    # 相反，generate_password_hash() 用于安全地散列密码，并存储该散列。
                    # 这不能阻挡字典攻击
                    (username, generate_password_hash(password)),
                )
                # 由于此查询修改了数据，因此之后需要调用 db.commit() 来保存更改。
                db.commit()
                
            # 如果用户名已经存在，将出现 sqlite3.IntegrityError，这应该作为另一个验证错误显示给用户。
            except db.IntegrityError:
                error = f"User {username} is already registered."
                
            # 存储用户后，他们将被重定向到登录页面。 
            # url_for() 根据其名称生成登录视图的 URL。 
            # 这比直接编写 URL 更可取，因为它允许您稍后更改 URL 而无需更改链接到它的所有代码。 
            # redirect() 生成对生成的 URL 的重定向响应。
            else:
                return redirect(url_for("auth.login"))
            
        # 如果验证失败，则向用户显示错误。 flash() 存储在呈现模板时可以检索的消息。
        flash(error)
        
    # 当用户最初导航到 auth/register 时，或者出现验证错误时，应显示带有注册表单的 HTML 页面。
    # render_template() 将呈现一个包含 HTML 的模板。
    return render_template('auth/register.html')

#####
# 登录
#####

# 这个视图和上述 register 视图原理相同。

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        # 与 register 有以下不同之处：首先需要查询用户并存放在变量中，以备后用。
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        
        if user is None:
            error = 'Incorrect username.'
            
        # check_password_hash() 以相同的方式哈希提交的 密码并安全的比较哈希值。
        # 如果匹配成功，那么密码就是正确的。
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            
        if error is None:
            
            # session 是一个 dict ，它用于储存横跨请求的值。
            # 当验证 成功后，用户的 id 被储存于一个新的会话中。
            # 会话数据被储存到一个 向浏览器发送的 cookie 中，在后继请求中，浏览器会返回它。
            # Flask 会安全对数据进行 签名 以防数据被篡改。
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)
        
    return render_template('auth/login.html')

# 现在用户的 id 已被储存在 session 中，可以被后续的请求使用。
# 请每个请求的开头，如果用户已登录，那么其用户信息应当被载入，以使其可用于 其他视图。
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
#####
# 注销
#####

# 注销的时候需要把用户 id 从 session 中移除。 
# 然后 load_logged_in_user 就不会在后继请求中载入用户了。

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#####
# 在其他视图中验证
#####

# 用户登录以后才能创建、编辑和删除博客帖子。在每个视图中可以使用 装饰器 来完成这个工作。

def login_required(view):
    
    # 装饰器返回一个新的视图，该视图包含了传递给装饰器的原视图。
    # 新的函数检查用户 是否已载入。
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        
        # 如果已载入，那么就继续正常执行原视图，否则就重定向到登录页面。 
        # 我们会在博客视图中使用这个装饰器。
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view

# url_for() 函数根据名称和参数生成视图的 URL。 
# 它与视图关联的名称也称为端点 Endpoints ，默认情况下它与视图函数的名称相同。
# 例如，前文被加入应用工厂的 hello() 视图端点为 'hello' ，可以使用 url_for('hello') 来连接。
# 如果视图有参数，后文会看到，那么可使用 url_for('hello', who='World') 连接。
# 当使用蓝图的时候，蓝图的名称会添加到函数名称的前面。
# 上面的 login 函数 的端点为 'auth.login' ，因为它已被加入 'auth' 蓝图中。