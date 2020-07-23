#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 15:30:23 2020

@author: imen
"""

import datetime
from datetime import date
import pandas as pd
import seaborn as sns
import scipy.stats as stat
from scipy.stats import norm
from scipy.stats import weibull_min
from scipy.stats import triang
from scipy.stats import alpha
from scipy.stats import tvar
from scipy.stats import tstd
from sklearn import dummy
from sklearn import neighbors
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sty import fg, bg, ef, rs
import numpy as np
import matplotlib.pyplot as plt
#%pylab inline
sns.set()
data = pd.read_csv('/home/imen/Bureau/obsolescence_prediction-4f8018a8fe74e337cbb345b9ef41e6df111f30da/data1.csv', sep=';')
data.head()

tronq_data = data.drop(columns=['date fin commercialisation (déduite)', 'différence', 'prédécesseur',
       'successeur', 'type écran', 'certificat de résistance','nombre avis'])
tronq_data = tronq_data.drop(columns=['dxomark','Ouverture capteur selfie (ƒ/)','Ouverture capteur principal (ƒ/)', 'endurance générale ','endurance pour vidéos', 'endurance pour appeler', 'endurance pour surfer']) #265,160,45
#,'résistant aux rayures', 'gorilla glass', 'certificat de résistance','extensible','fingerprint', 'proximité',
#       'accéléromètre', "lumière d'ambiance", 'Boussole', 'gyroscope','baromètre', 'NFC', 'jack', 'radio FM', 'computer sync', 'tethering',
#       'VoLTE', 'OTA', 'bluetooth', '2G (FR)', '3G (FR)', '4G (FR)', '5G (FR)','2G (US)', '3G (US)', '4G (US)', '5G (US)', '2G (JP)', '3G (JP)',
#       '4G (JP)', '5G (JP)', '2G (CN)', '3G (CN)', '4G (CN)', '5G (CN)','nombre avis', 'général (avis)', 'rayures? (avis)', 'joli? (avis)',
#       'pratique? (avis) ', 'soleil? (avis)', 'son? (avis)', 'fluide? (avis)','jeux? (avis)', 'photos diurnes (avis)', 'photos nocturnes (avis)',
#       'selfies? (avis)', 'flash? (avis)', 'appels? (avis)', 'GPS? (avis)','Wifi? (avis)'])



data_float = tronq_data.copy()
for k in data_float.keys():
    if k not in ['marque', 'modèle']:
        if k not in ['résistant aux rayures', 'gorilla glass','extensible','fingerprint', 'proximité',
       'accéléromètre', "lumière d'ambiance", 'Boussole', 'gyroscope','baromètre', 'NFC', 'jack', 'radio FM', 
       'computer sync', 'tethering', 'VoLTE', 'OTA','date début commercialisation']:
            data_float[k] = [float(val.replace(",",".")) if isinstance(val, str) else val for val in data_float[k]]
        else:
            for i in range(len(data_float[k])):
                if k == "date début commercialisation":
                    if data_float[k][i] == data_float[k][i]:
                        liste_date = data_float[k][i].split('/')
                        if len(liste_date)==3:
                            data_float[k][i] = datetime.date(int(liste_date[2]),int(liste_date[1]),int(liste_date[0]))
                        else:
                            data_float[k][i] = None
                else:                        
                    if data_float[k][i] != data_float[k][i]: 
                        data_float[k][i] = 0
                    elif data_float[k][i].find("N/A")+data_float[k][i].find("Non")+1>=0:
                        data_float[k][i] = 0
                    elif data_float[k][i].find("Oui")+data_float[k][i].find("NFC market dependent")+1>=0:
                        data_float[k][i] = 1
data_float.head()

entrees = []
obso = ['obso ventes totales','obso trends']
for k in data_float.keys():
    if k not in ['marque', 'modèle', 'obso ventes totales','date début commercialisation']:
        entrees.append(k)
for i,k in enumerate(entrees):
    #plt.subplot(len(entrees),1,i+1)   
    print(k)
    plt.figure(figsize=(12,4))
    plt.plot(data_float[k], data_float[obso[0]],'o', label=data_float['marque']+" "+data_float['modèle'])
    plt.ylabel(obso[0]+' (jours)')
    plt.xlabel(k)
    plt.legend(bbox_to_anchor=(1.5, 1))
    plt.show()
data_etiquetees = data_float.loc[data_float[obso[0]] == data_float[obso[0]]]
print("[taille départ]", data_float.shape[0])
print("étiquetage","-"+str(data_float.shape[0]-data_etiquetees.shape[0]))
data_netoyees = data_etiquetees.copy()
shape = data_etiquetees.shape[0]
for k in data_etiquetees.keys():  
    if k != obso[1]:
        data_netoyees = data_netoyees.loc[data_netoyees[k] == data_netoyees[k]]
        if k == obso[0]:
            data_netoyees = data_netoyees.loc[data_netoyees[k] > 0] 
        print(k,"-"+str(shape-data_netoyees.shape[0]))  
        shape = data_netoyees.shape[0]
print("[taille arrivée]", data_netoyees.shape[0])

y = np.array([int(val) for val in data_netoyees[obso[0]]])

#separation aleatoire entre donnees d'entrainement et donnees de test 
#from sklearn import model_selection
#X_train, X_test, y_train, y_test = model_selection.train_test_split(data_netoyees.drop(['marque', 'modèle','date début commercialisation', 'obso ventes totales'],axis=1), y, test_size=0.3 )
#y = np.array([int(val) for val in data_netoyees['obso ventes totales']])

#separation aleatoire entre donnees d'entrainement et donnees de test
annee_avantapres = datetime.date(2016,12,31)
train = data_netoyees.loc[data_netoyees['date début commercialisation']<=annee_avantapres]
test = data_netoyees.loc[data_netoyees['date début commercialisation']>annee_avantapres]

#train['date début commercialisation'] = [datetime.date(int(d.split('-')[0]),int(d.split('-')[1]),int(d.split('-')[2])) for d in train['date début commercialisation']]
#test['date début commercialisation'] = [datetime.date(int(d.split('-')[0]),int(d.split('-')[1]),int(d.split('-')[2])) for d in train['date début commercialisation']]

print("pourcentage de données d'entraînement sur données totales",round((train.shape[0]/data_netoyees.shape[0])*100,1),"%") 
X_train = train.drop([obso[0],obso[1],'modèle', 'marque','date début commercialisation'], axis=1)
X_test = test.drop([obso[0],obso[1],'modèle', 'marque','date début commercialisation'], axis=1)
y_train = np.array([int(val) for val in train[obso[0]]])
y_test = np.array([int(val) for val in test[obso[0]]])
std_scale = StandardScaler().fit(X_train)
X_train_std = std_scale.transform(X_train)
X_test_std = std_scale.transform(X_test)
def distrib(x,debut,scale,var):
    """modèle de distribution"""
    #return alpha.pdf(x, 0.8, debut-scale/10, scale)#*var*scale   
    #return stat.norm.pdf(x,debut,scale)#*var*scale
    #return alpha.pdf(x, 0.8, debut, scale)*scale*var 
    return weibull_min.pdf(x, 1.1, debut, scale)*scale*var



def show_distrib(data, y_,option):
    """afficher proprement le vecteur y en fonction du temps avec le modèle de distribution distrib"""
    t = np.arange(datetime.date(2010,1,1).toordinal(),datetime.date(2021,1,1).toordinal(),1)
    fig, ax = plt.subplots(figsize=(12,3))
    for index,(i,ligne) in enumerate(data.iterrows()):
        y = distrib(t,ligne["date début commercialisation"].toordinal(),y_[index],1)
        plt.plot(t,y,option)
    ax.set_xlim([datetime.date(2010,1,1),datetime.date(2021,1,1)])
    plt.show()

def randomDumb(X_train=[], X_test=[], y_train=[], y_test=[]):
    if len(y_test)==0:
        return "Random (naïf)"#string name
    else:    
        y_pred_random = np.random.randint(np.min(y_train), np.max(y_train), y_test.shape)
        return np.sqrt(metrics.mean_squared_error(y_test, y_pred_random)),y_pred_random



def moyDumb(X_train=[], X_test=[], y_train=[], y_test=[]):
    if len(X_train)==0:
        return "Moyenne (naïf)"#string name
    else:  
        dum = dummy.DummyRegressor(strategy='mean')
        dum.fit(X_train, y_train)
        y_pred_dum = dum.predict(X_test)
        return np.sqrt(metrics.mean_squared_error(y_test, y_pred_dum)),y_pred_dum



def medDumb(X_train=[], X_test=[], y_train=[], y_test=[]):
    if len(X_train)==0:
        return "Médiane (naïf)"#string name
    else:  
        dum = dummy.DummyRegressor(strategy='median')
        dum.fit(X_train, y_train)
        y_pred_dum = dum.predict(X_test)
        return np.sqrt(metrics.mean_squared_error(y_test, y_pred_dum)),y_pred_dum



def foret(X_train=[], X_test=[], y_train=[], y_test=[]):
    if len(X_train)==0:
        return "forêt aléatoire"#string name
    else:
        from sklearn.ensemble import RandomForestRegressor
        foret = RandomForestRegressor()
        modele = foret.fit(X_train_std, y_train)
        y_pred_foret = modele.predict(X_test_std)
        score_foret = np.sqrt(metrics.mean_squared_error(y_test, y_pred_foret))
        return score_foret, y_pred_foret



def sgdRegressor(X_train=[], X_test=[], y_train=[], y_test=[]):
    if len(X_train)==0:
        return "SGD"#string name
    else:
        from sklearn.linear_model import SGDRegressor 
        sgd = SGDRegressor()
        modele = sgd.fit(X_train, y_train)
        y_pred_sgd = modele.predict(X_test)
        score_sgd = np.sqrt(metrics.mean_squared_error(y_test, y_pred_sgd))
        return score_sgd, y_pred_sgd


def gradientRegressor(X_train=[], X_test=[], y_train=[], y_test=[]):
    if len(X_train)==0:
        return "Gradient Boosting"#string name
    else:    
        from sklearn.ensemble import GradientBoostingRegressor
        grad = GradientBoostingRegressor(random_state=1, n_estimators=10)
        modele = grad.fit(X_train, y_train)
        y_pred_grad = modele.predict(X_test)
        return np.sqrt(metrics.mean_squared_error(y_test, y_pred_grad)),y_pred_grad



def mlpRegressor(X_train=[], X_test=[], y_train=[], y_test=[]):
    if len(X_train)==0:
        return "MLP"#string name
    else:    
        from sklearn.neural_network import MLPRegressor
        mlp = MLPRegressor(max_iter=10000, solver='lbfgs')
        modele = mlp.fit(X_train, y_train)
        y_pred_mlp = modele.predict(X_test)
        return np.sqrt(metrics.mean_squared_error(y_test, y_pred_mlp)),y_pred_mlp


def knnRegressor(X_train=[], X_test=[], y_train=[], y_test=[]):
    if len(X_train)==0:
        return "KNN-10"#string name
    else:    
        from sklearn import neighbors
        knn = neighbors.KNeighborsRegressor(n_neighbors=10)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        return np.sqrt(metrics.mean_squared_error(y_test, y_pred)), y_pred

def pretty_print(key, value, fg, bgcolor, bgvalue): #37: white, 33: yellow, 34: blue
    print("\033[1;"+fg+";"+bgcolor+"m "+key+" "*(19-len(key)),bg(bgvalue),str(round(value,1))," "*(8-len(str(round(value,1)))), bg.rs)



def benchmark(liste_fonction, liste_affichage, X_train, X_test, y_train, y_test, test): 
    lut = [202, 203, 204, 205, 206, 207, 171, 135, 99, 63, 27, 33, 39, 45, 51, 49]#50, 48, 47, 46]
    colorbar = "\n"
    for l in lut:
        colorbar += bg(l)+"  "+bg.rs
    lut.reverse()
    defaut_debiles = [randomDumb, moyDumb, medDumb]
    defaut_intelligentes = [foret,sgdRegressor,gradientRegressor,mlpRegressor]
    valeur_bg = {} 
    valeur_brute = {}
    y_resultat = {}
    for f in defaut_debiles+defaut_intelligentes+liste_fonction:
        valeur_brute[f()], y_resultat[f()] = f(X_train, X_test, y_train, y_test)
  
    minimum = np.min([x for x in valeur_brute.values()])
    maximum = np.max([x for x in valeur_brute.values()])
    for f in defaut_debiles+defaut_intelligentes+liste_fonction: 
         valeur_bg[f()] = lut[int((valeur_brute[f()]-minimum)/(maximum-minimum)*(len(lut)-1))]
    print("\033[5;37;40m     Root Mean Squared Error    ")      #erreur quadratique moyenne pris à la racine carrée pour avoir des jours  
    print()
    
    print("\033[5;30;44m Méthodes naïves ")    
    for f in defaut_debiles:
        pretty_print(f(), valeur_brute[f()], "30", "44", valeur_bg[f()])
    
    print()
    
    print("\033[5;30;44m Autres méthodes ")    
    for f in defaut_intelligentes:
        pretty_print(f(), valeur_brute[f()], "30", "44", valeur_bg[f()])
   
    for f in liste_fonction:        
        pretty_print(f(), valeur_brute[f()], "30", "46", valeur_bg[f()])
    print()
    
    print("\033[5;37;40m Statistiques Modes ")
    pretty_print("minimum", np.min(y_test), "37", "40", 235)
    pretty_print("1er quartile", np.quantile(y_test, 0.25), "37", "40", 235)
    pretty_print("moyenne", np.mean(y_test),"37", "40", 235)
    pretty_print("médiane", np.median(y_test), "37", "40", 235)
    pretty_print("3ème quartile", np.quantile(y_test, 0.75), "37", "40", 235)
    pretty_print("maximum", np.max(y_test), "37", "40", 235)  
    
    print(colorbar)
    #show_distrib(train,y_train,'-')
    print()
    print("données tests")
    show_distrib(test,y_test,'-')
    for f in liste_affichage+liste_fonction:   
        print(f())
        show_distrib(test,y_resultat[f()],'--')
        
benchmark([knnRegressor],[moyDumb],X_train_std,X_test_std,y_train,y_test,test)

