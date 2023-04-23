from flask import Flask
from flask import render_template
from flask import request
import octosuiteweb
import json

Octo_Web = octosuiteweb.new_octosuite_class()
run = Octo_Web()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/commits')
def commits():
    return render_template('commits.html')

@app.route('/issues')
def issues():
    return render_template('issues.html')

@app.route('/repos')
def repos():
    return render_template('repos.html')

@app.route('/topics')
def topics():
    return render_template('topics.html')

@app.route('/users')
def users():
    return render_template('users.html')

@app.route('/user_repo')
def user_repo():
    username = request.args.get('username')
    limit = request.args.get('limit')
    link = request.args.get('link')
    return json.dumps(run.user_repos(username,limit,link)) if link else json.dumps(run.user_repos(username,limit))