from enum import unique
from sqlite3 import Cursor
from flask_sqlalchemy import SQLAlchemy
from crypt import methods
from flask import Flask,request,redirect,url_for,render_template,request
from numpy import unicode_
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/oraycan/Desktop/RANDOMFILM/Data/movies.db'
db = SQLAlchemy(app)


###### Film Kategori Realtionship #######

class dbkategori(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    movie_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)

###### Film Özellikler #######
class dbmovies(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    overview = db.Column(db.String)
    backdrop_path = db.Column(db.String)
    original_language = db.Column(db.String)
    original_title = db.Column(db.String)
    popularity = db.Column(db.Integer)
    poster_path = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    vote_average = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    adult = db.Column(db.Boolean)

###### Film Kategori #######
class dbgenres(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
###### GENRE ID TABLO #######

### User Table ##
class user(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25),unique = True)
    email = db.Column(db.String(100),unique = True)
    password = db.Column(db.String(25))
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    image = db.Column(db.Text, nullable = True)
    kayit_tarihi = db.Column(db.DateTime, default=datetime.utcnow)

class user_like(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    movie_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

class user_watchlist(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    movie_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

### Blog table
class blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.Text, nullable = True)
    image_url = db.Column(db.String)
    url = db.Column(db.String(120))
    view = db.Column(db.Integer)

### Blog Kategori
class blog_category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    article_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)

### Blog Kategori
class blog_category_name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String)

### Blog Kategori
class blog_tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer)
    blog_tag = db.Column(db.String)

### Blog Yorum
class blog_comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer)
    comment = db.Column(db.String)
    author = db.Column(db.String)
    onay = db.Column(db.Boolean)
    image = db.Column(db.String)


if __name__=="__main__":
    db.create_all()
    app.run(debug=True)