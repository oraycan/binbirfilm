from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,redirect,url_for,render_template,request
import db_create

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/oraycan/Desktop/RANDOMFILM/Data/movies.db'
db = SQLAlchemy(app)


idkat = db_create.dbkategori.query.order_by(db_create.dbkategori.movie_id).all()
liste = []

for i in idkat:
    i = i.id
    liste.append(i)

for y in liste:
    sorgu = db_create.dbkategori.query.filter(db_create.dbkategori.movie_id==y).distinct()
    print(sorgu)

"""
for i in idkat:
    i=i.movie_id
    if i in liste2:
        print("BU FİLM EKLİ")
    else:
        db.session.query(db_create.dbkategori).filter(db_create.dbkategori.movie_id==i).delete()
        db.session.commit()
        print(f"{i} id'li film silindi ")
"""
