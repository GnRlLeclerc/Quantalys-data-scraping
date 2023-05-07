"""
Module that fetches the required fields using the requests module
"""
import asyncio
from api.requests import main_page_search, fonds_page_from_product_id
from bs4 import BeautifulSoup
from httpx import AsyncClient
from typing import List, Dict, TypedDict
import numpy as np


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

    # It is not defined for some funds
    if srri_rating is None:
        return np.nan

    return int(srri_rating.text)


async def test_agregate_from_isin(queue: asyncio.Queue, isin: str) -> FundsData:
    """Test : agregate all necessary data
    """
    async with AsyncClient(timeout=None) as client:

        search_results: List[Dict[str, str]] = (await main_page_search(isin, client)).json()["data"]

        if len(search_results) == 0:
            await queue.put(isin)  # Communicate to the progress bar
            return {}

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
        await queue.put(isin)  # Communicate to the progress bar

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


def print_progress_bar(count: int, total: int, bar_length: int = 60) -> None:
    """Prints a progress bar in the terminal"""
    percent_complete = count / total
    num_bar_filled = int(percent_complete * bar_length)
    num_bar_empty = bar_length - num_bar_filled
    bar = '|' + '#' * num_bar_filled + '-' * num_bar_empty + '|'
    percent_str = "{:.0%}".format(percent_complete)
    progress_msg = f'Progress: {percent_str} {bar} {count}/{total}'
    print('\r', progress_msg, end='', flush=True)


async def display_progress_bar(queue: asyncio.Queue, total: int) -> None:
    """Read the queue and update the progress bar value"""

    completed_tasks = 0

    while True:
        await queue.get()

        completed_tasks += 1
        print_progress_bar(completed_tasks, total)

        if completed_tasks == total:
            print()
            break
