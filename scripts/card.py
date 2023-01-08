from abc import ABC
from os import path
from sys import exit
from types import MethodType

from scripts.detect_region import ConnectionEdge

# Chemin vers le fichier texte pour l'initialisation des cartes
path_init = path.join(path.dirname(__file__), '..\\ressources\\card_ini.txt')
###############################################################################
#                              Deck                                           #
###############################################################################
"""
Name correspond au nom du deck que nous souhaitons crée, il doit s'appeler comme ceci :
    ACTION_CHEMIN / ROLE / REWARD
"""


class Deck:
    # Permet de générer un deck de carte
    def __init__(self, name, extension, replace, nb_players):  # chaque carte possède un nom et une description
        self.name = name
        self.extension = extension
        self.replace = replace
        self.list_card = []
        # Appel de la fonction qui charge les cartes
        self.load_cards(nb_players)
    
    # Permet de piocher une carte
    def draw_card(self, i=0):  # sert pour la pioche d'une carte
        # i est le nombre de cartes que l'on souhaite piocher
        if len(self.list_card) == 0: return False
        return self.list_card.pop(i)  # sinon envoie la première carte et la supprime
    
    # Permet de charger les cartes
    def load_cards(self, nb_players):  # Gere le chargement des cartes en le lisant dans un fichier txt
        i = 1
        write = False  # Sert à détecter si on est dans la partie des cartes ou on doit écrire
        status = None  # Prend le nom de la catégorie qu'il lit et regarde si c'est celle desirée
        with open(path_init, 'r') as f:  # ferme automatiquement le fichier a la fin de la lecture
            for line in f:
                line = line.strip()
                if line.upper() == self.name.upper():  # Regarde si le nom correspond a la partie qu'on veut écrire
                    status = self.name.upper()
                    """
                    self.extension contient 2 argument 
                    self.extension dit si l'extension est activée ou non
                    self.replace dit si quand l'extension est activée il faut remplacer les cartes du jeu de base
                    """
                    # Si l'extension est activée, nous devons prendre en compte les cartes de l'extension via un
                    # systeme de write
                    if self.replace:
                        write = False
                    else:
                        write = True
                elif line == "EXTENSION" and status == self.name and self.extension:
                    write = True
                    # Condition d'arrêt, le mot END est détecté est status est deja défini, ce qui veut dire que nous
                    # avons deja écrit
                # Ou nous détectons le mot EXTENSION est celle-ci est désactivée
                elif status == self.name and ((line == "END") or (line == "EXTENSION" and not self.extension)):
                    break
                # Si la ligne n'est pas vide alors nous écrivons
                elif line != "" and write:
                    line = line.split(';')
                    if status == "ACTION_CHEMIN":
                        if len(line) == 4:  # Si la longueur des arguments ==4 alors nous sommes forcément sur une
                            # carte action
                            self.list_card += int(line[0]) * [CardAction(line[1], line[2], line[3])]
                        else:  # La longeur d'une carte chemin est variable selon ses paramètres, mais toujours >4
                            [self.list_card.append(CardChemin(line)) for i in range(int(line[0]))]
                    elif status == "ROLE":
                        if not self.extension:
                            nb = 3  # le nombre de chercheurs de base est défini à trois
                            if nb_players == 4: nb += 1  # s'il y a quatre joueurs, nous passons à 4 chercheurs
                            while nb / nb_players < 0.7: nb += 1  # la proportion de chercheur doit toujours est au
                            # moins de 70% dans la manche
                            if line[0][0] == "S": nb = (nb_players - nb) + 1  # formule pour obtenir le nombre de
                            # saboteur
                            self.list_card += nb * [CardRole(line[0], line[1])]
                        else:  # Quand l'extension est activée nous chargeons toutes les cartes, peu importe le nb
                            # de joueurs
                            self.list_card += int(line[0]) * [CardRole(line[1], line[2])]
                    
                    elif status == "REWARD":
                        self.list_card += int(line[0]) * [CardReward(line[1], line[2], line[3])]
                    else:  # Sert à savoir si le nom saisi est faux, utile pour debug
                        print("deck avec le nom de propriété indéfinis ! ERREUR")
                        exit()
                    i += 1
    
    def __str__(self):
        res = "o-----o " + self.__class__.__name__ + ":" + self.name + " o-----o"
        res += "\nCeci est un deck de cartes"
        return res


