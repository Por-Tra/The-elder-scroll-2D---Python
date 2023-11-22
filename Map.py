from dataclasses import dataclass
import pygame
import pytmx
import pyscroll

from player import *



@dataclass
class Portal:

    from_world: str  #quel monde
    origin_point: str    #sur quel point
    target_world: str    #sur quel monde
    teleport_point: str   #point de téléporation



@dataclass    #équivalent du __init__
class Map:

    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npc: list[NPC]

class MapManager:

    def __init__(self, ecran, joueur):
        self.maps = dict()              #'house' -> Map("house, walls,group)
        self.screen = ecran
        self.player = joueur
        self.current_map = 'map'        #carte de début


    #chargement des maps et NPC
        #pour aller dans la grotte
        self.register_map("map" , portals=[
            Portal(from_world='map' , origin_point='enter_cave',target_world='cave',teleport_point='spawn_cave')
        ],npcs=[
            NPC("pnj_1",qt_points=4 )
        ])

        #pour aller sur la première map
        self.register_map("cave", portals=[
            Portal(from_world='cave',origin_point='exit_cave',target_world='map',teleport_point='exit_cave_spawn')
        ])

        self.teleport_player('spawn')
        self.teleport_NPC()

    def check_collisions(self):
        

        #portail
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x,point.y,point.width,point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        #collision
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self,name_point):
        """
        place le joueur à son spawn
        :param name_point:
        :return:
        """
        point = self.get_object(name_point)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()      #pour éviter les bug de téléportation avec les collisions


    def register_map(self,name,portals=[], npcs=[]):
        """
        enregistrer les maps
        :param name:
        :return:
        """
        tmx_data = pytmx.util_pygame.load_pygame(f"./assets/map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Les collisions
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner les différents calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        group.add(self.player)

        #récupérer les npcs et les ajouters au groupe
        for npc in npcs:
            group.add(npc)

        #cree objet map
        self.maps[name] = Map(name,walls,group,tmx_data, portals, npcs)

    #récupérer la map
    def get_map(self):return self.maps[self.current_map]

    #récupérer le group
    def get_group(self): return self.get_map().group

    #récuperer les murs
    def get_walls(self): return self.get_map().walls

    #récuperer les coordonné du spawn du joueur
    def get_object(self,name): return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_NPC(self):
        """
        teleporte le NPC dans son spawn
        :return:
        """

        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npc

            for npc in npcs:
                npc.load_point(self)
                npc.teleport_point()


    def draw(self):
        """
        déssiner la carte
        :return:
        """
        self.get_group().draw(self.screen)  #déssiner le calque
        self.get_group().center(self.player.rect.center)  #centré caméra

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npc:
            npc.move()
