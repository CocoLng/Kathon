from scripts.card import input_player


def options(extension):  # Menu d'options proposé au joueur
    print("\n[0] /!\ Quitter le programme")
    print("[-1] Rappel de votre role")
    print("[-2] Passer votre tour")
    if extension:  # Cette règle n'est disponible que si l'extension est activée
        print("[-3] DÉFAUSSER 2 CARTES, pour se retirer un malus")


def ask_pos():  # Demande la position de la carte à mettre sur le plateau
    pos = []
    while True:
        try:
            pos = input(
                "Taper la position(int) ou vous voulez jouer votre carte, (taper stop pour annuler), forme:\nX Y\n")
            if pos.upper() == "STOP":  # Annule la saisie
                print("\n")
                return False
            x, y = pos.split()
            pos = [int(x), int(y)]
            break
        except ValueError:
            print("Valeur Incorrecte")
            continue
    return pos


def flip_card(card):  # Retourne la carte que le joueur a choisie
    # Les antipodes sont, comme leur nom l'indique, les cartes qui sont en face l'une de l'autre. Les échanger
    # revient à tourner la carte.
    antipode_d_u = ['down', 'up']  # Liste des antipodes d'up et down
    antipode_l_r = ['right', 'left']  # Liste des antipodes de left et right
    try:
        for porte in card.borders:  # Pour chaque porte de la carte, on l'inverse avec son antipode
            if porte.name in antipode_d_u:
                porte.name = antipode_d_u[antipode_d_u.index(porte.name) - 1]
            if porte.name in antipode_l_r:
                porte.name = antipode_l_r[antipode_l_r.index(porte.name) - 1]

        card.aff = True  # On affiche la carte tournée au joueur
    except (IndexError, ValueError):  # En cas d'erreur, on retourne False pour faire rejouer le joueur
        return False
    return True


