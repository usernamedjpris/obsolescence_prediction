# obsolescence_prediction
Détermination des risques d'obsolescence dans les smartphones

**Constat :** évolution très rapide des smartphones dans le temps 
**Segment d'étude :** segment de marché du haut de gamme
**Objectif de l'étude :** `détecter` et `prédire` la fin de vie d'un produit.

# Risques d'obsolescence dans les smartpohones
```

**Constat :** évolution des smartphones dans le temps très rapide 
**Segment d'étude :** segment de marché du iphone (haut de gamme) 
**Objectif de l'étude :** on essaie de `détecter` et `prédire` la fin de vie d'un smartphone haut de gamme

```

## Définition de l'obsolescence

On peut distinguer deux formes d'obsolescence : 
- **l'obsolescence technique** qui est liée aux limites technologiques du produit : fin de vie des composants, produit plus assez performant etc..
- **l'obsolescence psychologique**, liée à la perception du produit par le consommateur : produit démodé, nouveau produit avec un meilleur design etc

## Étude de 2016 de Jennings, Wu et Terpenny

### Résumé de l'étude

Une étude similaire à celle que nous cherchons à effectuer a déjà été réalisée : https://ieeexplore-ieee-org.gorgone.univ-toulouse.fr/document/7543522

L'étude se focalise davantage sur l'obsolescence technique que sur l'obsolescence psychologique. Les chercheurs ont rassemblés les caractéristiques techniques d'environ 7000 téléphones grâce à du web scrapping. Ces données sont accessibles à l'adresse http://connor.ie/research. A partir de ces données, ils ont essayé de créer un modèle permettant de prédire le risque d'obsolescence d'un smartphone.
ils ont utilisé diverses méthodes comme des forêts aléatoires, des réseaux de neurone et des machines supports vecteurs. La meilleure précision semble venir des forêts aléatoires.

### Critique de l'étude

Cette étude date de 2016. Depuis, de nombreux smartphones ont vu le jour et mériteraient d'être ajoutés au modèle. De plus le modèle développé n'inclut pas vraiment la perception du consommateur sur le produit : pour créer la courbe du cycle de vie du smartphone, les chercheurs ont utilisé essentiellement les ventes des smartphones. Il serait intéressant de creuser davantage l'impact du marketing sur l'obsolescence. Enfin les caractéristiques techniques étudiés pourraient être plus complètes : l'une d'elle était la possibilité d'envoyer des SMS, ce que n'importe quelle smartphone peut faire aujourd'hui. Il pourrait être pertinent, d'utiliser des informations provenant de benchmark pour avoir des informations pointues sur les caractéristiques techniques des smartphones.  


```

--> sur quantité de vente (mais problèmes de confidentialité pour le volume de vente d'un smartphone en particulier)
Période de la date de sortie d'un produit et la date après laquelle le fournisseur cesse la vente. 

autre ex. : [maintenabilité] au bout de 7 ans : plus de mise à jour du driver ou de l'OS

```

Déterminer le volume de vente par trimestre de chaque modèle de smartphone à partir de :
- la vente totale ("de tous les modèles de smartphones") trimestrielle communiqué par l'entreprise 
- le diagramme de gantt des modèles sortis
- la courbe type de vente de chaque modèle en fonction du temps (gaussienne ?)

-> exemple : cas des iphones 
-> critique : le nombre de modèles d'iphone : la technique perdra beaucoup de justesse s'il y a beaucoup de modèle dans la gamme (eg. samsung)

### Des raisons multiples
```
- concurrents
- technologie
- effet de mode (taille de l'écran)


si Apple était seule : vente en gaussienne (7 ans (largeur à mi-hauteur?) -> 2,5σ plutôt)
mais l'arrivée des concurrents ou nouvelle techno ou effet de mode peut raccourcir cette largeur à mi-hauteur
il peut y avoir aussi deux bosses parfois...
Peut-on corréler la fin d'un produit avec le début d'un autre ?
```
### 3 sources d'exploration

#### Les caractéristiques techniques 
```

- caméra 8mpx
-Téléphone démontable
-Batterie Amovible
-poids
-taille de l'écran
-résolution de l'écran
-autonomie de la batterie 
-taille des appareils photos
-navigateur web utilisé
-port jack
-bluetooth
-email
-radio
-GPS
-mode vibreur
-clavier physique

on va avoir un ensemble de caractéristiques aussi loin en arrière que possible (dès 2003 ça serait bien) des smartphones haut de gamme 

```

--> caractéristiques générales : 

- gsmarena.com
https://www.gsmarena.com/apple-phones-48.php

- kimovil.com
https://www.kimovil.com/fr/comparatif-smartphone/f_min_d+eurPrice.640 pour avoir une idée des marques dans le segment haut de gamme actuellement
https://www.kimovil.com/fr/prix-telephones-apple pour avoir les caractéristiques de tous les modèles de la marque apple
https://www.kimovil.com/fr/prix-telephones-samsung ...ou samsung


--> benchmark des performances des smartphones

- geekbench.com [CPU]
https://browser.geekbench.com/v5/cpu/search?utf8=%E2%9C%93&q=iphone+ depuis l'iphone 5s 

- gfxbench.com [GPU]
https://gfxbench.com/result.jsp /!\ beaucoup de smartphones non pris en charge

- antutu.com [CPU + GPU + MEM + UX]
http://www.antutu.com/en/ranking/ios1.htm
https://www.kimovil.com/fr/prix-telephones-apple

- dxomark.com [camera]
https://www.dxomark.com/category/smartphone-reviews/ depuis l'iphone 5s




#### Les nouvelles ~~technologies~~ dynamiques 
```

- Brevets déposés avec google patent : https://www.google.com/?tbm=pts

brevet déposé : hypothèse que brevets tout de suite se concrétisent rapidement en produit vendu

```

--> Partenariat avec une marque lambda
exemple de Huawei, champion des cameras (frontale et principale) depuis son partenariat avec Leica

- google actualité dans les archives : (/!\ recherche sémantique)
https://news.google.com/search?q=partenariat%20smartphone&hl=fr&gl=FR&ceid=FR%3Afr aujourd'hui
https://www.google.com/search?q=partenariat+smartphone&rlz=1C1EKKP_enFR749FR749&biw=1920&bih=1067&source=lnt&tbs=cdr%3A1%2Ccd_min%3A2007%2Ccd_max%3A2008&tbm=nws en 2007



#### Les consommateurs
```

- google trends : trace des courbe de requête pour un produit 
- commentaires : la prise en compte de son avis serait un gros plus parce que semble avoir un effet non négligeable sur les tendances

```
