from flask import render_template, redirect
from . import main

@main.app_errorhandler(404)
def not_found(e):
    print(e)
    return '40404 040404 !!!'

@main.app_errorhandler(500)
def internal_error(e):
    print(e)
    return '50500 500500 !!!'
