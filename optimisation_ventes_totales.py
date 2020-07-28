#encoding: utf-8
## Paramètre global du projet
racine_projet = 'E:/eDocuments/obso/'

## Librairies
# dates/utils
import datetime
from datetime import date
import pandas as pd
import math
import copy
import numpy as np
# scipy
import scipy.stats as stat
from scipy.stats import norm
from scipy.stats import alpha
from scipy.stats import exponweib
from scipy.optimize import minimize
from scipy.stats import weibull_min
from scipy.stats import triang
# beautiful print/plot
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
pd.options.mode.chained_assignment = None # enlever des prints de warnings
# les widgets jupyter qui sont à enlever à terme...
import ipywidgets as widgets
from ipywidgets import Layout
from IPython.display import clear_output
from IPython.display import display





## Importation des fichiers 
# - dates de début commercialisation 
# - nombres de ventes par trimestre

def importer_ventes():
    global racine_projet
    
    # importation des fichiers
    globals()['dates'] = pd.read_csv(racine_projet+'dates.csv', sep=';')
    globals()['ventes'] = pd.read_csv(racine_projet+'vente_tout_constructeurs.csv', sep=';')
    
    # formatage des dates en datetime.date   
    for i,debut in enumerate(dates["date"]):
        if not(isinstance(debut, datetime.date)): 
            if debut != debut: 
                continue # on continue seulement si pas NaN
            if debut.find("/")<0:
                continue # on continue seulement si c'est pas dans le format
            dates["date"][i] = datetime.date(int(debut.split("/")[2]),int(debut.split("/")[1]),int(debut.split("/")[0]))
            
    # axe des x : temps discrétisé en trimestre 
    globals()['trimestre']  = [datetime.date(int(d.split("/")[2]),int(d.split("/")[1]),int(d.split("/")[0])).toordinal() for d in ventes["Trimestre"]]
    globals()['limites'] = [date.fromordinal(trimestre[0]),date.fromordinal(trimestre[-1])]







### Code modèles de distribution
ladistribution = 'alpha'
nb_sample = 1
leseuil = 80 #%
ax = plt.gca()

# fonction de distribution
def distrib(x,debut,largeur,hauteur,offset):
    """modèles de distribution (pour affichage de l'allure de la courbe [plot])"""
    global ladistribution
    if ladistribution == "alpha":
        return alpha.pdf(x, 0.8, debut-largeur/10, largeur)*hauteur*largeur  
    elif ladistribution == "gauss":
        return stat.norm.pdf(x,debut,largeur)*hauteur*largeur
    elif ladistribution == "triangle":
        return triang.pdf(x,0,debut,largeur)*hauteur*largeur 
    elif ladistribution == "weibull":
        return weibull_min.pdf(x, 1.1, debut+offset, largeur)*hauteur*largeur
    
def distrib_quantile(q,largeur):
    """modèles de distribution pour partager en quantile (pour affichage du seuil [axvline])"""
    global ladistribution
    if ladistribution == "alpha":
        return alpha.ppf(q, 0.8, 0, largeur)  
    elif ladistribution == "gauss":
        return stat.norm.ppf(q, 0, largeur)
    elif ladistribution == "triangle":
        return triang.ppf(q, 0, 0, largeur) 
    elif ladistribution == "weibull":
        return weibull_min.ppf(q, 1.1, 0, largeur)
    
# -------------------------------------------------------------------------------------------------------------------------- 
# fonctions d'affichage pour Widget Jupyter laissées pour l'inspiration.

def show_samples():
    """fonction principale d'affichage des allures des courbes de distributions"""
    globals()["out_samples"] = widgets.Output(layout=Layout(height='400px', width = '1000px')) # zone d'affichage
    globals()["int_range"] = widgets.IntSlider(value=1, description="Aperçus", max=25) # glissière d'entier
    globals()["seuil_range"] = widgets.IntSlider(value=80, description="seuil (%)", max=99) # glissière d'entier
    globals()["d"] = widgets.Dropdown(options=['alpha', 'weibull', 'triangle', 'gauss']) # menu déroulant
    global ax
    plt.ioff()
    fig, ax = plt.subplots(figsize=(11,6))
    display(d,seuil_range,int_range,out_samples)
    # relier les widgets aux fonction de mise à jour
    seuil_range.observe(update_seuil, names='value')
    int_range.observe(update_samples, names='value')
    d.observe(change_distrib, names='value')
    # initialiser le tout
    change_distrib({'new':'alpha'})
    update_seuil({'new':80})   
    update_samples({'new':1})  
    
