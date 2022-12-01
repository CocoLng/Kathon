# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:00:38 2022

@author: coren
"""
from abc import ABC  #, abstractmethod
    
class Card(ABC):
    def __init__ ( self , nom , description ) :
        self.nom = nom
        self.description = description
        
                
    def __str__(self):
        res = "o-----o "+self.nom+" o-----o"
        res += "\n"+self.description
        
        return res
    
class CardAction(Card):
    def __init__(self,nom,description,effet):
        super().__init__(nom,description)
        if hasattr ( CardAction , effet ) :
            self.effet = getattr(CardAction,effet)
        else :
            self.effet = True

        
    def quel_joueur():
        print("Sur quel joueur voulez vous appliquer l'effet (taper le chiffre)")
        #mettre une liste de joueur en mode : 1- JeanIve 2-Rodolphe 3-......
        #return joueur  
    def break_pioche():
        print("Jtai cassée")
    def break_lampe():
        return print("test")
    
class CardActionExtension(CardAction):
    def __init__(self,nom,description,effet):
        super().__init__(nom,description,effet)
        if self.effet:
            self.effet = getattr(CardActionExtension,effet )
        
    def voleur():
        return print("Ceci est un vol")
       
            

class CardChemins(Card):
    def __init__(self,nom,description,bordure,special):
        super().__init__(nom,description)
        self.bordure = bordure
        self.special = special #non destructible si special, spawn et gold        
    
    @property
    def bordures(self):
        return self.bordure


class CardRole(Card):
    def __init__(self,nom,description):
        super().__init__(nom,description)

        
        
C1 = CardActionExtension("Pioche Cassée","Cette carte casse la pioche de la cible","break_pioche")
C1.effet()
CR = CardRole("Mineur", "Tu mines")
#C1.effet = getattr(effet,"break_pioche")
#doSomething = getattr(user, 'doSomething')
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