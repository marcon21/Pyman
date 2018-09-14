import pygame, sys
from pygame.locals import *
import random
from PIL import Image

def create_coins(map_image, dictionary, block_size, width):
    """Function that, given a pixeled image of a map, a dictionary with various color for the relative blocks, their image and other information, the size of the block and the width of the monitor return a map the dimension of the map_image moltiplied by the block_size
    """
    coinmap_image = Image.open(map_image)

    coinmap_raw = list(coinmap_image.getdata()) #getting data(color) from the image
    map = []
    small_coin = []
    big_coin = []
    x = 0
    y = 0

    for element in coinmap_raw: #the image of the block
        if element == (255, 255, 0) or element == (255, 0, 0):
            if element == (255, 255, 0):
                surface_sprite = pygame.transform.scale(
                    pygame.image.load(dictionary[element][0]),
                    (block_size, block_size))

                coin = Coin(surface_sprite, x, y, dictionary[element][1])

            elif element == (255, 0, 0):
                surface_sprite = pygame.transform.scale(
                    pygame.image.load(dictionary[element][0]),
                    (block_size, block_size))

                coin = Bigcoin(surface_sprite, x, y, dictionary[element][1])

            map.append(coin)
        x += block_size
        if x == width:
            x = 0
            y += block_size

    return map


def place_coins(coinmap_group, window):
    for coin in coinmap_group:
        coin.draw(window, coin.rect.x, coin.rect.y)

class Coin(pygame.sprite.Sprite):
    """The class of the various 'coins'"""

    def __init__(self, image, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))


class Bigcoin(pygame.sprite.Sprite):
    """The class of the big 'coins'"""

    def __init__(self, image, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))
