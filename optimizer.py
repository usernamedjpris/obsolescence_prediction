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




## forme de la courbe de distribution hypothèse 
def distrib(t, x, debut, scale, var, offset):
        
        """
        renvoie la distribution selectionnee avec les parametres specifies
        
        t : type de distribution, 'a' pour alpha, 't' pour triangulaire, 'w' pour weibull
        x : array des abscisses
        debut : abscisse où debute la distribution
        scale : parametre de largeur
        var : parametre de hauteur
        offset : permet de decaler legerement le debut de la distribution pour alpha et triangulaire. Pour Weibull ce parametre au parametre de forme
        
        """

        if t == 'a':
                return alpha.pdf(x, 0.8, debut-scale/10+offset, scale/1.7)*var*scale if scale and var > 0 else [0]*len(x)
        elif t == 'w':
                return weibull_min.pdf(x,offset, debut, scale)*var
        elif t == 't':
                return triang.pdf(x, 0.1, debut+ offset, scale)*scale*var





def listOfSmartphone(name):
        
        """
        
        renvoie la liste des smartphones contenus dans le .txt name
        
        name : str, nom du fichier txt contenant les noms de tous les modeles
        
        """

        with open(name) as file: #indiquer le chemin du fichier txt contenant les noms de tous les modeles
                modeles = file.readlines()
                return modeles


def collectSmartphoneData(name):  
        
        """
        
        recupere toutes les donnees sur tous les modeles de smartphone
        
        name : str, le nom du fichier contenant toutes les data des smartphones 
        
        
        
        """
        csvfile = pd.read_csv(name, sep=';') #indiquer chemin du fichier recensant toutes les caracteristiques des modeles
        return csvfile



def formatNameModel(modele):
        
        """
        
        formate la chaine de caractere correspondant au nom du modele pour la faire correspondre au nom du fichier csv telecharge via google trends
        
        modele : str, le nom du modele dans le fichier txt ou dans le csv contenant toutes les datas relatives au smartphones
        
        
        """
        newmodele = modele.replace('+', ' plus')
        newmodele = newmodele.replace('(', ' ')
        newmodele = newmodele.replace(')', '')
        newmodele = newmodele.replace('\n', '')
        if newmodele.find(',') != -1:
                newmodele = newmodele.split(',')[0]
        return newmodele
        

def gatherLaunchdate(data):
        
        """
        
        Rassemble les dates de lancement des smartphones lorsqu'elles sont renseignees, depuis le talbleau de data
        
        data: tableau des donnees de tous les smartphones
        
        
        """
        datedebut = {} #dictionnaire dont les cles sont les noms des modeles et ou sont renseignees les dates de lancement
        
        for marque, modele, d  in zip(data["marque"], data["modèle"], data["date début commercialisation"]):                 
                                  
                ##formatage du fichier csv et recuperation de la date de lancement du modele
                modele = formatNameModel(modele)
                try:
                        datedebut[marque+" "+modele] = date(int(d.split("/")[2]),int(d.split("/")[1]),int(d.split("/")[0]))
                except (IndexError, AttributeError):
                        datedebut[marque+" "+modele] = None
        return datedebut

            
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
        cumul = [0 for i in range(len(abscisses))]
        largeur, hauteur, offset = X[0], X[1], X[2]
        y = distrib(t, abscisses, date, largeur, hauteur, offset)
        cumul = [cumul[i]+x for i,x in enumerate(y)]           
        result = float(abs(sum([abs(x-y) for x,y in zip(cumul, courbe_brute)])))
        return result

## solution
def montre_solution(t, X, date, courbe_brute, abscisses, modele):
        
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


def recoverRawTrends(modele, directory='modtrends'):
        
        donnees_brutes = pd.read_csv(directory+'\\'+modele+'.csv', sep=',')
        donnees_brutes["Mois"] = [date(int(x.split("-")[0]), int(x.split("-")[1]),1).toordinal() for x in donnees_brutes["Mois"]] 
        donnees_brutes[modele] = [x for x in donnees_brutes[modele]]
        return donnees_brutes

