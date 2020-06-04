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
- nb de caméras etc.

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