###############################################################################
#                             Structures Cartes                               #
###############################################################################

class Card(ABC):  # Classe abstraite qui sert de base pour les cartes
    def __init__(self, name, description):  # chaque carte possède un nom et une description
        self.name = name
        self.description = description
    
    def __str__(self):
        A = len(self.description) // 2
        res = "o-----o " + self.name + " o-----o"
        if '\n' in self.description:
            A = len(self.description[:self.description.index('\n')]) // 2
        res += "\n" + ' ' * (len(res) // 2 - A) + self.description
        res += "\no----------------------o"
        return res


class CardChemin(Card):
    # Permet de créer une carte chemin avec la gestion des bordures
    def __init__(self, arg):
        # arg contient toute la ligne lu dans cardinit.txt
        super().__init__(arg[1], arg[2])
        
        self.is_start = arg  # Si la carte est une carte de spawn
        self.special = arg  # Si la carte possède un effet spécial
        self.reveal = arg  # Si la carte est révélée
        self.config = list(arg[3].split(":"))  # Contient les informations de la carte
        self.port = list(arg[4].split(","))  # Contient les portes d'accès de la carte pour les futures connexions
        self.borders = self.port  # Sert a définir les connexions de la carte avec ses voisines
        self.aff = True
        if len(arg) >= 9:
            if arg[8]:
                self.effect = MethodType(globals()[self.special], self)
    
    # La carte chemin est lu par le boardgame, player
    # Il y a des conditions sur comment ses valeurs sont attribuées, d'où l'usage de setter
    
    @property
    def special(self):
        return self.__special
    
    @special.setter
    def special(self, special):
        self.__special = None
        if len(special) >= 7:
            self.__special = special[6]  # non destructible si special, spawn et gold
    
    @property
    def is_start(self):
        return self.__is_start
    
    @is_start.setter
    def is_start(self, is_start):
        self.__is_start = False
        if len(is_start) >= 8:
            self.__is_start = bool(is_start[7])
    
    @property
    def reveal(self):
        return self.__reveal
    
    @reveal.setter
    def reveal(self, reveal):
        # soit bool, soit list
        self.__reveal = True
        try:
            if len(reveal) >= 6:
                if reveal[5] == 'False':
                    self.__reveal = False
        except TypeError:
            self.__reveal = reveal
    
    @property
    def borders(self):
        return self.__borders
    
    @borders.setter
    def borders(self, port):
        self.__borders = []
        [self.__borders.append(ConnectionEdge(i, self.special, self.special == 'START')) for i in port]
        for chemins, portes in zip(self.config, self.borders):
            [portes.connect(portes_) for connections, portes_ in zip(chemins, self.borders) if int(connections) == 1]
    
    @property
    def aff(self):
        if self.reveal:
            return self.__aff
        return ["┏━━━┓", "┃   ┃", "┃   ┃", "┃   ┃", "┗━━━┛"]
    
    @aff.setter
    def aff(self, update):
        self.__aff = aff_ch(self.borders, self.special, self.name)
        if '\n' in self.description:
            self.description = self.description[:self.description.index('\n')]
        self.description = self.description + ''.join(
            ['\n' + " " * (len(self.name) // 2 - len(i) // 2 + 7) + i for i in self.aff])


class CardRole(Card):
    # Permet de créer une carte rôle
    def __init__(self, name, description):
        super().__init__(name, description)


class CardReward(Card):
    # Permet de créer une carte récompense, quand l'extension est désactivée
    def __init__(self, name, description, pepite):
        super().__init__(name, description)
        self.pepite = pepite


class CardAction(Card):
    # les cartes action sont des cartes avec un effet
    def __init__(self, name, description, effect,
                 arg=None):  # les cartes actions ne nécessitent pas tous la liste des joueurs
        super().__init__(name, description)
        
        self.effect = MethodType(globals()[effect], self)
        # on ajoute la méthode contenant le nom effect dans notre object, les autres
        # ne sont pas chargés car inutiles
        if arg is None:
            arg = []
        self.arg = arg
    
    ###############################################################################
    #                             Méthodes Communes                               #
    ###############################################################################
    """
    target_player est la seule méthode de base inclus dans notre classe, car toute carte action on a besoin
    Les fonctions ci dessous n'ont pas besoin d'accédé a un objet
    arg[0] contient la liste des Joueurs, le joueurs actuel est en position 0
    arg[1] contient la map_game
    """
    
    def target_player(self, list_player_targetable):
        print(f'Sur quel joueur voulez vous appliquer {self.name}')
        [print('┃', i, ': ', x.name, sep=' ', end='┃') for i, x in
         enumerate(list_player_targetable, 1)]  # laisse le joueur pouvoir se cibler
        print("\n")
        return list_player_targetable[input_player(1, len(list_player_targetable)) - 1]


# les fonctions si dessous sont appelables par tous types de cartes

def has_effect(effect, target_p):
    if effect in target_p.status:  # regarde si le Target Player possède deja l'effet
        return True
    return False


def edit_status(ajout, effect_play, target_p):
    Done = False
    # si le joueur n'as pas déja l'effet alors on peut lui mettre
    if ajout and not (has_effect(effect_play, target_p)):
        target_p.status.append(effect_play)
        Done = True
        print(f"Mouhaha, l'opération sur {target_p.name} c'est déroulé sans accroc.\n")
    # si on veut lui retirer(ajout=False), on regarde que la cible possède l'effet
    elif not ajout and has_effect(effect_play, target_p):
        target_p.status.remove(effect_play)
        Done = True
        print(
            f"Mais c'était sur enfaite, sur que l'oprération sur {target_p.name} n'allait pas rencontrer de "
            f"difficulté majeures.\n")
    return Done


def input_player(mini, maxi):  # demande un input entre mini et maxi et return le res
    selected = None
    while True:
        try:  # redemande jusqu'a validité
            selected = input('Taper le chiffre désiré : ')
            selected = int(selected)
            if selected < mini or selected > maxi:
                raise ValueError
            if selected == 0: raise KeyboardInterrupt  # permet de quittez si 0 est entrer et que nous sommes dans le
            # menu
            break
        except ValueError:
            print(f'❌ Valeur "{selected}" incorrecte, veuillez réessayer entre {mini} et {maxi}\n')
            continue
        except KeyboardInterrupt:
            try:
                confirm = input("\n/!\ Confirmer de quitter le programme y/n ?")
                if confirm[:1].upper() == "Y":
                    raise KeyboardInterrupt
                else:
                    print("\nOk, on continue")
                    continue
            except KeyboardInterrupt:
                print("\nVous quittez le programme, au revoir")
                exit()
    return selected


###############################################################################
#                      Listes des Effets Disponibles                          #
###############################################################################
"""
Ici chaque méthode correspond a un effet possible, qui se fait charger dans la carte action 
qui lorsque jouer éxécute l'effet, le faite de ne pas le mettre dans la classe action permet
de ne pas charger tous les effects dans l'object alors que ce dernier ne peut en avoir qu'un seul
"""

###############################################################################
#                           Break & Repair Outils                             #
###############################################################################
"""
Nom des Cartes qui impactent les outils :

    Cassage de Pioche || Reparation de Pioche
    Cassage de Lanterne || Reparation de Lanterne
    Cassage de Wagon || Reparation de Wagon

Les cartes qui contiennent deux réparations : 
    Reparation de Pioche et Lanterne
    Reparation de Pioche et Wagon
    Reparation de Wagon et Lanterne
Les noms peuvent être inversées

Lors de l'initialisation le nom[0] de la carte dit si on casse ou repare
Le nom[2] nous dit quel est l'outil ciblé'
L'effet est lui stocker dans l'attribut "effet" qui pointe vers la méthode "impact_tools"
Donc effect = impact_tools a l'initialisation pour appeler la fonction
"""


def impact_tools(self):
    Name_list = self.name.split()
    list_Player_targetable = []
    if Name_list[0] == "Cassage":  # Si nous ne cassons pas nous réparons
        [list_Player_targetable.append(player) for player in self.arg[0] if not (Name_list[2]) in player.status]
        if len(list_Player_targetable) == 0:
            print(f"\nTous le monde a deja son/sa {Name_list[2]} de cassé.... Veuillez faire un autre choix\n")
            return False
        Target_P = self.target_player(list_Player_targetable)
        return edit_status(True, Name_list[2], Target_P)
    [list_Player_targetable.append(player) for player in self.arg[0] if Name_list[2] in player.status]
    if len(list_Player_targetable) == 0:
        print("\nPersonne n'as besoin de la réparation que vous proposez.... Veuillez faire un autre choix\n")
        return False
    Target_P = self.target_player(list_Player_targetable)
    if len(Name_list) == 5:  # Si nous avons deux effet pour la réparation    
        Done = edit_status(False, Name_list[4], Target_P)
        Done2 = edit_status(False, Name_list[2], Target_P)
        Done = Done or Done2
    else:
        Done = edit_status(False, Name_list[2], Target_P)
    if not Done: print(
        f"\nAIE, l'opération sur {Target_P.name} est un échec, il/elle n'as pas besoin de notre cadeau/l'as deja "
        f"reçus.\n")
    return Done


###############################################################################
#                         Avalanche & Plan Secret                             #
###############################################################################

def collapsing(self):  # Avalanche/Éboulement
    while True:
        VAL = input(
            f'Chosir x entre {self.arg[1].decalage[0]} et {len(self.arg[1].MAP) + self.arg[1].decalage[0] - 1}\n'
            f'Chosir y entre {self.arg[1].decalage[1]} et {len(self.arg[1].MAP[0]) + self.arg[1].decalage[1] - 1}\n'
            ' x y:\n')
        VAL = VAL.split(' ')
        if VAL == 'stop':
            return False
        try:
            VAL = [int(i) for i in VAL]
            break
        except ValueError:
            print('incorrect value')
    return self.arg[1].del_card(VAL)


def secret_plan(self):  # Plan Secret, permet de visualiser une des 3 cartes d'arrivée
    while True:
        print("Quel carte souhaitez-vous visualiser ?\n 1-Haut 2-Milieu 3-Bas\n")
        selected = input_player(1, 3)
        if selected == 1 and not (
                self.arg[1].current([8, 2]).reveal):  # on vérifie que la carte n'est pas déja visible, on sait jamais..
            print(f"\nLa carte du Haut est un/une {self.arg[1].current([8, 2]).name}\n")
            return True
        elif selected == 2 and not self.arg[1].current([8, 0]).reveal:
            print(f"\nLa carte du Milieu est un/une {self.arg[1].current([8, 0]).name}\n")
            return True
        elif selected == 3 and not self.arg[1].current([8, -2]).reveal:
            print(f"\nLa carte en Bas est un/une {self.arg[1].current([8, -2]).name}\n")
            return True
        print("\nCette carte est deja visible...Veuillez en choisir une autre")


###############################################################################
#                        Chargement d'une Extension                           #
###############################################################################

def inspect(self):  # Inspection, permet de voir le role d'un joueur
    Target_P = self.target_player(self.arg[0])
    print(f"SPOILER ALERTE :\n{Target_P.name} est en réalité un :\n{Target_P.role}.")
    Done = True
    return Done


def switch_role(self):  # Changement de Role, permet de changer le role d'un joueur
    print("Sélectionnez un joueur avec qui changer de role :")
    Target_P = self.target_player(self.arg[0])
    temp = Target_P.role
    Target_P.role = self.arg[0][0].role
    self.arg[0][0].role = temp
    print(f"Vous êtes désormais un {self.arg[0][0].role}")
    Done = True
    return Done


def switch_hand(self):  # Changement de Main, permet de changer la main d'un joueur avec la sienne
    print("Avec quel joueur souhaitez-vous inverser votre deck de cartes ?")
    Target_P = self.target_player(self.arg[0])
    self.arg[0][0].main.remove(self)
    self.arg[0][0].main.append(self.arg[0][0].main[0])
    temp = Target_P.main
    Target_P.main = self.arg[0][0].main
    self.arg[0][0].main = temp
    self.arg[0][0].main.remove(self.arg[0][0].main[-1])
    Done = True
    return Done


"""
Gère l'effet d'emprisonnement et de libération en réutilisant edit_effet
A l'initialisation, le nom doit être "Emprisonnement" pour mettre en prison, choix libre pour libérer
L'effet doit être "jail_handler"
"""


def jail_handler(self):
    list_Player_targetable = []
    if self.name == "Emprisonnement":  # Réutilisation de edit_effet
        [list_Player_targetable.append(player) for player in self.arg[0] if not (self.name) in player.status]
        if len(list_Player_targetable) == 0:
            print("\nTous le monde est en prison....Veuillez faire un autre choix\n")
            return False
        Target_P = self.target_player(list_Player_targetable)
        return edit_status(True, "Emprisonnement", Target_P)
    # si on n'emprisonne pas alors on libère
    [list_Player_targetable.append(player) for player in self.arg[0] if "Emprisonnement" in player.status]
    if len(list_Player_targetable) == 0:
        print("\nPersonne n'est en prison....Veuillez faire un autre choix\n")
        return False
    Target_P = self.target_player(list_Player_targetable)
    return edit_status(False, "Emprisonnement", Target_P)


"""
Gère l'effet de vol et de retrait via la carte pas touche
A l'initialisation, le nom doit être "Voleur" pour activer le vol en fin de manche, choix libre pour le retirer
L'effet doit être "thief_handler"
"""


def thief_handler(self):
    if self.name == "Voleur":  # Réutilisation de edit_effet
        return edit_status(True, "Voleur", self.arg[0][0])  # applique l'effet voleur au joueur actuel
    list_Player_targetable = []
    [list_Player_targetable.append(player) for player in self.arg[0] if "Voleur" in player.status]
    if len(list_Player_targetable) == 0:
        print("\nPersonne n'as le statut de voleur.... Veuillez faire un autre choix\n")
        return False
    Target_P = self.target_player(list_Player_targetable)
    return edit_status(False, "Voleur", Target_P)


"""
Vous pouvez ajouter vos effet personnels ici, puis crée la carte en l'ajoutant dans /ressource/card_ini.txt
Il faudra, lors de l'initialisation, mettre dans effet le même nom que celle de la méthode'
"""


def DOOR(self):  # Effet Porte, utilise pour l'exetension, permet de mettre un flag sur une zone
    IO = []
    IND = []
    for i in self.borders:
        i.source = False
    
    for i in self.borders:
        if i.flag_loop is not None:
            IND.append(i.flag_loop)
            IO.append(i)
        else:
            IND.append(i.flag_loop)
            IO.append(i)
    if IND[0] != IND[1]:
        
        if 'START' in IND:
            
            for co in self.borders:
                if co != self.name and co != 'START':
                    co.flag = self.name
            IO[IND.index('START') - 1].source = True
        elif (self.name in IND) and (None in IND):
            IO[IND.index(self.name) - 1].source = True
        else:
            for co in self.borders:
                if co != 'D':
                    co.flag = 'D'
            if None in IND:
                IO[IND.index(None)].source = True
            else:
                IO[IND.index('D')].source = True
        for i in self.borders:
            if i.source:
                i.reconstruc_path(i)


def START(self):  # Initialise les bordures de la carte
    for i in self.borders:
        i.reconstruc_path(i)


###############################################################################
#                          Affichage d'une Carte                              #
###############################################################################
def aff_ch(card, special, name):
    C = [True for creat in range(14)]
    
    HELLO_I = [K.inputo for K in card]
    HELLO_O = [K.outputo for K in card]
    
    PATH = []
    COM = []
    
    for K, connect_I, connect_O in zip(card, HELLO_I, HELLO_O):
        if not (K.name in PATH):
            PATH.append(K.name)
            
            for CI in connect_I:
                
                if CI in card:
                    if COM == [] and CI != []:
                        COM.append(K)
                    
                    if COM != [] and (K in COM):
                        for CI_ in connect_I:
                            if CI_ in card:
                                if not (CI_ in COM):
                                    COM.append(CI_)
            for CO in connect_O:
                
                if CO in card:
                    if COM == [] and CO != []:
                        COM.append(K)
                    
                    if COM != [] and (K in COM):
                        for CO_ in connect_O:
                            if CO_ in card:
                                if not (CO_ in COM):
                                    COM.append(CO_)
    
    C[4], C[5], C[6], C[9], C[10] = False, False, False, False, False
    if not ('up' in PATH):
        C = [not val for val in C]
    
    lock = [val for val in C]
    
    C[3], C[7], C[8], C[9], C[10] = False, False, False, False, False
    if not ('down' in PATH):
        C = [not c if l is True else False for l, c in zip(lock, C)]
    
    lock = [val for val in C]
    
    C[1], C[5], C[7], C[9], C[11] = False, False, False, False, False
    if not ('left' in PATH):
        C = [not c if l is True else False for l, c in zip(lock, C)]
    
    lock = [val for val in C]
    
    C[2], C[6], C[8], C[9], C[11] = False, False, False, False, False
    if not ('right' in PATH):
        C = [not c if l is True else False for l, c in zip(lock, C)]
    
    if len(COM) == 4:
        C = [False for val in C]
        C[0] = True
    
    if len(COM) == 2 and C[12]:
        C = [False for val in C]
        NAME = [K.name for K in COM]
        
        if "up" in NAME and "left" in NAME or "down" in NAME and "right" in NAME:
            C[12] = True
        elif "up" in NAME and "right" in NAME or "down" in NAME and "left" in NAME:
            C[13] = True
        elif "up" in NAME and "down" in NAME or "right" in NAME and "left" in NAME:
            C[11] = True
    
    if len(COM) == 0:
        C = [False for val in C]
        C[9] = True
    
    center = "╬" * C[0] + "╠" * C[1] + "╣" * C[2] + "╩" * C[3] + "╦" * C[4] + "╔" * C[5] + "╗" * C[6] + "╚" * C[
        7] + "╝" * C[8] + "░" * C[9] + "═" * C[10] + "║" * C[11] + '▚' * C[12] + '▞' * C[13]
    if special == 'DOOR':
        center = 'G'
        if name == 'BLUE':
            center = 'B'
    
    if special == 'cristaux':
        center = 'C'
    if special == 'START':
        center = 'S'
    if special == 'PEPITE':
        center = 'G'
    if special == 'PIERRE':
        center = 'P'
    
    aff1 = "┏━" + ("║" if "up" in PATH else "━") + "━┓"
    aff2 = "┃ " + ("║" if "up" in PATH else " ") + " ┃"
    aff3 = ("══" if "left" in PATH else "┃ ") + center + ("══" if "right" in PATH else " ┃")
    aff4 = "┃ " + ("║" if "down" in PATH else " ") + " ┃"
    aff5 = "┗━" + ("║" if "down" in PATH else "━") + "━┛"
    
    return [aff1, aff2, aff3, aff4, aff5]
