#Programme principale du projet
#lorsque exécuter, le jeu se lancez

#plus info avec help_game()  avec la commande dans le shell>>> help(help_game)

from main_choice import *

app = Application()
app.menu()
 
clock = pygame.time.Clock()

while app.statut:
    app.update()


pygame.quit()