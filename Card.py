# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:00:38 2022

@author: coren
"""

    

class card_action:
    def __init__(self,nom,description,effet):
        self.nom = nom
        self.description = description
        if hasattr ( card_action , effet ) :
            self.effet = getattr(card_action,effet)
        else :
            self.effet = True
        
    def __str__(self):
        res = "Le nom de cette carte action est : "+self.nom
        res += "\n"+self.description
        
        return res
        
    def quel_joueur():
        print("Sur quel joueur voulez vous appliquer l'effet (taper le chiffre)")
        #mettre une liste de joueur en mode : 1- JeanIve 2-Rodolphe 3-......
        #return joueur
    def break_pioche():
        print("1")
    def break_lampe():
        return print("test")
    
class card_action_extension(card_action):
    
    def __init__(self,nom,description,effet):
        super().__init__(nom,description,effet)
        if self.effet :
            self.effet = getattr(card_action_extension,effet )
        
    def voleur():
        return print("Ceci est un vol")
       
            
"""
class card_chemins:
    def __init__(self,bordure,special):
        self.bordure = bordure
        self.special = special #non destructible si special, spawn et gold
        self.A = []
        
        a activer si on a mis l'extension
        if extension:
            self.gemmes
        
    
    @property
    def bordures(self):
        return self.bordure

class card_role:
    def __init__(self):

        self.A = []
"""
        
        
C1 = card_action_extension("Pioche Cassée","Cette carte casse la pioche de la cible","break_pioche")
C1.effet()
#C1.effet = getattr(effet,"break_pickaxe")
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