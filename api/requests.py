"""
Request functions for the API
"""
from httpx import AsyncClient
from typing import TypedDict, List, Dict
from api.quantalys import get_main_page_search_data_for_isin


class FastSearchResult(TypedDict):
    sCodeISIN: str
    sNom: str
    ID_Produit: int


async def fast_search(isin: str, client: AsyncClient) -> List[FastSearchResult]:
    """Fast search using an ISIN number"""

    url = "https://www.quantalys.com/Recherche/Produits"

    return await client.post(url, data={
        "sSearch": isin,
        "maxItem": "6"  # default max set in the website
    })


class MainPageResult(TypedDict):
    data: List[Dict[str, str]]


async def main_page_search(isin: str, client: AsyncClient) -> MainPageResult:
    """Main page data search using an ISIN number"""

    url = "https://www.quantalys.com/Recherche/Data"

    return await client.post(url, data=get_main_page_search_data_for_isin(isin))


async def fonds_page_from_product_id(Product_ID: int, client: AsyncClient) -> str:
    """Get the fonds page from the product ID.
    Only way to get the SRRI rating"""

    url = f"https://www.quantalys.com/Fonds/{Product_ID}"

    return await client.get(url)
