from api.data import test_agregate_from_isin
import asyncio
import pandas as pd

from time import time


"""
RESTE A FAIRE :
* analyser le secteur et style de gestion
* voir la zone géo depuis la main page
* faire la fonction qui génère un excel pour comparer
* faire l'interface graphique


A partir de la recherche complète, les attributs qu'on recherche sont les suivants

-   Nom du fonds
-   Rating Quantalys (nombre de petites étoiles)
-   Note SRRI (note sur 5)
-   Sharpe ratio jsp??
-   Stupende support (actions, obligations, multi asset...)
-   Zone géographique
-   Secteurs et style de gestion (c'est plus subjectif, plus difficile...)

ce sonts:

* nom du fonds : sNom (remarque : il y a même l'url)
* rating quantalys : nStarRating
* note sri  (1 seul r, apparemment): J'AI PAS TROUVE ==================================== requête à faire
* sharpe ratio : nSharpe3a (1a et 5a sont aussi disponibles)

Pour le reste : aller voir dans les autres onglets

* stupende support: sGroupeCat_rng1
* zone géographique : sGroupeCat_Specific_Dynamic (retirer le truc précédent pour ne laisser que le pays)

* secteur et style de gestion ? voir d'après les colonnes existantes
=> voir où c'est écrit dans quantalys : Composition (voir les requêtes de données)

trouver le srri aussi, il est sur la page

TODO : voir les requêtes plus détaillées faites sur les pages, c'est peut-6etre mieux
BUG
BUG


=> structure du code pour l'instant : faire des fonctions qui font les requêtes ? Créer un sous dossier api ? tools ?



TODO : ATTENTION A FAIRE DE LA GESTION D'EXCEPTIONS POUR QUE RIEN NE FOUTE LA MERDE SI ÇA MARCHE PAS

avec pyinstaller, faire une petite fenêtre où on rentre l'isin, et ça crée un csv avec les données.
Si on rentrait une ligne/ colonne (voir le format du copié collé depuis excel => séparé par un retour à la ligne?),
ça renvoie le csv avec tout
"""

# test_agregate_from_isin(TEST_ISIN)
# asyncio.run(test_agregate_from_isin("LU1327551674"))

# Pour cette dernière, il y a beaucoup moins de trucs dans la page compositions.
# Il faudra fallback sur la page principale

ISINs = [
    "LU1670606760",
    "LU1890796300",
    "FR0013285004",
    "LU1720048575",
    "LU1645746287",
    "LU0982019712",
    "LU0982019803",
    "LU1997245920",
    "LU1865149980",
    "LU0709024276",
    "LU1946895866",
    "LU1327551674",
    "LU2034159157",
    "LU2025541991",
    "LU1992131562",
    "LU1961090997",
    "LU1602090620",
    "LU1136108757",
    "LU2034161138",
    "LU0976572031",
    "LU0905751987",
    "LU0256883504",
    "LU1543696782",
    "LU0414047521",
    "LU2240143094",
    "FR00140017Q1",
    "LU1720046108",
    "LU1548499711",
    "LU2278554956",
    "LU0962745641",
    "LU1766616152",
    "LU1942584456",
    "LU2092390199",
    "FR0013498516",
    "FR0013498490",
    "FR0013498482",
    "FR0013496247",
    "FR0013507894",
    "FR0010017731",
    "LU2153615351",
    "LU2153615278",
    "FR0013505955",
    "LU2073791589",
    "LU2243672016",
    "FR0050000928",
    "FR0010451260",
    "LU2106854214",
    "LU0774943673",
    "LU1602090547",
    "FR0010339481",
    "LU1597245650",
    "LU1861215462",
    "LU1861216601",
    "LU0326423067",
    "FR0013276136",
    "IE00BK0VJR25",
    "IE00BF1T7090",
    "LU1293438005",
    "LU0992626480",
    "LU0992628858",
    "LU0992627298",
    "IE00BZ0X9Y02",
    "LU1861294665",
    "LU1653750171",
    "LU1530900684",
    "LU1683287889",
    "LU1718488734",
    "FR0013403714",
    "FR0010581728",
    "LU1781815995",
    "FR0013301561",
    "LU2049492049",
    "LU0605514057",
    "LU0605515880",
    "LU0976567114",
    "LU1892830321",
    "LU1065170968",
    "LU0976565332",
    "IE00BHBFD812",
    "LU1622557467",
    "FR0013287257",
    "LU0995139267",
    "LU1983259968",
    "LU2003419376",
    "LU1529809060",
    "FR0013305950",
    "LU1004823719",
    "LU1004824444",
    "IE00BMYPCM06",
    "LU1842711761",
    "LU0042381250",
    "LU0266117687",
    "IE00BMPRXW24",
    "IE00BDZRX185",
    "IE00BF2F4L66",
    "LU1951223343",
    "LU0914733646",
    "LU0841558611",
    "LU0841586075",
    "FR0011036920",
    "LU2023201044",
    "LU0270904351",
    "LU0503633769",
    "IE00BCCW5L37",
    "IE00B3W9BG81",
    "IE00BYQDND46",
    "IE00BDSTPS26",
    "IE00B39T3767",
    "IE00BFZ89B79",
    "IE00BYXVX196",
    "IE00B80G9288",
    "IE00BDT57V65",
    "IE00B7W3YB45",
    "IE0032883534",
    "LU2121415777",
    "LU0871827464",
    "LU0792910480",
    "LU0940006702",
    "LU2145462300",
    "LU2146189746",
    "FR00QU000022",
    "FR0011161181",
    "LU1862449409",
    "LU0889564604",
    "LU0976564954",
    "LU0976564954",
    "FR0013292331",
    "LU2147879626",
    "LU1683484361",
    "LU1936213682",
    "LU1918004273",
    "LU1683482589",
    "LU1683487380",
]


async def main():
    coroutine_list = []
    queue = asyncio.Queue()  # Wait for coroutine end messages, to display a progress bar

    for isin in ISINs:
        coroutine_list.append(asyncio.create_task(
            test_agregate_from_isin(queue, isin)))

    results = await asyncio.gather(*coroutine_list)

    df = pd.DataFrame.from_records(results)

    # df.fillna(0, inplace=True)

    # int_columns = ["quantalys_rating", "srri_rating"]
    # df[int_columns] = df[int_columns].astype(int)

    df.to_csv("test.csv")

start = time()
asyncio.run(main())
end = time() - start
print(f"Time to run : {end}")
"""
Ceux là sont not found...
=> Certains n'en ont pas ! Faire en sorte que ça ne plante pas en faisant de la gestion
d'exception aux différents niveaux de fetch

error : srri_rating is None 62215
error : srri_rating is None 2018090
error : srri_rating is None 781479
error : srri_rating is None 407574
error : srri_rating is None 705929
error : srri_rating is None 767225
error : srri_rating is None 820805
error : srri_rating is None 868036

Il y a des trucs à rassifier, on verra ce qu'en dit edouard,
pour l'instant il faut que je finisse mon info et que je bosse mon psc. (même si j'adore ce genre de projets)

"""
