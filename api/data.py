"""
Module that fetches the required fields using the requests module
"""
import asyncio
from api.requests import main_page_search, fonds_page_from_product_id
from bs4 import BeautifulSoup
from httpx import AsyncClient
from typing import List, Dict, TypedDict
import numpy as np
import os

LAST_BAR_LENGTH = 0  # Flush the progress bar


# Defined in priority order. The first match gets returned
PREDEFINED_GEO_ZONE_VALUES = [
    "Pays Emergents Amérique du Sud",
    "Pays Emergents Monde",
    "Monde",
    "Zone Euro",
    "Europe",
    "Etats-Unis",
    "Chine",
    "Asie",
    "France",
    "USD",
    "Euro",
]


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


def parse_srri_rating_from_fonds_page(soup: BeautifulSoup) -> int:
    """Parse the SRRI rating from the fonds page html code using beautifulsoup"""

    # Get SRRI rating number
    srri_rating = soup.find(
        "div", {"class": "indic-srri indic-srri-selected"})

    # It is not defined for some funds
    if srri_rating is None:
        return np.nan

    return int(srri_rating.text)


def parse_geo_zone_from_fonds_page(soup: BeautifulSoup) -> str | None:
    """Parse the geographical zone from the fonds page html code using beautifulsoup"""

    # Find the table entry
    # Warning : there is a space at the end !
    dts = soup.find_all("dt")

    # For some reason, soup.find("dt", text="Catégorie Quantalys ") does not work
    for dt in dts:
        if dt.text == "Catégorie Quantalys ":
            table_entry = dt

    # Find the next dt sibling
    dt_sibling = table_entry.find_next_sibling("dd")

    # Get its text content
    quantalys_category = dt_sibling.find("a").text

    # Get the first occurrence from the predefined values
    for predefined_value in PREDEFINED_GEO_ZONE_VALUES:
        if predefined_value in quantalys_category:
            return predefined_value

    return None  # Default : not found


async def agregate_from_isin(queue: asyncio.Queue, isin: str) -> FundsData:
    """Agregate all necessary data
    """
    try:

        async with AsyncClient(timeout=None) as client:

            #######################################################
            #            INFO FROM THE QUICK SEARCH               #
            #######################################################
            search_results: List[Dict[str, str]] = (await main_page_search(isin, client)).json()["data"]

            if len(search_results) == 0:
                wipe_progress_bar()
                print("Could not find ISIN", isin, "on Quantalys")
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

            #######################################################
            #                INFO FROM THE FUND PAGE              #
            #######################################################
            # Parsing the fund page in order to get more precise information
            fonds_page_html = await fonds_page_from_product_id(product_id, client)
            soup = BeautifulSoup(fonds_page_html.text, 'html.parser')

            # Parse the SRRI rating
            srri_rating = parse_srri_rating_from_fonds_page(soup)

            # Parse the geographical zone from more precise predefined values.
            # If no predefined value is found, we keep the previous value
            precise_geo_zone = parse_geo_zone_from_fonds_page(soup)
            if precise_geo_zone is not None:
                geo_zone = precise_geo_zone

            #######################################################
            #                    RETURN THE DATA                  #
            #######################################################

            await queue.put(isin)  # Communicate to the progress bar

            return {
                "ISIN": isin,
                "Nom du fond": fund_name,
                "Rating Quantalys": quantalys_rating,
                "Rating SRRI": srri_rating,
                "Sharpe Ratio": sharpe_ratio_3a,
                "Stupende Support": stupende_support,
                "Zone Géo": geo_zone,
                "Secteur et Style": sector_and_style
            }
    except Exception as e:
        wipe_progress_bar()
        print("Error with ISIN : ", isin, ":", e)
        await queue.put(isin)  # Communicate to the progress bar
        return {}


def print_progress_bar(count: int, total: int, bar_length: int = 60) -> None:
    """Prints a progress bar in the terminal"""
    global LAST_BAR_LENGTH

    terminal_width = os.get_terminal_size().columns

    if bar_length > terminal_width + 30:
        bar_length = terminal_width - 30

    percent_complete = count / total
    num_bar_filled = int(percent_complete * bar_length)
    num_bar_empty = bar_length - num_bar_filled
    bar = '|' + '#' * num_bar_filled + '-' * num_bar_empty + '|'
    percent_str = "{:.0%}".format(percent_complete)
    progress_msg = f'Progress: {percent_str} {bar} {count}/{total}'

    LAST_BAR_LENGTH = len(progress_msg)
    print('\r', progress_msg, end='', flush=True)


def wipe_progress_bar() -> None:
    """Erase the progress bar, in order to display a message"""
    print("\r", " " * LAST_BAR_LENGTH, end='\r', flush=True)


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
