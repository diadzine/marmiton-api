# -*- coding: utf-8 -*-
"""Marmiton API Recipe builder"""
from typing import List

from .recipe import RecipeDifficulty, RecipePrice, RecipeType


class RecipeBuilder:
    def __init__(self):
        self.infos = {}

    def with_name(self, name: str) -> 'RecipeBuilder':
        self.infos['name'] = name
        return self

    def with_description(self, desc: str) -> 'RecipeBuilder':
        self.infos['description'] = desc
        return self

    def with_url(self, url: str) -> 'RecipeBuilder':
        self.infos['url'] = url
        return self

    def with_rate(self, rate: float) -> 'RecipeBuilder':
        self.infos['rate'] = rate
        return self

    def with_tags(self, tags: List[str]) -> 'RecipeBuilder':
        self.infos['tags'] = tags
        return self

    def with_difficulty(self, d: RecipeDifficulty) -> 'RecipeBuilder':
        self.infos['difficulty'] = d
        return self

    def with_budget(self, b: RecipePrice) -> 'RecipeBuilder':
        self.infos['budget'] = b
        return self

    def with_author(self, s: str) -> 'RecipeBuilder':
        self.infos['author'] = s
        return self

    def with_people(self, nb: int) -> 'RecipeBuilder':
        self.infos['people'] = nb if not isinstance(nb, bool) else None
        return self

    def with_ingredients(self, ing: List[str]) -> 'RecipeBuilder':
        self.infos['ingredients'] = ing
        return self

    def with_preparation_time(self, prep: int) -> 'RecipeBuilder':
        self.infos['prepTime'] = prep
        return self

    def with_total_time(self, total: int) -> 'RecipeBuilder':
        self.infos['totalTime'] = total
        return self

    def with_steps(self, steps: List[str]) -> 'RecipeBuilder':
        self.infos['steps'] = steps
        return self

    def with_images(self, images: List[str]) -> 'RecipeBuilder':
        self.infos['images'] = images
        return self

    def build(self):
        return self.infos


class MarmitonQueryBuilder:
    def __init__(self):
        self.query_string = {}

    def with_title_containing(self, q: str) -> 'MarmitonQueryBuilder':
        self.query_string['aqt'] = q
        return self

    def with_price(self, p: RecipePrice) -> 'MarmitonQueryBuilder':
        self.query_string['exp'] = str(p.value)
        return self

    def with_difficulty(self, d: RecipeDifficulty) -> 'MarmitonQueryBuilder':
        self.query_string['dif'] = str(d.value)
        return self

    def with_type(self, t: RecipeType) -> 'MarmitonQueryBuilder':
        self.query_string['dt'] = t.value
        return self

    def taking_less_than(self, minutes: int) -> 'MarmitonQueryBuilder':
        self.query_string['ttlt'] = str(minutes)
        return self

    def vegetarian(self) -> 'MarmitonQueryBuilder':
        self.query_string['prt'] = '1'
        return self

    def vegan(self) -> 'MarmitonQueryBuilder':
        self.query_string['prt'] = '3'
        return self

    def without_gluten(self) -> 'MarmitonQueryBuilder':
        self.query_string['prt'] = '2'
        return self

    def without_dairy_products(self) -> 'MarmitonQueryBuilder':
        self.query_string['prt'] = '4'
        return self

    def raw(self) -> 'MarmitonQueryBuilder':
        self.query_string['rct'] = '3'
        return self

    def without_oven(self) -> 'MarmitonQueryBuilder':
        self.query_string.pop('rct', None)
        self.query_string['rct'] = ['2', '3']
        return self

    def with_photo(self) -> 'MarmitonQueryBuilder':
        self.query_string['pht'] = '1'
        return self

    def build(self) -> str:
        # The title query is mandatory but can be empty
        if 'aqt' not in self.query_string:
            self.query_string['aqt'] = ''
        return '&'.join(
            [
                f"{key}={value}"
                if not isinstance(value, list) else '&'.join(
                    [
                        f"{key}={v}" for v in value
                    ]
                )
                for key, value in self.query_string.items()
            ]
        )
