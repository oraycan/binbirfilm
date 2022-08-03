import random,sqlite3,os.path,requests,os,urllib.request
from sqlite3 import Cursor
from flask_sqlalchemy import SQLAlchemy
from crypt import methods
from flask import Flask,request,redirect,url_for,render_template,request,flash,session
from datetime import datetime
from numpy import empty
from Data import db_create
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,EmailField
from passlib.hash import sha256_crypt
from functools import wraps
from sqlalchemy import desc
from werkzeug.utils import secure_filename



#### FLASK SQL & Dosya BAĞLANTISI & Ayarlar###
PROFILE = 'static/images/profiles'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/oraycanyagmur/Desktop/RANDOMFILM/Data/movies.db'
db = SQLAlchemy(app)
app.secret_key= "randomfilm"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = "static/uploads"
app.config['PROFILE'] = PROFILE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#### FLASK SQL BAĞLANTISI ###

#### SQLITE BAĞLANTISI ###
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "Data/movies.db")
with sqlite3.connect(db_path,check_same_thread=False) as dbmovies:

    cur=dbmovies.cursor()
#### SQLITE BAĞLANTISI ###

# Login Required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("İlk önce giriş yapmalısınız","warning")
            return redirect(url_for("login"))
    return decorated_function
# Login Required bitiş

#### Kayıt Ol Formu ###
class RegisterForm(Form):
    name = StringField("İsim :", validators=[validators.Length(min=4 ,max=40 , message="İsminiz 3 İle 25 Karakter Olmalı")])
    surname = StringField("Soyisim :", validators=[validators.Length(min=4 ,max=40 , message="Soyisminiz 3 İle 25 Karakter Olmalı")])    
    username = StringField("Kullanıcı Adı :", validators=[validators.length(min=4 , max=40, message="Kuallnıcı adı 4 İle 15 Karakter Olmalı")])
    email = StringField("E-mail Adresi :", validators=[validators.Email(message="Email Adresini Yanlış Girdiniz")])
    password = PasswordField("Parola :",validators=[
        validators.DataRequired(message="Lütfen Şifrenizi Girin"),
        validators.EqualTo("confirm" , message="Şifreniz uyuşmuyor")
    ])
    confirm = PasswordField("Parola Tekrar :")
#### Kayıt Ol Formu Bitiş###  

# Makale Ekleme Formu
class BlogForm(Form):
    title = StringField("Başlık",validators=[validators.Length(min = 5 , max = 85)])
    content = TextAreaField("İçerik",validators=[validators.Length(min=15)])
    tags = StringField("Etiketler (Virgül İle Ayırın)",validators=[validators.Length(min = 5 , max = 120)])
# Makale Ekleme Formu BİTİŞ

# Kategori Ekleme Formu
class CatForm(Form):
    kategori = StringField("Kategori",validators=[validators.Length(min = 3 , max = 85)])
# Makale Ekleme Formu BİTİŞ

# LOGİN FORMU
class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")
# END LOGİN FORMU 

#### Kayıt Ol Sayfası ###
@app.route("/kayitol" , methods=['GET','POST'])
def kayitol():
    if "username" in session:
        return redirect(url_for("index"))
    else:
        form = RegisterForm(request.form)
        if request.method == "POST" and form.validate():
            #profil urlsi
            url = form.username.data 

            if url is not None:
                for i in url:
                    if i == "İ":
                        flash("Kullanıcı Adınızda Boşluk ' ', Sayı ve Türkçe Karakter kullanmayın ","alert")
                        return redirect(url_for("kayitol"))
                    elif i == "ı":
                        flash("Kullanıcı Adınızda Boşluk ' ', Sayı ve Türkçe Karakter kullanmayın ","alert")
                        return redirect(url_for("kayitol"))
                    elif i == "ü" or i == "Ü":
                        flash("Kullanıcı Adınızda Boşluk ' ', Sayı ve Türkçe Karakter kullanmayın ","alert")
                        return redirect(url_for("kayitol"))
                    elif i == "Ö" or i == "ö":
                        flash("Kullanıcı Adınızda Boşluk ' ', Sayı ve Türkçe Karakter kullanmayın ","alert")
                        return redirect(url_for("kayitol"))
                    elif i == "Ş" or i == "ş":
                        flash("Kullanıcı Adınızda Boşluk ' ', Sayı ve Türkçe Karakter kullanmayın ","alert")
                        return redirect(url_for("kayitol"))
                    elif i == "Ç" or i == "ç":
                        flash("Kullanıcı Adınızda Boşluk ' ', Sayı ve Türkçe Karakter kullanmayın ","alert")
                        return redirect(url_for("kayitol"))
                  
            
            newuser= db_create.user(username=form.username.data,
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            password=sha256_crypt.encrypt(form.password.data)
            )

            usercheck = form.username.data
            mailcheck = form.email.data
            ucs = cur.execute("Select username from user where username = (?)",(usercheck,))
            uc = ucs.fetchone()
            mcs = cur.execute("Select email from user where email = (?)",(mailcheck,))
            mc = mcs.fetchone()

            if uc is not None :
                flash("Kullanıcı Adı Sistemimizde Zaten Kayıtlı. ","alert")
                return redirect(url_for("kayitol"))
            elif mc is not None :
                flash("E-Posta Adresi Sistemimizde Zaten Kayıtlı. ","alert")
                return redirect(url_for("kayitol"))  
            elif url.isalpha() == False:
                flash("Kullanıcı Adınızda Boşluk ' ', Sayı ve Türkçe Karakter kullanmayın ","alert")
                return redirect(url_for("kayitol"))         
            else:
                db.session.add(newuser)
                db.session.commit()
                flash("Kayıt İşlemi Gerçekleşti, Giriş Yapabilirsiniz","success")
                return redirect(url_for("login"))
        else:
            return render_template("kayitol.html", form = form)
