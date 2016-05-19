from flask import render_template, redirect, request
from . import main

@main.app_errorhandler(404)
def not_found(e):
    # print(e)
    return render_template('404.html')

@main.app_errorhandler(500)
def internal_error(e):
    # print(e)
    return render_template('500.html')
