#Construit les entités nécessaires au jeu
#donc joueur, NPC et monstres
#et ainsi crée leur attribut comme les méthodes pour suivre le joueur, attaquer, etc

import pygame
import animation



class Entity(animation.AnimateSprite):
    """
    constructeur d'entité
    """

    def __init__(self, name, x, y) -> None:
        super().__init__(name)

        self.image = self.get_image(0, 640, 64, 64)  # image par défaut
        self.image.set_colorkey([0, 0, 0])  #retire le contour noir du spreet

        self.position = [x, y]
        self.old_position = self.position.copy()

        self.rect = self.image.get_rect()  # box d'attaque où l'entité peut se faire attaquer
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 16)
        self.vision = pygame.Rect(0, 0, 300, 300)
        self.limit_box_follow = pygame.Rect(0, 0, 32, 32)  #box à porté du joueur


        if name == 'Archer':
            self.attaque_rect = pygame.Rect(0, 0, 1000, 1000)
        elif name == 'Mage':
            self.attaque_rect = pygame.Rect(0, 0, 600, 600)
        else:
            self.attaque_rect = self.image.get_rect()


    def save_location(self): self.old_position = self.position.copy()

    #mouvement des entités
    def move_up(self):
        self.change_animation('up')
        self.position[1] -= self.speed
    def move_down(self):
        self.change_animation('down')
        self.position[1] += self.speed
    def move_right(self):
        self.change_animation('right')
        self.position[0] += self.speed
    def move_left(self):
        self.change_animation('left')
        self.position[0] -= self.speed

    def update(self):
        """
        met à jour les positions et rectangle(hitbox)
        :return:
        """
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.vision.midbottom = self.rect.midbottom
        self.limit_box_follow.topleft = self.position
        self.attaque_rect.midbottom = self.rect.midbottom

    def move_back(self):
        """
        permet de replacer le joueur là où il était avant qu'il entre en collision
        :return: None
        """
        self.position = self.old_position
        self.update()

class Player(Entity):
    """
    constructeur du joueur
    """

    def __init__(self, personnage_choisi):
        super().__init__(personnage_choisi, 0, 0)

        self.personnage = personnage_choisi
        self.max_heart = 600
        self.heart = self.max_heart
        self.hit = 0.4  #dégat du joueur s'adapte au boucle + par défaut pour le mage

        if self.personnage == 'Archer':
            self.hit = 0.20
        elif self.personnage == 'Chevalier':
            self.hit = 0.60

    def attacks_from_player(self):
        """
        detect si le joueur attaque
        :return: True
        sinon None
        """
        pressed = pygame.key.get_pressed()
        return any([
            pressed[pygame.K_UP],
            pressed[pygame.K_DOWN],
            pressed[pygame.K_RIGHT],
            pressed[pygame.K_LEFT]
        ])

    def verif_si_mort(self):
        """
        verifie si le joueur est mort ou pas
        :return: (bool) True sinon rien
        """
        if self.heart < 1:
            self.speed = 0
            self.change_animation('dead')

    #attaque du joueur
    def attaque_left(self):
        self.change_animation('attaque_left')
    def attaque_right(self):
        self.change_animation('attaque_right')
    def attaque_up(self):
        self.change_animation('attaque_up')
    def attaque_down(self):
        self.change_animation('attaque_down')



class Monster(Entity):
    """
    constructeur de monstre
    """

    def __init__(self, name, spawn, vie):
        super().__init__(name, 0, 0)

        self.speed = 1
        self.hit = 0.1

        self.name_point = spawn
        self.spawn_point = []
        self.current_point = 0
        self.max_heart = vie
        self.heart = self.max_heart

        self.follow = True

    def verif_si_mort(self):
        """
        verifie si le joueur est mort ou pas
        :return: (bool) True sinon rien
        """
        if self.heart < 1:
            self.follow = False
            self.speed = 0
            self.change_animation('dead')

    def mob_spawn(self):
        """
        permet de téléporter le monstre à son spawn
        :return:
        """

        localisation = self.spawn_point[self.current_point]
        self.position[0] = localisation.x
        self.position[1] = localisation.y
        self.save_location()  # validé la téléportation


    def load_mob_spawn(self, tmx_data):
        """
        charge le point de spawn du monstre
        :param tmx_data:
        :return:
        """

        point = tmx_data.get_object_by_name(f"{self.name_point}")
        rect = pygame.Rect(point.x, point.y, point.width, point.height)
        self.spawn_point.append(rect)


    def following(self, player):
        """
        le monstre pourchasse le joueur
        déplacement + animation de déplacement
        :return:
        """

        if self.follow:    #pour eviter les problèmes de speed

            self.speed = 1
            pos_player_x, pos_player_y = player.position[0], player.position[1]
            pos_mob_x, pos_mob_y = self.position[0], self.position[1]

            pos_x = pos_player_x - pos_mob_x
            pos_y = pos_player_y - pos_mob_y

            if abs(pos_x) > abs(pos_y):
                if pos_x > 0:
                    self.move_right()
                else:
                    self.move_left()

            elif abs(pos_x) < abs(pos_y):
                if pos_y > 0:
                    self.move_down()
                else:
                    self.move_up()

    def attaque_player(self, player):
        """
        verifié si le joueur se trove en haut, bas, gauche, droite
        pour changer l'animation d'attaque
        :param player:
        :return:
        """


        pos_player_x, pos_player_y = player.position[0], player.position[1]
        pos_mob_x, pos_mob_y = self.position[0], self.position[1]

        pos_x = pos_player_x - pos_mob_x
        pos_y = pos_player_y - pos_mob_y

        if abs(pos_x) > abs(pos_y):
            if pos_x > 0:
                self.change_animation('attaque_right')
            else:
                self.change_animation('attaque_left')

        elif abs(pos_x) < abs(pos_y):
            if pos_y > 0:
                self.change_animation('attaque_down')
            else:
                self.change_animation('attaque_up')


class NPC(Entity):

    """
    constructeur de NPC
    """

    def __init__(self, name, qt_points, dialogo=None):
        super().__init__(name, 0, 0)
        self.dialog = dialogo if dialogo is not None else []
        self.speed = 1
        self.nb_points = qt_points
        self.points = []
        self.nom = name
        self.current_point = 0   #=premier points de la liste de points

    def move(self):
        """
        permet au npc d'aller d'un point A à un point B
        :return:
        """
        current_point = self.current_point      #point A
        target_point = self.current_point + 1   #point B

        #verifie si le tour a été fait par le npc
        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]   #aller point A
        target_rect = self.points[target_point]     #aller point B

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 1:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 1:
            self.move_up()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 1:
            self.move_right()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 1:
            self.move_left()


        #on change de nouveau points
        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def teleport_point(self):
        """
        définit le point de spawn du NPC
        :return:
        """

        localisation = self.points[self.current_point]
        self.position[0] = localisation.x
        self.position[1] = localisation.y
        self.save_location()   #validé la téléportation

    def load_point(self, tmx_data):
        """
        récupere les points de passage du pnj
        :return:
        """

        for num in range(1, self.nb_points+1):
            point = tmx_data.get_object_by_name(f"{self.nom}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
