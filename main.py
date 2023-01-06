# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:00:38 2022

@author: coren
"""
from sys import exit
from scripts.player import Human
from scripts.card import input_player #nous réutilisons la fonction input player de card.py
from scripts.game import game_handler,readfile

###############################################################################
#                                Fonctions                                    #
###############################################################################

        
def init_player(extension): #Gere la creations des Joueurs via la saisie de leur nom, avec une résistance prévu a toute épreuve, normalement...
    list_players = []
    print("\nSaisir 'STOP' pour forcer l'arret.\nNe rien taper (ou Ctrl+C), si le nombre de joueur minimum est atteint, pour poursuivre vers l'initialisation.")
    while True :
        try:  # redemande jusqu'a validité
            New_input = input("Taper le nom d'un joueur : ")
            New_input = New_input.strip()#enlève les espaces au début/fin
            if New_input == "" : raise KeyboardInterrupt #fin de saisie si rien n'est envoyé et que 2 ou 3j sont crées 
            if New_input.upper() == "STOP" : exit() #Quitte de force la saisie, utilse car KeyboardInterrupt sert a continuer, car plus rapide en test/jeu
            if len(New_input) > 20 : raise ValueError
            for player in list_players : 
                if (player.name.lower() == New_input.lower()) : 
                    raise ValueError
            list_players.append(Human(New_input))
            if (len(list_players)==10 and not(extension) )or(len(list_players)==12 and extension) : raise KeyboardInterrupt
            
        except ValueError:
            print(f'❌ Erreur, le nom "{New_input}" est déja utilisé ou trop long (20 charactères max), veuillez en séléctionner un autre.')
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

def recap(P_list,nb_manches):#Fait le recap en fin de manche et regarde si 3 rounds sont passer
    readfile('..\\ressources\\SaboteurTxt.txt',2)
    list_players.sort(key=lambda player: player.score, reverse=True)
    [(print(i, ': ', player.name,'(',player.role.name,')','[',player.score,'pts]', sep='', end='\n')) for i, player in enumerate(list_players, 1)]
    print(f"\n{list_players[0].name} à un avantage de {list_players[0].score-list_players[1].score}pts comparer à {list_players[1].name}.")
    
    if nb_manches >3 :
        readfile('..\\ressources\\SaboteurTxt.txt',3)
        print(f"\nLe grand gagnant est {list_players[0].name} !! \nFélicitation, en espérant être ré-exécuter prochainement.\n Et n'oubliez pas de rester zen, comme mon code source")
        return False
    print("\n[1] Continuez la partie\n[0] /!\ Quittez le programme (Ctrl + C)\n")
    input_player(0, 1)
    return True


 ###############################################################################
 #                                   Main                                      #
 ###############################################################################  

while True : #Menu principal
    readfile('..\\ressources\\SaboteurTxt.txt')
    res_input = input_player(0, 3)
    if res_input == 1 :
         readfile('..\\ressources\\PresentationSubMenu.txt')
         readfile('..\\ressources\\PresentationSubMenu.txt',input_player(0, 2))
         input_player(0, 1)
    elif res_input == 2:
        extension = False
        break
    elif res_input == 3:
        extension = True
        break
#initialisation de player
list_players = init_player(extension)
nb_manches = 1 #On fera forcement une manche
run_game = True
P_list = list_players.copy()
#Boucle Game Running
while run_game :
    readfile('..\\ressources\\SaboteurTxt.txt',1)
    round_done = game_handler(extension,P_list)
    if round_done : nb_manches +=1 
    else : break
    run_game = recap(list_players,nb_manches)

         
