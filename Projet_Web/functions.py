import logging
import mysql 
import mysql.connector  as my
import pandas as pd
import re
import pickle
import nltk 
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
stop_words = stopwords.words('english')


# Prétraitement des données 

def clean_data(text):
    # supprimer les caractères uniques
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text) 
    # supprimer les caractères uniques du début
    text = re.sub(r'\^[a-zA-Z]\s+', ' ', text) 
    # Remplacer plusieurs espace par un seul espace 
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    # Conversion en minuscule
    text = text.lower()
    
    rm_words = [w for w in text.split() if w.lower() not in stop_words]
    rm_words = ' '.join(rm_words)
    
    return rm_words

# Tokénisation et Lemmatization de texte brut (synopsis)
def tokenizer_lemmatizer(text):
    # Création des tokens en utilisant le tokenizer standard scikit-learn
    std_tokenizer = TfidfVectorizer().build_tokenizer() 
    # Construction des tokens 
    tokens = std_tokenizer(text) 
    # Effectuer la lemmatization pour chaque token en utilisant NLTK
    # Construction des lemmatizer 
    lemma = nltk.stem.WordNetLemmatizer()
    # Remplir la liste par les tokens lemmatizés de chaque text 
    tokens_lemmatizer = []
    for token in tokens:
        tokens_lemmatizer.append( lemma.lemmatize(token) ) 
    return tokens_lemmatizer

def get_data():
    # recupérer les données des films déja stocker dans la BDD
    mydb = my.connect(
        host="localhost",
        user="root",
        password="root",
        database="films",
        unix_socket = "/Applications/MAMP/tmp/mysql/mysql.sock",
    )

    cursor = mydb.cursor()

    try:
        sql = "SELECT title, synopsis, genre FROM film"
        cursor.execute(sql)
        myresult = cursor.fetchall()
        cursor.close()
        mydb.commit()
    except Exception as e:
        logging.warning(e)

    dataframe = pd.DataFrame(myresult, columns=['title','synopsis', 'genre'])
    # Retourner les résultats(synopsis) dans un dataframe
    return dataframe
