from flask import request, session, redirect, url_for, render_template
from AppConfig import AppConfig


class Login(AppConfig):  # 登录页面

    def login(self):  # 登录
        if session.get(self.KEY_IS_LOGIN):  # 如果已经登录，重定向到首页
            return redirect(url_for("index"))
        if request.method == "POST":
            username = request.form.get("username")  # 获取用户名和密码
            password = request.form.get("password")  # 获取用户名和密码
            error_message = None  # 错误信息
            if not username or not password:
                error_message = "用户名或密码不能为空"
                return render_template(
                    "login.html",
                    error_message=error_message,
                    username=username,
                )
            if username == "admin" and password == "passwd":
                session[self.KEY_IS_LOGIN] = True
                return redirect(url_for("index"))
            else:
                error_message = "用户名或密码错误"
                return render_template(
                    "login.html",
                    error_message=error_message,
                    username=username,
                )

        return render_template("login.html")
