##########
# 本教程中我们将会创建一个名为 Flaskr 的具备基本功能的博客应用。
# 应用用户可以 注册、登录、发贴和编辑或者删除自己的帖子。可以打包这个应用并且安装到其他电脑上。
##########

#####
# 项目布局
#####
# $ mkdir tutorial
# $ cd tutorial
# (Windows)
# $ $env:FLASK_APP = "tutorial"

# 教程项目包含如下内容:
# * flaskr/ ，一个包含应用代码和文件的 Python 包。
# * tests/ ，一个包含测试模块的文件夹。
# * venv/ ，一个 Python 虚拟环境，用于安装 Flask 和其他依赖的包。
# * 告诉 Python 如何安装项目的安装文件。
# * 版本控制配置，如 git 。不管项目大小，应当养成使用版本控制的习惯。
# * 项目需要的其他文件。

#####
# /path/to/root/folder
# ├── flaskr/
# │   ├── __init__.py
# │   ├── db.py
# │   ├── schema.sql
# │   ├── auth.py
# │   ├── blog.py
# │   ├── templates/
# │   │   ├── base.html
# │   │   ├── auth/
# │   │   │   ├── login.html
# │   │   │   └── register.html
# │   │   └── blog/
# │   │       ├── create.html
# │   │       ├── index.html
# │   │       └── update.html
# │   └── static/
# │       └── style.css
# ├── tests/
# │   ├── conftest.py
# │   ├── data.sql
# │   ├── test_factory.py
# │   ├── test_db.py
# │   ├── test_auth.py
# │   └── test_blog.py
# ├── venv/
# ├── setup.py
# └── MANIFEST.in
#####

#####
# 版本控制
#####

# 创建 .gitignore
# 参考 .gitignore 文件

import os

from flask import Flask

def create_app(test_config=None):
    """创建并设置 APP
    """
    # * __name__ 是当前 Python 模块的名称。应用需要知道在哪里设置路径， 使用 __name__ 是一个方便的方法。
    # * instance_relative_config=True 告诉应用配置文件是相对于 instance folder 的相对路径。
    #   实例文件夹在 flaskr 包的外面，用于存放本地数据（例如配置密钥和数据库），不应当提交到版本控制系统。
    app = Flask(__name__, instance_relative_config=True)

    # 设置一个应用的 缺省配置
    app.config.from_mapping(

        # SECRET_KEY 是被 Flask 和扩展用于保证数据安全的。
        # 在开发过程中， 为了方便可以设置为 'dev' ，但是在发布的时候应当使用一个随机值来 重载它！
        SECRET_KEY='dev',

        # DATABASE SQLite 数据库文件存放在路径。它位于 Flask 用于存放实例的 app.instance_path 之内。
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # 载入这个实例设置，如果存在就不测试
    if test_config is None:
        
        # 使用 config.py 中的值来重载缺省配置，如果 config.py 存在的话。 
        # 例如，当正式部署的时候，用于设置一个正式的 SECRET_KEY 。
        app.config.from_pyfile('config.py', silent=True)

    # 载入传入的参数
    else:
        
        # test_config 也会被传递给工厂，并且会替代实例配置。这样可以实现 测试和开发 的配置分离，相互独立。
        app.config.from_mapping(test_config)

    # 确保实例文件夹存在
    try:

        # os.makedirs() 可以确保 app.instance_path 存在。 
        # Flask 不会自动创建实例文件夹，但是必须确保创建这个文件夹，因为 SQLite 数据库文件会被保存在里面。
        os.makedirs(app.instance_path)

    except OSError:
        pass

    @app.route('/hello')
    def hello():
        """创建一个简单的路由
        """
        return 'Hello, World!'

    #####
    # 定义和操作数据库
    #####

    # 完成 db.py
    from . import db
    db.init_app(app)

    #####
    # 初始化数据库文件
    #####

    # 现在 init-db 已经在应用中注册好了，可以与 flask 命令一起使用了。 
    # 使用的方式与 run 命令类似。
    # 现在要关闭 Flask 服务器
    # 然后运行 flask init-db

    ##########
    # 蓝图和视图
    ##########

    #####
    # 创建蓝图
    #####

    # 使用 app.register_blueprint() 导入并注册 蓝图。新的代码放在工厂函数的尾部返回应用之前。
    from . import auth
    app.register_blueprint(auth.bp)

    # 认证蓝图将包括注册新用户、登录和注销视图。
    # --> auth.py
    
    ##########
    # 博客蓝图
    ##########
    
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

