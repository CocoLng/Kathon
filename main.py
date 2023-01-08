from sys import exit

from scripts.card import input_player  # nous réutilisons la fonction input player de card.py
from scripts.game import Game, readfile


###############################################################################
class Main:  # Classe principale

    def __init__(self):
        self.extension = Menu()  # Menu de lancement
        self.nb_manches = 0  # Nombre de manches jouées
        self.list_players = self.init_player()  # Liste de noms des joueurs

    def recap(self) -> bool:
        print("Enter", self.nb_manches)
        [print("Inside", player.name,player.score) for player in self.list_players] # Affiche les scores des joueurs
        readfile('..\\ressources\\SaboteurTxt.txt', 2)
        self.list_players.sort(key=lambda player: player.score, reverse=True)
        [(print(i, ': ', player.name, '[', player.score, 'pts]', '(', player.role.name, ')', sep='', end='\n')) for
         i, player in enumerate(self.list_players, 1)]
        print(
            f"\n{self.list_players[0].name} à un avantage de {self.list_players[0].score - self.list_players[1].score}pts comparer à {self.list_players[1].name}.")

        if self.nb_manches == 3:
            readfile('..\\ressources\\SaboteurTxt.txt', 3)
            print(
                f"\nLe grand gagnant est {self.list_players[0].name} !! \nFélicitation, en espérant être ré-exécuter "
                f"prochainement.\nEt n'oubliez pas de rester zen, comme mon code source")
            
        print("\n[1] Continuez la partie\n[0] /!\ Quittez le programme (Ctrl + C)\n")
        input_player(0, 1)

    def init_player(self) -> list:
        # Gere la creations des Joueurs via la saisie de leur nom, avec une résistance prévu a toute épreuve,
        # normalement...
        self.list_players = []  # Liste des joueurs
        print(
            "\nSaisir 'STOP' pour forcer l'arrêt.\nNe rien taper (ou Ctrl+C), si le nombre de joueur minimum est "
            "atteint, pour poursuivre vers l'initialisation.")
        while True:
            New_input = ''
            try:  # redemande jusqu'a validité
                New_input = input("Taper le nom d'un joueur : ")
                New_input = New_input.strip()  # enlève les espaces au début/fin
                if New_input == "": raise KeyboardInterrupt  # fin de saisie si rien n'est envoyé et que 2 ou 3j sont
                # crées
                if New_input.upper() == "STOP": exit()  # Quitte de force la saisie, utilsé car KeyboardInterrupt
                # sert à continuer, car plus rapide en test/jeu
                if len(New_input) > 20: raise ValueError
                for player in self.list_players:
                    if player.lower() == New_input.lower():
                        raise ValueError
                self.list_players.append(New_input)
                if (len(self.list_players) == 10 and not self.extension) or (
                        len(self.list_players) == 12 and self.extension): raise KeyboardInterrupt

            except ValueError: # Si le nom est déjà utilisé ou trop long
                print(
                    f'❌ Erreur, le nom "{New_input}" est deja utilisé ou trop long (20 charactères max), veuillez en '
                    f'sélectionner un autre.')
                continue
            except KeyboardInterrupt: # Si l'arrêt de la saisie est demandé
                if (len(self.list_players) < 3 and not self.extension) or (
                        len(self.list_players) < 2 and self.extension):
                    if self.extension: # Si le mode extension est activé, il faut au moins 2 joueurs
                        New_input = 2 - len(self.list_players)
                    else: # Sinon, il faut au moins 3 joueurs
                        New_input = 3 - len(self.list_players)
                    print(
                        f"\n❌ Le nombre de joueurs minimum n'est pas atteint, veuillez rajouter encore {New_input} joueurs.")
                    continue
                print("\n\nFin de la saisie des Joueurs, voici la liste :")
                [(print('P', i, ': ', x, sep='', end='  ')) for i, x in enumerate(self.list_players, 1)] #
                break

        return self.list_players

    def run_game(self): # Gere le déroulement du jeu
        game = Game(self) # Création de la partie
        while True: # Comptes les nombres de manches jouées, sort quand 3 manches sont jouées
            self.list_players = game.__enter__() # Lance la manche
            self.nb_manches += 1 # Incrémente le nombre de manches jouées
            self.recap() # Affiche le récapitulatif de la manche
            if self.nb_manches == 3: break
        #return True if self.nb_manches == 3 else False


###############################################################################
#                                Fonctions                                    #
###############################################################################
def Menu() -> bool: # Menu de lancement, retourne True si l'extension est activée
    while True:  # Menu principal
        readfile('..\\ressources\\SaboteurTxt.txt') # Affiche le menu
        res_input = input_player(0, 3)
        if res_input == 1: # Partie texte explicative
            readfile('..\\ressources\\PresentationSubMenu.txt')
            readfile('..\\ressources\\PresentationSubMenu.txt', input_player(0, 3))
            input_player(0, 1)
        elif res_input == 2: # Sans extension
            return False
        elif res_input == 3: # Avec extension
            return True


###############################################################################
#                                   Main                                      #
###############################################################################

main = Main() # Initialisation le jeu
main.run_game() # Lance le jeu