class Player:  # Classe du joueur humain

    def __init__(self, name):
        self.score = 0
        self.name = name
        self.role = None
        self.main = []  # Liste des cartes dans la main du joueur
        self.status = []  # Liste des malus du joueur, contient également l'attribut voleur

    def __str__(self):
        Aff = "-" * 20
        return Aff + f"\n name = {self.name}" + f"\n score = {self.score}" + f"\n card = {[i.name for i in self.main]}" + '\n' + Aff

    @property
    def score(self):  # Retourne le score du joueur
        return self.__score

    @score.setter  # Modifie le score du joueur, vérifie que le score est positif
    def score(self, score):
        if score >= 0:
            self.__score = score
        else:
            print("Impossible de retirer des point au joueur, il en a pas")

    def del_card(self, extension=False, deck=None, quantitee=1):  # Retire une carte de la main du joueur et la défause
        volontaire = False  # Permet de savoir si le joueur a choisi de se retirer un malus, si False, il se retire un
        # malus
        if len(self.main) < quantitee:  # Si le joueur n'a pas assez de carte pour défausser
            print("Vous n'avez pas asser de cartes")
            return False
        if len(deck.list_card) == 0:  # Si le paquet de carte est vide
            print("\n❌ Le deck est vide. Vous ne récupérez pas de cartes.\nContinuez ?\n[1]Oui\n[2]Non")
            res = input_player(1, 2)  # Demande au joueur s'il veut continuer, si oui, il ne récupère pas de carte
            if res == 2: return False
        elif extension and deck and quantitee == 1:  # Si l'extension est activée et que le joueur veut défausser une
            # à trois cartes
            volontaire = True
            print(f"Combien de cartes voulez-vous piochez ? (1-{min(len(deck.list_card), 3)})")
            quantitee = input_player(1, min(len(deck.list_card), 3))

        for i in range(quantitee):  # Pour chaque carte à défausser
            print("Voici votre main :")
            [print(f"[{i}] {card.name}") for i, card in enumerate(self.main, 1)]
            print("Quelle carte voulez vous défausser, -1 pour annuler ?")
            card = input_player(-1, len(self.main))
            if card > 0:  # Si le joueur a choisi une carte, pas le menu
                card = self.main[card - 1]
            else:
                return False
            if card in self.main:  # Carte qui va être défaussé
                print(f"\nVous avez défaussée {card.name}")
                self.main.remove(card)
            else:
                print("Cette carte n'est pas presente dans votre main")
                return False
        # Si le joueur était volontaire, alors il pioche autant de carte que demandé
        if volontaire: self.get_card(deck, quantitee - 1)  # -1 car a la fin du tour il re pioche
        return True

    def play(self, p_list, map_game, extension, deck):  # Fonction qui permet au joueur de jouer
        # Regarde si le joueur a un malus, qui n'est pas le voleur
        if len(self.status) != 0 and not ((len(self.status) == 1) and self.status[0] == "Voleur"):
            print("Aie..\nVous êtes affectés par ceci :")
            [print(f"- {status}") for status in self.status if status != "Voleur"]
            print("Ceci va vous empêchez de posez des cartes chemins tant que vous ne vous en débarrassez pas.\n")

        # Si le joueur n'a pas de status, ou que le status est le voleur, alors il peut jouer aussi des cartes chemins
        print("\nVoici votre main :")
        [print(f"[{i}] {card.name}") for i, card in enumerate(self.main, 1)]  # Affiche la main du joueur
        options(extension)  # Affiche les options menu du joueur
        if extension:  # Si l'extension est activée, alors on peut défausser 2 cartes pour se retirer un malus
            v_min = -3  # valeur minimale de l'input
        else:
            v_min = -2
        card = input_player(v_min, len(self.main))

        try:
            if card > 0: # Si le joueur a choisi une carte, pas le menu, alors on l'attribue
                card = self.main[card - 1]
            else: # Si le joueur a choisi le menu
                if card == -1: # Rappel du role du joueur
                    print(f"\nRappel, vous êtes un :\n{self.role}\n")
                    return False # On retourne False pour faire rejouer le joueur
                # Si le joueur veut défausser une carte, on vérifie qu'il a un malus à se retirer
                if card == -3 and (("Voleur" not in self.status) and len(self.status) == 1) and len(self.status) != 0:
                    print("\nSélectionnez deux cartes que vous défaussait, puis vous perdrez un malus :\n")
                    if self.del_card(False, deck, 2):
                        print("Quel malus souhaitez-vous supprimer ?")
                        [print(f"[{i}] {status}") for i, status in enumerate(self.status, 1) if status != "Voleur"]
                        del self.status[input_player(1, len(self.status)) - 1]
                        return True
                    else:
                        return False
                elif card == -3: # Si le joueur veut défausser deux carte mais qu'il n'a pas de malus
                    print("\n❌ Vous n'avez pas de malus a supprimé, veuillez choisir une autre option.\n\n")
                    return False
                else:
                    return self.del_card(extension, deck)

            if card.__class__.__name__ == 'CardChemin': # Si la carte est un chemin
                if len(self.status) == 0 or self.status[0] == 'Voleur': # Si le joueur n'a pas de malus, ou que le
                    # malus est le voleur

                    while True: # Boucle pour demander au joueur ou il veut poser sa carte
                        print(f"Vous allez jouer :{print(card)}")
                        print("[1] Continuer\n[2] Tourner la carte\n[3] Retour selection")
                        rep = input_player(1, 3)
                        if rep == 1: # Si le joueur veut jouer la carte
                            print(map_game)
                            pos = ask_pos()
                            if pos and map_game.add_card(card, pos): # Si la carte a été posée, on la retire de la main
                                self.main.remove(card)
                                return True
                            else:
                                return False
                        elif rep == 2: # Si le joueur veut tourner sa carte
                            flip_card(card)
                        else:
                            return False

            if card.__class__.__name__ == 'CardAction': # Si la carte est une action
                card.arg = [p_list, map_game] # On lui donne les arguments du jeu actuel
                if card.effect(): # Si l'effet de la carte a été appliqué
                    try:
                        self.main.remove(card) # On retire la carte de la main, certaines cartes peuvent s'auto
                        # détruire d'ou le try
                    except ValueError:
                        pass  # la carte se détruit parfois d'elle meme, donc on ne fait rien dans ce cas
                    return True
            return False

        except IndexError:
            print("Vous n'avez pas asser de cartes")
            return False

    def get_card(self, deck, nbr_carte=1): # Fonction qui permet au joueur de piocher des cartes
        Done = False
        if len(deck.list_card) != 0: # Si le deck n'est pas vide
            Done = True
            for n in range(nbr_carte): # On pioche autant de carte que demandé
                card = deck.draw_card()
                if card:
                    self.main.append(card)
                Done = card and Done # Si la carte a été piochée, alors Done est True
                print(f"Vous avez pioché : {self.main[-1].name}")
        return Done # Si Done est True, alors le joueur a pioché une carte
