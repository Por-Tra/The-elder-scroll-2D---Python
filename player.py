import pygame

#from pygame.sprite import _Group


global choix_personnage


class Entity(pygame.sprite.Sprite):

    def __init__(self,name,x,y) -> None:
        super().__init__()
        self.sprite_sheet = pygame.image.load(f'./assets/character/{name}.png')
        self.image = self.get_image(0,0)
        self.image.set_colorkey([0,0,0])  #retire le contour noir du spreet
        self.rect = self.image.get_rect()
        self.position = [x,y]
        
        self.animation = {
            'down': self.get_image(0,640),
            'up':self.get_image(0,768),
            'right':self.get_image(0,704),
            'left':self.get_image(0,576)
        }
        self.feet = pygame.Rect(0,0, self.rect.width * 0.5, 16)
        self.old_position = self.position.copy()
        self.speed = 2

    def get(self):
        self.image = self.animation["down"]
        self.image.set_colorkey([0, 0, 0])
        return self.image

    def save_location(self): self.old_position = self.position.copy()


    #méthode de déplacement
    def move_player(self, type):
        self.image = self.animation[type]
        self.image.set_colorkey([0, 0, 0])
        if type == "up":
            self.position[1] -= self.speed
        elif type == "down":
            self.position[1] += self.speed
        elif type == "right":
            self.position[0] += self.speed
        elif type == "left":
            self.position[0] -= self.speed

    def update(self):
        """

        :return:
        """
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        """
        permet de replacer le joueur là où il était avant qu'il entre en collision
        :return: None
        """
        self.position = self.old_position
        self.update()

    def get_image(self,x,y):
        """donne les coordonnée en x et y de l'image(spreet)

        Args:
            x (int): coordoné x
            y (int): coordoné y
        """
        image = pygame.Surface([64,64])  #texture du perso
        image.blit(self.sprite_sheet, (0,0),(x, y, 64, 64) )
        return image


class Player(Entity):

    def __init__(self):
        super().__init__('Archer',0,0)

class NPC(Entity):

    #il faut faire un chemin sur tiled pour que le pnj le suive

    def __init__(self,name):
        super().__init__(name,0,0)
