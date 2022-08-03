from urllib import response
import requests
import random
from sqlite3 import Cursor
from flask_sqlalchemy import SQLAlchemy
from crypt import methods
from flask import Flask,request,redirect,url_for,render_template,request
from datetime import datetime
import db_create

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/oraycan/Desktop/RANDOMFILM/Data/movies.db'
db = SQLAlchemy(app)


iddb = db_create.dbmovies.query.order_by(db_create.dbmovies.id).all()
idkat = db_create.dbkategori.query.order_by(db_create.dbkategori.movie_id).all()
liste2 = []
liste1 = []
sayac=1

for i in iddb:
    i = i.id
    liste1.append(i)

for y in idkat:
    y=y.movie_id
    if y in liste1:
        print(sayac)
        sayac+=1
    else:
        liste2.append(y)
        print("BU FİLM YOKKİ")

print("Bittti",liste2)


if __name__=="__main__":
    db.create_all()
    app.run(debug=True)