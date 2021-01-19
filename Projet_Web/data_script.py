
import logging
import mysql 
import mysql.connector  as my
from scraping import scrapingData

mydb = my.connect(
    host="localhost",
    user="root",
    password="root",
    database="films",
    unix_socket = "/Applications/MAMP/tmp/mysql/mysql.sock",
)

# Insérer les données dans la table film
def insertData(category, cursor):
    sql = "insert into film(title, synopsis, genre) VALUES (%s, %s, %s)"
    # Appel de la fonction qui permet de scraper 1000 film par genre (sur le site imdb)
    data = scrapingData(category)
    cursor.executemany(sql, data)

try:
    cursor = mydb.cursor()
    req = "CREATE TABLE IF NOT EXISTS film (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(225), synopsis TEXT, genre VARCHAR(225))"
    cursor.execute(req)
    print('Scraping des données depuis imdb.com ...')

    insertData('action', cursor)
    insertData('horror', cursor)
    insertData('romance', cursor)

    print('Insertion des données scraper en BDD ...')

    cursor.close()
    mydb.commit()
except Exception as e:
    logging.warning(e)
