import pygame
import animation


#from pygame.sprite import _Group





class Entity(animation.AnimateSprite):

    def __init__(self,name,x,y) -> None:
        super().__init__(name)

        self.image = self.get_image(0,0)
        self.image.set_colorkey([0,0,0])  #retire le contour noir du spreet
        self.rect = self.image.get_rect()
        self.position = [x,y]
        

        self.feet = pygame.Rect(0,0, self.rect.width * 0.5, 16)
        self.old_position = self.position.copy()


    def get(self):
        """
        image par défaut
        :return:
        """
        self.image = self.animation["down"]
        self.image.set_colorkey([0, 0, 0])
        return self.image

    def save_location(self): self.old_position = self.position.copy()

    #changement des animations



    #mouvement des entités

    def move_up(self,):
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

    def move_back(self):
        """
        permet de replacer le joueur là où il était avant qu'il entre en collision
        :return: None
        """
        self.position = self.old_position
        self.update()




class Player(Entity):

    def __init__(self):
        super().__init__('Archer',0,0)

        self.heart = 100
        self.shield = 10
        self.hit = 20  #dégat


class NPC(Entity):

    #il faut faire un chemin sur tiled pour que le pnj le suive

    def __init__(self,name, qt_points):
        super().__init__(name,0,0)


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

    def load_point(self,tmx_data):
        """
        récupere les points de passage du pnj
        :return:
        """

        for num in range(1,self.nb_points+1):
            point = tmx_data.get_object_by_name(f"{self.nom}_path{num}")
            rect = pygame.Rect(point.x, point.y,point.width,point.height)
            self.points.append(rect)


