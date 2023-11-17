import pygame
import pytmx
import pyscroll
from player import *

class Game:

    def __init__(self) -> None:
        """création de la fenètre de jeu
        """
        #créer la fenetre
        self.screen = pygame.display.set_mode((1200,900))
        pygame.display.set_caption("The Elder Scroll 2D")

        #charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        map_layer.zoom = 2

        #générer un joueur
        player_position = tmx_data.get_object_by_name("spawn")  # récupération de l'objet qui est dans la map qui défini le spawn
        self.player = Player(player_position.x, player_position.y) # mise en place du joueur sur la map

        #définir liste qui stock tout les rectangles de collisions

        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)


            

    def handle_input(self):

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation("up")
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation("down")
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation("left")
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation("right")

    def run(self):
        """pour garder la fenetre ouverte ou la fermé
           exécuter le code du jeu
        """

        clock = pygame.time.Clock()

        run = True
        
        while run:

            self.handle_input()
            self.group.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)  #dessiner les calques sur l'écran
            pygame.display.flip()

            for eve in pygame.event.get():
                if eve.type == pygame.QUIT:
                    run = False

            clock.tick(60)  #les fps

        pygame.quit()
