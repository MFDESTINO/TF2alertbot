#!/usr/bin/env python3
# TF2 panel bot
# by Daniel Couto, 12/05/2020

from PIL import Image
from random import choice
import os
import sys
import json


def generate_recipe_file(recipe_file, num_panels=72):
    from itertools import combinations

    panels = list(range(num_panels))
    recipes = list(combinations(panels, 3))

    with open(recipe_file, 'w') as json_file:
        json.dump(recipes, json_file, indent=4)


def get_recipe(recipe_file):
    with open(recipe_file, 'r') as json_file:
        recipes = json.load(json_file)

    recipe = choice(recipes)

    # once a recipe is used, its removed from the file to avoid repetitions
    recipes.remove(recipe)
    with open(recipe_file, 'w') as json_file:
        json.dump(recipes, json_file, indent=4)
    return recipe


def make_panel_image(output_fname, recipe):
    src_dir = os.path.join(os.getcwd(), 'src')
    base_image_path = os.path.join(src_dir, 'base.png')
    panels_dir = os.path.join(src_dir, 'panels')

    output = Image.open(base_image_path).convert("RGBA")
    for i in range(len(recipe)):
        panel = str(recipe[i] + 1) + ".png"
        panel_img = Image.open(os.path.join(panels_dir, panel)).convert("RGBA")
        output = Image.alpha_composite(output, panel_img)

    output.save(output_fname)


if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.argv[0]))
    recipe = get_recipe("recipes.json")
    print(recipe)
    make_panel_image("output.png", recipe)
