from flask import Flask, render_template, request, redirect, url_for, flash, abort

from app import app

@app.route('/')
def index():
    html = {}
    html['title']          = "Welcome back - Login"
    html['description']    = "Welcome back. Nice to see you."
    html['content']        = "This is a test!"
    return render_template('index.html', html=html)