#### Kayıt Ol Sayfası Bitiş ###

#### Login Sayfası ###
@app.route("/login" , methods=['GET','POST'])
def login():
    if "username" in session:
        return redirect(url_for("index"))
    else:
        form = LoginForm(request.form)

        if request.method == 'POST':
            username = form.username.data
            password = form.password.data

            usernameform = cur.execute("Select * from user where username = (?)",(username,))
            usercheck = cur.fetchone()

            if usercheck is not None:
                password_check = usercheck[3]
                if sha256_crypt.verify(password,password_check):
                    flash("Başarıyla Giriş Yapıldı","success")
                    session["logged_in"] = True
                    session["username"] = username
                    return redirect(url_for("index"))
                else:
                    flash("Şifre hatalı","danger")
                    return redirect(url_for("login"))
            else:
                flash("Kullanıcı Adı Bulunamadı","danger")
                return redirect(url_for("login"))
        else:
            return render_template("login.html", form = form)
###$ Login Sayfası Bitiş ###

#LOGOUT SAYFA BAŞLANGIÇ
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
#LogOut Bitiş

## ANA SAYFA ##
@app.route("/")
def index():
    film_kategori_sorgu = cur.execute('SELECT movie_id from dbkategori')
    film_kategori_filtre= cur.fetchall()

    randomno = random.randint(0,len(film_kategori_filtre)-1)
    randomsec = film_kategori_filtre[randomno]
    randomfilm = randomsec[0]
    randomsonuc = db_create.dbmovies.query.filter_by(id=randomfilm).first()
    kategoriler = db_create.dbkategori.query.filter_by(movie_id=randomfilm).all()
    kategori = []

    randomno1 = random.randint(0,len(film_kategori_filtre)-1)
    randomsec1 = film_kategori_filtre[randomno1]
    randomfilm1 = randomsec1[0]
    randomsonuc1 = db_create.dbmovies.query.filter_by(id=randomfilm1).first()
    kategoriler1 = db_create.dbkategori.query.filter_by(movie_id=randomfilm1).all()
    kategori1 = []

    randomno2 = random.randint(0,len(film_kategori_filtre)-1)
    randomsec2 = film_kategori_filtre[randomno2]
    randomfilm2 = randomsec2[0]
    randomsonuc2 = db_create.dbmovies.query.filter_by(id=randomfilm2).first()
    kategoriler2 = db_create.dbkategori.query.filter_by(movie_id=randomfilm2).all()
    kategori2 = []
    ## FRAGMAN SORGUSU DAHA SONRA DATABASE'E EKLENECEK ##   
    fragman_url1 = "https://api.themoviedb.org/3/movie/"
    fragman_url2= "/videos?api_key=d371bf9bed387314401dc007338464f8&language=en-US"

   
    try:
        response = requests.get(fragman_url1+str(randomsonuc.id)+fragman_url2)
        infos = response.json()
        fragman_result = infos["results"]
        sonuc = fragman_result[0]
        fragman = sonuc["key"]
    except:
        fragman="Fragman Bulunamadı"

    try:
        response1 = requests.get(fragman_url1+str(randomsonuc1.id)+fragman_url2)
        infos1 = response1.json()
        fragman_result1 = infos1["results"]
        sonuc1 = fragman_result1[0]
        fragman1 = sonuc1["key"]
    except:
        fragman1="Fragman Bulunamadı"
    
    try:
        response2 = requests.get(fragman_url1+str(randomsonuc2.id)+fragman_url2)
        infos2 = response2.json()
        fragman_result2 = infos2["results"]
        sonuc2 = fragman_result2[0]
        fragman2 = sonuc2["key"]
    except:
        fragman2="Fragman Bulunamadı"
        ## FRAGMAN SORGUSU DAHA SONRA DATABASE'E EKLENECEK  BİTİŞ##   

        ## Kategori Sorgusu ##  
    for i in kategoriler:
        i = i.category_id
        genres= db_create.dbgenres.query.filter_by(id=i).all()
        for y in genres:
            y=y.name
            kategori.append(y)
    for i in kategoriler1:
        i = i.category_id
        genres= db_create.dbgenres.query.filter_by(id=i).all()
        for y in genres:
            y=y.name
            kategori1.append(y)
    for i in kategoriler2:
        i = i.category_id
        genres= db_create.dbgenres.query.filter_by(id=i).all()
        for y in genres:
            y=y.name
            kategori2.append(y)

    ### Popular Filmler ###
    popular_url = "https://api.themoviedb.org/3/movie/popular?api_key=d371bf9bed387314401dc007338464f8&language=tr-TR&page=1"
    response_popular = requests.get(popular_url)
    infos_popular = response_popular.json()
    popular_result = infos_popular["results"]
    ### Popular Filmler Bitiş###

        ### Yaklaşan Filmler ###
    upcoming_url = "https://api.themoviedb.org/3/movie/upcoming?api_key=d371bf9bed387314401dc007338464f8&language=tr-TR&page=1"
    response_upcoming = requests.get(upcoming_url)
    infos_upcoming = response_upcoming.json()
    upcoming_result = infos_upcoming["results"]
    ### Yaklaşan Filmler Bitiş###

    ### En çok film olan kategoriler###
    encokfilm_kategori_sorgu = cur.execute('select category_id from (select category_id, COUNT(*) as sayi from dbkategori group by category_id) tbl where sayi > 1 ORDER BY sayi DESC')
    encokfilm_kategori_filtre = cur.fetchall()
    sayi=1
    encokkategori=[]
    
    for i in encokfilm_kategori_filtre:
        if sayi <=4 :
            i = i[0]
            genres= db_create.dbgenres.query.filter_by(id=i).all()
            for y in genres:
                y=y.name
                encokkategori.append(y)
                sayi+=1
        else:
            break
    
    check=[]
    # Blog Sorgusu
    blog = db_create.blog.query.order_by(desc(db_create.blog.tarih)).limit(4)
    
    ### PRINT EKRANI###
    return render_template("index.html",
    randomsonuc=randomsonuc,kategori=kategori,fragman=fragman,
    randomsonuc1=randomsonuc1,kategori1=kategori1,fragman1=fragman1,
    randomsonuc2=randomsonuc2,kategori2=kategori2,fragman2=fragman2,
    popular_result=popular_result,
    upcoming_result=upcoming_result,
    encokkategori=encokkategori,blog=blog,check=check)


