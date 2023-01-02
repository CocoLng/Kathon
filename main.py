# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:00:38 2022

@author: coren
"""
import os
from card import input_player #nous réutilisons la fonction input player de card.py


def readfile(path_join,part_explain = 0):
    with open(os.path.join(os.path.dirname(__file__),path_join),'r') as f: 
        f_split = f.read().split("SUB_EXPLAIN")
        print(f_split[part_explain])
        
def init_player(extension):
    list_players = []
    print("\nSaisir 'STOP'(ou Ctrl+C) pour arreter la saisie, ne rien taper entraine egalement l arret")
    while True :
        try:  # redemande jusqu'a validité
            New_input = input("Taper le nom d'un joueur : ")
            New_input = New_input.strip()
            if New_input == "" : raise KeyboardInterrupt 
            if New_input.upper() == "STOP" : raise KeyboardInterrupt
            list_players.append(New_input)
            if (len(list_players)==10 and not(extension) )or(len(list_players)==12 and extension) : raise KeyboardInterrupt
        except ValueError:
            print(f'❌ Valeur incorrecte, veuillez réessayer entre {min} et {max}\n')
            continue
        except KeyboardInterrupt:
            if (len(list_players)<3 and not(extension) )or(len(list_players)<2 and extension) : 
                print("Le nombre de joueurs minimum n'est pas atteint, veuillez continuer")
                continue
            print("\nFin de la saisie des Joueurs, voici la liste :")
            [print(i, ': ', x, sep='', end='  ') for i, x in enumerate(list_players, 1)]
            break
   
while True : 
    readfile('ressources\\SaboteurTitle.txt')
    res_input = input_player(0, 3)
    if res_input == 1 :
         readfile('ressources\\PresentationSubMenu.txt')
         readfile('ressources\\PresentationSubMenu.txt',input_player(0, 2))
         input_player(0, 1)
    if res_input == 2:
        extension = False
        break
    if res_input == 3:
        extension = True
        break

init_player(extension)
         

# with open(os.path.join(os.path.dirname(__file__),'ressources\\SaboteurTitle.txt'),'r') as f: # The with keyword automatically closes the file when you are done
#     print (f.read())
    
# 

# with open(os.path.join(os.path.dirname(__file__),'ressources\\SaboteurTitle.txt'),'r') as f: # The with keyword automatically closes the file when you are done
#     print (f.read())
        
