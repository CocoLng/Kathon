from sys import exit

import scripts.game as game
from scripts.card import input_player  # nous réutilisons la fonction input player de card.py
# from scripts.game import game_handler, readfile
from scripts.player import Human


###############################################################################
class Main:  # Classe principale
    def __init__(self):
        self.extension = Menu()
        # on lance le menu
        self.nb_manches = 0
        self.list_players = self.init_player()
        while self.recap:
            p_list = self.list_players.copy()
            game.game_handler(p_list, self.extension)
            self.nb_manches += 1
        exit()

    def recap(self) -> bool:
        if self.nb_manches == 0: pass
        game.readfile('..\\ressources\\SaboteurTxt.txt', 2)
        self.list_players.sort(key=lambda player: player.score, reverse=True)
        [(print(i, ': ', player.name, '[', player.score, 'pts]', '(', player.role.name, ')', sep='', end='\n')) for
         i, player in enumerate(self.list_players, 1)]
        print(
            f"\n{self.list_players[0].name} à un avantage de {self.list_players[0].score - self.list_players[1].score}pts comparer à {self.list_players[1].name}.")

        if self.nb_manches == 3:
            game.readfile('..\\ressources\\SaboteurTxt.txt', 3)
            print(
                f"\nLe grand gagnant est {self.list_players[0].name} !! \nFélicitation, en espérant être ré-exécuter "
                f"prochainement.\nEt n'oubliez pas de rester zen, comme mon code source")
            return False
        print("\n[1] Continuez la partie\n[0] /!\ Quittez le programme (Ctrl + C)\n")
        input_player(0, 1)
        return True

    def init_player(self) -> list:
        # Gere la creations des Joueurs via la saisie de leur nom, avec une résistance prévu a toute épreuve,
        # normalement...
        self.list_players = []
        print(
            "\nSaisir 'STOP' pour forcer l'arret.\nNe rien taper (ou Ctrl+C), si le nombre de joueur minimum est "
            "atteint, pour poursuivre vers l'initialisation.")
        while True:
            New_input = ''
            try:  # redemande jusqu'a validité
                New_input = input("Taper le nom d'un joueur : ")
                New_input = New_input.strip()  # enlève les espaces au début/fin
                if New_input == "": raise KeyboardInterrupt  # fin de saisie si rien n'est envoyé et que 2 ou 3j sont
                # crées
                if New_input.upper() == "STOP": exit()  # Quitte de force la saisie, utilse car KeyboardInterrupt
                # sert à continuer, car plus rapide en test/jeu
                if len(New_input) > 20: raise ValueError
                for player in self.list_players:
                    if player.name.lower() == New_input.lower():
                        raise ValueError
                self.list_players.append(Human(New_input))
                if (len(self.list_players) == 10 and not self.extension) or (
                        len(self.list_players) == 12 and self.extension): raise KeyboardInterrupt

            except ValueError:
                print(
                    f'❌ Erreur, le nom "{New_input}" est deja utilisé ou trop long (20 charactères max), veuillez en '
                    f'sélectionner un autre.')
                continue
            except KeyboardInterrupt:
                if (len(self.list_players) < 3 and not self.extension) or (
                        len(self.list_players) < 2 and self.extension):
                    if self.extension:
                        New_input = 2 - len(self.list_players)
                    else:
                        New_input = 3 - len(self.list_players)
                    print(
                        f"\n❌ Le nombre de joueurs minimum n'est pas atteint, veuillez rajouter encore {New_input} joueurs.")
                    continue
                print("\n\nFin de la saisie des Joueurs, voici la liste :")
                [(print('P', i, ': ', x.name, sep='', end='  ')) for i, x in enumerate(self.list_players, 1)]
                break

        return self.list_players


###############################################################################
#                                Fonctions                                    #
###############################################################################
def Menu() -> bool:
    while True:  # Menu principal
        game.readfile('..\\ressources\\SaboteurTxt.txt')
        res_input = input_player(0, 3)
        if res_input == 1:
            game.readfile('..\\ressources\\PresentationSubMenu.txt')
            game.readfile('..\\ressources\\PresentationSubMenu.txt', input_player(0, 2))
            input_player(0, 1)
        elif res_input == 2:
            return False
        elif res_input == 3:
            return True


###############################################################################
#                                   Main                                      #
###############################################################################
if __name__ == '__main__':
    Main()  # on lance le programme
