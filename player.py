import pygame

#from pygame.sprite import _Group



class Player(pygame.sprite.Sprite):

    def __init__(self,x,y) -> None:
        super().__init__()
        self.sprite_sheet = pygame.image.load('chevalier_spreet_32x32.png')
        self.image = self.get_image(0,0)
        self.image.set_colorkey([0,0,0])  #retire le contour noir du spreet
        self.rect = self.image.get_rect()
        self.position = [x,y]
        self.speed = 3
        
        self.animation = {
            'down': self.get_image(0,640), #704
            'up':self.get_image(0,768), #576
            'right':self.get_image(0,704), #768
            'left':self.get_image(0,576) #640
        }

    def change_animation(self,name):
        self.image = self.animation[name]
        self.image.set_colorkey([0,0,0])

    #méthode de déplacement
    def move_right(self): self.position[0] += self.speed  #on ajoute une vitesse

    def move_left(self): self.position[0] -= self.speed  #on ajoute une vitesse

    def move_up(self): self.position[1] -= self.speed  #on ajoute une vitesse

    def move_down(self): self.position[1] += self.speed  #on ajoute une vitesse

    def update(self) :
        self.rect.topleft = self.position

    

    def get_image(self,x,y):
        """donne les coordonnée en x et y de l'image(spreet)

        Args:
            x (int): coordoné x
            y (int): coordoné y
        """
        image = pygame.Surface([64,64])  #texture du perso
        image.blit(self.sprite_sheet, (0,0),(x, y, 64, 64) )
        return image