## Film Öneri ##
@app.route("/film_bul", methods=['GET', 'POST'])
def film_bul():
    ## Kategori Seçimi ##
    if request.method == "POST":
        check = request.form.getlist("kategori") #index kategori çekimi
        imdb = request.form.get("imdb") #index puan çekimi
        imdb = float(imdb)
        ## Hiç Bir Şey Seçilmez İse ##
        if len(check)==0 and (imdb == 0):
            film_kategori_sorgu = cur.execute('SELECT movie_id from dbkategori')
            film_kategori_filtre= cur.fetchall()

            randomno = random.randint(0,len(film_kategori_filtre)-1)
            randomsec = film_kategori_filtre[randomno]
            randomfilm = randomsec[0]
            randomsonuc = db_create.dbmovies.query.filter_by(id=randomfilm).first()
            kategoriler = db_create.dbkategori.query.filter_by(movie_id=randomfilm).all()
            kategori = []

            for i in kategoriler:
                i = i.category_id
                genres= db_create.dbgenres.query.filter_by(id=i).all()
                for y in genres:
                    y=y.name
                    kategori.append(y)
            flash("Herhangi Bir Kategori veya Puan Seçmediniz Rastgele Bir Film Getirildi...","danger")
            return render_template("film_bul.html",randomsonuc=randomsonuc,kategori=kategori)
        ## IMDB Seçilir Kategori Seçilmez ise ##
        elif len(check) == 0 and imdb > 0 :
            film_kategori_sorgu= cur.execute('select id from dbmovies where vote_average >=(?)',(imdb,))
            film_kategori_filtre= cur.fetchall()

            randomno = random.randint(0,len(film_kategori_filtre)-1)
            randomsec = film_kategori_filtre[randomno]
            randomfilm = randomsec[0]
            randomsonuc = db_create.dbmovies.query.filter_by(id=randomfilm).first()
            kategoriler = db_create.dbkategori.query.filter_by(movie_id=randomfilm).all()
            kategori = []

            for i in kategoriler:
                i = i.category_id
                genres= db_create.dbgenres.query.filter_by(id=i).all()
                for y in genres:
                    y=y.name
                    kategori.append(y)
            return render_template("film_bul.html",randomsonuc=randomsonuc,kategori=kategori)
        ## 1 Tane Kategori Seçilir İse ##
        elif len(check) == 1 :
            id1= check[0]
            
            film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  1 AND dbmovies.vote_average >=(?)',(id1,imdb))
            film_kategori_filtre= cur.fetchall()

            randomno = random.randint(0,len(film_kategori_filtre)-1)
            randomsec = film_kategori_filtre[randomno]
            randomfilm = randomsec[0]
            randomsonuc = db_create.dbmovies.query.filter_by(id=randomfilm).first()
            kategoriler = db_create.dbkategori.query.filter_by(movie_id=randomfilm).all()
            kategori = []

            for i in kategoriler:
                i = i.category_id
                genres= db_create.dbgenres.query.filter_by(id=i).all()
                for y in genres:
                    y=y.name
                    kategori.append(y)
            return render_template("film_bul.html",randomsonuc=randomsonuc,kategori=kategori,check=check)
        ## 2 Tane Kategori Seçilir İse ##   
        elif len(check) == 2 :
            id1= check[0]
            id2= check[1]
            
            film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  2 AND dbmovies.vote_average >=(?)',(id1,id2,imdb))
            film_kategori_filtre= cur.fetchall()

            if len(film_kategori_filtre) == 0 :
                film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  1 AND dbmovies.vote_average >=(?)',(id1,id2,imdb))
                film_kategori_filtre= cur.fetchall()
                

            randomno = random.randint(0,len(film_kategori_filtre)-1)
            randomsec = film_kategori_filtre[randomno]
            randomfilm = randomsec[0]
            randomsonuc = db_create.dbmovies.query.filter_by(id=randomfilm).first()
            kategoriler = db_create.dbkategori.query.filter_by(movie_id=randomfilm).all()
            kategori = []

            for i in kategoriler:
                i = i.category_id
                genres= db_create.dbgenres.query.filter_by(id=i).all()
                for y in genres:
                    y=y.name
                    kategori.append(y)
            return render_template("film_bul.html",randomsonuc=randomsonuc,kategori=kategori)
        ## 3 Tane Kategori Seçilir İse ##   
        elif len(check) == 3 :
            id1= check[0]
            id2= check[1]
            id3= check[2]
            
            film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  3 AND dbmovies.vote_average >=(?)',(id1,id2,id3,imdb))
            film_kategori_filtre= cur.fetchall()

            if len(film_kategori_filtre) == 0 :
                film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  2 AND dbmovies.vote_average >=(?)',(id1,id2,id3,imdb))
                film_kategori_filtre= cur.fetchall()
                if len(film_kategori_filtre) == 0 :
                    film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  1 AND dbmovies.vote_average >=(?)',(id1,id2,id3,imdb))
                    film_kategori_filtre= cur.fetchall()
                

            randomno = random.randint(0,len(film_kategori_filtre)-1)
            randomsec = film_kategori_filtre[randomno]
            randomfilm = randomsec[0]
            randomsonuc = db_create.dbmovies.query.filter_by(id=randomfilm).first()
            kategoriler = db_create.dbkategori.query.filter_by(movie_id=randomfilm).all()
            kategori = []

            for i in kategoriler:
                i = i.category_id
                genres= db_create.dbgenres.query.filter_by(id=i).all()
                for y in genres:
                    y=y.name
                    kategori.append(y)
            return render_template("film_bul.html",randomsonuc=randomsonuc,kategori=kategori)
        ## 4 Tane Kategori Seçilir İse ##   
        elif len(check) == 4 :
            id1= check[0]
            id2= check[1]
            id3= check[2]
            id4= check[3]
            
            film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  4 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,imdb))
            film_kategori_filtre= cur.fetchall()

            if len(film_kategori_filtre) == 0 :
                film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  3 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,imdb))
                film_kategori_filtre= cur.fetchall()
                if len(film_kategori_filtre) == 0 :
                    film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  2 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,imdb))
                    film_kategori_filtre= cur.fetchall()
                    if len(film_kategori_filtre) == 0 :
                        film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  1 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,imdb))
                        film_kategori_filtre= cur.fetchall()
                

            randomno = random.randint(0,len(film_kategori_filtre)-1)
            randomsec = film_kategori_filtre[randomno]
            randomfilm = randomsec[0]
            randomsonuc = db_create.dbmovies.query.filter_by(id=randomfilm).first()
            kategoriler = db_create.dbkategori.query.filter_by(movie_id=randomfilm).all()
            kategori = []

            for i in kategoriler:
                i = i.category_id
                genres= db_create.dbgenres.query.filter_by(id=i).all()
                for y in genres:
                    y=y.name
                    kategori.append(y)
            return render_template("film_bul.html",randomsonuc=randomsonuc,kategori=kategori)
        ## 5 Tane Kategori Seçilir İse ##   
        elif len(check) == 5 :
            id1= check[0]
            id2= check[1]
            id3= check[2]
            id4= check[3]
            id5= check[4]
            
            film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  5 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,id5,imdb))
            film_kategori_filtre= cur.fetchall()

            if len(film_kategori_filtre) == 0 :
                film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  4 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,id5,imdb))
                film_kategori_filtre= cur.fetchall()
                if len(film_kategori_filtre) == 0 :
                    film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  3 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,id5,imdb))
                    film_kategori_filtre= cur.fetchall()
                    if len(film_kategori_filtre) == 0 :
                        film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  2 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,id5,imdb))
                        film_kategori_filtre= cur.fetchall()
                        if len(film_kategori_filtre) == 0 :
                            film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  1 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,id5,imdb))
                            film_kategori_filtre= cur.fetchall()
                

            randomno = random.randint(0,len(film_kategori_filtre)-1)
            randomsec = film_kategori_filtre[randomno]
            randomfilm = randomsec[0]
            randomsonuc = db_create.dbmovies.query.filter_by(id=randomfilm).first()
            kategoriler = db_create.dbkategori.query.filter_by(movie_id=randomfilm).all()
            kategori = []

            for i in kategoriler:
                i = i.category_id
                genres= db_create.dbgenres.query.filter_by(id=i).all()
                for y in genres:
                    y=y.name
                    kategori.append(y)
            return render_template("film_bul.html",randomsonuc=randomsonuc,kategori=kategori)
        ## 6 Tane Kategori Seçilir İse ##   
        elif len(check) == 6 :
            id1= check[0]
            id2= check[1]
            id3= check[2]
            id4= check[3]
            id5= check[4]
            id6= check[5]
            
            film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  6 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,id5,id6,imdb))
            film_kategori_filtre= cur.fetchall()

            if len(film_kategori_filtre) == 0 :
                film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  5 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,id5,id6,imdb))
                film_kategori_filtre= cur.fetchall()
                if len(film_kategori_filtre) == 0 :
                    film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  4 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,id5,id6,imdb))
                    film_kategori_filtre= cur.fetchall()
                    if len(film_kategori_filtre) == 0 :
                        film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  3 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,id5,id6,imdb))
                        film_kategori_filtre= cur.fetchall()
                        if len(film_kategori_filtre) == 0 :
                            film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  2 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,id5,id6,imdb))
                            film_kategori_filtre= cur.fetchall()
                            if len(film_kategori_filtre) == 0 :
                                film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?,?,?,?,?,?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  1 AND dbmovies.vote_average >=(?)',(id1,id2,id3,id4,id5,id6,imdb))
                                film_kategori_filtre= cur.fetchall()
                

            randomno = random.randint(0,len(film_kategori_filtre)-1)
            randomsec = film_kategori_filtre[randomno]
            randomfilm = randomsec[0]
            randomsonuc = db_create.dbmovies.query.filter_by(id=randomfilm).first()
            kategoriler = db_create.dbkategori.query.filter_by(movie_id=randomfilm).all()
            kategori = []

            for i in kategoriler:
                i = i.category_id
                genres= db_create.dbgenres.query.filter_by(id=i).all()
                for y in genres:
                    y=y.name
                    kategori.append(y)
            return render_template("film_bul.html",randomsonuc=randomsonuc,kategori=kategori)
        ## 7 Tane Kategori Seçilir İse ##
        elif len(check) >= 7:
            film_kategori_sorgu = cur.execute('SELECT movie_id from dbkategori')
            film_kategori_filtre= cur.fetchall()

            randomno = random.randint(0,len(film_kategori_filtre)-1)
            randomsec = film_kategori_filtre[randomno]
            randomfilm = randomsec[0]
            randomsonuc = db_create.dbmovies.query.filter_by(id=randomfilm).first()
            kategoriler = db_create.dbkategori.query.filter_by(movie_id=randomfilm).all()
            kategori = []

            for i in kategoriler:
                i = i.category_id
                genres= db_create.dbgenres.query.filter_by(id=i).all()
                for y in genres:
                    y=y.name
                    kategori.append(y)
            flash("Çok Fazla Kategori Seçtin. Lütfen En Fazla 5 Kategori Seçin...","danger")
            return render_template("film_bul.html",randomsonuc=randomsonuc,kategori=kategori)
                       
    ## Kategori Seçilmeden Gelecek Ana Sayfa ##    
    else:
        film_kategori_sorgu = cur.execute('SELECT movie_id from dbkategori')
        film_kategori_filtre= cur.fetchall()

        randomno = random.randint(0,len(film_kategori_filtre)-1)
        randomsec = film_kategori_filtre[randomno]
        randomfilm = randomsec[0]
        randomsonuc = db_create.dbmovies.query.filter_by(id=randomfilm).first()
        kategoriler = db_create.dbkategori.query.filter_by(movie_id=randomfilm).all()
        kategori = []

        randomno1 = random.randint(0,len(film_kategori_filtre)-1)
        randomsec1 = film_kategori_filtre[randomno1]
        randomfilm1 = randomsec1[0]
        randomsonuc1 = db_create.dbmovies.query.filter_by(id=randomfilm1).first()
        kategoriler1 = db_create.dbkategori.query.filter_by(movie_id=randomfilm1).all()
        kategori1 = []

        randomno2 = random.randint(0,len(film_kategori_filtre)-1)
        randomsec2 = film_kategori_filtre[randomno2]
        randomfilm2 = randomsec2[0]
        randomsonuc2 = db_create.dbmovies.query.filter_by(id=randomfilm2).first()
        kategoriler2 = db_create.dbkategori.query.filter_by(movie_id=randomfilm2).all()
        kategori2 = []



        ## FRAGMAN SORGUSU DAHA SONRA DATABASE'E EKLENECEK ##   
        fragman_url1 = "https://api.themoviedb.org/3/movie/"
        fragman_url2= "/videos?api_key=d371bf9bed387314401dc007338464f8&language=en-US"

        response = requests.get(fragman_url1+str(randomsonuc.id)+fragman_url2)
        infos = response.json()
        fragman_result = infos["results"]
        try:
            sonuc = fragman_result[0]
            fragman = sonuc["key"]
        except:
            fragman="Fragman Bulunamadı"

        response1 = requests.get(fragman_url1+str(randomsonuc1.id)+fragman_url2)
        infos1 = response1.json()
        fragman_result1 = infos1["results"]
        try:
            sonuc1 = fragman_result1[0]
            fragman1 = sonuc1["key"]
        except:
            fragman1="Fragman Bulunamadı"

        response2 = requests.get(fragman_url1+str(randomsonuc2.id)+fragman_url2)
        infos2 = response2.json()
        fragman_result2 = infos2["results"]
        try:
            sonuc2 = fragman_result2[0]
            fragman2 = sonuc2["key"]
        except:
            fragman2="Fragman Bulunamadı"
         ## FRAGMAN SORGUSU DAHA SONRA DATABASE'E EKLENECEK  BİTİŞ##   

         ## Kategori Sorgusu ##  
        for i in kategoriler:
            i = i.category_id
            genres= db_create.dbgenres.query.filter_by(id=i).all()
            for y in genres:
                y=y.name
                kategori.append(y)
        for i in kategoriler1:
            i = i.category_id
            genres= db_create.dbgenres.query.filter_by(id=i).all()
            for y in genres:
                y=y.name
                kategori1.append(y)
        for i in kategoriler2:
            i = i.category_id
            genres= db_create.dbgenres.query.filter_by(id=i).all()
            for y in genres:
                y=y.name
                kategori2.append(y)

        ### Popular Filmler ###
        popular_url = "https://api.themoviedb.org/3/movie/popular?api_key=d371bf9bed387314401dc007338464f8&language=tr-TR&page=1"
        response_popular = requests.get(popular_url)
        infos_popular = response_popular.json()
        popular_result = infos_popular["results"]
        ### Popular Filmler Bitiş###

         ### Yaklaşan Filmler ###
        upcoming_url = "https://api.themoviedb.org/3/movie/upcoming?api_key=d371bf9bed387314401dc007338464f8&language=tr-TR&page=1"
        response_upcoming = requests.get(upcoming_url)
        infos_upcoming = response_upcoming.json()
        upcoming_result = infos_upcoming["results"]
        ### Yaklaşan Filmler Bitiş###

        ### En çok film olan kategoriler###
        encokfilm_kategori_sorgu = cur.execute('select category_id from (select category_id, COUNT(*) as sayi from dbkategori group by category_id) tbl where sayi > 1 ORDER BY sayi DESC')
        encokfilm_kategori_filtre = cur.fetchall()
        sayi=1
        encokkategori=[]
        
        for i in encokfilm_kategori_filtre:
            if sayi <=4 :
                i = i[0]
                genres= db_create.dbgenres.query.filter_by(id=i).all()
                for y in genres:
                    y=y.name
                    encokkategori.append(y)
                    sayi+=1
            else:
                break
        
        check=[]
        # Blog Sorgusu
        blog = db_create.blog.query.order_by(desc(db_create.blog.tarih)).limit(4)
        
        ### PRINT EKRANI###
        return render_template("film_bul.html",
        randomsonuc=randomsonuc,kategori=kategori,fragman=fragman,
        randomsonuc1=randomsonuc1,kategori1=kategori1,fragman1=fragman1,
        randomsonuc2=randomsonuc2,kategori2=kategori2,fragman2=fragman2,
        popular_result=popular_result,
        upcoming_result=upcoming_result,
        encokkategori=encokkategori,blog=blog,check=check)



