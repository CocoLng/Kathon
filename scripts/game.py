# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 12:27:55 2022

@author: coren
"""
from card import input_player,Deck
from player import Human


P1=Human("1")
P2=Human("2")
P3=Human("3")
P_list = [P1,P2,P3]
P1.status = ["bug"]
P3.status = ["baaaug"]
def init_round(extension,P_list):
    Deck_Action = Deck("ACTION",[extension,False])
    Deck_Chemin = Deck("CHEMIN",[extension,False])
    Deck_Role = Deck("ROLE",[extension,extension])
    if not(extension) : Deck_Reward = Deck("REWARD")
    [x.status.clear() for x in P_list]
    Deck_Action.shuffle()
    Deck_Chemin.shuffle()
    Deck_Role.shuffle()
    Deck_Reward.shuffle()
    return Deck_Action,Deck_Chemin,Deck_Role,Deck_Reward

def run_round(extension,P_list):
    input_player(0, 1)
    pass

Deck_Action,Deck_Chemin,Deck_Role,Deck_Reward = init_round(False, P_list)