from flask import Flask, escape, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello_world():
    return 'Hello World!'

# 传递参数

@app.route('/user/<username>')
def profile(username):
    # show the user profile for that user
    # return 'User %s' % escape(username)
    return '{}\'s profile'.format(escape(username))

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)


# 唯一的 URL / 重定向行为
# 区别在于是否在最后有斜杠 / 

@app.route('/projects/')
def projects():
    # 在访问没有斜杠结尾的 URL 时，会自动重定向到斜杠
    return 'The project page'

@app.route('/about')
def about():
    # 在访问有斜杠结尾的 URL 时，会返回 404 错误
    return 'The about page'

# HTTP 方法
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Do the login'
    else:
        return 'Show the login form'

# URL 构建
# 使用 url_for() 来构建 URL，在生产环境中使用的都是绝对路径

with app.test_request_context():
    # 在服务器接收到一个请求时，
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

# 静态文件
# 创建 /static 文件夹
# 例：
# url_for('static', filenemt='style.css')
# 文件位置应该是 static/style.css

# 渲染模板 - Jinja2 模板引擎
from flask import render_template
@app.route('/hello/')
@app.route('/hello/<name>')
def hellon(name=None):
    return render_template('hello.html', name=name)

# 自动转义默认开启。因此，如果 name 包含 HTML ，那么会被自动转义。
# 如果你可以 信任某个变量，且知道它是安全的 HTML （例如变量来自一个把 wiki 标记转换为 HTML 的模块），
# 那么可以使用 Markup 类把它标记为安全的，或者在模板 中使用 |safe 过滤器。更多例子参见 Jinja 2 文档。

from flask import Markup
Markup('<strong>Hello %s!</strong>') % '<blink>hacker</blink>'
# Markup(u'<strong>Hello &lt;blink&gt;hacker&lt;/blink&gt;!</strong>')
Markup.escape('<blink>hacker</blink>')
# Markup(u'&lt;blink&gt;hacker&lt;/blink&gt;')
Markup('<em>Marked up</em> &raquo; HTML').striptags()
# u'Marked up \xbb HTML'

# 请求对象
from flask import request

# @app.route('/login2', methods=['POST', 'GET'])
# def login2():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#     # the code below is executed if the request method was GET or the credentials were invalid
#     return render_template('login.html', error=error)
# 当 form 属性中不存在这个键时会发生什么？会引发一个 KeyError 。 
# 如果你不像捕捉一个标准错误一样捕捉 KeyError ，那么会显示一个 HTTP 400 Bad Request 错误页面。
# 因此，多数情况下你不必处理这个问题。

# 文件上传
# 不要忘记在 HTML 表单中设置 enctype="multipart/form-data" 属性
from flask import request
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/' + secure_filename(f.filename))
# 更好的上传方式参见 https://flask.net.cn/patterns/fileuploads.html#uploading-files

# Cookies
from flask import request, make_response

@app.route('/cookiesr')
def cookiesr():
    # 读取 cookies
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.
    return render_template('hello.html', name=username)

@app.route('/cookiesw')
def cookiesw():
    # 储存 cookies
    resp = make_response(render_template('hello.html'))
    resp.set_cookie('username', 'the username')
    return resp

# 重定向和错误
# 使用 redirect() 函数可以重定向。使用 abort() 可以 更早退出请求，并返回错误代码:
from flask import abort, redirect, url_for
@app.route('/redirect')
def red():
    return redirect(url_for('login3'))

@app.route('/login3')
def login3():
    abort(401)

# 订制出错页面
from flask import render_template

@app.errorhandler(401)
def page_not_found(error):
    return render_template('page_not_found.html'), 401

# 关于响应
# 1. 如果视图返回的是一个响应对象，那么就直接返回它。
# 2. 如果返回的是一个字符串，那么根据这个字符串和缺省参数生成一个用于返回的 响应对象。
# 3. 如果返回的是一个字典，那么调用 jsonify 创建一个响应对象。
# 4. 如果返回的是一个元组，那么元组中的项目可以提供额外的信息。元组中必须至少 包含一个项目，且项目应当由 (response, status) 、 (response, headers) 或者 (response, status, headers) 组成。 status 的值会重载状态代码， headers 是一个由额外头部值组成的列表 或字典。
# 5. 如果以上都不是，那么 Flask 会假定返回值是一个有效的 WSGI 应用并把它转换为 一个响应对象。

# @app.errorhandler(404)
# def not_found(error):
#     return render_template('error.html'), 404
@app.errorhandler(404)
def not_found(error):
    # 对上面简单的 404 返回，可以使用 make_response() 包裹返回表达式，获得响应对象，并对该对象 进行修改，然后再返回:
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

# JSON 格式的 API
@app.route("/me")
def me_api():
    # 简单的字典
    return {
        "username": 'xxia',
        "theme": 'black',
        "image": "user_image",
    }

# @app.route("/users")
# def users_api():
#     # 复杂的过程
#     users = get_all_users()
#     return jsonify([user.to_json() for user in users])


# 会话 Session
# 使用会话之前你必须设置一个密钥
from flask import Flask, session, redirect, url_for, escape, request
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # random bytes

@app.route('/homesession')
def homesession():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/loginsession', methods=['GET', 'POST'])
def loginsession():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('homesession'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logoutsession')
def logoutsession():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('homesession'))


# 如何生成一个好的密钥
# 在控制台运行：
# python -c 'import os; print(os.urandom(16))'


# 消息闪现
# 一个好的应用和用户接口都有良好的反馈，否则到后来用户就会讨厌这个应用。 
# Flask 通过闪现系统来提供了一个易用的反馈方式。
# 闪现系统的基本工作原理是在请求结束时 记录一个消息，提供且只提供给下一个请求使用。通常通过一个布局模板来展现闪现的 消息。
# flash() 用于闪现一个消息。
# 在模板中，使用 get_flashed_messages() 来操作消息。
# 完整的例子参见 https://flask.net.cn/patterns/flashing.html#message-flashing-pattern


# 日志
# 有时候可能会遇到数据出错需要纠正的情况。
# 例如因为用户篡改了数据或客户端代码出错 而导致一个客户端代码向服务器发送了明显错误的 HTTP 请求。
# 多数时候在类似情况下 返回 400 Bad Request 就没事了，但也有不会返回的时候，而代码还得继续运行 下去。
# 以下是一些日志调用示例:

app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')
# logger 是一个标准的 Logger Logger 类， 更多信息详见官方的 logging 文档。
# 更多内容请参阅 https://flask.net.cn/errorhandling.html#application-errors 。


# 集成 WSGI 中间件
# 如果想要在应用中添加一个 WSGI 中间件，那么可以包装内部的 WSGI 应用。假设为了 解决 lighttpd 的错误，你要使用一个来自 Werkzeug 包的中间件，那么可以这样做:
# from werkzeug.contrib.fixers import LighttpdCGIRootFix
# app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
# LighttpdCGIRootFix 已经被取消


# 部署到网络服务器
# https://flask.net.cn/deploying/index.html#deployment



