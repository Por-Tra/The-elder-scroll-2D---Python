from dataclasses import dataclass
import pygame
import pytmx
import pyscroll


@dataclass    #équivalent du __init__
class Map:

    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup

class MapManager:

    def __int__(self):
        self.maps = dict()   #'house' -> Map("house, walls,group)
        self.current_map = 'map'    #carte de début

    def register_map(self,name):
