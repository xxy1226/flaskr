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

