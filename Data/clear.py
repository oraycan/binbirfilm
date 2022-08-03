from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,redirect,url_for,render_template,request
import db_create

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/oraycan/Desktop/RANDOMFILM/Data/movies.db'
db = SQLAlchemy(app)

iddb = db_create.dbmovies.query.order_by(db_create.dbmovies.id).all()
idkat = db_create.dbkategori.query.order_by(db_create.dbkategori.movie_id).all()
liste2 = []
liste3 = []
sayac=1
sayac2=1


for y in iddb:
    y=y.id
    liste2.append(y)

for i in idkat:
    i=i.movie_id
    if i in liste2:
        print("BU FİLM EKLİ")
    else:
        db.session.query(db_create.dbkategori).filter(db_create.dbkategori.movie_id==i).delete()
        db.session.commit()
        print(f"{i} id'li film silindi ")

