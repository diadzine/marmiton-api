# -*- coding: utf-8 -*-
"""Marmiton API Recipe related types"""

from enum import Enum


class RecipePrice(Enum):
    """
    How much money would be spent by buying all the stuff required
    to make the Recipe.
    """

    CHEAP = 1
    MEDIUM = 2
    EXPENSIVE = 3


class RecipeDifficulty(Enum):
    """
    Level of difficulty to produce the Recipe.
    """

    VERY_EASY = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4


class RecipeType(Enum):
    """
    Type of the Recipe.
    """

    STARTER = 'entree'
    MAIN_COURSE = 'platprincipal'
    DESSERT = 'dessert'
    SIDE_DISH = 'accompagnement'
    SAUCE = 'sauce'
    BEVERAGE = 'boisson'
    CANDY = 'confiserie'
    ADVICE = 'conseil'


class Recipe:
    """
    Recipe class.
    """
    def __init__(
            self,
            name,
            description,
            url,
            rate,
            images,
            tags,
            difficulty,
            budget,
            author,
            people,
            ingredients,
            prepTime,
            totalTime,
            steps
            ):
        """Init method or constructor."""
        self.name = name
        self.description = description
        self.url = url
        self.rate = rate
        self.images = images
        self.tags = tags
        self.difficulty = difficulty
        self.budget = budget
        self.author = author
        self.people = people
        self.ingredients = ingredients
        self.prepTime = prepTime
        self.totalTime = totalTime
        self.steps = steps
