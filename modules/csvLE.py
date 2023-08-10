import csv
from scraping import Produit

# enregistrer les produits dans un fichier CSV
def save_produits_to_csv_file(path_fichier , liste_produits ):
    # Ouvrez le fichier en mode écriture ('w') avec l'encodage UTF-8 et newline vide
    with open(path_fichier, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Écrivez la première ligne d'en-tête dans le fichier CSV
        writer.writerow(['Code', 'Label'])
     
        # Parcourez la liste de produits et écrivez chaque produit dans le fichier CSV
        for produit in liste_produits:
            
            writer.writerow([produit.code,  produit.label])

#  Lire les produits à partir un fichier CSV
def read_produits_from_file(path_fichier):
    liste_produits = []

    # Ouvrir le fichier CSV en mode lecture
    with open(path_fichier, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        # Parcourir les lignes du fichier CSV
        for row in reader:
            # Créer un objet Produit à partir des données de la ligne
            produit = Produit(row[0]  , row[1].replace('\xa0',' ') )
            liste_produits.append(produit)

    # Supprimer l'en-tête (la ligne Code,Label ) 
    liste_produits.pop(0)

    # Retourner la liste des produits
    return liste_produits