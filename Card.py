# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:00:38 2022

@author: coren
"""
from abc import ABC  #, abstractmethod
from player import Human
#from board_game import BordGame
    
class Card(ABC):
    def __init__ ( self , name , description ) : #chaque carte possède un nom et une description
        self.name = name
        self.description = description

           
    def __str__(self): 
        res = "o-----o "+self.name+" o-----o"
        res += "\n"+self.description
        
        return res
    
class CardAction(Card):
    def __init__(self,name,description,effect): #les cartes action sont des cartes avec un effet
        super().__init__(name,description)
        self.effect = effect
        
    @property
    def effect ( self ) :
        return self.__effect
    @effect.setter
    def effect ( self,effect ) :
        self.__effect = getattr(self.__class__,effect) #stock le pointeur de la function désirée
             
        
###############################################################################
#                           Fonctions Communes                                #
###############################################################################

    def target_player(self):
        print(f'Sur quel joueur voulez vous appliquer {self.name} (taper le chiffre)')
        #mettre une liste de joueur en mode : 1- JeanIve 2-Rodolphe 3-......
        return P1
    
    def input_player(self,min,max): #demande un input entre min et max et return le res
        while True:
            try: #redemande jusqu'a validité
                selected = input('Taper le chiffre désiré : ')
                selected = int(selected)
                if selected < min or selected > max:
                    raise ValueError
                break
            except ValueError :
                print(f'❌ Valeur "{selected}" incorrecte, veuillez réessayer entre {min} et {max}\n')
        return selected
        
    def has_effect(self,effect,Target_P):
        if effect in Target_P.statuts: #regarde si le Target Player possède deja l'effet
            return True 
        return False 
    
    def edit_effect(self,ajout,effect_play,Target_P):
        Done = False
        if ajout and not(self.has_effect(effect_play,Target_P)):#si le joueur n'as pas déja l'effet alors on peut lui mettre
            Target_P.statuts.append(effect_play)
            Done = True
        elif not(ajout) and self.has_effect(effect_play,Target_P):#si on veut lui retirer(ajout=False), on regarde que la cible possède l'effet
            Target_P.statuts.remove(effect_play)
            Done = True
        return Done
        
    
 
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
    Donc effect = impact_tools a l'inistialisation pour appeler la fonction
    """

    def impact_tools(self):
        Done = False
        Target_P = self.target_player()
        Name_list = self.name.split()
        if Name_list[0]=="Cassage" : # Si nous ne cassons pas nous réparons
            return self.edit_effect(True,Name_list[2],Target_P)
        elif len(Name_list)==5 : # Si nous avons deux effet pour la réparation
            Done =  self.edit_effect(False,Name_list[4],Target_P)
        Done =  Done or self.edit_effect(False,Name_list[2],Target_P)
        return Done       

###############################################################################
#                         Avalanche & Plan Secret                             #
###############################################################################

    def collapsing(self):
        Done = False
        #appel de la fonction pos
        #appelde la fct del carte if not special
        Done = True
        return Done
        
    def secret_plan(self):
        Done = False
        print("Quel carte souhaitez-vous visualiser ?\n 1-Haut 2-Milieu 3-Bas\n")
        selected = self.input_player(0,3)
        #flip card
        print(selected)
        Done = True
        
###############################################################################
#                         Chargement d'une Extenion                           #
###############################################################################    
class CardActionExtension(CardAction):
    def __init__(self,name,description,effect):
        super().__init__(name,description,effect)
     
    
    def inspect(self):
        Done = False
        Done = True
        return Done
    
    def switch_role(self):
        Done = False
        Done = True
        return Done
    
    def switch_hand(self):
        Done = False
        Done = True
        return Done
    
    """
    Gère l'effet d'emprisonnement et de libération en réutilisant edit_effet
    A l'initialisation, le nom doit être "Emprisonnement" pour mettre en prison, choix libre pour libérer
    L'effet doit être "jail_handler"
    """
    def jail_handler(self):
        Target_P = self.target_player()
        if self.name=="Emprisonnement" : # Réutilisation de edit_effet
            return self.edit_effect(True,"Emprisonnement",Target_P)
        return self.edit_effect(False,"Emprisonnement",Target_P)# si on emprisonne pas alors on libère
    
    """
    Gère l'effet de vol et de retrait via la carte pas touche
    A l'initialisation, le nom doit être "Voleur" pour activer le vol en fin de manche, choix libre pour le retirer
    L'effet doit être "thief_handler"
    """    
    def thief_handler(self):
        Target_P = self.target_player()
        if self.name=="Voleur" : # Réutilisation de edit_effet
            return self.edit_effect(True,"Voleur",Target_P)
        return self.edit_effect(False,"Voleur",Target_P)
     
"""
Vous pouvez ajouter vos effet personnels ici, puis crée la carte en l'ajoutant dans /ressource/card_ini.txt
Vous avez juste lors de l'initialisation a mettre dans effet le même nom que celle de la méthode'
"""       

class CardChemins(Card):
    def __init__(self,name,description,borders,special,reveal):
        super().__init__(name,description)
        self.borders = borders
        self.reveal = reveal
        self.special = special #non destructible si special, spawn et gold        


class CardRole(Card):
    def __init__(self,name,description):
        super().__init__(name,description)
        
class CardReward(Card):
    def __init__(self,name,description,pepite):
        super().__init__(name,description)
        self.pepite = pepite

        
P1= Human("Jeanazsd")
C1 = CardActionExtension("Cassage de Wagon","Cette carte casse la pioche de la cible","impact_tools")
C2 = CardAction("Reparation de Wagon et Pioche","Cette carte casse la pioche de la cible","impact_tools")