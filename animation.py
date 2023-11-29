import pygame


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self,name):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f'./assets/character/{name}.png')
        self.animation_index = 0    #affiche l'image 0 donc la première servira pour faire les animations
        self.speed = 2
        self.clock = 0


        self.animation = {
            'down': self.get_images(640),
            'up': self.get_images(512),
            'right': self.get_images(704),
            'left': self.get_images(576)
        }

    def change_animation(self,name):
        """
        change l'animation de l'entité en fonction de son deplacement
        :param name:
        :return:
        """
        self.image = self.animation[name][self.animation_index]    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!bug ici
        self.image.set_colorkey(0,0)
        self.clock += self.speed * 8    #limiteur de vitesse d'animation

        if self.clock >= 100:

            self.animation_index += 1   #passer à l'image d'après

            #verifi si le parcour d'image est fini pour le remettre à 0

            if self.animation_index >= len((self.animation[name])):
                self.animation_index = 0

            self.clock = 0

    def get_images(self, y):
        """
        parcours l'image qui contient les différent déplacement du joueur et les stock dans un tableau images
        :param y: valeur y de l'image
        :return:(list) les images pour faire une animation
        """

        images = []

        for i in range(0,9):
            x = i*64
            image = self.get_image(x,y)
            images.append(image)

        return images

    def get_image(self,x,y):
        """donne les coordonnée en x et y de l'image(spreet)

        Args:
            x (int): coordoné x
            y (int): coordoné y
        """
        image = pygame.Surface([64,64])  #texture du perso
        image.blit(self.sprite_sheet, (0,0),(x, y, 64, 64) )
        return image