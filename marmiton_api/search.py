# -*- coding: utf-8 -*-
"""Marmiton API Recipe search"""
import requests
from typing import List, Optional

from .parser import RecipesParser
from .recipe import Recipe

BASE_URL = 'https://www.marmiton.org'
ENDPOINTS = {
    'query': lambda: f"{BASE_URL}/recettes/recherche.aspx",
}
# Number of recipes per page (this isn't constant)
RECIPES_PER_PAGE = 13
DEFAULT_OPTIONS = {
    'limit': RECIPES_PER_PAGE,
}


async def search_recipes(qs: str, opt: Optional[dict] = None) -> List[Recipe]:
    options = {**DEFAULT_OPTIONS, **opt} if opt else DEFAULT_OPTIONS
    recipes = []

    for i in range(1, options['limit']):
        url = f"{ENDPOINTS['query']}?{qs}"
        url += f"&page={i + 1}"
        request = await requests.get(url)
        if request.status_code != 200:
            break
        html_body = request.text
        recipes.extend(
            await RecipesParser.parse_search_results(html_body, BASE_URL)
        )

    return recipes[:options['limit']]
