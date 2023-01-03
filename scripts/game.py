# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 12:27:55 2022

@author: coren
"""
from scripts.card import input_player,Deck
from scripts.player import Human


P1=Human("1")
P2=Human("2")
P3=Human("3")
P_list = [P1,P2,P3]
P1.status = ["bug"]
P3.status = ["baaaug"]

def init_round(extension,P_list):
    #Initialisation des decks
    Deck_Action = Deck("ACTION",[extension,False])
    Deck_Chemin = Deck("CHEMIN",[extension,False])
    Deck_Role = Deck("ROLE",[extension,extension])
    Deck_Reward = Deck("REWARD",[extension,extension])
    Decks = [Deck_Action,Deck_Chemin,Deck_Role,Deck_Reward]
    [x.shuffle() for x in Decks]
    
    #Effacement des status, et supression des cartes restantes
    [(player.status.clear(),player._Human__main.clear()) for player in P_list]
    #assignement d'un role a chaque joueur, le deck role est déja mélangé
    for i,player in enumerate(P_list,1) : player.role=Deck_Role.list_card[i]
    
    repartition(Decks,P_list)
    return Decks

def repartition(Decks,P_list):
    pass


def run_round(extension,P_list):
    input_player(0, 1)
    pass

P3._Human__main.append("test")
Decks = init_round(False,P_list)