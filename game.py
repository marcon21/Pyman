import pygame
from pygame.locals import *
from generate_map import create_map, draw_map
from djikstra import *
from math import sqrt

pygame.init()

block_size = 32

GAME_RES = WIDTH, HEIGHT = 28 * block_size, 31 * block_size
FPS = 60
GAME_TITLE = 'PyMAN'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values

background_color = (150, 150, 150) # RGB value
speed = 2
non_touching_position = (32, 32)


class Pyman(pygame.sprite.Sprite):
    """The class of the main character"""

    def __init__(self, image, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def touch_node(self):   #detect collision between PyMan and nodes
        if (self.rect.x, self.rect.y) in node_list:
            return True

    def wall_collide(self): #detect if PyMan is colliding with a wall
        if pygame.sprite.spritecollide(self, wall_group, False) != []:
            return True

    def position(self, non_touching_position):  #return the position of PyMan
        if pygame.sprite.spritecollide(self, wall_group, False) == []:
            return (self.rect.x, self.rect.y)
        else:
            self.rect.x  = non_touching_position[0]
            self.rect.y = non_touching_position[1]
            return non_touching_position

    def move(self, direction):  #give PyMan the ability to move
        self.teleport()
        if direction == "up":
            self.rect.y += self.speed * -1
        if direction == "down":
            self.rect.y += self.speed * 1
        if direction == "right":
            self.rect.x += self.speed * 1
        if direction == "left":
            self.rect.x += self.speed * -1

    def teleport(self):     #allow PyMan to teleport when he's outside the map
        if self.rect.x < -self.rect.width:
            self.rect.x = WIDTH
        if self.rect.x > WIDTH:
            self.rect.x = -self.rect.width


pyman_image = pygame.image.load("./image/pyman.png")
pyman_image = pygame.transform.scale(pyman_image, (block_size - 2,
                                                   block_size - 2))

pyman = Pyman(pyman_image, 32, 32, speed)   #create PyMan instance
pyman_group = pygame.sprite.Group(pyman)


class Ghost(pygame.sprite.Sprite):
    """The class for the 4 ghosts"""


    def __init__(self, image, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def nearest_node(self, pacman_rect, node_list):
        nearest_node = node_list[10]
        min_dist = WIDTH + HEIGHT

        for node in node_list:
            if [node[0], node[1]] != [self.rect.x, self.rect.y]:
                if node[0] == self.rect.x or node[1] == self.rect.y:
                    distanceGhostToNode = distance([self.rect.x, self.rect.y], node)
                    distanceNodeToPacman = distance(node, [pacman_rect[0], pacman_rect[1]])
                    totalDistance = distanceGhostToNode + distanceNodeToPacman
                    # print(totalDistance, node)
                    if totalDistance < min_dist:
                        min_dist = totalDistance
                        nearest_node = node


        """if pacman_rect.x == self.rect.x or pacman_rect.y == self.rect.y:
            if min[1] > distance(g_pos, p_pos):
                min = (p_pos, None)
                """

        return nearest_node


    def move(self):
        end_pos = self.nearest_node([pyman.rect[0], pyman.rect[1]], node_list)
        print((self.rect.x, self.rect.y), "SELF")
        print(end_pos, "END POS")
        print((pyman.rect.x, pyman.rect.y), "Pyman")
        print()

        if self.rect.x != end_pos[0]:
            if self.rect.x > end_pos[0]:
                self.rect.x -= self.speed / 2
            else:
                self.rect.x += self.speed / 2

        if self.rect.y != end_pos[1]:
            if self.rect.y > end_pos[0]:
                self.rect.y -= self.speed / 2
            else:
                self.rect.y += self.speed / 2


def distance(startPos, endPos):
    delta_x = abs(startPos[0] - endPos[0])
    delta_y = abs(startPos[1] - endPos[1])
    delta = sqrt(delta_x ** 2 + delta_y ** 2)
    return delta


ghost_image = pygame.image.load("./image/ghost.png")
ghost_image = pygame.transform.scale(ghost_image, (block_size,
                                                   block_size))

ghost = Ghost(ghost_image, 256, 32, speed)   #create Ghost instance
ghost_group = pygame.sprite.Group(ghost)




map_image = "./image/PixelMap.png"
map_bg = "./image/PacmanLevel-1.png"

dict_map = {
    (0, 0, 0):  ("./image/trasparente.png", True), # wall
    (255, 255, 255): ("./image/trasparente.png", False), # bg
    (0, 255, 0): ("./image/bg.png", False), # node
    (0, 0, 255): ("./image/trasparente.png", False) # node
}

map = create_map(map_image, dict_map, block_size, WIDTH) #create the map
wall_array = []
for blocks in map:
    if blocks.wall == True:
        wall_array.append(blocks)

wall_group = pygame.sprite.Group(wall_array)

node_list = node_position(map_image, (0, 255, 0), block_size, WIDTH)

# End of Game Values
direction = ""
new_direction = direction

# Game loop
game_ended = False
while not game_ended:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            game_ended  = True
            break
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game_ended  = True
                break

    keys_pressed = pygame.key.get_pressed()

    #detect if any key is pressed
    if keys_pressed[K_s] or keys_pressed[K_DOWN]:
        new_direction = "down"
    if keys_pressed[K_w] or keys_pressed[K_UP]:
        new_direction = "up"
    if keys_pressed[K_a] or keys_pressed[K_LEFT]:
        new_direction = "left"
    if keys_pressed[K_d] or keys_pressed[K_RIGHT]:
        new_direction = "right"

    #allow PyMan to move only if it's on a node or the movement is opposite
    if not pyman.wall_collide():
        if (pyman.touch_node() or
            direction == "down" and new_direction == "up" or
            direction == "up" and new_direction == "down" or
            direction == "left" and new_direction == "right" or
            direction == "right" and new_direction == "left"):
            direction = new_direction
    else:   #allow PyMan to get out of the wall...
        direction = new_direction

    #getting the position that is not touching the wall
    non_touching_position = pyman.position(non_touching_position)
    pyman.move(direction)
    ghost.move()
    # Game logic

    # Display update
    draw_map(map, map_bg, window)
    pyman_group.draw(window)
    ghost_group.draw(window)

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
exit(0)