# Kategoriler Sayfası
@app.route("/kategoriler")
def kategoriler():
    return render_template("kategoriler.html")

## Kategori Detay SAYFA BAŞLANGIÇ
@app.route("/kategori/<kategori_ismi>")
def kategori(kategori_ismi):
    if kategori_ismi == "vahsibati" :
        kategori_ismi = "Vahşi Batı"
        film_kategori_sorgu = cur.execute('SELECT * from dbgenres where name=(?)',(kategori_ismi,))
        kategori_ismi = "vahsibati"
    elif kategori_ismi == "Suc" :
        kategori_ismi = "Suç"
        film_kategori_sorgu = cur.execute('SELECT * from dbgenres where name=(?)',(kategori_ismi,))
        kategori_ismi = "Suc"
    elif kategori_ismi == "bilimkurgu" :
        kategori_ismi = "Bilim-Kurgu"
        film_kategori_sorgu = cur.execute('SELECT * from dbgenres where name=(?)',(kategori_ismi,))
        kategori_ismi = "bilimkurgu"
    elif kategori_ismi == "Savas" :
        kategori_ismi = "Savaş"
        film_kategori_sorgu = cur.execute('SELECT * from dbgenres where name=(?)',(kategori_ismi,))
        kategori_ismi = "Savas"
    elif kategori_ismi == "Muzik" :
        kategori_ismi = "Müzik"
        film_kategori_sorgu = cur.execute('SELECT * from dbgenres where name=(?)',(kategori_ismi,))
        kategori_ismi = "Muzik"
    else:
        film_kategori_sorgu = cur.execute('SELECT * from dbgenres where name=(?)',(kategori_ismi.capitalize(),))
    kategori_film= cur.fetchall()
    id= kategori_film[0][0]
     
    film_kategori_sorgu= cur.execute('select movie_id from dbkategori INNER JOIN dbmovies on dbkategori.movie_id=dbmovies.id WHERE dbkategori.category_id in (?) GROUP by dbkategori.movie_id HAVING COUNT(dbmovies.id)  >=  1 ORDER by dbmovies.release_date DESC',(id,))
    film_id= cur.fetchall()

    film_id = [i[0] for i in film_id]
    page = request.args.get('page', 1 , type=int)
    filmler = db.session.query(db_create.dbmovies).order_by((desc(db_create.dbmovies.release_date))).filter(db_create.dbmovies.id.in_((film_id))).paginate(page=page , per_page=12)


    return render_template("kategori.html",kategori_ismi=kategori_ismi,
    kategori_film=kategori_film,
    filmler=filmler,
    film_id=film_id)
