from flask import Flask,render_template, request, url_for, flash, redirect


app = Flask(__name__)


@app.route('/')
def index():    
    return render_template ('index.html')