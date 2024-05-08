from flask import Flask, render_template, request, redirect, url_for, session
import os
import binascii


class AppConfig:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = binascii.hexlify(os.urandom(24)).decode("utf-8")
        self.KEY_IS_LOGIN = "is_login"
        self.username = "admin"