## Kategori Detay SAYFA Bitiş

## Film Detay Sayfası Başlangıç
@app.route("/film/<string:id>")
def filmdetay(id):
    #filmara
    film_url="https://api.themoviedb.org/3/movie/"+id+"?api_key=d371bf9bed387314401dc007338464f8&language=tr-TR"
    film_sorgu=requests.get(film_url)
    filmara = film_sorgu.json()
    #oyuncu
    oyuncu_url1 = "https://api.themoviedb.org/3/movie/"
    oyuncu_url2= "/credits?api_key=d371bf9bed387314401dc007338464f8&language=tr-TR"
    oyuncu_sorgu = requests.get(oyuncu_url1+id+oyuncu_url2)
    infos = oyuncu_sorgu.json()
    cast = infos["cast"]
    #fragman
    fragman_url1 = "https://api.themoviedb.org/3/movie/"
    fragman_url2= "/videos?api_key=d371bf9bed387314401dc007338464f8&language=en-US"
    response = requests.get(fragman_url1+str(id)+fragman_url2)
    infos = response.json()
    fragman_result = infos["results"]
    try:
        sonuc = fragman_result[0]
        fragman = sonuc["key"]
    except:
        fragman="Fragman Bulunamadı"

    # Benzer Filmler
    benzerurl = "https://api.themoviedb.org/3/movie/"
    benzerurl2 = "/similar?api_key=d371bf9bed387314401dc007338464f8&language=tr-TR&page=1"
    benzer_sorgu=requests.get(benzerurl+str(id)+benzerurl2)
    benzer_info = benzer_sorgu.json()
    benzer = benzer_info["results"]
    return render_template("film.html",filmara=filmara,cast=cast,fragman=fragman,benzer=benzer)
    ## Film Detay Sayfası Bitiş

