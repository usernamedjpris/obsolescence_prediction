#encoding: utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys #Pour pouvoir utiliser le clavier
import selenium as sel
import builtins as blt
import time #Le module time va nous permettre de mettre des delais pour temporiser les chargements des pages
import io
from datetime import date


navigateur = webdriver.Chrome() #Definit le driver qui va etre utlise
navigateur.set_window_size(800,680) #(largeur,hauteur)


## utilitaires
liste_des_vars = []
dict_core = {"Single-Core":1, "Dual-Core":2, "Quad-Core":4, "Hexa-Core":6, "Octo-Core":8}
dict_mois = {"Janvier":1, "Février":2, "Mars":3, "Avril":4, "Mai":5, "Juin":6, "Juillet":7, "Août":8, "Septembre":9, "Octobre":10, "Novembre":11, "Décembre":12}

def capture_and_attribute(section):
    """une section est une liste de variable, valeur : cette fonction attribue la valeur à une nouvelle variable du nom du premier du nom de la variable donné par la section"""
    for i in range(len(section)//2):
        nom = section[2*i].split(" ")[0].replace("?","")
        globals()[nom] = section[2*i+1]   
        global liste_des_vars
        liste_des_vars.append(nom)

def int_(text_avec_unite, index=0):
    return int(text_avec_unite.split(" ")[index])

def float_(text_avec_unite, index=0):
    return float(text_avec_unite.split(" ")[index])

def relativise_(texte):
    accoudoir = texte.replace(" sur ","/").replace("Tout (","")
    if accoudoir.find(")")>0:
        accoudoir = accoudoir.replace(")","")
        accoudoir += "/"+accoudoir
    return accoudoir

def reinitialise():
    global liste_des_vars
    for var in liste_des_vars:        
        globals()[var] = "N/A"

navigateur.get("https://www.kimovil.com/fr/prix-telephones-apple") #Le navigateur va s'ouvrir et va charger cette page
#time.sleep(1) #On met en pause le programme 3 secondes pour etre sur que la page charge correctement
gamme = navigateur.find_elements_by_xpath('//*[@id="margin"]/div[2]/div/ul/li/a') #On localise la liste des smartphones
gamme = [ el.get_attribute("href") for el in gamme]

for page in gamme:
    reinitialise()
    print("\n\nurl :", page)
    navigateur.get(page)
    navigateur.execute_script("var elements = document.getElementsByClassName('sub'); for(var i=0;i<elements.length; i++){elements[i].innerText = ''}")
    
    ## Fiche technique    
    intitule = navigateur.find_element_by_xpath('//*[@id="sec-start"]').text.replace("Prix et caractéristiques du\n","").split(" ")   
    marque, modele = intitule[0], ' '.join(intitule[1:]) # le premier mot c'est la marque et le reste c'est le nom du modele...
    print("marque : ", marque, "\nmodèle :", modele)
    
    Date = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[1]/div/dl[2]/dd[1]').text.split(",")[0].split(" ")
    Date = date(int(Date[1]),dict_mois[Date[0]],1)
    print("date : ",Date)
    
    try:
        Prédécesseur = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[1]/div/dl[3]/dd[1]/ul/li/a').text
        Successeur = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[1]/div/dl[3]/dd[2]/ul/li/a').text        
    except sel.common.exceptions.NoSuchElementException:   
        try:
            relation = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[1]/div/dl[3]/dt[1]').text
            if  relation == "Prédécesseur":   
                Prédécesseur = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[1]/div/dl[3]/dd[1]/ul/li/a').text
                Successeur = "N/A"
            elif relation == "Successeur":
                Prédécesseur = "N/A"
                Successeur = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[1]/div/dl[3]/dd[1]/ul/li/a').text
        except sel.common.exceptions.NoSuchElementException: 
            pass
    print("prédécesseur : ", Prédécesseur, "\nsuccesseur : ", Successeur)
    
    
    
    ## Antutu
    antutu = float(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[2]/div/ul[2]/li[4]/a/span[2]').text)
    print("antutu : ", antutu) 
    
    
    ## Structure
    structure = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[2]/div/dl[1]').text.split("\n")
    capture_and_attribute(structure)
    
    Taille = Taille.split(" ") # mm
    Largeur, Hauteur, Epaisseur = float(Taille[0]), float(Taille[3]), float(Taille[6])
    print("largeur (mm) : ", Largeur, "\nhauteur (mm) : ", Hauteur, "\nepaisseur (mm) : ", Epaisseur)

    Poids = float_(Poids) #float(Poids.replace("g","")) # g
    print("masse (g) : ", Poids)    

    Surface = float_(Surface) #float(Surface.replace("%","")) # %
    print("surface utile (%) : ", Surface) 

    try:
        certificat = Certificat          
    except blt.NameError:
        certificat = "Non"      
    print("certificat : ", certificat)
    
    
    ## Écran
    écran = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[2]/div/dl[2]').text.split("\n")
    capture_and_attribute(écran)
    ecran_type = Type
    print("type :", ecran_type)
    Densité = int_(Densité)  #int(Densité.split(" ")[0])
    print("densité (ppi) :", Densité)
    l, h = float_(Résolution), float_(Résolution,2)#float(Résolution.split(" ")[0]), float(Résolution.split(" ")[2])
    print("largeur (px) : ", l, "\nhauteur (px) : ", h)    
    if (Autres.find("Scratch resistant")>0):
        resistant = "Oui"
    else:
        resistant = "Non"
    if (Autres.find("Gorilla")>0):
        gorilla = Autres[Autres.find("Gorilla")+15]
    else:
        gorilla ="Non"


    ## Processeur
    processeur = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[3]/div[1]/dl[1]').text.split("\n")
    capture_and_attribute(processeur)
    nb_processeur = dict_core[Type]
    print("nombre de processeur :", nb_processeur)
    Fréquence = float_(Fréquence)
    print("frequence (Ghz) :",Fréquence)
    
    ## RAM
    ram = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[3]/div[1]/dl[3]').text.split("\n")
    capture_and_attribute(ram)
    RAM = int_(RAM)
    print("RAM (GB) :",RAM) 
    
    ## Stockage
    stockage = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[3]/div[1]/dl[5]').text.split("\n")
    capture_and_attribute(stockage)
    Capacité = int_(Capacité)  
    print("capacité (GB) :", Capacité, "\nextensible :", Extensible)
    
    ## Capteurs
    capteurs = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[3]/div[1]/dl[7]').text.split("\n")
    capture_and_attribute(capteurs)
    print("fingerprint :", Fingerprint, "\nproximité :", Proximité, "\naccéléromètre :", Accéléromètre, "\nlumière d'ambiance :", Lumière, "\nboussole :", Boussole, "\ngyroscope :", Gyroscope, "\nbaromètre :", Baromètre)
    
    ## Batterie
    Batterie = int_(navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[2]/div/ul[2]/li[5]/a/span[2]').text)
    print("capacité (mAh) : ", Batterie)     
    
    ## Connectivité
    connexions = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[6]/div[3]/dl[8]').text.split("\n")
    capture_and_attribute(capteurs)
    capture_and_attribute(connexions)
    
    print("NFC :", NFC, "\njack :", Audio, "\nradio FM :", Radio, "\ncomputer sync :", Computer, "\nOTA sync :", OTA, "\ntethering :", Partager, "\nVoLTE :", VoLTE)
        
    bluetooth = navigateur.find_element_by_xpath('//*[@id="margin"]/div[2]/div/div[5]/section[6]/div[3]/dl[4]').text.split("\n")
    capture_and_attribute(capteurs)
    capture_and_attribute(bluetooth)
    Version = float_(Version,1)
    print("bluetooth", Version)
    
    cinqG_fr = relativise_(navigateur.find_element_by_xpath('//*[@id="country-coverage-data"]/dl[1]/dd/ul/li[1]/div[2]').text)
    quatreG_fr = relativise_(navigateur.find_element_by_xpath('//*[@id="country-coverage-data"]/dl[1]/dd/ul/li[2]/div[2]').text)
    troisG_fr = relativise_(navigateur.find_element_by_xpath('//*[@id="country-coverage-data"]/dl[1]/dd/ul/li[3]/div[2]').text)
    deuxG_fr = relativise_(navigateur.find_element_by_xpath('//*[@id="country-coverage-data"]/dl[1]/dd/ul/li[4]/div[2]').text)    
    print("2G (FR) :", deuxG_fr, "\n3G (FR) :", troisG_fr, "\n4G (FR) :", quatreG_fr, "\n5G (FR) :", cinqG_fr)
    
    connectivite = navigateur.find_element_by_xpath('//*[@id="country-coverage"]/div[4]/a').get_attribute("href")
    
    #print("url :", connectivite.replace("FR","US"))    
    navigateur.get(connectivite.replace("FR","US"))
    cinqG_us = relativise_(navigateur.find_element_by_xpath('//*[@id="main-wrapper"]/div[1]/div[1]/div/table/tbody/tr[1]/td[3]/ul/li[1]/div[2]').text)
    quatreG_us = relativise_(navigateur.find_element_by_xpath('//*[@id="main-wrapper"]/div[1]/div[1]/div/table/tbody/tr[1]/td[3]/ul/li[2]/div[2]').text)
    troisG_us = relativise_(navigateur.find_element_by_xpath('//*[@id="main-wrapper"]/div[1]/div[1]/div/table/tbody/tr[1]/td[3]/ul/li[3]/div[2]').text)
    deuxG_us = relativise_(navigateur.find_element_by_xpath('//*[@id="main-wrapper"]/div[1]/div[1]/div/table/tbody/tr[1]/td[3]/ul/li[4]/div[2]').text)        
    print("2G (US) :", deuxG_us, "\n3G (US) :", troisG_us, "\n4G (US) :", quatreG_us, "\n5G (US) :", cinqG_us)    
        
    
    #print("url :", connectivite.replace("FR","JP"))   
    navigateur.get(connectivite.replace("FR","JP"))
    cinqG_jp = relativise_(navigateur.find_element_by_xpath('//*[@id="main-wrapper"]/div[1]/div[1]/div/table/tbody/tr[1]/td[3]/ul/li[1]/div[2]').text)
    quatreG_jp = relativise_(navigateur.find_element_by_xpath('//*[@id="main-wrapper"]/div[1]/div[1]/div/table/tbody/tr[1]/td[3]/ul/li[2]/div[2]').text)
    troisG_jp = relativise_(navigateur.find_element_by_xpath('//*[@id="main-wrapper"]/div[1]/div[1]/div/table/tbody/tr[1]/td[3]/ul/li[3]/div[2]').text)
    deuxG_jp = relativise_(navigateur.find_element_by_xpath('//*[@id="main-wrapper"]/div[1]/div[1]/div/table/tbody/tr[1]/td[3]/ul/li[4]/div[2]').text) 
    print("2G (JP) :", deuxG_jp, "\n3G (JP) :", troisG_jp, "\n4G (JP) :", quatreG_jp, "\n5G (JP) :", cinqG_jp)    
    
    
    #print("url :", connectivite.replace("FR","CN"))   
    navigateur.get(connectivite.replace("FR","CN"))
    cinqG_ch = relativise_(navigateur.find_element_by_xpath('//*[@id="main-wrapper"]/div[1]/div[1]/div/table/tbody/tr[1]/td[3]/ul/li[1]/div[2]').text)
    quatreG_ch = relativise_(navigateur.find_element_by_xpath('//*[@id="main-wrapper"]/div[1]/div[1]/div/table/tbody/tr[1]/td[3]/ul/li[2]/div[2]').text)
    troisG_ch = relativise_(navigateur.find_element_by_xpath('//*[@id="main-wrapper"]/div[1]/div[1]/div/table/tbody/tr[1]/td[3]/ul/li[3]/div[2]').text)
    deuxG_ch = relativise_(navigateur.find_element_by_xpath('//*[@id="main-wrapper"]/div[1]/div[1]/div/table/tbody/tr[1]/td[3]/ul/li[4]/div[2]').text)     
    print("2G (CH) :", deuxG_ch, "\n3G (CH) :", troisG_ch, "\n4G (CH) :", quatreG_ch, "\n5G (CH) :", cinqG_ch)
    
navigateur.quit()