# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:00:38 2022

@author: coren
"""
#from abc import ABC  #, abstractmethod
    
from player import Human
#from board_game import BordGame
import Card
        
P1= Human("Moi")
P2= Human("Cible")
P_list=[P1,P2]


A3 = Card.CardActionExtension("Cassage de Wagon","Cette carte casse la pioche de la cible","impact_tools",P_list)
A2 = Card.CardAction("Reparation : Wagon & Pioche","Cette carte casse la pioche de la cible","impact_tools",P_list)

A1 = Card.CardActionExtension("Inspection","Cette carte casse la pioche de la cible","switch_hand",P_list)

#J'arrive pas a add de cartes
#P1.add_card(P1, A2)

print(A1.effect(A1))
# print(A2.effect)
# print(A1.effect)


# mab = BordGame()
# W1 = [True,True,True,True]

# mab.add_card(W1,[0,0])
# mab.add_card(W1,[5,10])
# mab.add_card(W1,[1,1])
# mab.add_card(W1,[-5,2])
# mab.add_card(W1,[-4,-5])

# mab.del_card([5,10])