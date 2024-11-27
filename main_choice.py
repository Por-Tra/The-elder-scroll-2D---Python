#première interface que l'on voit losque le jeu est lancer
#elle permet de choisir un des trois personnages disponible:
#Chevalier, Mage, Archer
#et possède un bouton quitter
#lorsque l'on clic sur le personnage que l'on veut, le jeu se lance directement

from game import *


surfaceW = 1200 #Dimension de la fenêtre / Largeur
surfaceH = 900 #Dimension de la fenêtre / Longueur

pygame.init()
 
class Menu :
    """ Création et gestion des boutons d'un menu """
    def __init__(self, application, *groupes):
        self.couleurs = dict(
            normal=(0, 200, 0),
            survol=(0, 200, 200),
        )
        font = pygame.font.SysFont('Helvetica', 24, bold=True)
        # noms des menus et commandes associées
        items = (
            ('Chevalier', application.chevalier),
            ('Mage', application.mage),
            ('Archer', application.archer),
            ('QUITTER', application.quitter)
        )
        x = 600
        y = 300
        self._boutons = []
        for texte, cmd in items:
            mb = MenuBouton(
                texte,
                self.couleurs['normal'],
                font,
                x,
                y,
                200,
                50,
                cmd
            )
            self._boutons.append(mb)
            y += 120
            for groupe in groupes:
                groupe.add(mb)
 
    def update(self):
        """
        met a jour l'interface
        :return:
        """
        clicGauche, *_ = pygame.mouse.get_pressed()
        posPointeur = pygame.mouse.get_pos()
        for bouton in self._boutons:
            # Si le pointeur souris est au-dessus d'un bouton
            if bouton.rect.collidepoint(*posPointeur):
                # Changement du curseur par un quelconque
                pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                # Changement de la couleur du bouton
                bouton.dessiner(self.couleurs['survol'])
                # Si le clic gauche a été pressé
                if clicGauche:
                    # Appel de la fonction du bouton
                    bouton.executerCommande()
                break
            else :
                # Le pointeur n'est pas au-dessus du bouton
                bouton.dessiner(self.couleurs['normal'])
        else :
            # Le pointeur n'est pas au-dessus d'un des boutons
            # initialisation au pointeur par défaut
            pygame.mouse.set_cursor(*pygame.cursors.arrow)


class MenuBouton(pygame.sprite.Sprite):
    """ Création d'un simple bouton rectangulaire """
    def __init__(self, texte, couleur, font, x, y, largeur, hauteur, commande) :
        super().__init__()
        self._commande = commande
 
        self.image = pygame.Surface((largeur, hauteur))
 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
 
        self.texte = font.render(texte, True, (0, 0, 0))
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (largeur/2, hauteur/2)
 
        self.dessiner(couleur)
 
    def dessiner(self, couleur):
        """
        déssine les boutons
        :param couleur: tuple
        :return:
        """
        self.image.fill(couleur)
        self.image.blit(self.texte, self.rectTexte)
 
    def executerCommande(self):
        """Appel de la commande du bouton"""
        self._commande()

class Application :
    """ Classe maîtresse gérant les différentes interfaces du jeu """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("The Elder Scroll 2D")
 
        self.fond = (150,)*3
 
        self.fenetre = pygame.display.set_mode((surfaceW,surfaceH))
        # Groupe de sprites utilisé pour l'affichage
        self.groupeGlobal = pygame.sprite.Group()
        self.statut = True
 
    def initialiser(self):
        """"""
        try:
            # Suppression de tous les sprites du groupe
            self.groupeGlobal.empty()
        except AttributeError:
            pass
 
    def menu(self):
        """Affichage du menu"""
        self.initialiser()
        self.ecran = Menu(self, self.groupeGlobal)

    #quitte le jeu
    def quitter(self): self.statut = False

    def chevalier(self):
        """permet de choisir le personnage Chevalier"""
        self.lancement("Chevalier")
    def mage(self):
        """permet de choisir le personnage Mage"""
        self.lancement("Mage")
        
    def archer(self):
        """permet de choisir le personnage Archer"""
        self.lancement("Archer")

    def lancement(self, name):
        """
        lance le jeu
        """
        game = Game(name)
        game.run()

    def update(self):
        """mise à jour"""
        events = pygame.event.get()
 
        for event in events:
            if event.type == pygame.QUIT:
                self.quitter()
                
 
        self.fenetre.fill(self.fond)
        self.ecran.update()
        self.groupeGlobal.update()
        self.groupeGlobal.draw(self.fenetre)
        pygame.display.update()
