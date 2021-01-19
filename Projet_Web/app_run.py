import pandas as pd 
import logging
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

from flask import Flask,render_template,url_for,request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer 

from functions import clean_data, tokenizer_lemmatizer, get_data



app = Flask(__name__)

# Retourne page d'accueil de l'application
@app.route('/')
def model():
	return render_template('model.html')

# Fonction qui génère le modèle, le victorizer et retourne le rapport de classification en plot 
@app.route('/training',methods=['POST'])
def training():
    # Charger les données 
    data_array= get_data()
    # Nettoyage des données 
    cleaned_data = data_array['synopsis'].apply(clean_data)
    # création du vectoriseur à l'aide de tokenizer_lemmatizer personnalisé, en effectuant un filtrage basse fréquence
    vectorizer = TfidfVectorizer(min_df = 3, tokenizer=tokenizer_lemmatizer)
    # construire la matrice tfidf pour le corpus qui sera utilisé pour construire des modèles de classification
    mtx_tf_idf = vectorizer.fit_transform(cleaned_data)
    
    # Enregistrement de victorizer
    with open('vectorizer', 'wb') as picklefile:
        pickle.dump(vectorizer,picklefile)
    # Initialisation de text_corpus par la matrice tfidf to array
    text_corpus = mtx_tf_idf.toarray()
    # Utilisation le genre comme labels pour entrainer le classifieur
    text_labels = data_array.genre
    # Avant de construire le classifieur :
    # On divise les données en deux parties ( une pour le training du classifieur et la deuxième pour tester la précision du classifieur)
    # Sklearn donne la fonctionnalité de fractionnement des données pour le training et le test 
    # Diviser les données ( 70% pour le training et 30% pour le test)
    train_x, test_x, train_y, test_y = train_test_split(text_corpus, text_labels, test_size=0.3)   
    # Construire le classifieur
    classifier_multi_nvby = MultinomialNB()
    # Training le classifieur 
    classifier_multi_nvby = classifier_multi_nvby.fit(train_x,train_y)  
    # Enregistrement du modèle 
    with open('text_classifier', 'wb') as picklefile:
        pickle.dump(classifier_multi_nvby,picklefile)
    # la prédiction des données de test par le classifieur 
    predict_nvby = classifier_multi_nvby.predict(test_x)
    
    if request.method == 'POST':
        # Mettre le rapport de classification dans un data frame 
        dictionnary_report = classification_report(test_y, predict_nvby, output_dict=True)
        classification_rpt = pd.DataFrame(dictionnary_report)
        # Ajuster la taille de la figure 
        plt.figure(figsize = (10,5))
        # Création de la figure à partir du data frame
        sns.heatmap(classification_rpt.iloc[:-1, :-2].T, annot=True, linewidths=.5)
        plt.yticks(rotation=0) 
        # Enregistrement de la figure dans le dossier static/images
        plt.savefig('./static/images/clf_plot.png')
    return render_template('result_plot.html', name = 'clf_plot', url ='./static/images/clf_plot.png')

# Retourne la page pour effectuer la prédiction/classification
@app.route('/training/predict')
def predict():
	return render_template('predict.html')

# Retourne le résultat de la prédiction/classification
@app.route('/training/predict/result',methods=['POST'])
def result():
	# Charger le modèle de classification 
    with open('text_classifier', 'rb') as loaded_model:
        model = pickle.load(loaded_model)
    # Charger le victorizer 
    with open('vectorizer', 'rb') as vectorizer:
        vectorizer = pickle.load(vectorizer)
    
    if request.method == 'POST':
        # Recupèrer le synopsis saisie dans la zone de texte 
        msg = request.form['message']
        data = [(msg)]
        # Mettre le synopsis dans un data frame 
        predict_dataframe = pd.DataFrame(data, columns=['synopsis'])
        # Appliquer le nettoyage sur le synopsis
        predict_dataframe['synopsis'].apply(clean_data)
        corpus_test = predict_dataframe.synopsis
        # Transformer le synopsis nettoyé en vecteurs
        mtx_tf_idf = vectorizer.transform(corpus_test)
        corpus = mtx_tf_idf.toarray()
        # Prédire/classificer le synopsis et retourner le genre 
        my_prediction = model.predict(corpus) 
    return render_template('result.html', prediction = my_prediction)

if __name__ == '__main__':
	app.run(debug=True)