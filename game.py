import pygame
import time
from pygame.locals import *
from generate_map import create_map, draw_map
from node_position import node_position
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

    def __init__(self, image, x, y, speed, life_pos, life_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.start_x = x
        self.start_y = y
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.speed = speed
        self.direction = ""
        self.new_direction = self.direction
        self.life_image = life_image
        self.rect_life = self.life_image.get_rect()
        self.life = 3
        self.life_pos = life_pos

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

    def move(self):  #give PyMan the ability to move
        self.teleport()
        if self.direction == "up":
            self.rect.y += self.speed * -1
        if self.direction == "down":
            self.rect.y += self.speed * 1
        if self.direction == "right":
            self.rect.x += self.speed * 1
        if self.direction == "left":
            self.rect.x += self.speed * -1

    def teleport(self):     #allow PyMan to teleport when he's outside the map
        if self.rect.x < -self.rect.width:
            self.rect.x = WIDTH
        if self.rect.x > WIDTH:
            self.rect.x = -self.rect.width

    def check_if_dead(self):
        if pygame.sprite.spritecollide(self, ghost_group, False) != []:
            self.restart()

    def restart(self):
        global ghost_group, game_over_image
        self.life -= 1
        if self.life <= 0:
            self.speed = 0
            for ghosts in ghost_group:
                ghosts.speed = 0
            game_over_rect = game_over_image.get_rect()
            window.blit(game_over_image,
                        (WIDTH / 2 - game_over_rect.width / 2,
                         HEIGHT / 2 - game_over_rect.height / 2))
        else:
            time.sleep(1)
            self.rect.x = self.start_x
            self.rect.y = self.start_y
            for ghosts in ghost_group:
                ghosts.rect.x =  ghosts.start_x
                ghosts.rect.y = ghosts.start_y

    def life_display(self):
        for life in range(self.life):
            window.blit(self.life_image,
                        (self.life_pos[0] + self.rect_life.width * life + 1,
                        self.life_pos[1]))



pyman_image = pygame.image.load("./image/pyman.png")
pyman_image = pygame.transform.scale(pyman_image, (block_size - 2,
                                                   block_size - 2))

life_image = pygame.image.load("./image/life.png")
life_image = pygame.transform.scale(life_image,
                                    (block_size + block_size // 2,
                                    block_size + block_size // 2))

pyman = Pyman(pyman_image, #create PyMan instance
              block_size * 1,
              block_size * 1, speed,
              [0, HEIGHT / 2 - 5 * block_size],
              life_image)


pyman_group = pygame.sprite.Group(pyman)

game_over_width = WIDTH
game_over_image = pygame.image.load("./image/game_over.png")
game_over_image = pygame.transform.scale(game_over_image,
                                        (game_over_width,
                                        int(game_over_width / 1.7777)))
class Ghost(pygame.sprite.Sprite):

    """The class for the 4 ghosts"""
    def __init__(self, image, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.start_x = x
        self.start_y = y
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.speed = speed
        self.last_node = (x, y)

    #finding the nearest node to the ghost
    def nearest_node(self, pacman_rect, node_list):
        nearest_node = None
        min_dist = WIDTH + HEIGHT

        for node in node_list:
            if node != self.last_node:
                if [node[0], node[1]] != [self.rect.x, self.rect.y]:
                    if node[0] == self.rect.x or node[1] == self.rect.y:
                        if not self.collide_wall(self.postion_node(node)):
                            distanceGhostToNode = distance([self.rect.x, self.rect.y], node)
                            distanceNodeToPacman = distance(node, pacman_rect)
                            totalDistance = distanceGhostToNode + distanceNodeToPacman
                            if totalDistance < min_dist:
                                min_dist = totalDistance
                                nearest_node = node

        if node[0] == self.rect.x or node[1] == self.rect.y:
            if distance(pacman_rect, (self.rect.x, self.rect.y)) < min_dist and \
            not self.collide_wall(self.postion_node(node)):
                nearest_node = pacman_rect

        return nearest_node

    #give the ghost the ability to move
    def move(self):
        end_pos = self.nearest_node([pyman.rect[0], pyman.rect[1]], node_list)
        if self.rect.x > end_pos[0]:
            self.rect.x -= self.speed
        if self.rect.x < end_pos[0]:
            self.rect.x += self.speed

        if self.rect.y > end_pos[1]:
            self.rect.y -= self.speed
        if self.rect.y < end_pos[1]:
            self.rect.y += self.speed

    #refresh the last node position
    def refresh_last_node(self, node_list):
        for node in node_list:
            if node == (self.rect.x, self.rect.y):
                self.last_node = node
                return None

    #detect if there is a wall in front of the ghost
    def collide_wall(self, direction):
        global block_size, wall_position
        if direction == "up":
            if (self.rect.x, self.rect.y - block_size) in wall_position:
                return True
        elif direction == "down":
            if (self.rect.x, self.rect.y + block_size) in wall_position:
                return True
        elif direction == "left":
            if (self.rect.x - block_size, self.rect.y) in wall_position:
                return True
        elif direction == "right":
            if (self.rect.x + block_size, self.rect.y) in wall_position:
                return True
        else:
                return False

    #the position of the node in reference to the PyMan one
    def postion_node(self, node):
        if node[0] == self.rect.x:
            if node[1] > self.rect.y:
                return "down"
            else:
                return "up"
        else:
            if node[0] > self.rect.x:
                return "right"
            else:
                return "left"

#function that find the distance between point a and b
def distance(a, b):
    delta_x = a[0] - b[0]
    delta_y = a[1] - b[1]
    return sqrt(delta_x ** 2 + delta_y ** 2)

#giving ghosts some shape!
ghost_image = pygame.image.load("./image/ghost.png")
ghost_image = pygame.transform.scale(ghost_image, (block_size,
                                                   block_size))

#create Ghosts instance
ghost1 = Ghost(ghost_image, block_size, HEIGHT - 2 * block_size, speed)
ghost2 = Ghost(ghost_image, WIDTH - 2 * block_size, block_size, speed)

ghost_list = [ghost1, ghost2]
ghost_group = pygame.sprite.Group(ghost_list)

#acquiring map images
map_image = "./image/PixelMap.png"
map_bg = "./image/PacmanLevel-1.png"

#a dictionary used for the creation of the map
dict_map = {
    (0, 0, 0):  ("./image/trasparente.png", True), # wall
    (255, 255, 255): ("./image/trasparente.png", False), # bg
    (0, 255, 0): ("./image/trasparente.png", False), # node
    (0, 0, 255): ("./image/trasparente.png", False) # sponsor
}

#creating the map
map = create_map(map_image, dict_map, block_size, WIDTH) #create the map
wall_array = []
for blocks in map:
    if blocks.wall == True:
        wall_array.append(blocks)

wall_group = pygame.sprite.Group(wall_array)
wall_position = []
for walls in wall_array:
    wall_position.append((walls.rect.x, walls.rect.y))

#creating a list of the node(crossings) of the map
node_list = node_position(map_image, (0, 255, 0), block_size, WIDTH)
# End of Game Values


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
        pyman.new_direction = "down"
    if keys_pressed[K_w] or keys_pressed[K_UP]:
        pyman.new_direction = "up"
    if keys_pressed[K_a] or keys_pressed[K_LEFT]:
        pyman.new_direction = "left"
    if keys_pressed[K_d] or keys_pressed[K_RIGHT]:
        pyman.new_direction = "right"

    #allow PyMan to move only if it's on a node or the movement is opposite
    if not pyman.wall_collide():
        if (pyman.touch_node() or
            pyman.direction == "down" and pyman.new_direction == "up" or
            pyman.direction == "up" and pyman.new_direction == "down" or
            pyman.direction == "left" and pyman.new_direction == "right" or
            pyman.direction == "right" and pyman.new_direction == "left"):
            pyman.direction = pyman.new_direction
    else:   #allow PyMan to get out of the wall...
        pyman.direction = pyman.new_direction

    #getting the position that is not touching the wall
    non_touching_position = pyman.position(non_touching_position)
    for ghosts in ghost_group:
        ghosts.refresh_last_node(node_list)
        ghosts.move()

    pyman.move()


    # Display update
    draw_map(map, map_bg, window)
    pyman_group.draw(window)
    ghost_group.draw(window)

    pyman.check_if_dead()
    pyman.life_display()

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
exit(0)
