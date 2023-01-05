from abc import ABC
from sys import exit
import types
import os
from scripts.detect_region import ConnectionEdge

from random import shuffle


path_init = os.path.join(os.path.dirname(__file__),'..\\ressources\\card_ini.txt')
###############################################################################
#                              Deck                                           #
###############################################################################
"""
Name correspond au nom du deck que nous souhaitons crée, il doit s'appeler comme ceci :
    ACTION_CHEMIN / ROLE / REWARD
"""
class Deck:
    def __init__(self, name,extension=[False,False],nb_players = 3):  # chaque carte possède un nom et une description
        self.name=name    
        self.extension = extension
        self.list_card= []
        self.load_cards(len(nb_players))
    def shuffle(self):
        return shuffle(self.list_card)  
    
    def draw_card(self,i=0):#sert pour la pioche d'une carte
        if len(self.list_card)==0 : return False#return False si le deck est vide
        return self.list_card.pop(i) #sinon envoie la première carte et la supprime
        
    def load_cards(self,nb_players):
        i = 1
        write = False
        status = None
        with open(path_init,'r') as f: #ferme automatiquement le fichier a la fin de la lecture
            for line in f:
                line = line.strip()
                if line == self.name:
                    status = self.name.upper()
                    if self.extension[1]==True:
                        write = False
                    else :
                        write = True
                elif line == "EXTENSION" and status == self.name and self.extension[0]==True :
                     write = True 
                elif status == self.name and ((line =="END") or (line == "EXTENSION" and self.extension[0]==False)): 
                    break
                elif line !="" and write:
                    line = line.split(';')
                    if status == "ACTION_CHEMIN" :
                        if len(line)==4:
                            self.list_card+=int(line[0])*[CardAction(line[1],line[2],line[3])]
                        else:
                            [self.list_card.append(CardChemin(line)) for i in range(int(line[0]))]
                    elif status == "ROLE":
                        if self.extension[0]==False:
                            nb = 3 #le nombre de chercheur de abse est définis a 3
                            if nb_players == 4 : nb +=1 #si il y a quatre joueur, nous passons a 4 chercheur
                            while  nb/nb_players < 0.7 : nb+=1 #la proportion de chercheur doit toujours est au moins de 70% dans la manche
                            if  line[2] == "saboteur" : nb = (nb_players-nb)+1 #formule pour obtenir le nombre de saboteur
                            self.list_card+=nb*[CardRole(line[0],line[1],line[2])]
                        else :
                            self.list_card+=int(line[0])*[CardRole(line[0],line[1],line[2])]
                        
                    elif status == "REWARD":
                        self.list_card+=int(line[0])*[CardReward(line[1],line[2],line[3])]
                    else :
                        print("Deck avec le nom de propriété indéfinis ! ERREUR")
                        exit()
                    i+=1

 
    def __str__(self):
        res = "o-----o "+ self.__class__.__name__ +":" +self.name + " o-----o"
        res += "\nCeci est un deck de cartes"
        res += "\nContient l'extension :"+self.extension
        return res

###############################################################################
#                             Structures Cartes                               #
###############################################################################

class Card(ABC):
    def __init__(self, name, description):  # chaque carte possède un nom et une description
        self.name = name
        self.description = description

    def __str__(self):
        res = "o-----o "+self.name+" o-----o"
        res += "\n"+self.description

        return res

class CardChemin(Card):
    def __init__(self, arg):
        super().__init__(arg[1], arg[2])

        self.is_start = arg
        self.special = arg
        self.reveal = arg
        self.config = list(arg[3].split(":"))
        self.port = list(arg[4].split(","))
        self.borders = self.port
        self.aff = True
        
        
    @property
    def special(self):
        return self.__special
    
    @special.setter
    def special(self,special):
        self.__special = None
        if len(special)>=7:
            self.__special = special[6]  # non destructible si special, spawn et gold
            
    @property
    def is_start(self):
        return self.__is_start
    
    @is_start.setter
    def is_start(self,is_start):
        self.__is_start = False
        if len(is_start)>=8 : 
            self.__is_start = bool(is_start[7])  
            
    @property
    def reveal(self):
        return self.__reveal
    
    @reveal.setter
    def reveal(self,reveal):
        #soit bool soit list
        self.__reveal = True
        try:
            if len(reveal)>=6:
                 if reveal[5] == 'False': 
                    self.__reveal = False            
        except TypeError:
                self.__reveal = reveal
                  
    @property
    def borders(self):
        return self.__borders
    
    @borders.setter
    def borders(self,port):
        self.__borders = []
        [self.__borders.append(ConnectionEdge(i,self.special , self.special=='START')) for i in port]
        for chemins,portes in zip(self.config,self.borders):
            [portes.connect(portes_) for connections, portes_ in zip(chemins,self.borders) if int(connections) ==1]

    @property
    def aff(self):
        if self.reveal:
            return self.__aff
        return ["┏━━━┓","┃   ┃","┃   ┃","┃   ┃","┗━━━┛"] 
    
    @aff.setter
    def aff(self,update):
        self.__aff = aff_ch(self.borders,self.special)

