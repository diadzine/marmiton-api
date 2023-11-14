# -*- coding: utf-8 -*-
"""Test fo Marmiton API Recipe parser"""
import pytest
import math
import time
from marmiton_api.builder import MarmitonQueryBuilder
from marmiton_api.search import search_recipes


@pytest.mark.asyncio
async def test_basic_query():
    recipes = await search_recipes('aqt=soja&rct=1&ttlt=40')
    for r in recipes:
        print(r)
        for key, value in r.items():
            print(f'{key} --> {value}')
            assert not isinstance(value, float) and not math.isnan(value)
            assert value is not None
            assert value is not None


@pytest.mark.asyncio
async def test_should_be_able_to_get_more_than_one_page():
    start = time.process_time()
    recipes = await search_recipes('aqt=soja', limit=46)
    assert len(recipes) == 46
    for r in recipes:
        print(r)
        for key, value in r.items():
            print(f'{key} --> {value}')
            assert not isinstance(value, float) and not math.isnan(value)
            assert value is not None
    end = time.process_time() - start
    print(end)


@pytest.mark.asyncio
async def test_simple_builder_request():
    rb = MarmitonQueryBuilder()
    qs = rb.vegan().build()
    recipes = await search_recipes(qs)
    for r in recipes:
        print(r)
        for key, value in r.items():
            print(f'{key} --> {value}')
            assert not isinstance(value, float) and not math.isnan(value)
            assert value is not None
