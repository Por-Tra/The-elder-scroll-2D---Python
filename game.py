#permet au jeu de se lancer
#il construit le joueur, les maps et les mets à jours 60 fois par seconde
#il gère les interaction de l'utilisateur (déplacement,attaque...)
import pygame.key
from Map import *
from dialog import *


class Game:
    """
    constructeur du jeu
    lance le jeu et crée les entrées claviers pour jouer
    """

    def __init__(self, nom_personnage) -> None:
        """création de la fenètre de jeu
        """

        self.running = True

        self.choix_du_perso = nom_personnage

        #créer la fenetre
        self.screen = pygame.display.set_mode((1200, 900))


        #générer un joueur et la map et les dialogues
        self.player = Player(self.choix_du_perso)# mise en place du joueur sur la map à partir de son spawn
        self.map_manager = MapManager(self.screen, self.player)
        self.dialogue_box = DialogBox()


    def handle_input(self):
        """
        déplacements du joueur et autre
        :return:
        """

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_z]:
            self.player.move_up()
        elif pressed[pygame.K_s]:
            self.player.move_down()
        elif pressed[pygame.K_q]:
            self.player.move_left()
        elif pressed[pygame.K_d]:
            self.player.move_right()
        elif pressed[pygame.K_r]:     #courrir
            self.player.speed = 3
        elif pressed[pygame.K_w]:     #marcher
            self.player.speed = 2
        elif pressed[pygame.K_UP]:
            self.player.attaque_up()
        elif pressed[pygame.K_DOWN]:
            self.player.attaque_down()
        elif pressed[pygame.K_RIGHT]:
            self.player.attaque_right()
        elif pressed[pygame.K_LEFT]:
            self.player.attaque_left()

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

        clock = pygame.time.Clock() # pour éviter de créé plusieurs fois Clock

        while self.running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialogue_box.render(self.screen)
            pygame.display.flip()


            for eve in pygame.event.get():
                if eve.type == pygame.QUIT:
                    self.running = False

                elif eve.type == pygame.KEYDOWN:
                    if eve.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collisions(self.dialogue_box)

            clock.tick(60)  #les fps

        pygame.quit()
