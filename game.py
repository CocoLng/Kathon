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
            globals()['A%s' % i] = card.CardAction(line[0],line[1],line[2])
            i+=1
        
        