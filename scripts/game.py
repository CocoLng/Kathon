from os import path
from random import shuffle
from time import sleep

from scripts.board_game import BoardGame
from scripts.card import Deck, input_player


class Game:
    def __init__(self, main):
        self.extension = main.extension
        self.p_list = main.list_players.copy()  # Nous permets de conserver la liste des joueurs initiaux,
        # pour les reward a la fin
        
        shuffle(self.p_list)  # Mélange la liste des joueurs
        self.p_round = self.p_list.copy()  # Les joueurs sans carte se font supprimer de la liste, donc on en fait
        # une copie
        self.decks = [Deck("ACTION_CHEMIN", self.extension, False, len(self.p_round)),
                      Deck("ROLE", self.extension, self.extension, len(self.p_round)),
                      Deck("REWARD", self.extension, self.extension, len(self.p_round))]
        self.win_card = None
        self.map = BoardGame()  # Création de la map_game
        
        self.init_round(), self.repartition_card()
        self.gold_found = self.run_round()  # Renvoie si la pépite a était trouvée ou non à la fin de la manche
        self.reward_time()
        cls_screen()  # Efface le terminal
    
    def next_player(self, nextP = None):  # Gere le passage au joueur suivant
        if nextP is None: nextP = self.p_round[0]
        cls_screen()  # Efface le terminal
        sleep(1)  # temps de nettoyer l'écran
        readfile('..\\ressources\\SaboteurTxt.txt', 4)
        print(f"C'est au tour de {nextP.name} !\n")
        input("Pressez enter pour continuer, sinon on peut aussi attendre tranquillement\n...")
    
    def init_round(self):  # Initialise une manche
        # Initialise la map_game est la position des cartes cachées
        pos = [[8, -2], [8, 0], [8, 2]]
        
        # connect la carte PEPITE à WIN
        self.win_card = self.decks[0].list_card[29]
        
        # Retire la carte spawn, et les pierre/gold
        self.map.add_card(self.decks[0].draw_card(30), [0, 0], True)
        # Retire les trois cartes cachées
        L = [self.decks[0].draw_card(27) for i in range(3)]
        shuffle(L)  # Permet de mélanger les 3 cartes cachées
        [self.map.add_card(CARD, POS, True) for CARD, POS in zip(L, pos)]  # Ajoute les cartes cachées à la map_game
        self.decks[0].list_card = self.decks[0].list_card[80:103]
        [shuffle(deck.list_card) for deck in self.decks]  # Mélange les cartes
        
        # Effacement des status et suppression des cartes restantes du précédent round, sécurité, si résidu de pointeur
        [(player.status.clear(), player.main.clear()) for player in self.p_round]
        # assignment d'un role à chaque joueur, le deck role est déja mélangé
        for i, player in enumerate(self.p_round, 1): player.role = self.decks[1].list_card[i]
    
    # Gere la répartition des cartes action/chemin entre les joueurs
    def repartition_card(self):
        if self.extension:
            self.decks[0].list_card = self.decks[0].list_card[9:]  # On retire les 10 premières cartes
            [player.main.append(self.decks[0].draw_card()) for player in self.p_round for i in range(6)]
        
        else:
            # S'il n'y a pas l'extension alors :
            # Tous les 2 joueurs, une carte en moins est donnée initialement
            nb_P_repart = 7 - len(self.p_round) // 2
            [player.main.append(self.decks[0].draw_card()) for player in self.p_round for i in range(nb_P_repart)]
    
    # Gere la manche en cours
    def run_round(self) -> bool:
        # Verifies que la pépite n'est pas trouvée et qu'un joueur a toujours au moins une carte
        first_player = self.p_round[0].name
        first_turn = True  # Permet de savoir si c'est le premier tour de la manche, pour afficher le role du joueur
        while True:
            P_Alive = True  # Permet de savoir si le joueur est encore en vie
            print(self.map)
            if first_turn: print(f"\n{self.p_round[0].name}, vous êtes :\n{self.p_round[0].role}\n")
            while True:  # tant qu'un joueur n'as pas joué
                if self.p_round[0].play(self.p_round, self.map, self.extension,
                                        self.decks[0]):  # Si le joueur qui va jouer
                    break  # A joué
            print(self.map)  # Affiche la nouvelle map_game
            if not (self.p_round[0].get_card(self.decks[0])):  # Si la pioche est vide
                if len(self.p_round[0].main) == 0:  # Si le joueur n'a plus de carte
                    self.p_round.pop(0)  # On le supprime de la liste des joueurs
                    P_Alive = False  # Le joueur est mort, car il n'a plus de carte
                else:
                    print("La pioche de carte est vide.")  # Message informatif disant que la pioche est vide
            if self.win_card.borders[0].flag_loop is not None: return True  # Si la pépite est trouvée
            # Une fois que le joueur a joué nous passons au suivant, stocké en position 0
            # Le joueur qui vient de finir son tour passe en dernière position
            if P_Alive: self.p_round = self.p_round[1:] + self.p_round[:1]  # Si le joueur est mort, on ne le remet
            # pas en fin de liste
            try:  # Regarde si le joueur suivant est le premier, si oui, nous n'afficherons plus le role du joueur
                if first_player == self.p_round[0].name: first_turn = False
            except IndexError:
                return False  # Si la liste des joueurs est vide, la partie est finie
            print("\nFIN de votre tour, analyser la map_game et retenez vos cartes si vous le désirez.")
            input("Pressez enter quand vous avez fini pour confirmer la fin de votre tour\n...")
            
            self.next_player()  # Gere le passage au joueur suivant
    
    def reward_time(self):  # Gere la récompense des joueurs
        """
        p_list va se faire filtrer de manière à conserver uniquement les gagnants du round
        nb_deleted est présent pour eviter de provoquer un décalage d'indice dans la list des joueurs
        """
        print(self.gold_found)
        nb_deleted = 0
        if not self.extension:
            if self.gold_found:  # les chercheurs ont gagné
                self.decks[2].list_card.sort(key=lambda card: card.pepite, reverse=True)
                if len(self.p_list) >= 10:
                    self.decks[2].list_card.append(self.decks[2].list_card[-1])  # s'il y a 10 joueurs
                    self.decks[2].list_card[-1].pepite = "0"
                [self.p_list.append(self.p_list.pop(0)) for x in self.p_list if x != self.p_round[0]]
                self.p_list.insert(0, self.p_list.pop())  # Fait repasser le joueur qui a trouver la pépite, devant
                for i in range(len(self.p_list)):
                    if self.p_list[i - nb_deleted].role.name[0] != "C":
                        del self.p_list[i - nb_deleted]
                        nb_deleted += 1
                for i, card_reward in enumerate(self.decks[2].list_card, 0):
                    if i == len(self.p_list) - 1: break
                    self.p_list[i].score += int(card_reward.pepite)
            
            else:  # les Saboteurs ont gagné
                for i in range(len(self.p_list)):
                    if self.p_list[i - nb_deleted].role.name[0] != "S":
                        del self.p_list[i - nb_deleted]
                        nb_deleted += 1
                nb_pepites = 4 - len(self.p_list) // 2
                for player in self.p_list:
                    player.score += int(nb_pepites)
        
        else:
            # Check pour des potentiels voleurs
            self.p_list[0].status.append("Voleur")
            P_voleur = []
            [P_voleur.append(player) for player in self.p_list if
             ("Voleur" in player.status) and not ("Emprisonnement" in player.status)]
            # DETECTION DES GEMMES GEOLOGUES
            nb_cristaux = 0
            card = None
            for map_c in self.map._BoardGame__map_:
                for card in map_c:
                    if card != [] and card.special == "cristaux": nb_cristaux += 1
                print(card, nb_cristaux)
            
            if self.gold_found:  # les Chercheurs gagnent
                for i in self.p_round:
                    print(i.role.name)
                if self.p_round[0].role.name[0] != "C":  # C'est un role spécial qui a fait la connection
                    list_flag = self.map.detect(self.win_card)
                    if 'START' in list_flag:
                        print('les', self.p_round[0].role.name, 'on gagné')
                        self.p_list = [joueurs for joueurs in self.p_list if
                                       self.p_round[0].role.name == joueurs.role.name]
                        nb_pepites = max(6 - len(self.p_list), 1)
                        for n in self.p_list:
                            if n.role.name != 'boss':
                                n.score += int(nb_pepites)
                            else:
                                n.score += int(nb_pepites) - 1
                            print(f'le joueur {n.name} est victorieux et a {n.score} il était {n.role.name}')
                    else:
                        if 'D' in list_flag:
                            self.p_list = [joueurs for joueurs in self.p_list if 'boss' in joueurs.role.name]
                            if not self.p_list:
                                self.p_list = [joueurs for joueurs in self.p_list if 'sabo' in joueurs.role.name]
                            nb_pepites = max(6 - len(self.p_list), 1)
                            for n in self.p_list:
                                n.score += int(nb_pepites) - 1
                                print(f'le joueur {n.name} est victorieux et a {n.score} il était {n.role.name}')
                        
                        elif 'GREEN' in list_flag or 'BLUE' in list_flag:
                            et = "et"
                            print(f"l'équipe {[et * (i - 1) + val for i, val in enumerate(list_flag)]} a gagné")
                            nb_pepites = max(6 - len(self.p_list), 1)
                            self.p_list = [joueurs for flag in list_flag for joueurs in self.p_list if
                                           joueurs.role.name in flag or 'boss' in joueurs.role.name]
                            for n in self.p_list:
                                if n.role.name != 'boss':
                                    n.score += int(nb_pepites)
                                else:
                                    n.score += int(nb_pepites) - 1
                                print(f'le joueur {n.name} est victorieux et a {n.score} il était {n.role.name}')
            
            else:  # les saboteurs gagnent
                for n, player in enumerate(self.p_list, 0):
                    if player.role.name[0] != ("S" or "P"):  # Saboteur or Profiteur
                        del self.p_list[n - nb_deleted]
                        nb_deleted += 1
                nb_pepites = max(6 - len(self.p_list), 1)  # Nombre de pépites en fonction du nombre de gagnants
                
                for n in range(len(self.p_list)):
                    if self.p_list[n].role.name[0] == "S":
                        self.p_list[n].score += int(nb_pepites)
                    else:
                        self.p_list[n].score += int(nb_pepites) - 1  # les saboteurs gagne 1 de moins
                    
                    # p.append(plaer) for list geo list gagnt si score !=0
            
            # if player.score == 0 : p_list.remove(player) #Si le score est nul, c'est que le gagnant a rien gagné
            # On va le retirer de la list des gagnants de manière à éviter qu'il puisse se faire voler
            # Tour des voleurs
            [print(player.name, player.score) for player in self.p_list]
            if len(P_voleur) != 0 and len(self.p_list) != 0:  # S'il y a des voleurs et des gagnants
                for player in P_voleur:
                    self.next_player(P_voleur)  # ne peut voler que les joueurs qui viennent de gagner
                    print("THIEF TIME hehe\nChoissiez à quel gagnant vous souhaitez voler une pépite :\n")
                    [(print('[', i, ']', x.name, "(", x.role.name, ')', sep='', end='  ')) for i, x in
                     enumerate(self.p_list, 1)]
                    selected = input_player(1, len(self.p_list))
                    self.p_list[selected - 1].score -= 1
                    player.score += 1
                    del P_voleur[0]


def cls_screen():  # Sert à effacer la console, utile pour masquer les informations d'un joueur à an autre
    # system('cls' if name=='nt' else 'clear')
    sleep(1)  # Attend 1 seconde pour laisser le temps de clear la console


def readfile(path_join, part_explain=0):  # Permet de lire un fichier texte, ici principalement à but d'affichage
    with open(path.join(path.dirname(__file__), path_join), 'r') as f:
        f_split = f.read().split("SUB_PART")  # Nous décomposons notre fichier tous les SUB_PART
        print(f_split[part_explain])  # Nous affichons la partie demandée
