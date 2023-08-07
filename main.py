import requests
from bs4 import BeautifulSoup
import csv
import timeit
import queue
from bs4 import BeautifulSoup
import urllib.parse

# Définissez l'URL de la liste des sections
URL_LISTE_SECTIONS = "https://www.douane.gov.dz/spip.php?page=tarif_douanier"

# Définissez le domaine de la douane
DOUANE_DOMAINE = "https://www.douane.gov.dz/"

# Définissez le nom du fichier CSV
NOM_FICHIER = "liste_produits.csv"

# Définissez le délai de temps entre les accès en seconde
TIME_DELAY = 1/1000

# Définissez le proxy
PROXY = "http://QX6:2023ESI2023ESI_@172.19.78.70:8080"
PROXIES = {
    "http":PROXY,
    "https" : PROXY
}

# Classe du produit
class Produit :
    def __init__(self, code , label ):
        self.code = code
        self.label = label


#  Extraire les liens d'un tbody d'une page
def get_links_from_page_tbody(url):

    liste_des_liens = []

    # Envoyez une requête GET à l'URL spécifié
    response = requests.get(url, verify=False,proxies=PROXIES)
    # time.sleep(TIME_DELAY)

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
    response = requests.get(url, verify=False,proxies=PROXIES)

    # time.sleep(TIME_DELAY)
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

# enregistrer les produits dans un fichier CSV
def save_produits_to_csv_file(nom_fichier , liste_produits ):
    # Ouvrez le fichier en mode écriture ('w') avec l'encodage UTF-8 et newline vide
    with open(nom_fichier, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Écrivez la première ligne d'en-tête dans le fichier CSV
        writer.writerow(['Code', 'Label'])
     
        # Parcourez la liste de produits et écrivez chaque produit dans le fichier CSV
        for produit in liste_produits:
            
            writer.writerow([produit.code,  produit.label])


if __name__ == "__main__":
    temps_debut = timeit.default_timer()
    # extraire les liens des sections de la page 
    print("liens des sections--------------------------------------------")

    liens_des_sections = get_links_from_page_tbody(url=URL_LISTE_SECTIONS)

    print(liens_des_sections)

    # ------------------------------------------------------------------------
    # extraire les liens des chapitres des pages
    print("liens des chapitres--------------------------------------------")
    liens_des_chapitre = []
    for lien in liens_des_sections :

        liens_des_chapitre += get_links_from_page_tbody(lien)

    print(liens_des_chapitre)

    # ------------------------------------------------------------------------
    # extraire les liens des rangees des pages
    print("liens des rangees--------------------------------------------")
    liens_par_rangee = []
    queue_rangee = queue.Queue()
    for lien in liens_des_chapitre : 
        for lien_rangee in  get_links_from_page_tbody(lien):
            queue_rangee.put(lien_rangee)

    # ------------------------------------------------------------------------
    # extraire les produits des pages
    liste_produits = []
    liste_liens_deuxieme_chance = []
    liste_liens_troisieme_chance = []

    while not queue_rangee.empty() : 
        lien = queue_rangee.get()
        print(lien) 
        try : 
            liste_produits += get_produits_from_page_tbody(lien)
        except Exception as e :
          
            # si l'accès à la page échoue alors on donne une deuxième chace à la page puis une troisième
            if lien not in liste_liens_deuxieme_chance:
                liste_liens_deuxieme_chance.append([lien , type(e).__name__])
                queue_rangee.put(lien)
            elif lien not in liste_liens_troisieme_chance:
                liste_liens_troisieme_chance.append([lien , type(e).__name__])
                queue_rangee.put(lien)
                
                
    # Sauvegarder les produits dans un fichier CSV    
    save_produits_to_csv_file(NOM_FICHIER,liste_produits)


    temps_fin = timeit.default_timer()

    duree_d_execution = (temps_fin - temps_debut) / 60

    # Afficher les résultats
    print("le code s'est execute en {:.3f} minutes".format(duree_d_execution))  
    print("nombre de produits : " ,len(liste_produits))
    print("nombre de liens qui ont eu une deuxieme chance  : " , len(liste_liens_deuxieme_chance))
    print("liste des liens qui ont eu une deuxieme chance  : " ,liste_liens_deuxieme_chance)
    print("nombre de liens qui ont eu une troisieme chance : " , len(liste_liens_troisieme_chance))
    print("liste des liens qui ont eu une troisieme chance : " ,liste_liens_troisieme_chance)


        
