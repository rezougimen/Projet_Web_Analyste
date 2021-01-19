from requests import get
from bs4 import BeautifulSoup

# Scraper 1000 films par genre sur le site imdb

def scrapingData(genre):
    movies = []
    starts = [str(i) for i in range(1,1001,50)]
    # Une boucle sur starts qui contient les premiers films de 1 à 20 pages 
    for start in starts:
        # Faire un requet get 
        response = get('https://www.imdb.com/search/title/?title_type=tv_movie&genres='+ genre +'&start='+ start)
        # Extraire le html avec BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')
        # Sélectionner les 50 films de chaque page (container)
        mv_containers = page_html.find_all('div', class_="lister-item mode-advanced")
        
        for container in mv_containers:
            # scraper le titre de film
            name = container.h3.a.text
            # scraper le synopsis de film
            synopsis = container.find_all("p", class_="text-muted")[-1].text.lstrip()
            movies.append((name,synopsis,genre))
        
    return movies
