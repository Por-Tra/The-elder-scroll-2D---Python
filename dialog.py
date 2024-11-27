import pygame

class DialogBox:

    # position du rectangle
    X_POSITION = 300
    Y_POSITION = 700

    def __init__(self):
        self.box = pygame.image.load('./dialogues/dialogue_box.png') #load l'image de la boite de dialogue
        self.box = pygame.transform.scale(self.box, (700, 150)) # taille du rectangle de tchat
        self.texts = [] # liste des différentes phrases des pnjs
        self.text_index = 0 # indice de la phrase dans le tableau
        self.letter_index = 0 # indice des lettres dans les phrases
        self.font = pygame.font.Font("./dialogues/dialog_font.ttf", 15) # police des caractères
        self.reading = False

    def execute(self, dialogo=[]):
        """
        Vérifie si on est en train de lire, si oui on passe au prochain texte si il existe
        Sinon on lance la boite de dialogue
        :param dialogo:
        :return:
        """
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialogo

    def render(self, screen):
        """
        Affiche le texte lettre par lettre dans la boite de dialogue
        :param screen:
        :return:
        """
        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index

            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION)) # Position de la boite de dialogue sur l'écran
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (200, 20, 20)) #couleur du texte, là c'est rouge
            screen.blit(text, (self.X_POSITION + 40, self.Y_POSITION + 60)) # position du texte sur l'ecran

    def next_text(self):
        """
        Passe d'une phrase à un autre si c'est possible
        :return:
        """
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            # Si on a tout lu, on ferme le dialogue
            self.reading = False
