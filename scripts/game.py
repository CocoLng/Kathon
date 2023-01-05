# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 12:27:55 2022

@author: coren
"""
from scripts.card import input_player,Deck
from scripts.player import Human


# P1=Human("1")
# P2=Human("2")
# P3=Human("3")
# P_list = [P1,P2,P3]
# P1.status = ["bug"]
# P3.status = ["baaaug"]

def init_round(extension,P_list):
    #Initialisation des decks
    Deck_ActionChemin = Deck("ACTION_CHEMIN",[extension,False],P_list)
    Deck_Role = Deck("ROLE",[extension,extension],P_list)
    Deck_Reward = Deck("REWARD",[extension,extension],P_list)
    Decks = [Deck_ActionChemin,Deck_Role,Deck_Reward]
    [x.shuffle() for x in Decks]
    
    #Effacement des status, et supression des cartes restantes
    [(player.status.clear(),player.main.clear()) for player in P_list]
    #assignement d'un role a chaque joueur, le deck role est déja mélangé
    for i,player in enumerate(P_list,1) : player.role=Deck_Role.list_card[i]
    
    repartition_card(extension,Decks[0],P_list)
    return Decks

def repartition_card(extension,Deck,P_list):
    if extension:
        pass
    
    nb_P_repart = 7 -len(P_list)//2
    [(player.main.append(card),Deck.list_card.pop(0)) for player in P_list for i,card in enumerate(Deck.list_card,1) if i<=nb_P_repart]


def run_round(extension,P_list):
    input_player(0, 1)
    pass
