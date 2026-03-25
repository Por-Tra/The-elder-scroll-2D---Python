#Gestionnaires de maps
#il charge les maps et les objets qui se trouvent à l'intérieur et place les joueur et autre entités
#gère aussi les collisions du joueur et autres entités

from dataclasses import dataclass

import pygame
import pygame.font
import pytmx
import pyscroll
from player import *
from dialog import *

@dataclass
class Portal:
    """
    Constructeur de portails pour aller vers d'autres map.
    """

    from_world: str      #quel monde
    origin_point: str    #sur quel point
    target_world: str    #sur quel monde
    teleport_point: str  #point de téléporation

@dataclass    #équivalent du __init__
class Map:
    """
    Constructeur de map qui permet de réunir les murs et autres.
    """

    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npc: list[NPC]
    monster: list[Monster]

class MapManager:
    """
    Constructeur des maps
    Génère, déssine et charge les maps ainsi que ce qu'il y a dedans.
    """

    def __init__(self, ecran, joueur):
        self.maps = dict()
        self.screen = ecran
        self.player = joueur
        self.current_map = 'map'        #carte par défaut


    #chargement des maps et NPC

        # go map
        self.register_map("map", portals=[
            Portal(from_world='map', origin_point='enter_cave', target_world='catacombes_map', teleport_point='spawn_cave')
        ], npcs=[
            NPC("pnj_1", qt_points=26, dialogo=['Salutation Voyageur !',
                                               'Vous êtes ici dans un village perdu.',
                                               "ICI la zone est dangereuse.",
                                               "Pourquoi ? C'est simple !",
                                               "Un grand tourment s'est abattu sur nous ...",
                                               'Le Seigneur des monstres est revenu du royaume des morts ...',
                                               'Cher voyageur, je vous demande de nous libérer de ce mal !',
                                               'En passant par la grotte au Nord-Est vous trouverez la crypte.',
                                               'En espérant vous revoir bientôt !']),
            NPC("pnj_2", qt_points=9, dialogo=['Bien le bonjour aventurier !',
                                               'Vas voir le gars qui se balade dans le village.',
                                               'Il va t expliquer pourquoi tu es ici.']),
            NPC("pnj_3", qt_points=1, dialogo=["T'es qui ?",
                                               "Part !!",
                                               'Tu fais quoi devant ma maison ?',
                                               "Si tu veux faire quelque chose, demande au type qui se balade",
                                               'Moi viens pas me déranger.']),
            NPC("pnj_4", qt_points=2, dialogo=['COUCOU !',
                                               "Je suis juste un simple pnj mal fait.",
                                               "Tu peux faire le tour du village si tu veux"])
        ])

        #go catacombes
        self.register_map("catacombes_map", portals=[
            Portal(from_world='catacombes_map', origin_point='exit_cave', target_world='map', teleport_point='exit_cave_spawn'),
            Portal(from_world='catacombes_map', origin_point='go_dungeon', target_world='Dungeon_map', teleport_point='enter_dungeon')
        ], npcs=[
            NPC('pnj_5', qt_points=1, dialogo=['Ah bien le bonjour aventurier !',
                                     'Vous ferez attention, il y a beacoup de monstres ici.',
                                     'Mais vous devez surement être fort.',
                                     'Donc ça ne devrait pas être difficile pour vous.',
                                     'PS: la sortie se trouve en bas à gauche ',
                                     'Bonne chance !'])
        ], monster=[
            Monster('bonome', spawn='spawn_mob_1', vie=75),
            Monster('sklt', spawn='spawn_mob_2', vie=50),
            Monster('cyclope', spawn='spawn_mob_3', vie=100),
            Monster('cyclope', spawn='spawn_mob_4', vie=100),
            Monster('bonome', spawn='spawn_mob_5', vie=75),
            Monster('sklt', spawn='spawn_mob_6', vie=50),
            Monster('sklt', spawn='spawn_mob_7', vie=50),
            Monster('sklt', spawn='spawn_mob_8', vie=50),
        ])

        #go dungeon
        self.register_map('Dungeon_map', portals=[
            Portal(from_world='Dungeon_map', origin_point='exit_D', target_world='catacombes_map', teleport_point='exit_dungeon'),
            Portal(from_world='Dungeon_map', origin_point='go_world', target_world='map', teleport_point='spawn')
        ], monster=[
            Monster('vampire', spawn='spawn_mob_1', vie=100),
            Monster('vampire', spawn='spawn_mob_2', vie=100),
            Monster('vampire', spawn='spawn_mob_3', vie=100),
            Monster('vampire', spawn='spawn_mob_4', vie=100),
            Monster('vampire', spawn='spawn_mob_5', vie=100),
            Monster('vampire', spawn='spawn_mob_6', vie=100),
            Monster('sklt', spawn='spawn_mob_7', vie=50),
            Monster('sklt', spawn='spawn_mob_8', vie=50),
            Monster('sklt', spawn='spawn_mob_9', vie=50),
            Monster('sklt', spawn='spawn_mob_10', vie=50),
            Monster('vampire', spawn='spawn_mob_11', vie=100),
            Monster('vampire', spawn='spawn_mob_12', vie=100),
            Monster('boss', spawn='Boss', vie=700)
        ])

        self.teleport_player('spawn')
        self.teleport_NPC()
        self.teleport_monster()

    

    def check_npc_collisions(self, dialog_box):
        """

        """
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite.dialog)

    def check_collisions(self):
        """
        regarde si le joueur entre en contact avec un rectangle spécifique et fait donc une action avec
        :return:
        """

        #portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        #collision avec joueur des pnj
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 2


            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

        # collision avec joueur des monstres

        for mob in self.get_group().sprites():

            if type(mob) is Monster:

                # si il est dans le champ de vision du mob
                if mob.vision.colliderect(self.player.rect):

                    # attaques du monstre
                    if mob.limit_box_follow.colliderect(self.player.rect) and mob.heart > 0:  # si à la porté du joueur et en vie
                        mob.attaque_player(self.player)  #animation
                        self.player.heart -= mob.hit

                    else:  # à la porté de la vision
                        mob.following(self.player)
                else:  # hors porté
                    mob.speed = 0  # bouge plus

                # attaques du joueur
                if mob.rect.colliderect(self.player.attaque_rect) and self.player.attacks_from_player():
                    mob.heart -= self.player.hit



                # collision du monstre avec un mur
                if mob.feet.collidelist(self.get_walls()) > -1:
                    mob.move_back()

    def teleport_player(self, name_point):
        """
        place le joueur à son spawn
        :param name_point:
        :return:
        """
        point = self.get_object(name_point)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()      #pour éviter les bugs de téléportation avec les collisions

    def teleport_monster(self):
        """
        Téléporte le monstre dans son spawn
        :return:
        """

        for map in self.maps:
            map_data = self.maps[map]
            monsters = map_data.monster

            for mob in monsters:
                mob.load_mob_spawn(map_data.tmx_data)
                mob.mob_spawn()

    def register_map(self, name, portals=None, npcs=None, monster=None):
        """
        enregistrer les maps et tout ce qu'il y a dedans
        :param name:
        :return:
        """
        if portals is None:
            portals = []
        if npcs is None:
            npcs = []
        if monster is None:
            monster = []

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

        # récupère les entité et les ajoute au groupe
        group.add(self.player)

        for npc in npcs:
            group.add(npc)

        for mob in monster:
            group.add(mob)

        #cree objet map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs, monster)

    #récupérer la map
    def get_map(self): return self.maps[self.current_map]

    #récupérer le group
    def get_group(self): return self.get_map().group

    #récuperer les murs
    def get_walls(self): return self.get_map().walls

    #récuperer les coordonnées du spawn du joueur
    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_NPC(self):
        """
        teleporte le NPC dans son spawn
        :return:
        """

        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npc

            for npc in npcs:
                npc.load_point(map_data.tmx_data)
                npc.teleport_point()

    def draw(self):
        """
        déssiner la carte et vie
        :return:
        """
        self.get_group().draw(self.screen)  #dessiner le calque
        self.get_group().center(self.player.rect.center)  #centrer la caméra
        self.draw_player_health_bar()
        self.draw_monsters_health_bars()

    def world_to_screen(self, world_x, world_y):
        """
        Convertit une position monde (x, y) en position écran selon la caméra centrée sur le joueur.
        """
        screen_width, screen_height = self.screen.get_size()
        screen_x = world_x - self.player.rect.centerx + (screen_width // 2)
        screen_y = world_y - self.player.rect.centery + (screen_height // 2)
        return screen_x, screen_y

    def draw_health_bar(self, x, y, width, height, current_health, max_health):
        """
        Dessine une barre de vie simple avec fond, contour et remplissage.
        """
        if max_health <= 0:
            return

        clamped_health = max(0, min(current_health, max_health))
        ratio = clamped_health / max_health

        bg_rect = pygame.Rect(x, y, width, height)
        fill_rect = pygame.Rect(x, y, int(width * ratio), height)

        pygame.draw.rect(self.screen, (60, 60, 60), bg_rect)
        pygame.draw.rect(self.screen, (220, 40, 40), fill_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, 2)

    def draw_player_health_bar(self):
        """
        Barre de vie du joueur affichée en HUD (fixe à l'écran).
        """
        self.draw_health_bar(20, 20, 250, 22, self.player.heart, self.player.max_heart)

    def draw_monsters_health_bars(self):
        """
        Barres de vie des monstres affichées juste au-dessus du sprite,
        avec un calcul basé sur les pieds (mob.feet).
        """
        for mob in self.get_map().monster:
            if mob.heart <= 0:
                continue

            feet_world_x = mob.feet.centerx
            feet_world_y = mob.feet.midbottom[1]
            sprite_top_world_y = feet_world_y - mob.rect.height

            screen_x, sprite_top_screen_y = self.world_to_screen(feet_world_x, sprite_top_world_y)
            bar_width = max(30, mob.rect.width)
            bar_height = 8
            bar_x = screen_x - (bar_width // 2)
            bar_y = sprite_top_screen_y - 10

            self.draw_health_bar(bar_x, bar_y, bar_width, bar_height, mob.heart, mob.max_heart)

    def update(self):
        """
        met à jour les méthodes
        :return:
        """
        self.get_group().update()
        self.check_collisions()

        self.player.verif_si_mort()

        #mouvement des npc par rapport à leur point de déplacement
        for npc in self.get_map().npc:
            npc.move()

        #verifie si l'entité ennemis est morte
        for mob in self.get_map().monster:
            mob.verif_si_mort()
