from flask import (Flask,Markup,redirect,request,Response,session, render_template, request,g,redirect, url_for,abort, flash, g,send_file)
import sqlite3
import os
from flask import request
from flask import jsonify
import random
import json
from flask_sqlalchemy import SQLAlchemy

import datetime
import functools
import os
import re
import urllib



app = Flask(__name__)
app.config.from_object(__name__)
#database test
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
#database test end
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body

##########################################################################



#returns quotes from quotes.json
def getQuote():

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url =os.path.join(SITE_ROOT, "static","quotes.json")
    json_data = json.load(open(json_url))
    json_list = json_data['quotes']
    json_extracted_list = []

    for i in json_list:
        json_extracted_list.append(i)

    json_rand = random.choice(json_extracted_list)
    return json_rand

def clientInfo():
    info_client=[]
    info_client.append(request.remote_addr)
    info_client.append(request.user_agent)
    return info_client

#returns tree of dir
def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore
    else:
        for name in lst:
            fn = os.path.join(path,name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))

    return tree




#routes index.html with the useragent and ip from the visiting client
@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
    return render_template('index.html',info_client=clientInfo(),quote=getQuote())

@app.route('/about')
def about():
    return render_template('about.html',quote=getQuote(),info_client=clientInfo())

@app.route('/hack')
def hack():
    path = "./static/infosec" #this is relative to the dir where you are executing ncos.py
    return render_template('hack.html',tree=make_tree(path),quote=getQuote(),info_client=clientInfo())

@app.route('/blog')
def blog():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "app.sqlite")
    with sqlite3.connect(db_path) as db:
        db.row_factory = sqlite3.Row

        cur = db.cursor()

        cur.execute("Select * from note;")
        text_row = cur.fetchall()
        #db.close()

    return render_template('blog.html',quote=getQuote(),info_client=clientInfo(),text_row=text_row)

@app.route('/static/infosec/e-zines/')
def ezines():
    path = "./static/infosec/e-zines"
    return render_template('ezines.html',quote=getQuote(),info_client=clientInfo(),tree=make_tree(path))




################ERROR404############################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def main():
	app.run(debug=True)

if __name__ == '__main__':
	main()
