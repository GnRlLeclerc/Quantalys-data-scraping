"""
Module that fetches the required fields using the requests module
"""
from api.requests import main_page_search, fonds_page_from_product_id
from bs4 import BeautifulSoup
from httpx import AsyncClient
from typing import List, Dict, TypedDict


class FundsData(TypedDict):
    name: str
    quantalys_rating: int
    srri_rating: int
    sharpe_ratio: str
    stupende_support: str
    geo_zone: str
    sector_and_style: str


def remove_stupende_from_geo_zone(stupende: str, geo_zone: str) -> str:
    """Helper function : remove the stupende part from the geo zone"""

    if geo_zone[:len(stupende)] == stupende:
        return geo_zone[len(stupende) + 1:]


def parse_srri_rating_from_fonds_page(html: str, product_id_debug) -> int:
    """Parse the SRRI rating from the fonds page html code using beautifulsoup"""

    soup = BeautifulSoup(html, 'html.parser')

    # Get SRRI rating number
    srri_rating = soup.find(
        "div", {"class": "indic-srri indic-srri-selected"})

    if srri_rating is None:  # BUG : pourquoi c'est none
        print("error : srri_rating is None", product_id_debug)
        return -1

    return int(srri_rating.text)


async def test_agregate_from_isin(isin: str, client: AsyncClient) -> FundsData:
    """Test : agregate all necessary data
    TODO : ne pas déclarer un client async pour chacune des requêtes
    """
    search_results: List[Dict[str, str]] = (await main_page_search(isin, client)).json()["data"]

    if len(search_results) == 0:
        return {"empty": True}

    data = search_results[0]

    # Extract useful data
    fund_name = data["sNom"]
    quantalys_rating = data["nStarRating"]
    srri_rating = None
    sharpe_ratio_3a = data["nSharpe3a"]
    stupende_support = data["sGroupeCat_rng1"]
    geo_zone = remove_stupende_from_geo_zone(  # BUG : parfois, ce n'est pas défini...
        stupende_support, data["sGroupeCat_Specific_Dynamic"])
    sector_and_style = None  # TODO

    # Request main page to get the SRRI rating
    product_id = data["ID_Produit"]
    fonds_page_html = await fonds_page_from_product_id(product_id, client)
    srri_rating = parse_srri_rating_from_fonds_page(
        fonds_page_html.text, product_id)

    # DEBUG : Print all this data
    # print(f"ISIN : {isin}")
    # print(f"Fund name : {fund_name}")
    # print(f"Quantalys rating : {quantalys_rating}")
    # print(f"SRRI rating : {srri_rating}")
    # print(f"Sharpe ratio 3a : {sharpe_ratio_3a}")
    # print(f"Stupende support : {stupende_support}")
    # print(f"Geo zone : {geo_zone}")
    # print(f"Sector and style : {sector_and_style}")

    return {
        "ISIN": isin,
        "name": fund_name,
        "quantalys_rating": quantalys_rating,
        "srri_rating": srri_rating,
        "sharpe_ratio": sharpe_ratio_3a,
        "stupende_support": stupende_support,
        "geo_zone": geo_zone,
        "sector_and_style": sector_and_style
    }
