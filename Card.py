# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:00:38 2022

@author: coren
"""
from abc import ABC  #, abstractmethod
from player import Humain
    
class Card(ABC):
    def __init__ ( self , name , description ) :
        self.name = name
        self.description = description

           
    def __str__(self):
        res = "o-----o "+self.name+" o-----o"
        res += "\n"+self.description
        
        return res
    
class CardAction(Card):
    def __init__(self,name,description,effect=True):#par defaut effet est a définir(True)
        super().__init__(name,description)
        self.effect = effect
        
    @property
    def effect ( self ) :
        return self.__effect
    @effect.setter
    def effect ( self,effect ) :
        if hasattr ( CardAction , effect ) :
            self.__effect = getattr(CardAction,effect)
             
        
    def target_player(self):
        print(f'Sur quel joueur voulez vous appliquer {self.name} (taper le chiffre)')
        #mettre une liste de joueur en mode : 1- JeanIve 2-Rodolphe 3-......
        return P1
        
    def try_effect(self,effect,Target_P):
        if not effect in Target_P.statu:
            return True #si le joueur n'as pas déja l'effet alors on peut lui mettre
        return False #sinon signaler que c'est impossible
    
###############################################################################
#                           Break & Repair Outils                             #
###############################################################################
   

    def breaker(self,effect_play,Target_P):
        Done = False
        if self.try_effect(effect_play,Target_P):
            Target_P.statu.append(effect_play)
            #Target_P.supp_carte()
            print(f'{effect_play} de {Target_P.name} a était cassée 👾')
            Done = True
        return Done
        
    def repair(self,effect_play,Target_P):
        Done = False
        if not(self.try_effect(effect_play,Target_P)):
            Target_P.statu.remove(effect_play)
            #Target_P.supp_carte()
            print(f'{effect_play} de {Target_P.name} a était réparée 🔧')
            Done = True
        return Done
        
 
    def break_pickaxe(self):
        Target_P = self.target_player() 
        self.breaker("Pickaxe",Target_P)
    def break_light(self):
        Target_P = self.target_player() 
        self.breaker("Light",Target_P)
    def break_cart(self):
        Target_P = self.target_player() 
        self.breaker("Cart",Target_P)

    def repair_pickaxe(self): 
        Target_P = self.target_player() 
        self.repair("Pickaxe",Target_P)
    def repair_light(self):
        Target_P = self.target_player() 
        self.repair("Light",Target_P)
    def repair_cart(self):
        Target_P = self.target_player() 
        self.repair("Cart",Target_P)

    def repair_pickaxe_light(self):
        Target_P = self.target_player() 
        self.repair("Pickaxe",Target_P)
        self.repair("Light",Target_P)
    def repair_cart_light(self):
        Target_P = self.target_player() 
        self.repair("Cart",Target_P)
        self.repair("Light",Target_P)
    def repair_pickaxe_cart(self):
        Target_P = self.target_player() 
        self.repair("Pickaxe",Target_P)
        self.repair("Cart",Target_P)

###############################################################################
#                         Avalanche & Plan Secret                             #
###############################################################################

    def collapsing(self):
        self.repair("Light","Pickaxe")
        
    def secret_plan(self):
        self.repair("Light","Cart")
    
class CardActionExtension(CardAction):
    def __init__(self,name,description,effect):
        super().__init__(name,description,effect)
        self.effect = effect
        
    @property
    def effect ( self ) :
        return self.__effect
    @effect.setter
    def effect ( self,effect ) :
        if effect:#par defaut effet est a définir(True)
        #si l'effet n'est  pas  contenue dans CardAction alors on regarde s'il l'ai dans celle ci
            if hasattr ( CardActionExtension , effect ) :
                self.__effect = getattr(CardActionExtension,effect)

        
    def voleur():
        return print("Ceci est un vol")
       
            

class CardChemins(Card):
    def __init__(self,name,description,bordure,special):
        super().__init__(name,description)
        self.bordure = bordure
        self.special = special #non destructible si special, spawn et gold        


class CardRole(Card):
    def __init__(self,name,description):
        super().__init__(name,description)
        
class CardReward(Card):
    def __init__(self,name,description,pepite):
        super().__init__(name,description)
        self.pepite = pepite

        
P1= Humain("Jeanazsd",2)
C1 = CardActionExtension("Cassage de Pioche","Cette carte casse la pioche de la cible","break_pickaxe")
C2 = CardActionExtension("Réparage de Pioche","Cette carte casse la pioche de la cible","repair_pickaxe_light")
# C1.effect()
# CR = CardRole("Mineur", "Tu mines")
"""
 ...... .. ......... .. ......... .. .. ............................................. ......... .. .
................................... .:!!:...........................................................
................................ .:!JP?:............................................................
.............................. .^?Y55~ .............................................................
............................. ^?J?5Y: ..............................................................
........................... .7J!?5J.................................................................
..........................:75G?J57 ...........J!:?^.................................................
........................ ^55P5PGP7^:.  .. .?:.....?^ ...............................................
.........................P5GJ??5GY5YJ?!:..?J.  ...!5:.. ............................................
........................:GPGPP5G5YYYYY55YY!:^~7JJYY55J?~............................................
........................~PYYPY7?JY5555YYPPPJY5YYYYYYYJ755: .........................................
....................... Y5YY5.  ..:^~!7P5P5YYY5Y5PJPYYJ?JY5~ .......................................
.......................:PYYP^ ......:.^GGP?!77777G5PJ77???GP^:. ...  ...............................
...................... !PJP! ......J?JJY#Y777775?J?!!P?~~~~7P5Y55YJJ!:...  .........................
...................... ?55J .......77JYY!~~^^^^7??JY?YJ??!~^~PG&BBGGBJJJ?77~:.......................
...................... JP5........ :~~57^~~7???7???7777!!J?~!5B#&#BGYJJJJPP5? ......................
...................... ?B^ ..... ^J5YP5J7!~7J?7!~~~~~~~~^:7J~?5&B#?7JY555P?5^ ......................
.......................~Y ......^PYYJP!!5PY777Y7~~~~~~~~~::YJJP#B#! ..~7J5?^ .......................
............................... YPYY5B5~77!!!!~~~~~~~~~~~^:YPP#BB#^ ..  ............................
................................J55?YGP5??7!~~~~~~~~~~~~~~~PG??5BY..................................
...............................^~5Y?PGP5P5YJ?7!~~~~~~~~~~~JPPP~!!...................................
...............................GBBBBB#PPPGBBGGP5YJ?!~~~~~JBGGB?~ ...................................
.............................. J#BBGBGGBPPBBBGPPGGGGPJ~~YG55PG#G....................................
.............................. :GBBPBGB#GGGBBGGGGGGGGBPPBGGGPP#Y....................................
................................P#BB#GPBGPGBBGPPPPPPPPGPPPPGB##~ ...................................
.............................. ^G#B##BGBBB#BGPPPPPPPPPPPPGGG#5?.....................................
................................:?Y7^GPPPPPGGGPJ??JJJPBBBGGB?  .....................................
..................................   5G5PBG57^.  .   .?PYYP? .......................................
.................................... ?5JYJ~. ..........Y5P7  .......................................
.................................... 7BGY~:........... J##GPJ~......................................
.. .. ...... .. .. ...... .. .. .....?BBB#B5~ ..... .. ^7!77!^.. .. ......... .. ...... .. .. ......
"""