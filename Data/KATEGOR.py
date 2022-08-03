import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "movies.db")
with sqlite3.connect(db_path) as db:

    cur=db.cursor()

id1 = input("1. kategori")
id2 = input("2. kategori")
id3 = input("3. kategori")
id4 = input("4. kategori")


print("******")
film2= cur.execute('SELECT movie_id from dbkategori WHERE category_id in (?,?,?,?) GROUP by movie_id HAVING COUNT(movie_id)  >=  4',
(id1,id2,id3,id4))

film = cur.fetchall()
list = []

for i in film:
    list.append(i)
    print(i)


"""print(list[0][0])"""
print(len(film))

print("-----")
