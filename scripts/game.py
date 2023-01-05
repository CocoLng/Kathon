# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 12:27:55 2022

@author: coren
"""
from random import shuffle
from scripts.card import input_player,Deck
from scripts.player import Human
from scripts.board_game import BoardGame
import os
from time import sleep

    
def game_handler(extension,P_list):
    Decks,MAP,WIN_CARD = init_round(extension, P_list)
    P_round = P_list.copy()
    #shuffle(P_round)
    repartition_card(extension,P_round,Decks[0])
    run_round(extension,P_round,MAP,Decks[0],WIN_CARD)
    return True
    
def cls_screen():
    os.system('cls' if os.name=='nt' else 'clear')
    
def readfile(path_join,part_explain = 0): #Permet de lire un fichier texte, ici principalement a but d'affichage
    with open(os.path.join(os.path.dirname(__file__),path_join),'r') as f: 
        f_split = f.read().split("SUB_PART")#Nous décomposons notre fichier tous les SUB_PART
        print(f_split[part_explain])
        
def next_player(P_round):
    readfile('..\\ressources\\SaboteurTxt.txt',4)
    print(f"\nC'est au tour de {P_round[0].name} !\n")
    input("Pressez une touche pour continuer, sinon on peut aussi attendre tranquillement")

    
def init_round(extension,P_list):
    pos = [[8,-2],[8,0],[8,2]]
    MAP = BoardGame()
    
    
    #Initialisation des decks
    Deck_ActionChemin = Deck("ACTION_CHEMIN",[extension,False],P_list)
    #connect la carte PEPITE a WIN
    WIN_CARD = Deck_ActionChemin.list_card[29]
    
    #init map,cartes initiales
    MAP.add_card(Deck_ActionChemin.draw_card(30),[0,0],True)
    L = [Deck_ActionChemin.draw_card(27) for i in range(3)]
    shuffle(L)
    [MAP.add_card(CARD,POS,True) for CARD,POS in zip(L,pos)]
    
    
    Deck_Role = Deck("ROLE",[extension,extension],P_list)
    Deck_Reward = Deck("REWARD",[extension,extension],P_list)
    Decks = [Deck_ActionChemin,Deck_Role,Deck_Reward]
    [shuffle(x.list_card) for x in Decks]
    
    #Effacement des status, et supression des cartes restantes
    [(player.status.clear(),player.main.clear()) for player in P_list]
    #assignement d'un role a chaque joueur, le deck role est déja mélangé
    for i,player in enumerate(P_list,1) : player.role=Deck_Role.list_card[i]
    
    return Decks,MAP,WIN_CARD

def repartition_card(extension,P_list,Deck):
    if extension:
        pass
    nb_P_repart = 7 -len(P_list)//2
    [(player.main.append(card) , Deck.list_card.pop(0)) for player in P_list for i,card in enumerate(Deck.list_card,1) if i<=nb_P_repart]


def run_round(extension,P_round,MAP,Deck_,WIN_CARD):
    tours = 0
    while WIN_CARD.borders[0].flag_loop == None and len(P_round) > 0:
        tours+=1
        print(f'tours: {tours}') 
        print(P_round[0].name,P_round[0].status)    
        print(MAP)
        while True:
            if P_round[0].play(P_round,MAP):
                break
        if not(P_round[0].get_card(Deck_)):
            if P_round[0].card_number == 0:
                P_round.pop(0)
        
        P_round = P_round[1:] + P_round[:1]
        cls_screen()
        sleep(1)
        next_player(P_round)
    return False
