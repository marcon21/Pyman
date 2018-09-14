import pygame, sys, random, math
from pygame.locals import *
from PIL import Image

def node_position(map, color, block_size, WIDTH):
    """Algorithm that find the position of each node in a given map
    map = node map
    color = node color in RGB (R, G, B)
    block_size = the size of the block(square)
    WIDTH = width of the map
    """

    image_nodemap = Image.open(map)
    nodemap_raw = list(image_nodemap.getdata())
    x, y = 0, 0
    nodes_pos = []

    for element in nodemap_raw: # Finding the node in the map
        if element == (color):
            nodes_pos.append((x, y))
        x += block_size

        if x == WIDTH:  # Check the end of the row
            x, y = 0, y + block_size

    return nodes_pos