# 404 Page
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# Blog Ekle
@app.route("/blog-ekle", methods=["GET","POST"])
@login_required
def makaleekle():
    form = BlogForm(request.form)
    #Kategori Ekleme
    kategori_cek = db_create.blog_category_name.query.order_by(db_create.blog_category_name.id)

    if request.method =="POST" and form.validate():
        baslik = form.title.data
        icerik = form.content.data
        tags = form.tags.data


        #Başlığı url'ye uygun Çevrilme
        url=baslik.replace(" ","-")
        url=url.replace(",","")
        url=url.replace(".","")
        url=url.replace("&","")
        url=url.replace("İ","I")
        url=url.replace("i","ı")
        url= url.lower()
        translationTable = str.maketrans("ğüçşıö","gucsio")
        url = url.translate(translationTable)
            
        # Fotoğraf Ekleme
        file = request.files["pic"]
        if file.filename == '':
            flash('Kapak Fotoğrafı Seçilmedi',"danger")
        if file and allowed_file(file.filename):
            filename = url
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            

        #Başlık ve içerik Ekleme
        yeni_blog = db_create.blog(title=baslik,content=icerik,author=session["username"],image=file.read(),url=url,view=0,image_url=filename)


        db.session.add(yeni_blog)
        db.session.commit()

        #Etiket ekleme
        tags = tags.split(",")
        for i in tags:
            tag_ekle= db_create.blog_tag(blog_id=yeni_blog.id,blog_tag=i)
            db.session.add(tag_ekle)
            db.session.commit()
        
        #Kategori ekleme
        check = request.form.getlist("kategori") #index kategori çekimi
        for i in check:
            cat_ekle= db_create.blog_category(article_id=yeni_blog.id,category_id=i)
            db.session.add(cat_ekle)
            db.session.commit()

        flash("Makale Eklendi","success")
        return redirect(url_for("bloglar"))
    else:
        return render_template("blog-ekle.html", form=form,kategori_cek=kategori_cek)
