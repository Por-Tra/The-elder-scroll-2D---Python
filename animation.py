#Dirige le système d'animation pour mouvements et attaques
#charge les images des joueurs et autres
#les images sont découpé selon la distance et la position y de la ligne voulu sur le png
#animations mis dans un dictionnaire et prélevé selon le nom

import pygame



class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name):
        """
        constructeur d'animation
        :param name:
        """
        super().__init__()

        self.nom_personnage = name

        self.sprite_sheet = pygame.image.load(f'./assets/character/{name}.png')
        self.animation_index = 0    #affiche l'image 0 donc la première servira pour faire les animations
        self.speed = 2
        self.clock = 0

        self.animation = {
            'down': self.get_images(640, 9, 64, 64, 64),
            'up': self.get_images(512, 9, 64, 64, 64),
            'right': self.get_images(704, 9, 64, 64, 64),
            'left': self.get_images(576, 9, 64, 64, 64),
            'dead': self.get_images(1280, 6, 64, 64, 64)
        }
        self.ajouter_les_attaques_en_fonction_du_personnages_choisi()

    def ajouter_les_attaques_en_fonction_du_personnages_choisi(self):
        """
        Charge les animations d'attaque et les ajoute à self animation car AUCUN n'attaque de la meme façon sur le sprite
        """
        if self.nom_personnage == "Archer":
            self.animation["attaque_down"] = self.get_images(1152, 12, 64, 64, 64)
            self.animation["attaque_left"] = self.get_images(1088, 12, 64, 64, 64)
            self.animation["attaque_up"] = self.get_images(1024, 12, 64, 64, 64)
            self.animation["attaque_right"] = self.get_images(1216, 12, 64, 64, 64)

        elif self.nom_personnage == "Mage":
            self.animation["attaque_down"] = self.get_images_attack(1792, 8, 192, 192, 96) 
            self.animation["attaque_left"] = self.get_images_attack(1600, 8, 192, 128, 96)
            self.animation["attaque_up"] = self.get_images_attack(1408, 8, 192, 128, 96)
            self.animation["attaque_right"] = self.get_images_attack(1984, 8, 192, 128, 96)
            
        #régler ici le problème de décalage
        else:
            self.animation["attaque_down"] = self.get_images_attack(1792, 6, 192, 192, 96)
            self.animation["attaque_left"] = self.get_images_attack(1600, 6, 192, 128, 96)
            self.animation["attaque_up"] = self.get_images_attack(1408, 6, 192, 128, 96)
            self.animation["attaque_right"] = self.get_images_attack(1984, 6, 192, 128, 96)



    def change_animation(self, name):
        """
        change l'animation de l'entité en fonction de son deplacement
        :param name: nom de l'animation
        :return:
        """

        # verifie si le parcour d'image est fini pour le remettre à 0
        if self.animation_index >= len((self.animation[name])) - 1:
            self.animation_index = 0

        self.image = self.animation[name][self.animation_index]

        self.image.set_colorkey((0, 0, 0))
        self.clock += self.speed * 8    #limiteur de vitesse d'animation

        if self.clock >= 100:

            self.animation_index += 1   #passer à l'image d'après

            #verifie si le parcour d'image est fini pour le remettre à 0
            if self.animation_index >= len((self.animation[name]))-1:
                self.animation_index = 0
            self.clock = 0

    def get_images(self, y, distance, taille_image, size_x, size_y):
        """
        parcours l'image qui contient les différents déplacements du joueur et les stock dans un tableau images
        :param y: coordonnées y de l'image
        :param distance: nombres d'images
        :param taille_image:
        :param size_x:
        :param size_y:
        :return: liste d'images
        """

        images = []

        for i in range(0, distance):
            x = i * taille_image
            image = self.get_image(x, y, size_x, size_y)
            images.append(image)

        return images

    def get_image(self, x, y, size_x, size_y):
        """
        prend l'image sur les coordonnées en x et y de l'image (spreet) et la taille        
        :param x: coordonnées x de l'image
        :param y: coordonnées y de l'image
        :param size_x: taille en x
        :param size_y: taille en y
        """
        image = pygame.Surface([size_x, size_y])  #texture du perso
        image.blit(self.sprite_sheet, (0, 0), (x, y, size_x, size_y))
        return image


    def get_image_attack(self, x, y, size_x, size_y):
        """
        prend l'image sur les coordonnées en x et y de l'image (spreet) et la taille pour les animations
        d'attaque
        :param x: coordonnées x de l'image
        :param y: coordonnées y de l'image
        :param size_x: taille en x
        :param size_y: taille en y
        """
        image = pygame.Surface([size_x, size_y])  #texture du perso
        image.blit(self.sprite_sheet, (-64, 0), (x, y, size_x, size_y))
        return image

    def get_images_attack(self, y, distance, taille_image, size_x, size_y):
        """
        parcours l'image qui contient les différents attaques du joueur et les stock dans un tableau images
        :param y: coordonnées y de l'image
        :param distance: nombres d'images
        :param taille_image:
        :param size_x:
        :param size_y:
        :return: liste d'images
        """

        images = []

        for i in range(0, distance):
            x = i * taille_image
            image = self.get_image_attack(x, y, size_x, size_y)
            images.append(image)

        return images
