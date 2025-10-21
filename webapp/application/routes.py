from flask import render_template, request, redirect, url_for
from application import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plumbing')
def plumbing():
    return render_template('plumbing.html')

@app.route('/heating')
def heating():
    return render_template('heating.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/book')
def book():
    return render_template('book.html')