# Blog Ekle

# Blog Sil
@app.route("/delete/<string:id>", methods=["GET","POST"])
@login_required
def delete(id):
    if session["username"] == "oraycan":
        cur.execute("delete from blog where id = (?)",(id,))
        dbmovies.commit()
        cur.execute("delete from blog_comment where article_id =(?)",(id,))
        dbmovies.commit()
        cur.execute("delete from blog_category where article_id =(?)",(id,))
        dbmovies.commit()
        return redirect(url_for("bloglar"))
    else:
        flash("Makale Silmeye Yetkiniz Yok","alert")
        return redirect(url_for("bloglar"))    
# Blog Sil

# Bloglar
@app.route("/blog")
def bloglar():
    # Blog Sorgusu
    page = request.args.get('page', 1 , type=int)
    blog = db_create.blog.query.order_by(desc(db_create.blog.tarih)).paginate(page=page , per_page=6)

    return render_template("blog.html",blog=blog)
# Bloglar

# Search
@app.route("/search",methods=["GET","POST"])
def search():
    if request.method == "POST":
        search = request.form.get("search")
        search_sorgu = cur.execute("SELECT title FROM blog WHERE  title LIKE '%deneme%' UNION ALL SELECT  title dbmovies FROM dbmovies WHERE title LIKE '%deneme%';")
        search_fetch = cur.fetchall()
        return print(search_sorgu)
    else:
        return render_template("search.html")
# Search

# Blog Detay
@app.route("/blog-detay/<blog_url>",methods=["GET","POST"])
def blogdetay(blog_url):
    if request.method == 'POST':
        user=db_create.user.query.filter_by(username=session["username"]).first()
        yorum = request.form.get("yorum")
        blogdetay = db_create.blog.query.filter_by(url=blog_url).first()
        yorum_ekle= db_create.blog_comment(comment=yorum,article_id=blogdetay.id,author=session["username"],onay=False,image=user.image)
        db.session.add(yorum_ekle)
        db.session.commit()
        flash("Yorumunuz Eklendi, Onaylandığında Yayınlanacak","success")

        blog_son_eklenen = db_create.blog.query.order_by(desc(db_create.blog.tarih))
        #Blog görüntülenme Sayısı
        sayac=blogdetay.view+1
        cur.execute("update blog set view = (?) where id =(?)",(sayac,blogdetay.id))
        dbmovies.commit()
        #Blog tagler
        tag = db_create.blog_tag.query.filter_by(blog_id=blogdetay.id)
        # BLog kAtegoriler sayı
        sayi = "SELECT count(category_name),blog_category_name.category_name FROM blog_category INNER JOIN blog_category_name ON blog_category.category_id =blog_category_name.id GROUP BY blog_category_name.category_name HAVING COUNT(*) > 0"
        sayi_sorgu=cur.execute(sayi)
        tum_kategoriler = sayi_sorgu.fetchall()

        yorumlar = db_create.blog_comment.query.filter_by(article_id=blogdetay.id).all()

        #En çok okunanlar
        cok_okunan = db_create.blog.query.order_by(desc(db_create.blog.view))


        return render_template("blog-detay.html",blog=blogdetay,
        blog_son_eklenen=blog_son_eklenen,
        tum_kategoriler=tum_kategoriler,
        cok_okunan=cok_okunan,
        yorumlar=yorumlar,tag=tag)


    else:
        #Blog Detay
        blogdetay = db_create.blog.query.filter_by(url=blog_url).first()
        blog_son_eklenen = db_create.blog.query.order_by(desc(db_create.blog.tarih))
        #Blog görüntülenme Sayısı
        sayac=blogdetay.view+1
        cur.execute("update blog set view = (?) where id =(?)",(sayac,blogdetay.id))
        dbmovies.commit()
        #Blog Kategoriler
        kategori = db_create.blog_category.query.filter_by(article_id=blogdetay.id).all()
        kategoriler=[]
        for i in kategori:
            i=i.category_id
            kategori_isim=db_create.blog_category_name.query.filter_by(id=i).all()
            for y in kategori_isim:
                y=y.category_name
                kategoriler.append(y)

        # BLog kAtegoriler sayı
        sayi = "SELECT count(category_name),blog_category_name.category_name FROM blog_category INNER JOIN blog_category_name ON blog_category.category_id =blog_category_name.id GROUP BY blog_category_name.category_name HAVING COUNT(*) > 0"
        sayi_sorgu=cur.execute(sayi)
        tum_kategoriler = sayi_sorgu.fetchall()

        yorumlar = db_create.blog_comment.query.filter_by(article_id=blogdetay.id).all()

        #En çok okunanlar
        cok_okunan = db_create.blog.query.order_by(desc(db_create.blog.view))

        #Blog tagler
        tag = db_create.blog_tag.query.filter_by(blog_id=blogdetay.id)

        return render_template("blog-detay.html",blog=blogdetay,
        blog_son_eklenen=blog_son_eklenen,
        tum_kategoriler=tum_kategoriler,
        cok_okunan=cok_okunan,yorumlar=yorumlar,tag=tag,
        kategoriler=kategoriler,kategori_isim=kategori_isim)
