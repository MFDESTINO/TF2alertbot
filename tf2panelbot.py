#!/usr/bin/env python3
# TF2 panel bot
# by Daniel Couto, 12/05/2020

from PIL import Image
from random import choice
import os
import sys


def make_panel(output_fname):
    os.chdir(os.path.dirname(sys.argv[0]))
    src_dir = os.path.join(os.getcwd(), 'src')
    base_image_path = os.path.join(src_dir, 'base.png')
    panels_dir = os.path.join(src_dir, 'panels')

    available_panels_list = os.listdir(panels_dir)

    output = Image.open(base_image_path).convert("RGBA")
    for i in range(3):
        panel = choice(available_panels_list)
        # same panel wont get selected 2 times
        available_panels_list.remove(panel)
        panel_img = Image.open(os.path.join(panels_dir, panel)).convert("RGBA")
        output = Image.alpha_composite(output, panel_img)

    output.save(output_fname)


if __name__ == "__main__":
    make_panel("output.png")
