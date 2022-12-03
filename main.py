# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:00:38 2022

@author: coren
"""
#from abc import ABC  #, abstractmethod
    
from player import Human
from board_game import BordGame
from Card import CardActionExtension,CardAction

        
P1= Human("Moi")
P2= Human("Cible")
P_list=[P1,P2]
A1 = CardActionExtension("Cassage de Wagon","Cette carte casse la pioche de la cible","impact_tools")

A2 = CardAction("Reparation Wagon Pioche","Cette carte casse la pioche de la cible","impact_tools")

A3 = CardActionExtension("Eboulement","Cette carte casse la pioche de la cible","collapsing")



A2.impact_tools(P_list)




mab = BordGame()
W1 = [True,True,True,True]

mab.add_card(W1,[0,0])
mab.add_card(W1,[5,10])
mab.add_card(W1,[1,1])
mab.add_card(W1,[-5,2])
mab.add_card(W1,[-4,-5])

mab.del_card([5,10])