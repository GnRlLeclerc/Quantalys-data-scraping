# Script de data scraping de données financières

## Objectif :

Faire une sorte de "macro" qui permettrait de récupérer des informations juste en entrant

Concrètement, le cahier des charges : TODO, et regarder la faisabilité, lui communiquer pour savoir si c'est ce qu'il veut
Voir le fichier excel attaché

À partir du code ISIN d'un fonds, récupérer des données sur Quantalys :

-   Nom du fonds
-   Rating Quantalys (nombre de petites étoiles)
-   Note SRRI (note sur 5)
-   Sharpe ratio jsp??
-   Stupende support (actions, obligations, multi asset...)
-   Zone géographique
-   Secteurs et style de gestion (c'est plus subjectif, plus difficile...)

Exemple d'une ligne
LU1670606760 ABN AMRO Parnassus US ESG Eq R \*\*\* 5 Actions US Tech, Cycliques, Value, Large Cap

## Autres pistes

Idée : utiliser pyinstaller pour le déploiement ?
=> en vrai, ça serait limite plus pratique de faire un site internet qui fasse ça, pour l'interface ? Mais il faut qu'ils aient node, sinon ?
