from flask import Blueprint, render_template

dashboard = Blueprint(__name__, "dashboard")


@dashboard.route('/')
def home():
    return render_template('index.html')
