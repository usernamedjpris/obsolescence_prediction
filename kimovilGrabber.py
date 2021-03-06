#encoding: utf-8
from selenium import webdriver
import selenium as sel
import builtins as blt
import time 
import io
from datetime import date
import csv



## utilitaires

dict_core = {"Single-Core":1, "Dual-Core":2, "Quad-Core":4, "Hexa-Core":6, "Octa-Core":8, "Deca-Core":10}
dict_mois = {"Janvier":1, "Février":2, "Mars":3, "Avril":4, "Mai":5, "Juin":6, "Juillet":7, "Août":8, "Septembre":9, "Octobre":10, "Novembre":11, "Décembre":12}
marques =  ["apple", "samsung", "oneplus", "huawei", "google", "motorola", "oppo", "xiaomi", "sony"] 

# e comme "extraction"
e = {"Résolution": 'N/A', "Taille": 'N/A', "Poids": 'N/A', "Surface": 'N/A', "Certificats": 'N/A', "Type": 'N/A', "Densité": 'N/A', "Autres": 'N/A', "Type": 'N/A', "Fréquence": 'N/A', "RAM": 'N/A', "Capacité": 'N/A', "Extensible": 'N/A', "Fingerprint": 'N/A', "Proximité": 'N/A', "Accéléromètre": 'N/A', "Lumière": "N/A", "Boussole": 'N/A', "Gyroscope": 'N/A', "Baromètre": 'N/A', "NFC": 'N/A', "Audio": 'N/A', "Radio": 'N/A', "Computer": 'N/A', "OTA": 'N/A', "Partager": 'N/A', "VoLTE": 'N/A', "OTA": 'N/A', "Version": 'N/A'}
# f comme "formattage"
f = {"Marque": 'N/A', "Modele": 'N/A', "Date": 'N/A', "Prédécesseur": 'N/A', "Successeur": 'N/A', "Antutu": 'N/A', "Largeur": 'N/A', "Hauteur": 'N/A', "Epaisseur": 'N/A', "Poids": 'N/A', "Surface": 'N/A', "certificat": 'N/A', "ecran_type": 'N/A', "Densité": 'N/A', "l": 'N/A', "h": 'N/A', "resistant":'N/A', "gorilla":'N/A', "nb_processeur": 'N/A', "Fréquence": 'N/A', "RAM": 'N/A', "Batterie": 'N/A', "Extensible": 'N/A', "Fingerprint": 'N/A', "Proximité": 'N/A', "Accéléromètre": 'N/A', "Lumière": 'N/A', "Boussole": 'N/A', "Gyroscope": 'N/A', "Baromètre": 'N/A', "Capacité": 'N/A', "NFC": 'N/A', "Audio": 'N/A', "Radio": 'N/A', "Computer": 'N/A', "OTA": 'N/A', "Partager": 'N/A', "VoLTE": 'N/A', "OTA": 'N/A', "Version": 'N/A', "deuxG_FR": 'N/A', "troisG_FR": 'N/A', "quatreG_FR": 'N/A', "cinqG_FR": 'N/A', "deuxG_US": 'N/A', "troisG_US": 'N/A', "quatreG_US": 'N/A', "cinqG_US": 'N/A', "deuxG_JP": 'N/A', "troisG_JP": 'N/A', "quatreG_JP": 'N/A', "cinqG_JP": 'N/A', "deuxG_CN": 'N/A', "troisG_CN": 'N/A', "quatreG_CN": 'N/A', "cinqG_CN": 'N/A'}
# c comme "caractéristique"
c = {"marque": 'N/A', "modèle": 'N/A', "date": 'N/A', "prédécesseur": 'N/A', "successeur": 'N/A', "antutu": 'N/A', "Résolution capteur principal (Mpx)" : 'N/A',"Ouverture capteur principal (ƒ/)" : 'N/A', "Résolution capteur selfie (Mpx)": 'N/A', "Ouverture capteur selfie (ƒ/)": 'N/A',"largeur (mm)": 'N/A', "hauteur (mm)": 'N/A', "epaisseur (mm)": 'N/A', "masse (g)": 'N/A', "surface utile (%)": 'N/A', "certificat de résistance": 'N/A', "type écran": 'N/A', "densité (ppi)": 'N/A', "largeur (px)": 'N/A', "hauteur (px)": 'N/A', "nombre de processeur": 'N/A', "fréquence (GHz)": 'N/A', "RAM (GB)": 'N/A', "capacité (GB)": 'N/A', "extensible": 'N/A', "fingerprint": 'N/A', "proximité": 'N/A', "accéléromètre": 'N/A', "lumière d'ambiance": 'N/A', "Boussole": 'N/A', "gyroscope": 'N/A', "baromètre": 'N/A', "capacité (mAh)": 'N/A', "NFC": 'N/A', "jack": 'N/A', "radio FM": 'N/A', "computer sync": 'N/A', "OTA sync": 'N/A', "tethering": 'N/A', "VoLTE": 'N/A', "OTA": 'N/A', "bluetooth": 'N/A', "2G (FR)": 'N/A', "3G (FR)": 'N/A', "4G (FR)": 'N/A', "5G (FR)": 'N/A', "2G (US)": 'N/A', "3G (US)": 'N/A', "4G (US)": 'N/A', "5G (US)": 'N/A', "2G (JP)": 'N/A', "3G (JP)": 'N/A', "4G (JP)": 'N/A', "5G (JP)": 'N/A', "2G (CN)": 'N/A', "3G (CN)": 'N/A', "4G (CN)": 'N/A', "5G (CN)": 'N/A', 'nombre avis' : 0, "général (avis)": 'N/A', "rayures? (avis)": 'N/A', "joli? (avis)":'N/A', "pratique? (avis)":'N/A', "soleil? (avis)":'N/A', "son? (avis)":'N/A', "fluide? (avis)":'N/A', "jeux? (avis)":'N/A', "photos diurnes (avis)":'N/A', "photos nocturnes (avis)":'N/A', "selfies? (avis)":'N/A', "flash? (avis)":'N/A', "appels? (avis)":'N/A', "GPS? (avis)":'N/A', "Wifi? (avis)":'N/A'}
# mappage entre f et coppo", 
map_ = {"Marque": 'marque', "Modele": 'modèle', "Date": 'date', "Prédécesseur": 'prédécesseur', "Successeur": 'successeur', "Antutu": 'antutu', "Largeur": 'largeur (mm)', "Hauteur": 'hauteur (mm)', "Epaisseur": 'epaisseur (mm)', "Poids": 'masse (g)', "Surface": 'surface utile (%)', "certificat": 'certificat de résistance', "ecran_type": 'type écran', "Densité": 'densité (ppi)', "l": 'largeur (px)', "h": 'hauteur (px)', "resistant":'résistant aux rayures', "gorilla":'gorilla glass', "nb_processeur": 'nombre de processeur', "Fréquence": 'fréquence (GHz)', "RAM": 'RAM (GB)', "Batterie": 'capacité (mAh)', "Extensible": 'extensible', "Fingerprint": 'fingerprint', "Proximité": 'proximité', "Accéléromètre": 'accéléromètre', "Lumière": "lumière d'ambiance", "Boussole": 'Boussole', "Gyroscope": 'gyroscope', "Baromètre": 'baromètre', "Capacité": 'capacité (GB)', "NFC": 'NFC', "Audio": 'jack', "Radio": 'radio FM', "Computer": 'computer sync', "OTA": 'OTA sync', "Partager": 'tethering', "VoLTE": 'VoLTE', "OTA": 'OTA', "Version": 'bluetooth', "deuxG_FR": '2G (FR)', "troisG_FR": '3G (FR)', "quatreG_FR": '4G (FR)', "cinqG_FR": '5G (FR)', "deuxG_US": '2G (US)', "troisG_US": '3G (US)', "quatreG_US": '4G (US)', "cinqG_US": '5G (US)', "deuxG_JP": '2G (JP)', "troisG_JP": '3G (JP)', "quatreG_JP": '4G (JP)', "cinqG_JP": '5G (JP)', "deuxG_CN": '2G (CN)', "troisG_CN": '3G (CN)', "quatreG_CN": '4G (CN)', "cinqG_CN": '5G (CN)'}


