import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

from config import TIME_DELAY, DOUANE_DOMAINE , PROXY

# Classe du produit
class Produit :
    def __init__(self, code , label ):
        self.code = code
        self.label = label

# Dictionnaire des proxies
proxies_dict = {
    "http":PROXY,
    "https" : PROXY
}

#  Extraire les liens d'un tbody d'une page
def get_links_from_page_tbody(url):

    liste_des_liens = []

    # Envoyez une requête GET à l'URL spécifié
    response = requests.get(url, verify=False,proxies=proxies_dict)
    time.sleep(TIME_DELAY)

    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    tbody = soup.find('tbody')

    # Parcourez chaque élément 'tr' à l'intérieur du tbod
    for tr in tbody.find_all('tr'):
    
        href = tr.get('data-href')
        if href : 
            lien = DOUANE_DOMAINE + str(href)
            # Ajoutez le lien créé à la liste
            liste_des_liens.append(lien)
    # Retourne la liste des liens extraits        
    return liste_des_liens
    
#  Extraire les produits d'un tbody d'une page
def get_produits_from_page_tbody(url):

    liste_produits = []

    # Envoyez une requête GET à l'URL spécifié
    response = requests.get(url, verify=False,proxies=proxies_dict)
    time.sleep(TIME_DELAY)


    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    tbody = soup.find('tbody')

    # Parcourez chaque élément 'tr' à l'intérieur du tbody
    for tr in tbody.find_all('tr'):
        href = tr.get('data-href')
        if href:
            
            td = tr.find_all("td")

            #  Extrait le texte du deuxième élément 'td' (index 1) comme étiquette du produit
            label = td[1].text

            # Analysez l'URL pour extraire le paramètre 'sous_position'        
            href = str(href)           
            parsed = urllib.parse.urlparse(href)
            params = urllib.parse.parse_qs(parsed.query)
            sous_position = params['sous_position'][0]
    
            # Créez un objet Produit avec les valeurs extraites et nettoyez l'étiquette
            produit = Produit(code=  sous_position ,  label= str(label).lstrip('- ') )
            print("code is :" + produit.code + " label is :" + produit.label )

            # Ajoutez le produit à la liste
            liste_produits.append(produit)

    # Retourne la liste des produits extraits
    return liste_produits