def optimize1Model(modele, datedebut):
        
        """
        
        Modelise la courbe google trends par une fonction mathematique en optimisant ses parametres. Parmi les trois distributions, on retient la meilleure
        
        modele: str, le modele a optimiser
        
        datedebut: dict, dictionnaire associant a chaque modele sa date de lancement
        
        return: une liste avec l'ecart cummule entre la modelisation et la courbe brute pour les trois lois, la meilleure distribution et l'estimation de l'obsolescence associee.
        
        """
        modele = formatNameModel(modele) 
        print('optimisation du modele : ',modele)
        donnees_brutes = recoverRawTrends(modele)


        ##recuperation ou calcul de la date de lancement
        launchdate = datedebut[modele]
        if not launchdate:
                launchdate = calculatelaunchdate(donnees_brutes["Mois"], donnees_brutes[modele])

        ##fonctions d'optimisations suivant la distribution choisie
        def objW(X):
                return objectif('w', X, launchdate.toordinal(), donnees_brutes[modele], donnees_brutes["Mois"])
        def objA(X):
                return objectif('a', X, launchdate.toordinal(), donnees_brutes[modele], donnees_brutes["Mois"])
        def objT(X):
                return objectif('t', X, launchdate.toordinal(), donnees_brutes[modele], donnees_brutes["Mois"])        

        ## minimizer
        x0W = [183, 25000, 1.15] #modelisation initiale pour Weibull
        bndsW = ((150, 1500), (24000,100000), (1.05, 1.9)) #bornes des parametres de la loi de Weibull
        x0A = [250,50, 0] #modelisation initiale pour Alpha et triangulaire
        bndsA = ((100, 5000),(1, 100), (-400, 50)) # bornes des parametres de la loi Alpha et triangulaires (entre 60 et 10000 jours, entre 1 et 100 unites ordonnée et entre -400 et 50 pour l'offset)
        resultW = minimize(objW, x0W, method='Powell', bounds=bndsW, options={'maxiter': 100000, 'maxfev': 1000,'return_all': True}) #fonction d'optimisation de notre modelisation
        ecartW = objectif('w', resultW.x, launchdate.toordinal(), donnees_brutes[modele], donnees_brutes["Mois"])
        min = 'w'
        resultA = minimize(objA, x0A, method='Powell', bounds=bndsA, options={'maxiter': 100000, 'maxfev': 1000,'return_all': True})
        ecartA = objectif('a', resultA.x, launchdate.toordinal(), donnees_brutes[modele], donnees_brutes["Mois"])
        if ecartA < ecartW:
                min = 'a'
        resultT = minimize(objT, x0A, method='Powell', bounds=bndsA, options={'maxiter': 100000, 'maxfev': 1000,'return_all': True})
        ecartT = objectif('a', resultT.x, launchdate.toordinal(), donnees_brutes[modele], donnees_brutes["Mois"])
        if (ecartT < ecartA and min =='a') or (ecartT < ecartW and min == 'w'):
                min = 't'
        print('meilleure distribution : '+min)
        print('Parametres optimisés : ', end='')
        if min =='a':  
                print(resultA.x)
                best = resultA
                minscore = round(alpha.ppf(0.8, 0.8, loc = launchdate.toordinal()-resultA.x[0]/10+resultA.x[2], scale = resultA.x[0]/1.7) - launchdate.toordinal())                                                                                                                                   
        elif min == 't':
                print(resultT.x)
                best = resultT
                minscore = round(triang.stats(0.1, launchdate.toordinal()+ resultT.x[2], resultT.x[0], 'm') + 2.5*math.sqrt(triang.stats(0.1, launchdate.toordinal()+ resultT.x[2], resultT.x[0], 'v')) - launchdate.toordinal())
        else:
                print(resultW.x)
                best = resultW
                minscore = round(weibull_min.stats(resultW.x[2], launchdate.toordinal(), resultW.x[0], 'm') + 2.5*math.sqrt(weibull_min.stats(resultW.x[2], launchdate.toordinal(), resultW.x[0], 'v')) - launchdate.toordinal())
        print()
       # montre_solution(min, best.x, launchdate.toordinal(), donnees_brutes[modele], donnees_brutes["Mois"], modele) #affichage de la solution
      
        return([modele, resultA.x, resultT.x, resultW.x], [modele, ecartT, ecartA, ecartW, min, minscore])         

def exportResults(result, name):
        
        """
        
        Exporte les resultats de l'algorithme d'optimisation dans  un fichier csv
        
        result: la liste contenant le resultat de l'algorithme
        
        name: le nom du fichier de sortie
        
        
        """
        with open(name, mode = 'w') as resultfile:
                writer = csv.writer(resultfile)
                writer.writerows(result)
                


def optimizeAllmodels(lstPhoneFile='allsmartphones.txt', dataPhoneFile='data.csv', comparativeFile='comparedistrib.csv', resultsFile='results.csv'):
        
        """
        
        Applique l'algorithme d'optimisation sur tous les modeles de telephones. Enregistre les resultats dans des fichiers csv.
        Les resultats se presentent sous deux formes : 
        -un fichier "comparativeFile" comportant un comparatif des ecarts observes entre les 3 types de distributions et avec l'estimation de l'obsolescence pour la meilleure distribution.
        -un fichier "resultsFile" composé des paramètres des distributions optimisées pour les trois types de distributions
        
        lstPhoneFile: nom du fichier txt contenant les noms des modeles a etudier
        
        dataPhoneFile: nom du fichier csv contenant les data sur tous les modeles de telephones
        
        comparativeFile: nom du fichier csv qui contiendra le comparatif des distributions
        
        resultsFile: nom du fichiers csv qui contiendra les parametres des trois distributions
        
        
        """
        
        allsmartphones = listOfSmartphone(lstPhoneFile)
        
        datasmartphones = collectSmartphoneData(dataPhoneFile)
        
        datedebut = gatherLaunchdate(datasmartphones)
        
        allresults = [['modele', 'largeurA', 'hauteurA', 'paramA', 'largeurT', 'hauteurT', 'paramT', 'largeurW', 'hauteurW', 'paramW']]
        
        comparedistrib = [['modele', 'triang', 'alpha', 'weibull', 'best', 'minscore' ]]        
        
        for smartphone in allsmartphones:
                
                results,comparatif = optimize1Model(smartphone, datedebut)
                
                comparedistrib.append(comparatif)
                allresults.append([results[0], results[1][0], results[1][1], results[1][2], results[2][0], results[2][1], results[2][2], results[3][0], results[3][1], results[3][2]])                                                        
                  
        exportResults(allresults, resultsFile)
        exportResults(comparedistrib, comparativeFile)
        
optimizeAllmodels()
        


        
        
