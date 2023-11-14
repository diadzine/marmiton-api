# -*- coding: utf-8 -*-
"""Marmiton API Recipe parser"""
import asyncio
import json
import re
import requests
from bs4 import BeautifulSoup as BS
from functools import partial
from requests.compat import urljoin
from typing import List, Optional

from .builder import RecipeBuilder
from .recipe import RecipeDifficulty, RecipePrice, Recipe


class RecipesParser:
    ISO_8601_REGEX = re.compile(
        r"^P(?!$)(\d+(?:\.\d+)?Y)?(\d+(?:\.\d+)?M)?(\d+(?:\.\d+)?W)?(\d+(?:\.\d+)?D)?"  # NOQA
        r"(T(?=\d)(\d+(?:\.\d+)?H)?(\d+(?:\.\d+)?M)?(\d+(?:\.\d+)?S)?)?$"
    )

    @staticmethod
    async def parse_search_results(dom: str,
                                   base_url: str
                                   ) -> List[partial[Recipe]]:
        recipes = await asyncio.gather(
            *[
                RecipesParser.parse_recipe(e, base_url)
                for e in BS(dom, "html.parser").select("main div > a.MRTN")
            ]
        )
        return [r for r in recipes if r]

    @staticmethod
    async def parse_recipe(element, base_url) -> Optional[partial[Recipe]]:
        url = urljoin(base_url, element["href"].strip())
        rb = (
            RecipeBuilder()
            .with_name(element.select_one("h4").text.strip())
            .with_rate(
                float(
                    element.select_one("span").text.strip().replace("/ 5", "")
                )
            )
            .with_url(url)
        )
        try:
            response = await requests.get(url)
            response.raise_for_status()
            return await RecipesParser.parse_recipe_content(response.text, rb)
        except Exception as e:
            print(f"Error fetching recipe content: {e}")
            return None

    @staticmethod
    async def parse_recipe_content(content, rb):
        recipe_data = json.loads(
            re.search(
                r'<script type="application/ld\+json">(.*?)</script>', content
            ).group(1)
        )
        if not (recipe_data and recipe_data["@type"] == "Recipe"):
            return None

        rb.with_ingredients(recipe_data.get("recipeIngredient", []))
        rb.with_author(recipe_data.get("author"))
        rb.with_images([recipe_data.get("image")].flat())
        rb.with_steps(
            [
                ri["text"]
                for ri in recipe_data.get("recipeInstructions", [])
            ]
        )
        rb.with_description(recipe_data.get("description"))

        keywords = recipe_data.get("keywords", "").split(", ")
        raw_budget, raw_difficulty = keywords[-1], keywords[-2]
        rb.with_difficulty(
            RecipesParser.parse_difficulty(raw_difficulty)
        ).with_budget(
            RecipesParser.parse_budget(raw_budget)
        ).with_tags(keywords)

        rb.with_preparation_time(
            RecipesParser.parse_iso8601(recipe_data.get("prepTime"))
        ).with_total_time(
            RecipesParser.parse_iso8601(recipe_data.get("totalTime"))
        )

        people = int(
            re.search(r"\d+", recipe_data.get("recipeYield", "0")).group()
        )
        rb.with_people(people)

        return rb.build()

    @staticmethod
    def parse_iso8601(duration: str) -> int:
        matches = RecipesParser.ISO_8601_REGEX.match(duration)
        minutes = int(matches.group(8)) if matches and matches.group(8) else 0
        hours = int(matches.group(7)) if matches and matches.group(7) else 0
        return hours * 60 + minutes

    @staticmethod
    def parse_budget(budget: str) -> RecipePrice:
        budget = budget.lower()
        if "bon marché" in budget:
            return RecipePrice.CHEAP
        elif "moyen" in budget:
            return RecipePrice.MEDIUM
        elif "assez cher" in budget:
            return RecipePrice.EXPENSIVE
        else:
            return RecipePrice.MEDIUM

    @staticmethod
    def parse_difficulty(difficulty: str) -> RecipeDifficulty:
        difficulty = difficulty.lower()
        if "très facile" in difficulty:
            return RecipeDifficulty.VERY_EASY
        elif "facile" in difficulty:
            return RecipeDifficulty.EASY
        elif "moyenne" in difficulty:
            return RecipeDifficulty.MEDIUM
        elif "difficile" in difficulty:
            return RecipeDifficulty.HARD
        else:
            return RecipeDifficulty.MEDIUM
