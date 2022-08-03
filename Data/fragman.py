from urllib import response
import requests
import random
from sqlite3 import Cursor
from flask_sqlalchemy import SQLAlchemy
from crypt import methods
from flask import Flask,request,redirect,url_for,render_template,request

"""
fragman_url1 = "https://api.themoviedb.org/3/movie/"
fragman_url2= "/videos?api_key=d371bf9bed387314401dc007338464f8&language=en-US"

response = requests.get(fragman_url1+"209247"+fragman_url2)
infos = response.json()
fragman_result = infos["results"]
sonuc = fragman_result[0]
fragman = sonuc["key"]

"""

###POPILAR

popular_url = "https://api.themoviedb.org/3/movie/popular?api_key=d371bf9bed387314401dc007338464f8&language=tr-TR&page=1"
response = requests.get(popular_url)
infos = response.json()
popular_result = infos["results"]

print(popular_result[0]["title"])