def update_samples(b):
    """affiche dans un ax global un graphique de nb_sample courbes avec les seuils verticalement"""
    flatui = ["#3498db", "#9b59b6", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
    global nb_sample, leseuil, ax
    nb_sample = b['new']
    ax.clear()
    x = np.arange(-3, 30, 0.05)
    for i in range(b['new']):
        largeur = i+0.2*10
        y = distrib(x,0,largeur,1,0)
        ax.plot(x,y, color=flatui[i%len(flatui)]) # flatui = échelle de couleur définie pour avoir plot et axvline de la même couleur 
        ax.axvline(x=distrib_quantile(leseuil/100,largeur),color=flatui[i%len(flatui)])        
    ax.set_xlim([-3,30])
    ax.set_title("allure de la courbe de distribution de ventes d'un modèle de smartphone pour différentes largeurs")
    with out_samples:
        clear_output(wait=True)
        display(ax.figure)

def update_seuil(b):
    global leseuil,nb_sample
    leseuil = b['new']
    update_samples({'new':nb_sample})
    
def change_distrib(b):
    global ladistribution,nb_sample
    ladistribution = b['new']
    update_samples({'new':nb_sample}) 

#show_samples()

# ----------------------------------------------------------------------------------------------------------------------------








### Code optimisation
lamarque = ['Apple']
methode = 'Powell'
renverse = False
lanorme = "norme 1"
minX, maxX = 60, 270
minY, maxY = 50000,60000000
offsetM, offsetP= -60, 180

def mini_obj(X, args, abscisses):
    """calcule la somme cumulée de toutes les courbes de distributions décrites par le vecteur X (largeur, hauteur)"""
    cumul = [0 for i in range(len(abscisses))]
    for i in range(int(len(X)/3)):
        largeur, hauteur, offset = X[i*3], X[i*3+1], X[i*3+2]
        date, ponderation = args[i*2], args[i*2+1]
        y=distrib(abscisses, date, largeur, hauteur, offset)
        cumul = [cumul[i]+x for i,x in enumerate(y)]    #*ponderation for i,x in enumerate(y)]             
    return cumul

def montre_solution(X, args, ventes_totales, abscisses, agregat_modeles):
    """montre la solution trouvée : vecteur X (largeur, hauteur) et courbe des cumuls ainsi que courbe des ventes totales"""
    global limites, leseuil
    cumul = [0 for i in range(len(abscisses))]
    fig, ax = plt.subplots(figsize=(12,6))
    for i in range(int(len(X)/3)):
        largeur, hauteur, offset = X[i*3], X[i*3+1], X[i*3+2]
        date, ponderation = args[i*2], args[i*2+1]
        y=distrib(abscisses, date, largeur, hauteur, offset)
        cumul = [cumul[i]+x for i,x in enumerate(y)]    #*ponderation for i,x in enumerate(y)]           
        ax.plot(abscisses, y, label=agregat_modeles[i]+"\nlargeur : "+str(round(largeur,1))+" hauteur : "+str(round(hauteur,1)))    #distrib_quantile(leseuil/100,largeur),1))+" hauteur : "+str(round(hauteur,1)))    
    ax.plot(abscisses, cumul, 'k', label="ventes cumulees")
    ax.plot(abscisses, ventes_totales, 'b', label="ventes totales")
    ax.legend(bbox_to_anchor=(1.5, 1))
    ax.set_xlim(limites)
    plt.show()

def objectif(X, args, ventes_totales, abscisses):
    """retourne la distance (norme 1 ou 2) entre les ventes totales et la courbe du cumul de toutes les distributions modèle par modèle"""
    global lanorme
    ventes_cumulees = mini_obj(X, args, abscisses)
    if lanorme == "norme 1":
        result = float(abs(sum([abs(x-y) for x,y in zip(ventes_cumulees, ventes_totales)])))
    elif lanorme == "norme 2":
        result = float(np.sqrt(sum([(x-y)**2 for x,y in zip(ventes_cumulees, ventes_totales)])))
    return result

def obj(X):
    """diminutif de objectif pour rentrer avec le bon nombre de paramètre dans l'optimiseur"""
    global dates, args, trimestre, ventes_totales 
    return objectif(X, args, [v for v in ventes_totales], [t for t in trimestre])


def optimiseur():
    """optimisation avec la fonction minimize de scipy"""
    globals()['args'] = []
    global renverse, methode, lamarque, args, ladistribution, ventes_totales, lanorme, offsetP, offsetM, minX, maxX, minY, maxY
    plt.close('all')
    ligne_resultat = ""
    for marque in lamarque:        
        agregat_modeles = dates.loc[lambda df: dates['marque'] == marque, :].groupby('date').apply(lambda x: ', '.join(x.modèle))
        ventes_totales = [0 if v != v else float(v.replace(",","."))*1000000  for v in ventes[marque]]
        df_args =  dates.loc[lambda df: dates['marque'] == marque, :].groupby('date').count()["marque"]
        x1 = []
        bnds = ()
        for date in df_args.index:        
            if isinstance(date, datetime.date):
                if not renverse:                    
                    args.append(date.toordinal())
                    args.append(df_args[date])
                    x1 = x1+[60,1000000,0]
                else:
                    args.append(df_args[date])
                    args.append(date.toordinal())
                    x1 = x1+[0,1000000,60]                                        
                bnds = bnds + ((minX, maxX*1.138591143459572),(minY, maxY),(offsetM,offsetP),)#(500000/df_args[date], 60000000/df_args[date]),)
        # a quoi peut servir renverse ??? je l'ai pas expliqué la dernière fois...
        # c'est une option qui permet de renverser l'ordre des smartphones (X) dans l'optimiseur :
        # au lieu que ce soit dans l'ordre chronologique ça va être anti chronologique
        # je me suis aperçu qu'on peut obtenir de meilleurs résultat en renversant cet ordre alors je l'ai laissé :)
        # c'est souvent lorsque la courbe des ventes totales est DECROISSANTE (comme pour Sony) que j'ai pu le voir.
        # je l'explique par le fait que la méthode Powell optimise dans un certain ordre et que les première courbes
        # optimisées sont un peu sur-estimées (pour réduire l'objectif qui est de réduire la différence de la somme 
        # totale des courbes de distribution avec la courbe des ventes (qui est initialement très haute) l'optimiseur
        # va grandir au maximum les premières courbes. Pour les suivantes un peu moins puisque il faut prendre en com-
        # pte le recouvrement des courbes dans le cumul... Donc pour une courbe des ventes croissante ça marche mais 
        # moins bien pour une courbe décroissante le recouvrement des premières courbes va contraindre les suivantes 
        # d'être toutes petites
        if renverse:
            args = args[::-1]
            x1 = x1[::-1]
        
        # ———————————————————————————————————————————————————————————— fonction de minimisation
        result = minimize(obj, x1, method = methode, bounds=bnds)
        # ————————————————————————————————————————————————————————————
        
        montre_solution(result.x, args, ventes_totales, trimestre, agregat_modeles)
        
        # ligne_resultat est la ligne qui présente l'écart obtenu et avec quels paramètres on l'a obtenu
        chronooupaschrono = "chrono" if not renverse else "antichrono"
        params = "["+ladistribution+", "+methode+", "+marque+", "+chronooupaschrono+"]"
        params += " "*(37-len(params))+" X("+str(minX)+", "+str(maxX)+")"+ " Y("+str(minY)+", "+str(maxY)+")"+ " Offset("+str(offsetM)+", "+str(offsetP)+")" 
        objectif = str(int(obj(result.x)))
        ligne_resultat += params+" "*(87-len(params))+" écart "+lanorme+" "*(11-len(objectif))+bg.red+fg.white+" "+objectif+" "+fg.rs+bg.rs
        
        #print au style format csv
        #for i in range(int(len(result.x)/3)):
        #    for modele in agregat_modeles[i].split(", "):
        #        print(modele+";"+str(result.x[i*3]).replace(".",","))
        
    return ligne_resultat
    




        
# -------------------------------------------------------------------------------------------------------------------------- 
# fonctions d'affichage pour Widget Jupyter laissées pour l'inspiration.

def optimisation():
    """fonction principale d'affichage"""
    # boutons
    globals()["button1"] = widgets.Button(description="Lancer optimisation") 
    globals()["button2"] = widgets.Button(description="Renverser chrono")
    # zones d'affichage
    globals()["out_optimizer"] = widgets.Output()
    globals()["out_historique"] = widgets.Output()        
    globals()["out_renverse"] = widgets.Output()
    # menus déroulants
    globals()["d_methode"] = widgets.Dropdown(options=['Powell', 'L-BFGS-B', 'TNC', 'SLSQP']) 
    globals()["d_norme"] = widgets.Dropdown(options=['norme 1', 'norme 2']) 
    globals()["d_brand"] = widgets.Dropdown(options=["Apple", "Samsung", "Xiaomi", "Oppo", "Vivo", "Sony", "Huawei",'Toutes']) 
    # glissière d'int
    globals()["minX_range"] = widgets.IntSlider(value=60, description="min X (jours)", min=30 , max=180)
    globals()["maxX_range"] = widgets.IntSlider(value=270, description="max X (jours)", min=30 , max=1460)
    globals()["minY_range"] = widgets.IntSlider(value=50000, description="min Y (ventes)", min=10000 , max=100000)
    globals()["maxY_range"] = widgets.IntSlider(value=60000000, description="max Y (ventes)", min=100000, max=100000000)
    globals()["offsetM_range"] = widgets.IntSlider(value=-60, description="Offset- (jours)", min=-270 , max=0)
    globals()["offsetP_range"] = widgets.IntSlider(value=180, description="Offset+ (jours)", min=0, max=270)
    plt.ioff()
    ax=plt.gca()
    
    # affichage des composants
    display(d_methode,d_brand,d_norme,button2,out_renverse,minX_range,maxX_range,minY_range,maxY_range,offsetM_range,offsetP_range,button1, out_optimizer, out_historique)
    
    # relation des composants aux fonctions de mises à jour
    button1.on_click(on_button1_clicked)
    button2.on_click(on_button2_clicked)
    d_methode.observe(change_method, names='value')
    d_brand.observe(change_brand, names='value')
    d_norme.observe(change_norme, names='value')
    minX_range.observe(change_minX, names='value')
    maxX_range.observe(change_maxX, names='value')
    minY_range.observe(change_minY, names='value')
    maxY_range.observe(change_maxY, names='value')    
    offsetM_range.observe(change_offsetM, names='value')
    offsetP_range.observe(change_offsetP, names='value') 
    
def on_button1_clicked(b):
    with out_optimizer:
        clear_output(wait=True) #pour afficher l'historique des graphes commenter cette ligne
        string = optimiseur()
    with out_historique:
        print(string)
        
def on_button2_clicked(b):
    global renverse
    renverse = not renverse    
    with out_renverse:
        clear_output(wait=True)
        print("les modèles sont dans l'ordre",("ANTI-" if renverse else "")+"chronologique")

def choose_brand(marque):
    global lamarque
    if marque == "Apple":
        lamarque = ['Apple']
    elif marque == "Samsung":
        lamarque = ['Samsung']  
    elif marque == "Xiaomi":
        lamarque = ['Xiaomi'] 
    elif marque == "Oppo":
        lamarque = ['Oppo'] 
    elif marque == "Vivo":
        lamarque = ['Vivo']
    elif marque == "Sony":
        lamarque = ['Sony']
    elif marque == "Huawei":
        lamarque = ['Huawei']
    elif marque == "Toutes":
        lamarque = ["Apple", "Samsung", "Xiaomi", "Oppo", "Vivo", "Sony", "Huawei"]
        
def change_norme(b):
    global lanorme 
    lanorme = b['new']        
def change_method(b):
    global methode 
    methode = b['new']    
def change_minX(b):
    global minX 
    minX = b['new']
def change_maxX(b):
    global maxX 
    maxX = b['new']
def change_minY(b):
    global minY 
    minY = b['new']
def change_maxY(b):
    global maxY 
    maxY = b['new']
def change_offsetM(b):
    global offsetM 
    offsetM = b['new']
def change_offsetP(b):
    global offsetP 
    offsetP = b['new']    
def change_brand(b):
    global brand 
    choose_brand(b['new'])
    
#optimisation()   
# ----------------------------------------------------------------------------------------------------------------------------
