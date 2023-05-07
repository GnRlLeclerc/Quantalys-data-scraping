# Script de data scraping de données financières

## Reste à faire

-   améliorer le stupende support
-   améliorer la geo zone
-   aggréger le secteur d'activité
-   faire une vraie fonction exécutable, pas juste main actuel

## Objectif :

Faire une sorte de "macro" qui permettrait de récupérer des informations juste en entrant le code ISIN d'un fonds.

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
Faire une version CLI, on verra si c'est utile pour lui (ça sera bien plus simple pour moi)
