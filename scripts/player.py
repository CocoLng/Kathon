from scripts.card import input_player


def options(extension):
    print("\n[0] /!\ Quitter le programme")
    print("[-1] Rappel de votre role")
    print("[-2] Passer votre tour")
    if extension:
        print("[-3] DEFFAUSSER 2 CARTES, pour se retirer un malus")


def ask_pos():
    pos = []
    while True:
        try:
            pos = input(
                "Taper la position(int) ou vous voulez jouer votre carte, (taper stop pour annuler), forme:\nX Y\n")
            if pos.upper() == "STOP":
                print("\n")
                return False
            x, y = pos.split()
            pos = [int(x), int(y)]
            break
        except ValueError:
            print("Valeur Incorrecte")
            continue
    return pos


def flip_card(card):
    antipode_d_u = ['down', 'up']
    antipode_l_r = ['right', 'left']
    try:
        for porte in card.borders:
            if porte.name in antipode_d_u:
                porte.name = antipode_d_u[antipode_d_u.index(porte.name) - 1]
            if porte.name in antipode_l_r:
                porte.name = antipode_l_r[antipode_l_r.index(porte.name) - 1]

        card.aff = True
    except (IndexError, ValueError):
        return False
    return True


class Human:

    def __init__(self, name):
        self.score = 0
        self.name = name
        self.role = None
        self.main = []
        self.status = []

    def __str__(self):
        Aff = "-" * 20
        return Aff + f"\n name = {self.name}" + f"\n score = {self.score}" + f"\n card = {[i.name for i in self.main]}" + '\n' + Aff

    def skip_turn(self):
        if len(self.main) == 0: return True
        return False

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        if score >= 0:
            self.__score = score
        else:
            print("impssible de retirer des point au joueur")

    def del_card(self, extension=False, deck=None, quantitee=1):
        volontaire = False
        if len(self.main) < quantitee:
            print("Vous n'avez pas asser de cartes")
            return False
        if len(deck.list_card) == 0:
            print("\n❌ Le deck est vide. Vous ne récupérez pas de cartes.\n Continuez ?\n[1]Oui\n[2]Non")
            res = input_player(1, 2)
            if res == 2: return False
        elif extension and deck and quantitee == 1:
            volontaire = True
            print(f"Combien de cartes voulez-vous piochez ? (1-{min(len(deck.list_card), 3)})")
            quantitee = input_player(1, min(len(deck.list_card), 3))

        for i in range(quantitee):
            print("Voici votre main :")
            [print(f"[{i}] {card.name}") for i, card in enumerate(self.main, 1)]
            print("Quelle carte voulez vous défausser, -1 pour annuler ?")
            card = input_player(-1, len(self.main))
            if card > 0:
                card = self.main[card - 1]
            else:
                return False
            if card in self.main:
                print(f"\nVous avez défaussée {card.name}")
                self.main.remove(card)
            else:
                print("Cette carte n'est pas presente dans votre main")
                return False
        if volontaire: self.get_card(deck, quantitee - 1)  # -1 car a la fin du tour il repioche
        return True

    def play(self, p_list, map_game, extension, deck):

        if len(self.status) != 0 and not ((len(self.status) == 1) and self.status[0] == "Voleur"):
            print("Aie..\nVous êtes affectés par ceci :")
            [print(f"- {status}") for status in self.status if status != "Voleur"]
            print("Ceci va vous empêchez de posez des cartes chemins tant que vous ne vous en débarrassez pas.\n")

        print("Voici votre main :")
        [print(f"[{i}] {card.name}") for i, card in enumerate(self.main, 1)]
        options(extension)
        if extension:
            v_min = -3  # valeur minimale de l'input
        else:
            v_min = -2
        card = input_player(v_min, len(self.main))

        try:

            if card > 0:
                card = self.main[card - 1]
            else:
                if card == -1:
                    print(f"\nRappel, vous êtes un :\n{self.role}\n")
                    return False
                if card == -3 and (("Voleur" not in self.status) and len(self.status) == 1) and len(self.status) != 0:
                    print("\nSéléctionnez deux cartes que vous defaussait, puis vous perdrez un malus :\n")
                    if self.del_card(False, deck, 2):
                        print("Quel malus souhaitez-vous supprimer ?")
                        [print(f"[{i}] {status}") for i, status in enumerate(self.status, 1)]
                        del self.status[input_player(1, len(self.status)) - 1]
                        return True
                    else:
                        return False
                elif card == -3:
                    print("\n❌ Vous n'avez pas de malus a supprimé, veuillez choisir une autre option.\n\n")
                    return False
                else:
                    return self.del_card(extension, deck)

            if card.__class__.__name__ == 'CardChemin':
                if len(self.status) == 0 or self.status[0] == 'Voleur':
                    ########################################
                    while True:
                        print(f"Vous allez jouer :{print(card)}")
                        print("[1] Continuer\n[2] Tourner la carte\n[3] Retour selection")
                        rep = input_player(1, 3)
                        if rep == 1:
                            pos = ask_pos()
                            if pos and map_game.add_card(card, pos):
                                self.main.remove(card)
                                return True
                            else:
                                return False
                        elif rep == 2:
                            flip_card(card)
                        else:
                            return False

            if card.__class__.__name__ == 'CardAction':
                card.arg = [p_list, map_game]
                if card.effect():
                    try:
                        self.main.remove(card)
                    except ValueError:
                        pass  # la carte se détruit parfois d'elle meme, comme switch_hand par exemple
                    return True
            return False

        except IndexError:
            print("Vous n'avez pas asser de cartes")
            return False

    def get_card(self, deck, i=1):
        Done = False
        if len(deck.list_card) != 0:
            Done = True
            for n in range(i):
                card = deck.draw_card()
                if card:
                    self.main.append(card)
                Done = card and Done
                print(f"Vous avez pioché : {self.main[-1].name}")
        return Done