class CardRole(Card):
    def __init__(self, name, description,role):
        super().__init__(name, description)
        self.role = role

class CardReward(Card):
    def __init__(self, name, description, pepite):
        super().__init__(name, description)
        self.pepite = pepite
        
class CardAction(Card):
    # les cartes action sont des cartes avec un effet
    def __init__(self, name, description, effect, arg=None):#les cartes actions ne nécéssitent pas tous la listes des joueurs
        super().__init__(name, description)
        
        self.effect = types.MethodType(globals()[effect], self) #on ajoute la méthode contenant le nom effect dans notre object, les autres ne sont pas chargés car inutiles
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
    arg[1] contient la MAP
    """
    def target_player(self):
        print(f'Sur quel joueur voulez vous appliquer {self.name} (taper le chiffre)')
        [print(i, ': ', x.name, sep='', end='  ') for i, x in enumerate(self.arg[0], 1)]#laisse le joueur pouvoir se cibler
        return self.arg[0][input_player(1, len(self.arg[0]))-1]

# les fonctions si desous sont appelable par tous type de cartes

def has_effect(effect, Target_P):
    if effect in Target_P.status:  # regarde si le Target Player possède deja l'effet
        return True
    return False

def edit_status(ajout, effect_play, Target_P):
    Done = False
    # si le joueur n'as pas déja l'effet alors on peut lui mettre
    if ajout and not(has_effect(effect_play, Target_P)):
        Target_P.status.append(effect_play)
        Done = True
    # si on veut lui retirer(ajout=False), on regarde que la cible possède l'effet
    elif not(ajout) and has_effect(effect_play, Target_P):
        Target_P.status.remove(effect_play)
        Done = True
    return Done
    
def input_player(min, max):  # demande un input entre min et max et return le res #self remove pour test !!!
    while True:
        try:  # redemande jusqu'a validité
            selected = input('Taper le chiffre désiré : ')
            selected = int(selected)
            if selected < min or selected > max:
                raise ValueError
            if selected == 0 : raise KeyboardInterrupt #permet de quittez si 0 est entrer et que nous sommes dans le menu
            break
        except ValueError:
            print(f'❌ Valeur "{selected}" incorrecte, veuillez réessayer entre {min} et {max}\n')
            continue
        except KeyboardInterrupt:
            print("\nVous quittez le programme, aurevoir")
            exit()
        else:
            print('break, Erreur inconnue')
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
Le nom[3] nous dit quel est l'outil ciblé'
L'effet est lui stocker dans l'attribut "effet" qui pointe vers la méthode "impact_tools"
Donc effect = impact_tools a l'initialisation pour appeler la fonction
"""

def impact_tools(self):
    Done = False
    Target_P = self.target_player()
    Name_list = self.name.split()
    if Name_list[0] == "Cassage":  # Si nous ne cassons pas nous réparons
        return edit_status(True, Name_list[2], Target_P)
    elif len(Name_list) == 5:  # Si nous avons deux effet pour la réparation
        Done = edit_status(False, Name_list[4], Target_P)
    Done = Done or edit_status(False, Name_list[2], Target_P)
    return Done

###############################################################################
#                         Avalanche & Plan Secret                             #
###############################################################################

def collapsing(self):
    pos = self.arg[0][0].ask_pos()
    return self.arg[1].del_card(pos)

def secret_plan(self):
    while True:
        print("Quel carte souhaitez-vous visualiser ?\n 1-Haut 2-Milieu 3-Bas\n")
        selected = input_player(1, 3)
        if selected == 1 and not(self.arg[1]._BoardGame.__main[8][2].reveal): #on vérifie que la carte n'est pas déja visible, on sait jamais..
            print(f"La carte du Haut(8,2) est un/une {self.arg[1][8][2].name}")
            return True
        elif selected == 2 and not(self.arg[1]._BoardGame.__main[8][0].reveal): 
            print(f"La carte du Miieu(8,0) est un/une {self.arg[1][8][0].name}")
            return True
        elif selected == 3 and not(self.arg[1]._BoardGame.__main[8][-2].reveal): 
            print(f"La carte en Bas(8,-2) est un/une {self.arg[1][8][-2].name}")
            return True
        print("\nCette carte est déja visible... En choisir une autre")

###############################################################################
#                         Chargement d'une Extenion                           #
###############################################################################

def inspect(self):
    Done = False
    Target_P = self.target_player()
    print(f"SPOILER ALERTE :\n{Target_P.name} est un {Target_P.role}.")
    Done = True
    return Done

def switch_role(self):
    Done = False
    print("Séléctionnez un joueur qui vera sont role changer ?")
    Target_P = self.target_player()
    temp = Target_P.role
    Target_P.role =  self.arg[0][0].role
    self.arg[0][0].role = temp
    Done = True
    return Done