def extrait_(section):
    """une section est une liste de variable, valeur : cette fonction attribue la valeur à une nouvelle variable du nom du premier du nom de la variable donné par la section"""
    for i in range(len(section)//2):
        nom = section[2*i].split(" ")[0].replace("?","")         
        global e
        e[nom] = section[2*i+1]  

def renomme_():
    """mappage entre f et c"""
    global f,c
    for el in f:
        c[map_[el]] = f[el]

def int_(text_avec_unite, index=0):
    """converti en entier le indexième mot"""
    return int(text_avec_unite.split(" ")[index])

def float_(text_avec_unite, index=0):
    """converti en float le indexième mot si possible"""
    try:
        return float(text_avec_unite.split(" ")[index])
    except blt.ValueError:
        return "N/A"  
    except blt.IndexError: 
        return "N/A"

def relativise_(texte):
    """converti en fraction reconnaissable par excel"""
    accoudoir = texte.replace(" sur ","/").replace("Tout (","")
    if accoudoir.find(")")>0:
        accoudoir = accoudoir.replace(")","")
        accoudoir += "/"+accoudoir
    return "="+accoudoir

def reinitialise_():
    """reinitialisation aux valeurs par défaut N/A pour chacun des dictionnaires"""
    global e,f,c
    e = {"Résolution": 'N/A', "Taille": 'N/A', "Poids": 'N/A', "Surface": 'N/A', "Certificats": 'N/A', "Type": 'N/A', "Densité": 'N/A', "Autres": 'N/A', "Type": 'N/A', "Fréquence": 'N/A', "RAM": 'N/A', "Capacité": 'N/A', "Extensible": 'N/A', "Fingerprint": 'N/A', "Proximité": 'N/A', "Accéléromètre": 'N/A', "Lumière": "N/A", "Boussole": 'N/A', "Gyroscope": 'N/A', "Baromètre": 'N/A', "NFC": 'N/A', "Audio": 'N/A', "Radio": 'N/A', "Computer": 'N/A', "OTA": 'N/A', "Partager": 'N/A', "VoLTE": 'N/A', "OTA": 'N/A', "Version": 'N/A'}
    f = {"Marque": 'N/A', "Modele": 'N/A', "Date": 'N/A', "Prédécesseur": 'N/A', "Successeur": 'N/A', "Antutu": 'N/A', "Largeur": 'N/A', "Hauteur": 'N/A', "Epaisseur": 'N/A', "Poids": 'N/A', "Surface": 'N/A', "certificat": 'N/A', "ecran_type": 'N/A', "Densité": 'N/A', "l": 'N/A', "h": 'N/A', "resistant":'N/A', "gorilla":'N/A', "nb_processeur": 'N/A', "Fréquence": 'N/A', "RAM": 'N/A', "Batterie": 'N/A', "Extensible": 'N/A', "Fingerprint": 'N/A', "Proximité": 'N/A', "Accéléromètre": 'N/A', "Lumière": 'N/A', "Boussole": 'N/A', "Gyroscope": 'N/A', "Baromètre": 'N/A', "Capacité": 'N/A', "NFC": 'N/A', "Audio": 'N/A', "Radio": 'N/A', "Computer": 'N/A', "OTA": 'N/A', "Partager": 'N/A', "VoLTE": 'N/A', "OTA": 'N/A', "Version": 'N/A', "deuxG_FR": 'N/A', "troisG_FR": 'N/A', "quatreG_FR": 'N/A', "cinqG_FR": 'N/A', "deuxG_US": 'N/A', "troisG_US": 'N/A', "quatreG_US": 'N/A', "cinqG_US": 'N/A', "deuxG_JP": 'N/A', "troisG_JP": 'N/A', "quatreG_JP": 'N/A', "cinqG_JP": 'N/A', "deuxG_CN": 'N/A', "troisG_CN": 'N/A', "quatreG_CN": 'N/A', "cinqG_CN": 'N/A'}
    c = {"marque": 'N/A', "modèle": 'N/A', "date": 'N/A', "prédécesseur": 'N/A', "successeur": 'N/A', "antutu": 'N/A', "Résolution capteur principal (Mpx)" : 'N/A',"Ouverture capteur principal (ƒ/)" : 'N/A', "Résolution capteur selfie (Mpx)": 'N/A', "Ouverture capteur selfie (ƒ/)": 'N/A',"largeur (mm)": 'N/A', "hauteur (mm)": 'N/A', "epaisseur (mm)": 'N/A', "masse (g)": 'N/A', "surface utile (%)": 'N/A', "certificat de résistance": 'N/A', "type écran": 'N/A', "densité (ppi)": 'N/A', "largeur (px)": 'N/A', "hauteur (px)": 'N/A', "nombre de processeur": 'N/A', "fréquence (GHz)": 'N/A', "RAM (GB)": 'N/A', "capacité (GB)": 'N/A', "extensible": 'N/A', "fingerprint": 'N/A', "proximité": 'N/A', "accéléromètre": 'N/A', "lumière d'ambiance": 'N/A', "Boussole": 'N/A', "gyroscope": 'N/A', "baromètre": 'N/A', "capacité (mAh)": 'N/A', "NFC": 'N/A', "jack": 'N/A', "radio FM": 'N/A', "computer sync": 'N/A', "OTA sync": 'N/A', "tethering": 'N/A', "VoLTE": 'N/A', "OTA": 'N/A', "bluetooth": 'N/A', "2G (FR)": 'N/A', "3G (FR)": 'N/A', "4G (FR)": 'N/A', "5G (FR)": 'N/A', "2G (US)": 'N/A', "3G (US)": 'N/A', "4G (US)": 'N/A', "5G (US)": 'N/A', "2G (JP)": 'N/A', "3G (JP)": 'N/A', "4G (JP)": 'N/A', "5G (JP)": 'N/A', "2G (CN)": 'N/A', "3G (CN)": 'N/A', "4G (CN)": 'N/A', "5G (CN)": 'N/A', 'nombre avis' : 0, "général (avis)": 'N/A', "rayures? (avis)": 'N/A', "joli? (avis)":'N/A', "pratique? (avis)":'N/A', "soleil? (avis)":'N/A', "son? (avis)":'N/A', "fluide? (avis)":'N/A', "jeux? (avis)":'N/A', "photos diurnes (avis)":'N/A', "photos nocturnes (avis)":'N/A', "selfies? (avis)":'N/A', "flash? (avis)":'N/A', "appels? (avis)":'N/A', "GPS? (avis)":'N/A', "Wifi? (avis)":'N/A'}


## contextualisation

navigateur = webdriver.Chrome() # Definit le driver qui va etre utlise


## boucle

for brand in marques:
    navigateur.get("https://www.kimovil.com/fr/prix-telephones-"+brand) # chargement de la page de la gamme de la marque
    gamme = navigateur.find_elements_by_xpath('//*[@id="margin"]/div[2]/div/ul/li/a') # On localise la liste des smartphones de la gamme
    gamme = [el.get_attribute("href") for el in gamme]
    donnees = []
    
    
    for i,page in enumerate(gamme):
        reinitialise_()
        print('\n\n[',i+1,"/",len(gamme),"]")
        print("url :", page)
        navigateur.get(page)

        ## Fiche technique    
        intitule = navigateur.find_element_by_xpath('//*[@id="sec-start"]').text.replace("Prix et caractéristiques du\n","").split(" ")   
        f['Marque'], f['Modele'] = intitule[0], ' '.join(intitule[1:]) # le premier mot c'est la marque et le reste c'est le nom du modele...
        print("marque : ", f['Marque'], "\nmodèle :", f['Modele'])
        

        f['Date'] = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[1]/div/dl[2]/dd[1]').text.split(",")[0].split(" ")
        try:        
            f['Date'] = date(int(f['Date'][1]), dict_mois[f['Date'][0]],1)
        except blt.IndexError:
            f['Date'] = f['Date'][0]
        except blt.ValueError:
            f['Date'] = "N/A"    
        print("date : ",f['Date'])
        
        
        navigateur.execute_script("var elements = document.getElementsByClassName('sub'); for(var i=0;i<elements.length; i++){elements[i].innerText = ''}")
        navigateur.execute_script("var elements = document.getElementsByTagName('dd'); for(var i=0;i<elements.length; i++){if(elements[i].innerText.length == 0){elements[i].innerText = 'N/A';} }") # expliciter les donnees non renseignée pour éviter les décalages dans l'extraction
        
        try:
            f['Prédécesseur'] = ' '.join(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[1]/div/dl[3]/dd[1]/ul/li/a').text.split(" ")[1:]) # on prend pas la marque mais que le modèle
            f['Successeur'] = ' '.join(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[1]/div/dl[3]/dd[2]/ul/li/a').text.split(" ")[1:])        
        except sel.common.exceptions.NoSuchElementException:   
            try:
                relation = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[1]/div/dl[3]/dt[1]').text
                if  relation == "Prédécesseur":   
                    f['Prédécesseur'] = ' '.join(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[1]/div/dl[3]/dd[1]/ul/li/a').text.split(" ")[1:])
                    f['Successeur'] = "N/A"
                elif relation == "Successeur":
                    f['Prédécesseur'] = "N/A"
                    f['Successeur'] = ' '.join(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[1]/div/dl[3]/dd[1]/ul/li/a').text.split(" ")[1:])
            except sel.common.exceptions.NoSuchElementException: 
                f['Prédécesseur'] = "N/A"
                f['Successeur'] = "N/A"
        print("prédécesseur : ", f['Prédécesseur'], "\nsuccesseur : ", f['Successeur'])
        
          
        ## Antutu
        f['Antutu'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[2]/div/ul[2]/li[4]/a/span[2]').text)
        print("antutu : ", f['Antutu'])     
        
        ## Photo  
        c['Résolution capteur principal (Mpx)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[2]/div/ul[2]/li[6]/a/span[2]/span[2]').text)
        c['Ouverture capteur principal (ƒ/)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[2]/div/ul[2]/li[6]/a/span[2]/span[2]').text.replace("ƒ/",""),-1)          
        print("résolution capteur principal (Mpx) : ", c['Résolution capteur principal (Mpx)'], "\nouverture capteur principal (ƒ/) : ", c['Ouverture capteur principal (ƒ/)']) 
        
        c['Résolution capteur selfie (Mpx)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[2]/div/ul[2]/li[6]/a/span[4]/span').text,1)
        c['Ouverture capteur selfie (ƒ/)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[2]/div/ul[2]/li[6]/a/span[4]/span').text.replace("ƒ/",""),-1)
        print("résolution capteur selfie (Mpx) : ", c['Résolution capteur selfie (Mpx)'], "\nouverture capteur selfie (ƒ/) : ", c['Ouverture capteur selfie (ƒ/)'])       
        
        ## Structure
        structure = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[2]/div/dl[1]').text.split("\n")
        extrait_(structure)
        
        e['Taille'] = e['Taille'].split(" ") # mm
        f['Largeur'], f['Hauteur'], f['Epaisseur'] = float(e['Taille'][0]), float(e['Taille'][3]), float(e['Taille'][6])
        print("largeur (mm) : ", f['Largeur'], "\nhauteur (mm) : ", f['Hauteur'], "\nepaisseur (mm) : ", f['Epaisseur'])
    
        f['Poids'] = float_(e['Poids']) # g
        print("masse (g) : ", f['Poids'])    
    
        f['Surface'] = float_(e['Surface']) # %
        print("surface utile (%) : ", f['Surface']) 
    
        f['certificat'] = e['Certificats']              
        print("certificat : ", f['certificat'])
        
        
        ## Écran
        écran = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[2]/div/dl[2]').text.split("\n")
        extrait_(écran)
        f['ecran_type'] = e['Type']
        print("type :", f['ecran_type'])
        
        f['Densité'] = int_(e['Densité']) 
        print("densité (ppi) :", f['Densité'])
        
        f['l'], f['h'] = float_(e['Résolution']), float_(e['Résolution'],2)
        print("largeur (px) : ", f['l'], "\nhauteur (px) : ", f['h'])    
        
        if (e['Autres'].find("Scratch resistant")>0):
            f['resistant'] = "Oui" 
        else:
            f['resistant'] = "Non"
        print("résistant aux rayures: ", f['resistant'])    
        
        if (e['Autres'].find("Gorilla")>0):
            f['gorilla'] = "Oui" 
        else:
            f['gorilla'] = "Non"
        print("gorilla glass : ", f['gorilla'])    
    
    
        ## Processeur
        processeur = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[3]/div[1]/dl[1]').text.split("\n")
        extrait_(processeur)
        f['nb_processeur'] = dict_core[e['Type']]
        print("nombre de processeur :", f['nb_processeur'])
        f['Fréquence'] = float_(e['Fréquence'])
        print("Frequence (GHz) :", f['Fréquence'])
        
        
        ## RAM
        ram = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[3]/div[1]/dl[3]').text.split("\n")
        extrait_(ram)
        f['RAM'] = float_(e['RAM'])
        print("RAM (GB) :", f['RAM']) 
        
        
        ## Stockage
        stockage = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[3]/div[1]/dl[5]').text.split("\n")
        extrait_(stockage)
        f['Capacité'] = int_(e['Capacité'])  
        f['Extensible'] = e['Extensible']
        print("capacité (GB) :", f['Capacité'], "\nextensible :", f['Extensible'])
        
        
        ## Capteurs
        capteurs = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[3]/div[1]/dl[7]').text.split("\n")
        extrait_(capteurs)
        f['Fingerprint'] = e['Fingerprint']
        f['Proximité'] = e['Proximité']
        f['Accéléromètre'] = e['Accéléromètre']
        f['Lumière'] = e['Lumière']
        f['Boussole'] = e['Boussole']
        f['Gyroscope'] = e['Gyroscope']
        f['Baromètre'] = e['Baromètre']
        print("fingerprint :", f['Fingerprint'], "\nproximité :", f['Proximité'], "\naccéléromètre :", f['Accéléromètre'], "\nlumière d'ambiance :", f['Lumière'], "\nBoussole :", f['Boussole'], "\ngyroscope :", f['Gyroscope'], "\nbaromètre :", f['Baromètre'])
        
        
        ## Batterie
        f['Batterie'] = int_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[2]/div/ul[2]/li[5]/a/span[2]').text)
        print("capacité (mAh) : ", f['Batterie'])     
        
        ## Avis
        try:
            c['nombre avis'] = int_(navigateur.find_element_by_xpath('//*[@id="sec-datasheet"]/li[2]/div/a/div[3]').text) 
            c['général (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="sec-datasheet"]/li[2]/div/a/div[2]/div').text)
            c['rayures? (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[2]/div/div[2]/div[2]/div[1]/div/div/div').text)
            c['joli? (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[2]/div/div[2]/div[2]/div[2]/div/div/div').text) 
            c['pratique? (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[2]/div/div[2]/div[2]/div[3]/div/div/div').text) 
            c['soleil? (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[2]/div/div[2]/div[2]/div[4]/div/div/div').text) 
            c['son? (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[3]/div[1]/div[2]/div[2]/div[1]/div/div/div').text) 
            c['fluide? (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[3]/div[1]/div[2]/div[2]/div[2]/div/div/div').text) 
            c['jeux? (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[3]/div[1]/div[2]/div[2]/div[3]/div/div/div').text) 
            c['appels? (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[6]/div[3]/div[2]/div[2]/div[1]/div/div/div').text) 
            c['GPS? (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[6]/div[3]/div[2]/div[2]/div[2]/div/div/div').text) 
            c['Wifi? (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[6]/div[3]/div[2]/div[2]/div[3]/div/div/div').text)        
            c['photos diurnes (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[4]/div/div[5]/div[2]/div[1]/div/div/div').text) 
            c['photos nocturnes (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[4]/div/div[5]/div[2]/div[2]/div/div/div').text) 
            c['selfies? (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[4]/div/div[5]/div[2]/div[3]/div/div/div').text) 
            c['flash? (avis)'] = float_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[4]/div/div[5]/div[2]/div[4]/div/div/div').text) 
            print('nombre avis :', c['nombre avis'])
            print('général (avis) :', c['général (avis)'])
            print('rayures? (avis) :', c['rayures? (avis)'])
            print('joli? (avis) :', c['joli? (avis)'])
            print('pratique? (avis) :', c['pratique? (avis)'])
            print('soleil? (avis) :', c['soleil? (avis)'])
            print('son? (avis) :', c['son? (avis)'])
            print('fluide? (avis) :', c['fluide? (avis)'])
            print('jeux? (avis) :', c['jeux? (avis)'])
            print('photos diurne (avis) :', c['photos diurnes (avis)'])
            print('photos nocturne (avis) :', c['photos nocturnes (avis)'])
            print('selfies? (avis) :', c['selfies? (avis)'])
            print('flash? (avis) :', c['flash? (avis)'])
            print('appels? (avis) :', c['appels? (avis)'])
            print('GPS? (avis) :', c['GPS? (avis)'])
            print('Wifi? (avis) :', c['Wifi? (avis)'])      
        
        except sel.common.exceptions.NoSuchElementException: 
            print('nombre avis : 0')
        
        ## Connectivité
        try:
            connexions = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[6]/div[3]/dl[8]').text.split("\n")
        except sel.common.exceptions.NoSuchElementException: 
            connexions = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[6]/div[3]/dl[7]').text.split("\n")
        extrait_(connexions) 
        f['NFC'] = e['NFC']
        f['Audio'] = e['Audio']
        f['Radio'] = e['Radio']
        f['Computer'] = e['Computer']
        f['OTA'] = e['OTA']
        f['Partager'] = e['Partager']
        f['VoLTE'] = e['VoLTE']    
        print("NFC :", f['NFC'], "\njack :", f['Audio'], "\nradio FM :", f['Radio'], "\ncomputer sync :", f['Computer'], "\nOTA sync :", f['OTA'], "\ntethering :", f['Partager'], "\nVoLTE :", f['VoLTE'])
            
        bluetooth = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[6]/div[3]/dl[4]').text.split("\n")
        extrait_(bluetooth)
        f['Version'] = float_(e['Version'],1)
        print("bluetooth", f['Version'])
        
        f['cinqG_FR'] = relativise_(navigateur.find_element_by_xpath('//*[@id="country-coverage-data"]/dl[1]/dd/ul/li[1]/div[2]').text)
        f['quatreG_FR'] = relativise_(navigateur.find_element_by_xpath('//*[@id="country-coverage-data"]/dl[1]/dd/ul/li[2]/div[2]').text)
        f['troisG_FR'] = relativise_(navigateur.find_element_by_xpath('//*[@id="country-coverage-data"]/dl[1]/dd/ul/li[3]/div[2]').text)
        f['deuxG_FR'] = relativise_(navigateur.find_element_by_xpath('//*[@id="country-coverage-data"]/dl[1]/dd/ul/li[4]/div[2]').text)    
        print("2G (FR) :", f['deuxG_FR'], "\n3G (FR) :", f['troisG_FR'], "\n4G (FR) :", f['quatreG_FR'], "\n5G (FR) :", f['cinqG_FR'])
        
        connectivite = navigateur.find_element_by_xpath('//*[@id="country-coverage"]/div[4]/a').get_attribute("href")
        
        #print("url :", connectivite.replace("FR","US"))    
        navigateur.get(connectivite.replace("FR","US"))
        try:
            prefix = '//*[@id="main-wrapper"]/div[1]/div[1]/div/table/tbody/tr[1]'
            navigateur.find_element_by_xpath(prefix)
        except sel.common.exceptions.NoSuchElementException: 
            prefix = '//*[@id="main-wrapper"]/div[1]/div[1]/div/table/tbody/tr' #cas ou seule le marché international est renseigné
        f['cinqG_US'] = relativise_(navigateur.find_element_by_xpath(prefix+'/td[3]/ul/li[1]/div[2]').text)
        f['quatreG_US'] = relativise_(navigateur.find_element_by_xpath(prefix+'/td[3]/ul/li[2]/div[2]').text)
        f['troisG_US'] = relativise_(navigateur.find_element_by_xpath(prefix+'/td[3]/ul/li[3]/div[2]').text)
        f['deuxG_US'] = relativise_(navigateur.find_element_by_xpath(prefix+'/td[3]/ul/li[4]/div[2]').text)        
        print("2G (US) :", f['deuxG_US'], "\n3G (US) :", f['troisG_US'], "\n4G (US) :", f['quatreG_US'], "\n5G (US) :", f['cinqG_US'])    
            
        
        #print("url :", connectivite.replace("FR","JP"))   
        navigateur.get(connectivite.replace("FR","JP"))
        f['cinqG_JP'] = relativise_(navigateur.find_element_by_xpath(prefix+'/td[3]/ul/li[1]/div[2]').text)
        f['quatreG_JP'] = relativise_(navigateur.find_element_by_xpath(prefix+'/td[3]/ul/li[2]/div[2]').text)
        f['troisG_JP'] = relativise_(navigateur.find_element_by_xpath(prefix+'/td[3]/ul/li[3]/div[2]').text)
        f['deuxG_JP'] = relativise_(navigateur.find_element_by_xpath(prefix+'/td[3]/ul/li[4]/div[2]').text) 
        print("2G (JP) :", f['deuxG_JP'], "\n3G (JP) :", f['troisG_JP'], "\n4G (JP) :", f['quatreG_JP'], "\n5G (JP) :", f['cinqG_JP'])    
        
        
        #print("url :", connectivite.replace("FR","CN"))   
        navigateur.get(connectivite.replace("FR","CN"))
        f['cinqG_CN'] = relativise_(navigateur.find_element_by_xpath(prefix+'/td[3]/ul/li[1]/div[2]').text)
        f['quatreG_CN'] = relativise_(navigateur.find_element_by_xpath(prefix+'/td[3]/ul/li[2]/div[2]').text)
        f['troisG_CN'] = relativise_(navigateur.find_element_by_xpath(prefix+'/td[3]/ul/li[3]/div[2]').text)
        f['deuxG_CN'] = relativise_(navigateur.find_element_by_xpath(prefix+'/td[3]/ul/li[4]/div[2]').text)     
        print("2G (CN) :", f['deuxG_CN'], "\n3G (CN) :", f['troisG_CN'], "\n4G (CN) :", f['quatreG_CN'], "\n5G (CN) :", f['cinqG_CN'])
            
    
        
        renomme_()
        donnees.append(c)
        
    ## importation en fichier csv   
    with open("data.csv", 'a', newline="") as fichier:
        scribe = csv.DictWriter(fichier, fieldnames=[el for el in c])
        scribe.writeheader()
        for enregistrement in donnees:
            scribe.writerow(enregistrement)      
    fichier.close()   

navigateur.quit()