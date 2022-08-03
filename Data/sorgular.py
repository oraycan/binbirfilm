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

"""
kategori =[{"id":28,"name":"Aksiyon"},
    {"id":12,"name":"Macera"},
    {"id":16,"name":"Animasyon"},
    {"id":35,"name":"Komedi"},
    {"id":80,"name":"Suç"},
    {"id":99,"name":"Belgesel"},
    {"id":18,"name":"Dram"},
    {"id":10751,"name":"Aile"},
    {"id":14,"name":"Fantastik"},
    {"id":36,"name":"Tarih"},
    {"id":27,"name":"Korku"},
    {"id":10402,"name":"Müzik"},
    {"id":9648,"name":"Gizem"},
    {"id":10749,"name":"Romantik"},
    {"id":878,"name":"Bilim-Kurgu"},
    {"id":10770,"name":"TV film"},
    {"id":53,"name":"Gerilim"},
    {"id":10752,"name":"Savaş"},
    {"id":37,"name":"Vahşi Batı"}]

for y in kategori:
    id = y["id"]
    name = y["name"]
    print(type(id),id,type(name),name)
    addcategory = db_create.dbgenres(id=id,name=name)
    db.session.add(addcategory)
    db.session.commit()
 """
###### GENRE ID TABLO #######

###### Request #######
url2= "https://api.themoviedb.org/3/discover/movie?api_key=d371bf9bed387314401dc007338464f8&language=tr-TR&sort_by=release_date.asc"
tarih1 = "&primary_release_date.gte="
tarih2 = "&primary_release_date.lte="
page = "&page="
yil1 = 2022
ay1=1
gun1=1
yil2 = 2022
ay2= 1
gun2 = 1
finalurl = url2+tarih1+str(yil1)+"-"+str(f"{ay1:02d}")+"-"+str(f"{gun1:02d}")+tarih2+str(yil2)+"-"+str(f"{ay2:02d}")+"-"+str(f"{gun2:02d}")
pagenum= 1
###### Request #######


###### DATABASE EKLEME YERİ

while True:
    ############ RESPONSE  ############
    response = requests.get(url2+tarih1+str(yil1)+"-"+str(f"{ay1:02d}")+"-"+str(f"{gun1:02d}")+tarih2+str(yil2)+"-"+str(f"{ay2:02d}")+"-"+str(f"{gun2:02d}")+page+str(pagenum))
    infos = response.json()
    results = infos["results"]

    if len(results) == 0 :
        print("****************")
        print(f"SAYFA NO :{pagenum} \n GÜN : {gun2}")
        pagenum=0
        gun2+=1
        gun1+=1
        if gun2 == 32:
            gun1=1
            gun2=1
            ay1+=1
            ay2+=1
            if ay1 == 13:
                break
                # print("Bütün Sene Okeyyy")
                # gun1=1
                # gun2=1
                # ay1=1
                # ay2=1
                # yil1-=1
                # yil2-=1
                # if yil1 == 1880:
                #     break    
    ############ RESPONSE  ############

    ############ PARÇALAMA BAŞLANGIÇ ############
    for i in results:
        original_title = i["original_title"]
        id = i["id"]    
        title = i["title"]
        poster_path = i["poster_path"]
        backdrop_path = i["backdrop_path"]
        genre_ids = i["genre_ids"]
        original_language = i["original_language"]
        overview = i["overview"]
        popularity = i["popularity"]
        tarih = i["release_date"]
        release_date = datetime.strptime(tarih, '%Y-%m-%d')
        vote_average = i["vote_average"]
        vote_count = i["vote_count"]
        adult = i["adult"]

        
    ############ PARÇALAMA BİTİŞ ############

        ###### FİLM EKLEME  BAŞLANGIÇ #####
        if release_date == None:
            release_date = "1993-04-08"
            release_date = datetime.strptime(tarih, '%Y-%m-%d')
            print("TARİHTEN DOLAYI HATA ALDIIIIKKK")

        filmler = db_create.dbmovies(release_date = release_date,
        id=id,
        original_title = original_title,
        title = title,
        poster_path = poster_path,
        backdrop_path = backdrop_path,
        original_language = original_language,
        overview = overview ,
        popularity = popularity,
        vote_average = vote_average,
        vote_count = vote_count,
        adult = adult)

        ############ ID SORGULAMA ############
        iddb = db_create.dbmovies.query.order_by(db_create.dbmovies.id).all()
        idlist = []
        for y in iddb:
            idlist.append(y.id)
        if filmler.id in idlist:
            print("********")
            print(f"------{filmler.title} ------ Filmi Zaten Var : {yil1} - {ay1} - {gun1} ")
            print("********")
        ############ ID SORGULAMA ############
        ############ BOŞ OVERVİEW SİLME ############
        elif overview =="":
            print( f"---- OVERVİEW BOŞ {yil1} - {ay1} - {gun1} --{pagenum} ")
        else:
        ############ FİLM KAYDETME ############
            print(f"{filmler.title} ------ Filmi Eklendi Tarih : {yil1} - {ay1} - {gun1} ")

            db.session.add(filmler)
            db.session.commit()
         ############ FİLM KAYDETME ############

        for k in genre_ids:
            denemekategori = db_create.dbkategori(category_id=k, movie_id=id)
            db.session.add(denemekategori)
            db.session.commit()
        
    pagenum += 1
      
###### DATABASE EKLEME YERİ

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)