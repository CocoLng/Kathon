# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:00:38 2022

@author: coren
"""
from abc import ABC
from sys import exit
from random import shuffle
import types
import os
import detect_region


path_init = os.path.join(os.path.dirname(__file__),'ressources\\card_ini.txt')
###############################################################################
#                              Deck                                           #
###############################################################################
"""
Name correspond au nom du deck que nous souhaitons crée, il doit s'appeler comme ceci :
    ACTION / CHEMIN / ROLE / REWARD
"""
class Deck:
    def __init__(self, name,extension=[False,False]):  # chaque carte possède un nom et une description
        self.name=name    
        self.extension = extension
        self.list_card= []
        self.load_cards()
        
    def shuffle(self):
        return shuffle(self.list_card)    
        
    def load_cards(self):
        status=None
        with open(path_init,'r') as f: #ferme automatiquement le fichier a la fin de la lecture
            for line in f:
                line = line.strip()
                if (line == self.name and self.extension[1]==False)or(line == "EXTENSION" and self.extension[0]==True):
                     status = self.name
                     i = 1
                elif line == "EXTENSION" and self.extension[0]==False:
                    status = None
                elif line !="" and status !=None:
                    line = line.split(';')
                    if status == "ACTION" :
                        globals()['A%s' % i] = CardAction(line[1],line[2],line[3])
                        self.list_card+=int(line[0])*[globals()['A%s' % i]]                    
                    elif status == "ROLE":
                        globals()['A%s' % i] = CardRole(line[1],line[2],line[3])
                        self.list_card+=int(line[0])*[globals()['A%s' % i]]
                    i+=1
 
    def __str__(self):
        res = "o-----o "+ self.__class__.__name__ +" o-----o"
        res += "\n"+"Ceci est un deck de cartes"
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

class CardChemins(Card):
    def __init__(self, name, description, borders, special="", reveal=False,indestructible = False):
        super().__init__(name, description)
        self.borders = borders
        self.reveal = reveal
        self.special = special  # non destructible si special, spawn et gold

class CardRole(Card):
    def __init__(self, name, description):
        super().__init__(name, description)

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
#Les méthodes si dessous sont chargès dans tous nos objets, car essentiels au fonctionnement de nos méthodes effect

    def target_player(self):
        print(f'Sur quel joueur voulez vous appliquer {self.name} (taper le chiffre)')
        [print(i, ': ', x.name, sep='', end='  ') for i, x in enumerate(self.arg[1], 1)]
        return self.arg[1][self.input_player(1, len(self.arg[1]))-1]

    def input_player(self, min, max):  # demande un input entre min et max et return le res
        while True:
            try:  # redemande jusqu'a validité
                selected = input('\nTaper le chiffre désiré : ')
                selected = int(selected)
                if selected < min or selected > max:
                    raise ValueError
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

    def has_effect(self, effect, Target_P):
        if effect in Target_P.status:  # regarde si le Target Player possède deja l'effet
            return True
        return False

    def edit_status(self, ajout, effect_play, Target_P):
        Done = False
        # si le joueur n'as pas déja l'effet alors on peut lui mettre
        if ajout and not(self.has_effect(effect_play, Target_P)):
            Target_P.status.append(effect_play)
            Done = True
        # si on veut lui retirer(ajout=False), on regarde que la cible possède l'effet
        elif not(ajout) and self.has_effect(effect_play, Target_P):
            Target_P.status.remove(effect_play)
            Done = True
        return Done
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
        return self.edit_status(True, Name_list[2], Target_P)
    elif len(Name_list) == 5:  # Si nous avons deux effet pour la réparation
        Done = self.edit_status(False, Name_list[4], Target_P)
    Done = Done or self.edit_status(False, Name_list[2], Target_P)
    return Done

###############################################################################
#                         Avalanche & Plan Secret                             #
###############################################################################

def collapsing(self):
    return True

def secret_plan(self):
    Done = False
    print("Quel carte souhaitez-vous visualiser ?\n 1-Haut 2-Milieu 3-Bas\n")
    selected = self.input_player(0, 3)
    #flip card
    print(selected)
    Done = True

###############################################################################
#                         Chargement d'une Extenion                           #
###############################################################################

def inspect(self):
    Done = False
    Target_P = self.target_player()
    print(Target_P.name)
    Done = True
    return Done

def switch_role(self):
    Done = False
    print("Séléctionnez un joueur qui vera sont role changer ?")
    Target_P = self.target_player()
    
    Done = True
    return Done

def switch_hand(self):
    Done = False
    print("Avec quel joueur souhaitez-vous inverser votre deck de cartes ?")
    Target_P1 = self.target_player()
    temp = Target_P1._Player__main
    Target_P1._Player__main =  self.arg[0]._Player__main
    self.arg[0]._Player__main = temp
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
        return self.edit_status(True, "Emprisonnement", Target_P)
    # si on emprisonne pas alors on libère
    return self.edit_status(False, "Emprisonnement", Target_P)

"""
Gère l'effet de vol et de retrait via la carte pas touche
A l'initialisation, le nom doit être "Voleur" pour activer le vol en fin de manche, choix libre pour le retirer
L'effet doit être "thief_handler"
"""

def thief_handler(self):
    if self.name == "Voleur":  # Réutilisation de edit_effet
        return self.edit_status(True, "Voleur", self.arg[0]) #applique l'effet voleur au joueur actuel
    Target_P = self.target_player()
    return self.edit_status(False, "Voleur", Target_P)


"""
Vous pouvez ajouter vos effet personnels ici, puis crée la carte en l'ajoutant dans /ressource/card_ini.txt
Il faudra, lors de l'initialisation, mettre dans effet le même nom que celle de la méthode'
"""
