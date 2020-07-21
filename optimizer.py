#encoding: utf-8
import pandas as pd
import numpy as np
import os
import math
import matplotlib.pyplot as plt
import csv
from scipy.stats import norm
from scipy.stats import alpha
from scipy.stats import lognorm
from scipy.stats import weibull_min
from scipy.stats import exponweib
from scipy.stats import triang
from scipy.optimize import minimize
from datetime import date




## forme de la courbe de distributionhypothèse 
def distrib(t, x,debut,scale,var, offset):
        
        """
        renvoie la distribution selectionnee avec les parametres specifies
        
        t : type de distribution, 'a' pour alpha, 't' pour triangulaire, 'w' pour weibull
        x : array des abscisses
        debut : abscisse où debute la distribution
        scale : parametre de largeur
        var : parametre de hauteur
        offset : permet de decaler legerement le debut de la distribution pour alpha et triangulaire. Pour Weibull ce parametre au parametre de forme
        
        """
        #return stat.norm.pdf(x,debut+scale/2,scale/6)*var#*scale
        #return lognorm.pdf(x,2, debut, scale/6)*var#*scale
        if t == 'a':
                return alpha.pdf(x, 0.8, debut-scale/10+offset, scale/1.7)*var*scale if scale and var > 0 else [0]*len(x)
        elif t == 'w':
                return weibull_min.pdf(x,offset, debut, scale)*var
        #return exponweib.pdf(x,debut, scale)
        elif t == 't':
                return triang.pdf(x, 0.1, debut+ offset, scale)*scale*var

## tests des distributions

x = np.arange(-3, 1000, 0.5)
y = distrib('w',x,600,180,25000, 1.15) #ref
y2 = distrib('w',x,1,500,50, 50) #plus large
y3 = distrib('w', x,1,600,50, 100) #plus haut
fig, ax = plt.subplots(figsize=(9,6))
ax.plot(x,y)
ax.plot(x,y2)
ax.plot(x,y3)
ax.set_xlim([-3,1000])
ax.set_title("courbe de distribution de ventes d'un modèle")

plt.show()




## donnees brutes
def fromApple(modele):
        
        """
        
        filtre les modeles de la marque Apple
        
        """
        return modele.find('Apple') != -1

def removecsv(x):
        """
        
        retire l'extension csv du nom du modele
        
        """
        return x.split('.')[0]

#allresult = [['modele', 'score']]

allresult = [['modele', 'triang', 'alpha', 'weibull', 'best' ]] #liste qui va recenser les distributions pour chaque modele

with open('scrap\\1033smartphones.txt') as file: #indiquer le chemin du fichier txt contenant les noms de tous les modeles
        modeles = file.readlines()

csvfile = pd.read_csv('scrap/data.csv', sep=';') #indiquer chemin du fichier recensant toutes les caracteristiques des modeles
datedebut = {}

for marque, modele, d  in zip(csvfile["marque"], csvfile["modèle"], csvfile["date"]): #formatage du fichier csv et recuperation de la date de lancement du modele
        modele = modele.replace('+', ' plus')
        modele = modele.replace('(', ' ')
        modele = modele.replace(')', '')
        if modele.find(',') != -1:
                modele = modele.split(',')[0]
        try:
                datedebut[marque+" "+modele] = date(int(d.split("/")[2]),int(d.split("/")[1]),int(d.split("/")[0]))
        except (IndexError, AttributeError):
                datedebut[marque+" "+modele] = None

print(len(datedebut))
            

def calculatelaunchdate(d, chiffres):
        
        """
        
        calcule la date de lancement du modele lorsqu'elle n'est pas specifiee dans le fichier data
        
        d : listes des dates
        
        chiffres : valeur de la popularite a la date d
        
        """
        
        lastzero = ""
        for dte, n in zip(d, chiffres):
                if n == 0:
                        lastzero = dte
                elif n == 100:
                        return date.fromordinal(lastzero)
                
