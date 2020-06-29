#encoding: utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import alpha
from scipy.stats import lognorm
from scipy.stats import weibull_min
from scipy.stats import exponweib
from scipy.stats import triang
from scipy.optimize import minimize
from datetime import date

## donnees brutes
donnees_brutes = pd.read_csv('multiTimeline.csv', sep=',')
donnees_brutes["Mois"] = [date(int(x.split("-")[0]), int(x.split("-")[1]),1).toordinal() for x in donnees_brutes["Mois"]] 
donnees_brutes["iphone 4s"] = [int(x.replace("< 1","0")) for x in donnees_brutes["iphone 4s"]] 
print(donnees_brutes.head())


## forme de la courbe de distributionhypothèse 
def distrib(x,debut,scale,var,param):
        #return stat.norm.pdf(x,debut+scale/2,scale/6)*var#*scale
        #return lognorm.pdf(x,2, debut, scale/6)*var#*scale
        #return alpha.pdf(x, 0.8, debut-scale/10, scale/1.7)*var*scale if scale and var > 0 else [0]*len(x)
        #return weibull_min.pdf(x,debut, scale) 
        #return exponweib.pdf(x,debut, scale)
        return triang.pdf(x, param, debut, scale)*scale*var

x = np.arange(-3, 1000, 0.5)
y = distrib(x,100,600,50,0.1) #ref
y2 = distrib(x,100,730,50,0.1) #plus large
y3 = distrib(x,100,600,100,0.1) #plus haut
fig, ax = plt.subplots(figsize=(9,6))
ax.plot(x,y)
ax.plot(x,y2)
ax.plot(x,y3)
ax.set_xlim([-3,1000])
ax.set_title("courbe de distribution de ventes d'un modèle")

plt.show()


## fonction objectif
def objectif(X, date, courbe_brute, abscisses):
        #print(X)
        cumul = [0 for i in range(len(abscisses))]
        largeur, hauteur,c = X[0], X[1], X[2]
        y = distrib(abscisses, date, largeur, hauteur, c)
        cumul = [cumul[i]+x for i,x in enumerate(y)]           
        result = float(abs(sum([abs(x-y) for x,y in zip(cumul, courbe_brute)])))
        #print(result)
        return result

def obj(X):
        global donnees_brutes
        return objectif(X, date(2011,10,1).toordinal(), donnees_brutes["iphone 4s"], donnees_brutes["Mois"])


## minimizer
x0 = [60,25,0.1]
bnds = ((60, 10000),(1, 100),(0,1)) # limites (entre 60 et 10000 jours, entre 1 et 100 unites ordonnée et entre 0 et 1 pour le parametre c)
result = minimize(obj, x0, method='Powell', bounds=bnds)


## solution
def montre_solution(X, date, courbe_brute, abscisses):
        cumul = [0 for i in range(len(abscisses))]
        fig, ax = plt.subplots(figsize=(9,6))
        largeur, hauteur, c = X[0], X[1], X[2]
        y=distrib(abscisses, date, largeur, hauteur, c)    
        print("largeur :",largeur)
        print("hauteur :",hauteur)
        print("c :",c)   
        ax.plot(abscisses, y, 'b', label="courbe modèle largeur : "+str(round(largeur,1))+" hauteur : "+str(round(hauteur,1))+" c : "+str(c))      
        ax.plot(abscisses, courbe_brute, 'k', label="courbe brute")
        ax.legend()
        plt.show()
        
montre_solution(result.x, date(2011,10,1).toordinal(), donnees_brutes["iphone 4s"], donnees_brutes["Mois"])