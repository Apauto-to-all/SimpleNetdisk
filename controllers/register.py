from flask import Flask, render_template, request, redirect, url_for, session
from AppConfig import AppConfig  # 导入所有的key


class Register(AppConfig):  # 注册页面

    def register(self):  # 注册
        if request.method == "POST":
            username = request.form.get("username")  # 用户名
            password = request.form.get("password")  # 获取密码
            confirm_password = request.form.get("confirm_password")  # 获取确认密码
            error_message = None  # 错误信息
            if not username or not password or not confirm_password:
                error_message = "用户名或密码不能为空"
                return render_template(
                    "register.html",
                    error_message=error_message,
                    username=username,
                )
            if password != confirm_password:
                error_message = "两次密码不一致"
                return render_template(
                    "register.html",
                    error_message=error_message,
                    username=username,
                )

        return render_template("register.html")  # 渲染注册页面
