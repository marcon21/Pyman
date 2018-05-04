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


def djikstra(start_node, destination_node, node_position_list, visited_node):
    """Algorithm that find the shortest path from the starting node to the
    destination node passing throug a node map, given each of the node position
    """
    ghost = True
    nearest_node = None
    distance = None
    while nearest_node != destination_node:
        print(start_node, node_position_list)
        if not ghost:
            node_position_list.remove(start_node)
        ghost = False
        adjacent_nodes = []

        # questa funzione passa attraverso i muri, ERRORE!!!!
        for node in node_position_list:
            if node[0] == start_node[0] or node[1] == start_node[1]:
                adjacent_nodes.append(node)

        for node in adjacent_nodes:
            new_distance = math.sqrt(
                (start_node[0] - node[0]) ** 2 +
                (start_node[1] - node[1]) ** 2
            ) + math.sqrt(
                (destination_node[0] - node[0]) ** 2 +
                (destination_node[1] - node[1]) ** 2
            )
            if distance != None:
                if distance > new_distance:
                    distance, nearest_node = new_distance, node
            else:
                distance, nearest_node = new_distance, node

        visited_node.append(nearest_node)
        start_node = nearest_node


    return visited_node

if __name__ == "__main__":
    lista = node_position("./image/node_map.png", (0, 255, 0), 32, 896)
    print(djikstra((32, 192), (32, 32), lista, []))
