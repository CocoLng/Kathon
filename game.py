# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 12:27:55 2022

@author: coren
"""
import card
from player import Human
import os

cur_path = os.path.dirname(__file__)
new_path = os.path.join(cur_path,'ressources\\card_ini.txt')

P1= Human("Moi")
P2= Human("Cible")
P_list=[P1,P2]

P_current= P1

arg=[P_current,P_list]

with open(new_path,'r') as f:
    for line in f:
        line = line.strip()
        if line == ("ACTION" or "CHEMIN" or "ROLE" or "REWARD"):
             status = line
             i = 1
        elif line == "EXTENSION" :
            break
        elif status == "ACTION" and line !="":
            line = line.split(';')
            globals()['A%s' % i] = card.CardAction(line[1],line[2],line[3])
            i+=1
        
A3 = card.CardAction("Cassage de Wagon","Cette carte casse la pioche de la cible","impact_tools")
A2 = card.CardAction("Reparation : Wagon & Pioche","Cette carte casse la pioche de la cible","impact_tools")

A1 = card.CardAction("Inspection","Cette carte casse la pioche de la cible","switch_hand")

#J'arrive pas a add de cartes dans player
#P1.add_card(P1, A2)
A3.arg = arg
print(A3.effect(A3))