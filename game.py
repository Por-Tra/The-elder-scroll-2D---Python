import pygame
import pytmx
import pyscroll
from player import Player
from Map import *



class Game:

    def __init__(self) -> None:
        """création de la fenètre de jeu
        """

        self.running = True


        #créer la fenetre
        self.screen = pygame.display.set_mode((1200,900))
        pygame.display.set_caption("The Elder Scroll 2D")

        #générer un joueur et la map
        self.player = Player() # mise en place du joueur sur la map à partir de son spawn
        self.map_manager = MapManager(self.screen,self.player)



            

    def handle_input(self):

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            self.running = False

        if pressed[pygame.K_UP]:
            self.player.move_player("up")

        elif pressed[pygame.K_DOWN]:
            self.player.move_player("down")

        elif pressed[pygame.K_LEFT]:
            self.player.move_player("left")

        elif pressed[pygame.K_RIGHT]:
            self.player.move_player("right")


    def update(self):
        """
        met à jour la map
        :return:
        """
        self.map_manager.update()

    def run(self):
        """pour garder la fenetre ouverte ou la fermé
           exécuter le code du jeu
        """

        clock = pygame.time.Clock()

        while self.running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            pygame.display.flip()

            for eve in pygame.event.get():
                if eve.type == pygame.QUIT:
                    self.running = False

            clock.tick(60)  #les fps

        pygame.quit()
