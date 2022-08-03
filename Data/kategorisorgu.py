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


url = "https://api.themoviedb.org/3/movie/"
url2= "?api_key=d371bf9bed387314401dc007338464f8&language=tr-TR"
list = []
idkat = db_create.dbkategori.query.order_by(db_create.dbkategori.movie_id).all()
liste2 = []

for u in idkat:
    u=u.movie_id
    liste2.append(u)

while True:
    iddb = db_create.dbmovies.query.order_by(db_create.dbmovies.id).all()
    for i in iddb:
        i = i.id
        response = requests.get(url+str(i)+url2)
        infos = response.json()
        results = infos["genres"]
        print(results)
        if i in liste2:
            print("Bu Film Eklendi")
            pass
        else:
            for z in results:
                genres = z["id"]
                tur = z["name"]
                print(genres, tur)
                denemekategori = db_create.dbkategori(category_id=genres, movie_id=i)
                db.session.add(denemekategori)
                db.session.commit()

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)