def switch_hand(self):
    Done = False
    print("Avec quel joueur souhaitez-vous inverser votre deck de cartes ?")
    Target_P1 = self.target_player()
    temp = Target_P1.main
    Target_P1.main =  self.arg[0][0].main
    self.arg[0][0].main = temp
    Done = True
    return Done

"""
Gère l'effet d'emprisonnement et de libération en réutilisant edit_effet
A l'initialisation, le nom doit être "Emprisonnement" pour mettre en prison, choix libre pour libérer
L'effet doit être "jail_handler"
"""

def jail_handler(self):
    Target_P = self.target_player()
    if self.name == "Emprisonnement":  # Réutilisation de edit_effet
        return edit_status(True, "Emprisonnement", Target_P)
    # si on emprisonne pas alors on libère
    return edit_status(False, "Emprisonnement", Target_P)

"""
Gère l'effet de vol et de retrait via la carte pas touche
A l'initialisation, le nom doit être "Voleur" pour activer le vol en fin de manche, choix libre pour le retirer
L'effet doit être "thief_handler"
"""

def thief_handler(self):
    if self.name == "Voleur":  # Réutilisation de edit_effet
        return edit_status(True, "Voleur", self.arg[0][0]) #applique l'effet voleur au joueur actuel
    Target_P = self.target_player()
    return edit_status(False, "Voleur", Target_P)


"""
Vous pouvez ajouter vos effet personnels ici, puis crée la carte en l'ajoutant dans /ressource/card_ini.txt
Il faudra, lors de l'initialisation, mettre dans effet le même nom que celle de la méthode'
"""


###############################################################################
#                          Affichage d'une Carte                              #
###############################################################################
def aff_ch(card,special):
    C = [True for creat in range(14)]
    
    HELLO_I = [K.inputo for K in card]
    HELLO_O = [K.outputo for K in card]
                    
    PATH = []
    COM = [] 

    for K,connect_I,connect_O in zip(card,HELLO_I,HELLO_O):
        if not(K.name in PATH):
            PATH.append(K.name)
            
            for CI in connect_I:

                if CI in card:
                    if COM == [] and CI != []:
                        COM.append(K)
           
                    if COM != [] and (K in COM):
                        for CI_ in connect_I:
                            if CI_ in card:
                                if not(CI_ in COM):
                                    COM.append(CI_)
            for CO in connect_O:
                        
                if CO in card:
                    if COM == [] and CO != []:
                        COM.append(K)
                        
                    if COM != [] and (K in COM):
                        for CO_ in connect_O:
                            if CO_ in card:
                                if not(CO_ in COM):
                                    COM.append(CO_)
                                    
                                      
    C[4],C[5],C[6],C[9],C[10] = False,False,False,False,False
    if not('up' in PATH):
        C = [not(val) for val in C]
    
    lock = [val for val in C]
        
    C[3],C[7],C[8],C[9],C[10] = False,False,False,False,False
    if not('down'in PATH):
        C = [not(c) if l == True else False for l,c in zip(lock,C)]
    
    lock = [val for val in C]
        
    C[1],C[5],C[7],C[9],C[11] = False,False,False,False,False
    if not('left' in PATH):
        C = [not(c) if l == True else False for l,c in zip(lock,C)]
    
    lock = [val for val in C]
        
    C[2],C[6],C[8],C[9],C[11] = False,False,False,False,False
    if not('right' in PATH):
        C = [not(c) if l == True else False for l,c in zip(lock,C)]
    
    
    if len(COM) == 4:
        C = [False for val in C]
        C[0] = True
        NAME = [K.name for K in COM]
        if "up" in NAME and "left" in NAME:
            C[12] = True                        
        elif"up" in NAME and "Down" in NAME:
            C[13] = True
            
        
    if len(COM) == 0:
        C = [False for val in C]
        C[9] = True

            
    center = "╬"*C[0] + "╠"*C[1] + "╣"*C[2] + "╩"*C[3] + "╦"*C[4] + "╔"*C[5] + "╗"*C[6] + "╚"*C[7] + "╝"*C[8] + "░"*C[9] + "═"*C[10]+"║"*C[11] + '▚'*C[12] + '▞'*C[13]
    if special == 'blue_door':
        center = 'B'
    if special == 'green_door':
        center = 'G'
    if special == 'cristaux':
        center = 'C'
    if special == 'START':
        center = 'S'
    if special == 'PEPITE':
        center = 'G'
    if special == 'PIERRE':
        center = 'P'
    
    aff1 = "┏━"+ ("║" if "up" in PATH else "━") + "━┓" 
    aff2 = "┃ "+ ("║" if "up" in PATH else " ") + " ┃" 
    aff3 = ("══" if "left" in PATH else "┃ ")+ center + ("══" if "right" in PATH else " ┃") 
    aff4 = "┃ "+("║" if "down" in PATH else " ")+ " ┃" 
    aff5 = "┗━"+("║" if "down" in PATH else "━")+ "━┛" 
    
    return [aff1,aff2,aff3,aff4,aff5] 
 