from dataclasses import dataclass
import pygame
import pytmx
import pyscroll


@dataclass    #équivalent du __init__
class Map:

    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap

class MapManager:

    def __int__(self,ecran,joueur):
        self.maps = dict()   #'house' -> Map("house, walls,group)
        self.screen = ecran
        self.player = joueur
        self.current_map = 'map'    #carte de début

        self.register_map("map")
        self.register_map("cave")

        self.teleport_player('spawn')

    def check_collisions(self):
        for sprite in self.get_group().sprites():
            if sprite.feeet.collidelist(self.get_walls()) > -1:
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
        self.player.save_location() #pour éviter les bug de téléportation avec les collisions


    def register_map(self,name):
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
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        group.add(self.player)

        #cree objet map
        self.maps[name] = Map(name,walls,group,tmx_data)

    #récupérer la map
    def get_map(self):return self.maps[self.current_map]

    #récupérer le group
    def get_group(self): return self.get_map().group

    #récuperer les murs
    def get_walls(self): return self.get_map().walls

    #récuperer les coordonné du spawn du joueur
    def get_object(self,name): return self.get_map().tmx_data.get_object_by_name(name)

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
