from flask import Flask, render_template, request, redirect, url_for, session
from AppConfig import AppConfig  # 导入所有的key
from controllers.login import Login  # 导入登录页面
from controllers.register import Register  # 导入注册页面

# from index import Index  # 导入首页页面


class Index(AppConfig):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数，初始化一些变量
        self.login = Login().login  # 登录页面
        self.register = Register().register  # 注册页面
        self.add_routes()  # 添加路由
        self.app.run(port=19764)  # 运行

    def add_routes(self):  # 添加路由
        self.app.add_url_rule("/", "home", self.home)  # 重定向到index
        self.app.add_url_rule("/index", "index", self.index)  # 首页，网盘进入的主页面
        self.app.add_url_rule(
            "/login", "login", self.login, methods=["GET", "POST"]
        )  # 登录
        self.app.add_url_rule(
            "/register", "register", self.register, methods=["GET", "POST"]
        )  # 注册

    def home(self):  # 重定向到index
        return redirect(url_for("index"))

    def index(self):  # 首页
        # 如果没有登录，重定向到登录页面
        if not session.get(self.KEY_IS_LOGIN):
            return redirect(url_for("login"))
        return f"Welcome to index page，{self.username}"


text = Index()
