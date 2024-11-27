#pas obligé d'être imprimée

def help_game():

    """
    modules externe utilisé:

            dataclasses:
                module qui simplifie la création de classes de données en réduisant
                la quantité de code que vous devez écrire, tout en fournissant des fonctionnalités
                utiles pour la manipulation des données. C'est particulièrement utile lorsque vous
                travaillez avec des classes dont le but principal est de stocker des données.
            pytmx:
                bibliothèque qui facilite l'intégration des cartes créées avec Tiled dans des projets
                de jeux en fournissant des outils pour analyser et utiliser les informations contenues
                dans les fichiers TMX. Cela permet aux développeurs de jeux de gérer plus facilement
                les aspects visuels et interactifs de leurs cartes.
            pyscroll:
                module qui simplifie le processus de gestion et d'affichage
                des cartes dans les jeux Pygame, fournissant ainsi une solution plus
                efficace et moins sujette aux erreurs pour la mise en œuvre du défilement de cartes.


    ----------------------------------------------------------------------------------------------------

    ----------------------------------------------------------------------------------------------------

    main.py:

    fichier principal qui lance le jeu en entier, cela comprend les fichier:
    main_choice.py
    game.py
    Map.py
    player.py
    animation.py

    c'est la boucle principal du jeu, la boucle est limité à 60 tours par seconde

        -import:
            main_choice.py



    ----------------------------------------------------------------------------------------------------

    main_choice.py:

    fichier où est lancée la première interface du jeu

        -import:
            game.py

    fichier qui exécute la première interface du jeu qui comporte 4 boutons:
        Chevalier: le personnage choisi dans le jeu sera le Chevalier
        Mage: le personnage choisi dans le jeu sera le Mage
        Archer: le personnage choisi dans le jeu sera le Archer
        Quitter: le jeu est alors dermé

    class:
        Menu():
            class principal du fichier qui exécute les commandes des boutons lorsque l'utilisateur clique deçu
            ou qui met à jour la couleur des boutons lorsque l'utilisateur le survole

            def update(self):
                met à jour l'interface
                :return:

        MenuBouton():
            crée les boutons en fonction de leur taille choisie et crée aussi le texte deçu (c'est dans le constructeur)
            ainsi que les commandes associés avec (dans le constructeur aussi)

            dessiner(self, couleur):
                dessine les boutons
                :param couleur: tuple
                :return:

            executerCommande(self):
                Appel de la commande du bouton




        Application():
            class qui construit les commandes des boutons et qui exécute le lancement du jeu dès lors qu'un
            bouton est cliqué par l'utilisateur

            initialiser(self):
                

            menu(self):
                Affichage du menu

            quitter(self):
                quitter l'interface

            chevalier(self):
                permet de choisir le personnage Chevalier

            mage(self):
                permet de choisir le personnage Mage

            archer(self):
                permet de choisir le personnage Archer

            lancement(self, name):
                lance le jeu

            update(self):
                mise à jour



    ----------------------------------------------------------------------------------------------------

    game.py:

    fichier du lancement du jeu

        -import:
            Map.py
            dialog.py


    class:
        Game():
            constructeur du jeu où l'on retrouve les touches pour jouer au jeu:
                z: avancer
                s: reculer
                q: aller à gaucher
                d: aller à droite
                r: courir
                w: marcher
                flèche haut: attaque haut
                flèche bas: attaque bas
                flèche droite: attaque droite
                flèche gauche: attaque gaucher

            met à jour tout les 60/1000 secondes, met en place le joueur et dessine la map

            handle_input(self):
                déplacements du joueur et autre

            update(self):
                met à jour la map
                :return:

            run(self):
                pour garder la fenêtre ouverte ou la fermer
                exécuter le code du jeu



    ----------------------------------------------------------------------------------------------------

    Map.py

    gestionnaire de carte et les collisions

        -import:
            dataclasses
            pytmx
            pyscroll
            player.py
            dialog.py

    class:
        Portal():
            regroupe un ensemble de données pour créer un chemin qui permettra au joueur lorsqu'il est en contacte
            d'être téléporté sur le monde choisi:
            from_world: str      quel monde
            origin_point: str    sur quel point
            target_world: str    sur quel monde
            teleport_point: str  point de téléporation

            fonctionne avec dataclasses

    ---------------------------

        Map():
            regroupe l'ensemble de données sur une carte : mur, entité et autres

            name: str  nom du monde
            walls: list[pygame.Rect]   tous les murs avec comme type collisions
            group: pyscroll.PyscrollGroup
            tmx_data: pytmx.TiledMap    la carte Tiled
            portals: list[Portal]       les portails
            npc: list[NPC]              entité
            monster: list[Monster]      entité

            fonctionne avec dataclasses

    ---------------------------

        MapManager():
            construit les maps et tout ce qu'il y a l'intérieur grâce aux classes précédentes
            ainsi que les entités qui sont mis sur leur point d'apparition

            check_collisions(self):
                regarde si le joueur entre en contact avec un rectangle spécifique et fait donc une action avec
                :return:

            teleport_player(self, name_point):
                place le joueur à son spawn
                :param name_point: str
                :return:

            register_map(self, name, portals=[], npcs=[], monster=[], boss=[]):
                enregistrer les maps et tout ce qu'il y a dedans
                :param name: str
                :return:

            get_map(self):
                récupère le nom de la map
                :return: self.maps[self.current_map]: str

            get_group(self):
                récupère un groupe de pyscroll
                :return: list objet de pyscroll

            get_walls(self):
                récupère les murs de la map
                :return: list objet de pyscroll

            get_object(self, name):
                récupère un objet avec son nom comme un spawn ou un portail (plus précisement les coordonnées)
                :return: objet pyscroll

            teleport_NPC(self):
                téléporte le NPC dans son spawn
                :return:

            draw(self):
                dessiner la carte
                :return:

            update(self):
                met à jour les méthodes
                :return:



    ----------------------------------------------------------------------------------------------------

    player.py

    crée les entités: les monstres, les NPC et le joueur
        -import:
            pygame
            animation.py



    class:
        Entity():
            crée les entités, leur boxs, leur image ainsi que leur déplacements

            save_location(self):
                sauvegarde les coordconnées de l'emplacement de l'entité

            move_up(self):
                mouvement vers le haut

            move_down(self):
                mouvement vers le bas

            move_right(self):
                mouvement vers la droite

            move_left(self):
                mouvement vers la gauche

            update(self):
                met à jour les positions et rectangle(hitbox)
                :return:

            move_back(self):
                permet de replacer le joueur là où il était avant qu'il entre en collision
                :return:



        Player():
            crée le joueur et vérifie si le joueur attaque

            verif_si_mort(self):
                vérifie si le joueur est mort ou pas
                :return: (bool) True sinon rien

            attacks_from_player(self):
                détecte si le joueur attaque
                :return: True
                sinon None

            attaque_left(self):
                attaque gauche du joueur (animation)
                :return:

            attaque_right(self):
                attaque gauche du joueur (animation)
                :return:

            attaque_up(self):
                attaque gauche du joueur (animation)
                :return:

            attaque_down(self):
                attaque gauche du joueur (animation)
                :return:



        Monster():
            crée les entités qui attaque le joueur (PVE)
            cette entité possède une méthode de suivi du joueur

            verif_si_mort(self):
                verifie si le joueur est mort ou pas
                :return: (bool) True sinon rien

            mob_spawn(self):
                permet de téléporter le monstre à son spawn
                :return:

            load_mob_spawn(self, tmx_data):
                charge le point de spawn du monstre
                :param tmx_data:
                :return:

            following(self, player):
                le monstre pourchasse le joueur
                :return:

            attaque_player(self, player):
                vérifie si le joueur se trove en haut, bas, gauche, droite
                pour changer l'animation
                :param player:
                :return:



        NPC():
            personnage non joueur et passif à Player
            suit un chemin précis sur la map ou peut ne pas bouger selon le choix de
            la configuration de la map et du code

            move(self):
                permet au npc d'aller d'un point A à un point B définit sur la map
                :return:

            teleport_point(self):
                définit le point de spawn du NPC
                :return:

            load_point(self, tmx_data):
                récupère les points de passage du pnj
                :return:




    ----------------------------------------------------------------------------------------------------

    animation.py

    fait les animations pour chaque entité (sauf Boss)

        -import:
            pygame



    class:
        AnimateSprite():
            prend sur le sprite sur une coordonné y choisie dans le constructeur
            cela peut être adapté pour une image voulu car certaines sont différentes des autres
            alors on modifie le x, la taille pour obtenir l'image voulu comme les attaques du chevalier
            ou du mage qui sont différents de celles de l'archer

            ajouter_les_attaques_en_fonction_du_personnages_choisi(self):
                Charge les animations d'attaque et les ajoute à self animation car AUCUN
                 n'attaque de la même façon sur le sprite

            change_animation(self, name):
                change l'animation de l'entité en fonction de son déplacement
                :param name: nom de l'animation
                :return:

            get_images(self, y, distance, taille_image, size_x, size_y):
                parcours l'image qui contient les différents déplacements du joueur et les stock dans un tableau d'images
                :param y: coordonnées y de l'image
                :param distance: nombres d'images
                :param taille_image:
                :param size_x:
                :param size_y:
                :return: liste d'images

            get_image(self, x, y, size_x, size_y):
                prend l'image sur les coordonnées en x et y de l'image (spreet) et la taille
                :param x: coordonnées x de l'image
                :param y: coordonnées y de l'image
                :param size_x: taille en x
                :param size_y: taille en y

            get_image_attack(self, x, y, size_x, size_y):
                prend l'image sur les coordonnées en x et y de l'image (spreet) et la taille pour les animations
                d'attaque
                :param x: coordonnées x de l'image
                :param y: coordonnées y de l'image
                :param size_x: taille en x
                :param size_y: taille en y

            get_images_attack(self, y, distance, taille_image, size_x, size_y):
                parcours l'image qui contient les différents attaques du joueur et les stock
                dans un tableau images
                :param y: coordonnées y de l'image
                :param distance: nombres d'images
                :param taille_image:
                :param size_x:
                :param size_y:
                :return: liste d'images



    ----------------------------------------------------------------------------------------------------

    dialog.py

    fait les dialogues des pnj, s'active lorsque le joueur est à proximité et appuie sur espace
    et fait aussi l'interface qui affiche la vie du joueur.

        -import:
            pygame

    class:
        DialogBox():

            execute(self, dialogo=[]):
                Vérifie si on est en train de lire, si oui on passe au prochain texte si il existe
                Sinon on lance la boite de dialogue
                :param dialogo: texte dit par le pnj
                :return:

            render(self, screen):
                Affiche le texte lettre par lettre dans la boite de dialogue
                :param screen: écran du jeu
                :return:

            next_text(self):
                Passe d'une phrase à un autre si c'est possible
                :return:
                    
     Merci d'avoir lu cette documentation

    """