## fonction objectif
def objectif(t, X, date, courbe_brute, abscisses):
        
        """
        
        calcule l'ecart absolu entre la courbe de tendance et la modelisation mathematique
        
        t : type de distribution
        
        X : 3-tuple contenant les parametres de largeur, hauteur et offset du modele mathematique
        
        date : dadte de debut de la distribution
        
        courbe_brute : ordonnees de la courbe de tendance
        
        abscisse : valeurs d'abscisses
        
        """
        #print(X)
        cumul = [0 for i in range(len(abscisses))]
        largeur, hauteur, offset = X[0], X[1], X[2]
        y = distrib(t, abscisses, date, largeur, hauteur, offset)
        cumul = [cumul[i]+x for i,x in enumerate(y)]           
        result = float(abs(sum([abs(x-y) for x,y in zip(cumul, courbe_brute)])))
        #print(result)
        return result







## solution
def montre_solution(t, X, date, courbe_brute, abscisses):
        
        """
        Affiche la courbe de modelisation obtenue apres optimisation ainsi que la courbe brute
        
        t : type de distribution
        
        X : 3-tuple contenant les parametres de largeur, hauteur et offset du modele mathematique
        
        date : dadte de debut de la distribution
        
        courbe_brute : ordonnees de la courbe de tendance
        
        abscisse : valeurs d'abscisses
        
        
        """
        cumul = [0 for i in range(len(abscisses))]
        fig, ax = plt.subplots(figsize=(9,6))
        largeur, hauteur, offset = X[0], X[1], X[2]
        print('écart smodele-reel :', objectif(t, X, date, courbe_brute, abscisses))
        y=distrib(t, abscisses, date, largeur, hauteur, offset)    
        ax.plot(abscisses, y, 'b', label="modele : "+modele+" courbe modèle largeur : "+str(round(largeur,1))+" hauteur : "+str(round(hauteur,1))+ " param : "+str(offset))      
        ax.plot(abscisses, courbe_brute, 'k', label="courbe brute")
        ax.legend()
        plt.show()



for modele in modeles: #iteration sur tous les modeles du fichier txt
        
        ##formatage
        
        modele = modele.replace('\n', '')
        modele = modele.replace('+', ' plus')
        modele = modele.replace('(', ' ')
        modele = modele.replace(')', '')
        if modele.find(',') != -1:
                modele = modele.split(',')[0]        
        print(modele)
        donnees_brutes = pd.read_csv('scrap\\modtrends\\'+modele+'.csv', sep=',')
        donnees_brutes["Mois"] = [date(int(x.split("-")[0]), int(x.split("-")[1]),1).toordinal() for x in donnees_brutes["Mois"]] 
        donnees_brutes[modele] = [x for x in donnees_brutes[modele]] 
       
        ##recuperation ou calcul de la date de lancement
        launchdate = datedebut[modele]
        if not launchdate:
                launchdate = calculatelaunchdate(donnees_brutes["Mois"], donnees_brutes[modele])
        print('date pour ce modele : ', launchdate)

        ##fonctions d'optimisations suivant la distribution choisie
        def objW(X):
                global donnees_brutes
                return objectif('w', X, launchdate.toordinal(), donnees_brutes[modele], donnees_brutes["Mois"])
        def objA(X):
                global donnees_brutes
                return objectif('a', X, launchdate.toordinal(), donnees_brutes[modele], donnees_brutes["Mois"])
        def objT(X):
                global donnees_brutes
                return objectif('t', X, launchdate.toordinal(), donnees_brutes[modele], donnees_brutes["Mois"])        
        
        ## minimizer
        x0W = [183, 25000, 1.15] #modelisation initiale pour Weibull
        bndsW = ((150, 1500), (24000,100000), (1.05, 1.9)) #bornes des parametres de la loi de Weibull
        x0A = [250,50, 0] #modelisation initiale pour Alpha et triangulaire
        bndsA = ((100, 5000),(1, 100), (-400, 50)) # bornes des parametres de la loi Alpha et triangulaires (entre 60 et 10000 jours, entre 1 et 100 unites ordonnée et entre -400 et 50 pour l'offset)
        result = minimize(objW, x0W, method='Powell', bounds=bndsW, options={'maxiter': 100000, 'maxfev': 1000,'disp': True, 'return_all': True}) #fonction d'optimisation de notre modelisation
        #allresult.append([modele, result.x[0]])      
                         
        montre_solution('w', result.x, launchdate.toordinal(), donnees_brutes[modele], donnees_brutes["Mois"]) #affichage de la solution
        
#with open('scrap\\obsoscorealpha.csv', mode = 'w') as resfile: 
 #       writer = csv.writer(resfile)
  #      writer.writerows(allresult)



        
        