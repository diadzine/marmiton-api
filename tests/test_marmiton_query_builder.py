# -*- coding: utf-8 -*-
"""Test fo Marmiton API Query builder"""
from marmiton_api.builder import MarmitonQueryBuilder
from marmiton_api.recipe import RecipeDifficulty, RecipePrice, RecipeType


def test_handle_heavy_restrictions():
    qb = MarmitonQueryBuilder()
    query = (
        qb.with_title_containing('soja')
        .vegan()
        .with_photo()
        .without_oven()
        .with_price(RecipePrice.CHEAP)
        .taking_less_than(45)
        .with_difficulty(RecipeDifficulty.EASY)
        .build()
    )
    assert query == 'aqt=soja&prt=3&pht=1&rct=2&rct=3&exp=1&ttlt=45&dif=2'


def test_without_providing_query_string():
    qb = MarmitonQueryBuilder()
    query = (
        qb.with_type(RecipeType.MAIN_COURSE)
        .vegetarian()
        .raw()
        .without_dairy_products()
        .without_gluten()
        .build()
    )
    assert query == 'dt=platprincipal&prt=1&rct=3&prt=4&prt=2&aqt='