# Blog Detay

# Blog Kategoriler
@app.route("/blog-kategori/<blog_kategori>")
def blog_kategori(blog_kategori):
    sorgu_name = db_create.blog_category_name.query.filter_by(category_name=blog_kategori).first()
    id = sorgu_name.id
    sorguid= cur.execute('select article_id from blog_category INNER JOIN blog on blog_category.article_id=blog.id WHERE blog_category.category_id in (?) GROUP by blog_category.article_id HAVING COUNT(blog.id)  >=  1 ORDER by blog.tarih DESC',(id,))
    blog_id= cur.fetchall()
    blog_id = [i[0] for i in blog_id]

    page = request.args.get('page', 1 , type=int)
    blog = db.session.query(db_create.blog).order_by((desc(db_create.blog.tarih))).filter(db_create.blog.id.in_((blog_id))).paginate(page=page , per_page=6)

    #Tüm Kategoriler
    sayi = "SELECT count(category_name),blog_category_name.category_name FROM blog_category INNER JOIN blog_category_name ON blog_category.category_id =blog_category_name.id GROUP BY blog_category_name.category_name HAVING COUNT(*) > 0"
    sayi_sorgu=cur.execute(sayi)
    tum_kategoriler = sayi_sorgu.fetchall()

    #En çok okunanlar
    cok_okunan = db_create.blog.query.order_by(desc(db_create.blog.view))
    
    return render_template("blog-kategori.html",
    sorgu_name=sorgu_name,
    blog=blog,
    blog_id=blog_id,
    tum_kategoriler=tum_kategoriler,
    cok_okunan=cok_okunan,
    blog_kategori=blog_kategori
    )
# Blog Kategoriler

# Kategori Ekle
@app.route("/add-category", methods=['GET', 'POST'])
@login_required
def add_category():
    if session["username"] == "oraycan":
        form = CatForm(request.form)
        if request.method == 'POST':
            kategori = form.kategori.data
            yeni_kategori=db_create.blog_category_name(category_name=kategori)
            db.session.add(yeni_kategori)
            db.session.commit()
            flash("Kategori Eklendi","success")
            return render_template("add_category.html",form=form)
        else:
            form = CatForm(request.form)
            return render_template("add_category.html",form=form)
    else:
        return redirect(url_for("index"))
# Kategori Ekle

#Profil Sayfası
@app.route("/profil/<username>", methods=['GET','POST'])
@login_required
def profil(username):
    if request.method=='POST':
       # Fotoğraf Ekleme
        file = request.files["avatar"]
        if file.filename == '':
            flash('Kapak Fotoğrafı Seçilmedi')
        if file and allowed_file(file.filename):
            filename = session["username"]
            file.save(os.path.join(app.config['PROFILE'], filename))

            cur.execute("update user set image = (?) where username =(?)",(filename,session['username']))
            dbmovies.commit()

        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')

        if session["username"] == username :
            user = db_create.user.query.filter_by(username=username).first()
            return render_template("profil.html",user=user)
        else:
            return redirect(url_for("login"))
    else:
        if session["username"] == username :
            user = db_create.user.query.filter_by(username=username).first()
            #Favori Filmler
            likemovie = db_create.user_like.query.filter_by(user_id=user.id).all()
            like_list=[]
            for i in likemovie:
                i=i.movie_id
                like_list.append(i)
            like_filmler = db.session.query(db_create.dbmovies).order_by((desc(db_create.dbmovies.release_date))).filter(db_create.dbmovies.id.in_((like_list)))


            return render_template("profil.html",user=user,like_filmler=like_filmler)
        else:
            return redirect(url_for("login"))
#Profil Sayfası

#Filmi Beğen
@app.route("/likemovie/<int:id>")
def likemovie(id):
    user=db_create.user.query.filter_by(username=session["username"]).first()
    likemovie = db_create.user_like(movie_id=id,user_id=user.id)
    like_list = db.session.query(db_create.user_like).filter_by(movie_id=id,user_id=user.id).all()
    username=user.username


    if len(like_list) == 0 :
        db.session.add(likemovie)
        db.session.commit()
        flash("Film Favorilere Eklendi","success")
        return redirect(url_for("profil",username=username))
    else:
        flash("Film Zaten Favorilerde","danger")
        return redirect(url_for("profil",username=username))

            
    #Filmi Beğen

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)