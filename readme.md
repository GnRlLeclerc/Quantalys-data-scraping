# Script de data scraping de données financières

## Reste à faire

-   améliorer le stupende support
-   aggréger le secteur d'activité

## Compilation en exécutable sur Windows :

Créer un venv python (Attention : les dépendances ont été freeze pour la version python `3.11.3`)

```bash
python -m venv venv
venv\Scripts\activate # Sur Windows
pip install -r requirements.txt
```

Pour lancer le script python :

```
python main.py
```

Pour compiler en exécutable :

```
pyinstaller --onedir --console --name Quantalys-ISIN --icon=quantalys.ico main.py
```

## Objectif :

Faire une sorte de "macro" qui permettrait de récupérer des informations juste en entrant le code ISIN d'un fonds.

À partir du code ISIN d'un fonds, récupérer des données sur Quantalys :

-   Nom du fonds
-   Rating Quantalys (nombre d'étoiles)
-   Note SRRI (note sur 5)
-   Sharpe ratio
-   Stupende support (actions, obligations, multi asset...)
-   Zone géographique
-   Secteurs et style de gestion (à agréger depuis les autres pages)

## Code :

-   [`main.py`](/main.py) : script principal, gère l'input utilisateur et le lancement des coroutines
-   [`api/`](/api/) : contient les fonctions d'interaction avec le site de Quantalys
    -   [`data.py`](/api/data.py) : contient les fonctions d'agrégation des données à partir des requêtes
    -   [`quantalys.py`](/quantalys.py) : contient l'API de Quantalys pour les requêtes les plus complexes
    -   [`requests.py`](/requests.py) : contient les fonctions de requêtes à Quantalys (coroutines asynchrones)
