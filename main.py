# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:00:38 2022

@author: coren
"""
import os
from scripts.player import Human
from scripts.card import input_player #nous réutilisons la fonction input player de card.py
from scripts.game import init_round

def readfile(path_join,part_explain = 0):
    with open(os.path.join(os.path.dirname(__file__),path_join),'r') as f: 
        f_split = f.read().split("SUB_PART")
        print(f_split[part_explain])
        
def init_player(extension):
    list_players = []
    print("\nSaisir 'STOP'(ou Ctrl+C) pour arreter la saisie, ne rien taper entraine également l'arrêt.")
    while True :
        try:  # redemande jusqu'a validité
            New_input = input("Taper le nom d'un joueur : ")
            New_input = New_input.strip()
            if New_input == "" : raise KeyboardInterrupt 
            if New_input.upper() == "STOP" : raise KeyboardInterrupt
            if New_input in list_players: raise ValueError
            list_players.append(Human(New_input))
            if (len(list_players)==10 and not(extension) )or(len(list_players)==12 and extension) : raise KeyboardInterrupt
        except ValueError:
            print(f'❌ Erreur, le nom "{New_input}" est déja utilisé, veuillez en séléctionner un autre.')
            continue
        except KeyboardInterrupt:
            if (len(list_players)<3 and not(extension) )or(len(list_players)<2 and extension) : 
                if extension  : New_input = 2-len(list_players)
                else : New_input = 3-len(list_players)
                print(f"\n❌ Le nombre de joueurs minimum n'est pas atteint, veuillez rajouter encore {New_input} joueurs.")
                continue
            print("\n\nFin de la saisie des Joueurs, voici la liste :")
            [(print('P',i, ': ', x.name, sep='', end='  ')) for i, x in enumerate(list_players, 1)]
            break
    return list_players
   
while True : 
    readfile('ressources\\SaboteurTxtMenu.txt')
    res_input = input_player(0, 3)
    if res_input == 1 :
         readfile('ressources\\PresentationSubMenu.txt')
         readfile('ressources\\PresentationSubMenu.txt',input_player(0, 2))
         input_player(0, 1)
    elif res_input == 2:
        extension = False
        break
    elif res_input == 3:
        extension = True
        break

list_players = init_player(extension)
nb_manches = 1
while True :
    readfile('ressources\\SaboteurTxtMenu.txt',1)
    Decks = init_round(extension,list_players)
    nb_manches +=1
    if nb_manches > 3 : break

         
