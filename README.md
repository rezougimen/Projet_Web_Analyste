# Projet fin d'etude Web 

## Une application qui permet de :

- Scrapper le site [imdb](https://www.imdb.com) où y'aurait des films avec leur catégorie.
- Alimenter la base de donnée d'entrainement de l'algorithme de classification à partir du résultat de scrapping.
- Rentrer le synopsis du film dans la zone de texte (l'entrée de l'algorithme) qui donne la prédiction du genre du film.  


## Installation de librairies requises : 
```
pip3 install pandas
```

```
pip3 install seaborn 
```
```
pip3 install nltk
```
```
pip3 install scikit-learn
```
```
pip3 install beautifulsoup4
```

```
pip3 install mysql-connector-python
```
```
pip3 install Flask
```

## Extraire les données et alimenter la base de données : 
```
python3 Projet_Web_Analyste/Projet_Web/data_script.py
```
## Lancer l'application :
```
python3 Projet_Web_Analyste/Projet_Web/app_run.py
```

## Accés à l'application :
http://46.101.76.241:5000/


## Exemples de synopsis pour tester l'application :

- Une célibataire à New-York (**Romantique**) : 
   A single girl living in New York tries to impress her high school nemesis by inventing the perfect boyfriend as her date to an impending wedding, then embarks on a string of blind dates to fill the bill.

- Sharknado (**Action**) :
   When a freak hurricane swamps Los Angeles, nature's deadliest killer rules sea, land, and air as thousands of sharks terrorize the waterlogged populace.

- Annabelle 2 : La Création du mal (**Horreur**) :
   Twelve years after the tragic death of their little girl, a doll-maker and his wife welcome a nun and several girls from a shuttered orphanage into their home, where they become the target of the doll-maker's possessed creation, Annabelle.
