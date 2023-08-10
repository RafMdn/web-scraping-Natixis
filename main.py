import timeit
import queue

from modules.config import URL_LISTE_SECTIONS ,PATH_FICHIER_LISTE_PRODUITS_AJOUTES, PATH_FICHIER_LISTE_PRODUITS_DOUANE ,PATH_FICHIER_LISTE_PRODUITS_RETIRES, DESTINATAIRES
from modules.scraping import  get_produits_from_page_tbody , get_links_from_page_tbody 
from modules.csvLE import read_produits_from_file , save_produits_to_csv_file
from modules.emailSender import send_emails




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

    # Lire l'ancienne liste 
    anciennne_liste_produits = read_produits_from_file(PATH_FICHIER_LISTE_PRODUITS_DOUANE)  

    # Trouver les produits ajoutés
    liste_produits_ajoutes = [produit for produit in liste_produits if produit.code not in [produit.code for produit in anciennne_liste_produits]]
    # Trouver les produits retirés
    liste_produits_retires = [produit for produit in anciennne_liste_produits if produit.code not in [produit.code for produit in liste_produits]]

    # Sauvegarder les produits dans des fichiers CSV    
    save_produits_to_csv_file(PATH_FICHIER_LISTE_PRODUITS_DOUANE,liste_produits)
    save_produits_to_csv_file(PATH_FICHIER_LISTE_PRODUITS_AJOUTES,liste_produits_ajoutes)
    save_produits_to_csv_file(PATH_FICHIER_LISTE_PRODUITS_RETIRES,liste_produits_retires)

    # Envoyer le résultat par mail
    send_emails(DESTINATAIRES)

    # Calcul du temps d'exécution 
    temps_fin = timeit.default_timer()
    duree_d_execution = (temps_fin - temps_debut) / 60

    # Afficher les résultats
    print("le code s'est execute en {:.3f} minutes".format(duree_d_execution))  
    print("nombre de produits : " ,len(liste_produits))
    print("nombre de liens qui ont eu une deuxieme chance  : " , len(liste_liens_deuxieme_chance))
    print("liste des liens qui ont eu une deuxieme chance  : " ,liste_liens_deuxieme_chance)
    print("nombre de liens qui ont eu une troisieme chance : " , len(liste_liens_troisieme_chance))
    print("liste des liens qui ont eu une troisieme chance : " ,liste_liens_troisieme_chance)
    print("nb acces : " , len(liens_par_rangee) + len(liens_des_chapitre) + len(liens_des_sections) + len(liste_liens_deuxieme_chance) + len(liste_liens_troisieme_chance) + 1)


        
