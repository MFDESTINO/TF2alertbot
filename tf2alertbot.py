#!/usr/bin/env python3
# TF2 panel bot
# by Daniel Couto, 12/05/2020

from PIL import Image
from random import choice
import os
import sys
import json
from autopost import AutoPostBot

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

def make_description(namefile, recipe):
    with open (namefile, "r") as f:
        names_raw = f.readlines()

    names_dict = {}
    names = []
    for n in names_raw:
        name_number = n[-2]
        name = n[:-3]
        names.append(name)
        names_dict[name] = name_number
    description = {}
    for i in recipe:
        description[names[i]] = names_dict[names[i]]
    d = {k: v for k, v in sorted(description.items(), key=lambda item: item[1])}
    return " ".join(list(d.keys()))

def post_alert():
    from datetime import datetime
    now = datetime.now()
    timestamp = now.strftime("%y-%m-%d-%H-%M")
    os.chdir(os.path.dirname(sys.argv[0]))
    print(timestamp)
    recipe = get_recipe('recipes.json')
    print(recipe)
    description = make_description('names2.txt', recipe).upper()
    make_panel_image('output.png', recipe)
    postbot = AutoPostBot('https://mbasic.facebook.com/TF2alertbot/')
    postbot.post_image('/home/friend/TF2alertbot/output.png', [description])

import multiprocessing as mp

if __name__ == "__main__":
    p = mp.Process(target=post_alert)
    p.start()
    p.join()
