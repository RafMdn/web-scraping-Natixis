import requests 
from bs4 import BeautifulSoup
import re
import urllib.parse

class Produit :
    def __init__(self, code , label ):
        self.code = code
        self.label = label


url = "https://www.douane.gov.dz/spip.php?page=tarif_douanier"
douane_url = "https://www.douane.gov.dz/"



response = requests.get(url, verify=False)
content = response.text

soup = BeautifulSoup(content, 'html.parser')
tbody = soup.find('tbody')
# tables = soup.find_all('table')
liens_par_section = []
print("liens par section--------------------------------------------")
for tr in tbody.find_all('tr'):
 
    href = str(tr.get('data-href'))
    print(href)
    lien = douane_url + href
    liens_par_section.append(lien)

print(liens_par_section)

# ------------------------------------------------------------------------

liens_par_chapitre = []
print("liens par chapitre--------------------------------------------")
for lien in liens_par_section : 
        
    response = requests.get(lien, verify=False)
    content = response.text

    soup = BeautifulSoup(content, 'html.parser')
    tbody = soup.find('tbody')
    # tables = soup.find_all('table')
    for tr in tbody.find_all('tr'):
    
        href = str(tr.get('data-href'))
        print(href)
        lien = douane_url + href
        liens_par_chapitre.append(lien)
        

print(liens_par_chapitre)


# ------------------------------------------------------------------------
cpt = 1
print("liens par rangee--------------------------------------------")
liens_par_rangee = []
for lien in liens_par_chapitre : 
    cpt += 1
    response = requests.get(lien, verify=False)
    content = response.text

    soup = BeautifulSoup(content, 'html.parser')
    tbody = soup.find('tbody')
    # tables = soup.find_all('table')
    for tr in tbody.find_all('tr'):
        href = str(tr.get('data-href'))
        print(href)
        lien = douane_url + href
        liens_par_rangee.append(lien)
    if cpt == 3 : break
        

print(liens_par_rangee)


cpt = 1

liste_produits = []
print("liens par produit--------------------------------------------")

for lien in liens_par_rangee : 
        
    response = requests.get(lien, verify=False)
    content = response.text

    soup = BeautifulSoup(content, 'html.parser')
    tbody = soup.find('tbody')
    # tables = soup.find_all('table')
    for tr in tbody.find_all('tr'):
    
        td = tr.find_all("td")
        code = td[0].text
        label = td[1].text
        if code != "":
            
            parsed = urllib.parse.urlparse(lien)
            params = urllib.parse.parse_qs(parsed.query)

            chapitre = params['chapitre'][0] 
            range = params['range'][0]

            print(chapitre) # 01
            print(range) # 01
           
            produit = Produit(code= str(chapitre) + str(range) + str(code).replace(" ","") ,  label= str(label).lstrip('- ') )
            liste_produits.append(produit)

            
        # if href : 
        #     print(href)   
        #     lien = douane_url + str(href)
        #     liens_produits.append(lien)
    if cpt == 3 : break

for produit in liste_produits:
    print("code is :" + produit.code + " label is :" + produit.label )

    

# # ------------------------------------------------------------------------
# cpt = 1

# liens_produits = []
# print("liens par produit--------------------------------------------")

# for lien in liens_par_rangee : 
        
#     response = requests.get(lien, verify=False)
#     content = response.text

#     soup = BeautifulSoup(content, 'html.parser')
#     tbody = soup.find('tbody')
#     # tables = soup.find_all('table')
#     for tr in tbody.find_all('tr'):
    
#         href = tr.get('data-href')
        
#         if href : 
#             print(href)   
#             lien = douane_url + str(href)
#             liens_produits.append(lien)
#     if cpt == 3 : break   

# print(liens_produits)
    
# # ------------------------------------------------------------------------


