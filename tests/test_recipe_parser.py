# -*- coding: utf-8 -*-
"""Test fo Marmiton API Recipe parser"""
import pytest
import requests
from marmiton_api.parser import RecipesParser


@pytest.mark.asyncio
async def test_using_sample_recipe_without_image():
    sample = await requests.get(
        'https://gist.githubusercontent.com/SoTrxII/299c3ee1750fc74526e4d8e0b4936944/raw/f26821214efd3aec90e0f4ca9d2841f6e348565b/sample_recipe.html'   # NOQA
    )
    r = await RecipesParser.parse_recipe(sample)
    assert r == {
        'author': 'lina_16542241',
        'ingredients': [
            '1 pots de yaourt soja nature',
            "1/2 pots d'huile",
            '2 pots de sucre',
            '2 pots de farine',
            '1 pots de maïzena',
            '1 oeufs',
            '1/2 sachets de levure',
            'pomme',
            'chocolat',
            'noix de coco rapée',
            'cannelle',
            'nappage chocolat',
        ],
        'tags': [
            'Muffins au yaourt de soja',
            'muffin',
            'yaourt',
            'huile',
            'sucre',
            'farine',
            'maïzena',
            'oeuf',
            'levure',
            'pomme',
            'chocolat',
            'noix de coco rapée',
            'cannelle',
            'nappage chocolat',
            'facile',
            'bon marché',
        ],
        'steps': [
            'Préchauffer le four à 180°C (thermostat 6).',
            'Dans un saladier, vider le pot de yaourt. Celui-ci servira de mesure.',    # NOQA
            "Ajouter l'huile. Mélanger.",
            'Ajouter le sucre. Mélanger.',
            'Ajouter la farine, puis la maïzena et la levure (tamisées si possible), tout en mélangeant.',  # NOQA
            "Ajouter l'oeuf. Bien mélanger.",
            'Ajouter à votre guise chocolat ou autre douceur pour obtenir des muffins encore meilleurs. Ils sont aussi très bons natures.',     # NOQA
            'Cuire pendant 15-20 min à 180°C dans des moules adaptés.',
        ],
        'people': 12,
        'budget': 1,
        'difficulty': 2,
        'prepTime': 15,
        'totalTime': 35,
    }


@pytest.mark.asyncio
async def test_using_sample_recipe_with_multiple_images():
    sample = await requests.get(
        'https://gist.githubusercontent.com/SoTrxII/6d39dc7c3c543b424c86d588b9281519/raw/44f5c935f431b51a317c2a673a8ce3bd3a5f8b4c/sample_recipe_image.html'     # NOQA
    )
    r = await RecipesParser.parse_recipe(sample)
    assert r == {
        'ingredients': [
            '7 pommes de terre',
            '20 cl de crème fraîche',
            '150 g de gruyère râpé',
            'sel',
            'poivre',
            '8 fines tranches de lard',
            '3 oeufs entiers',
            '1 fromage de chèvre',
            '1 pâte feuilletée',
        ],
        'author': 'Anonyme',
        'images': [
            'https://assets.afcdn.com/recipe/20170609/68312_w1024h1024c1cx2000cy3000.webp',     # NOQA
            'https://assets.afcdn.com/recipe/20170609/68312_w1024h768c1cx2000cy3000.webp',      # NOQA
            'https://assets.afcdn.com/recipe/20170609/68312_w1024h576c1cx2000cy3000.webp',      # NOQA
            'https://assets.afcdn.com/recipe/20170609/68312_w1024h1024c1cx2000cy3000.jpg',      # NOQA
            'https://assets.afcdn.com/recipe/20170609/68312_w1024h768c1cx2000cy3000.jpg',       # NOQA
            'https://assets.afcdn.com/recipe/20170609/68312_w1024h576c1cx2000cy3000.jpg',       # NOQA
        ],
        'steps': [
            'Cuire les pommes de terre à la vapeur.\nPréchauffer le four à 200°C (thermostat 6-7).', # NOQA
            'Tapisser le moule de tranches de lard.',
            'Mettre le râpé sur les tranches de lard. ',
            'Couper les pommes de terre en rondelles sur le râpé, puis le fromage de chèvre en tranches.', # NOQA
            'Battre dans un bol la crème, les oeufs, le sel et poivre, verser sur la préparation.', # NOQA
            'Mettre la pâte feuilletée dessus comme une tarte tatin et la piquer.', # NOQA
            'Cuire pendant 30 min suivant le four.',
        ],
        'description': 'pomme de terre, crème fraîche, gruyère râpé, sel, poivre, lard, oeuf, fromage de chèvre, pâte feuilletée', # NOQA
        'difficulty': 1,
        'budget': 1,
        'tags': [
            'Quiche tatin',
            'pomme de terre',
            'crème fraîche',
            'gruyère râpé',
            'sel',
            'poivre',
            'lard',
            'oeuf',
            'fromage de chèvre',
            'pâte feuilletée',
            'quiche Tatin',
            'très facile',
            'bon marché',
        ],
        'prepTime': 15,
        'totalTime': 45,
        'people': 6,
    }


@pytest.mark.asyncio
async def test_with_high_difficulty():
    sample = await requests.get(
        'https://www.marmiton.org/recettes/recette_poulet-fermier-pommes-de-terres-fleurs-de-courgettes_530770.aspx'      # NOQA
    )
    r = await RecipesParser.parse_recipe(sample)

    assert r['difficulty'] == 4
    assert r['budget'] == 3
