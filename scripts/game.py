# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 12:27:55 2022

@author: coren
"""
from random import shuffle
from scripts.board_game import BoardGame
from scripts.card import Deck,input_player
from os import path,system,name
from time import sleep

    
def game_handler(extension,P_list): #gere la réalisation d'une manche
    Decks,MAP,WIN_CARD = init_round(extension, P_list)
    shuffle(P_list) #Melange l'ordre des joueurs 
    P_round = P_list.copy()
    repartition_card(extension,P_round,Decks[0])
    status_win,P_round = run_round(extension,P_round,MAP,Decks[0],WIN_CARD)
    reward_time(extension,P_list,P_round,status_win,Decks[2],MAP)
    cls_screen()#Efface le terminal
    sleep(1)#temps de nettoyer l'ecran
    return True
    
def cls_screen(): #Sert a effacer la console, utile pour masquer les informations dun joueur à an autre
    #system('cls' if name=='nt' else 'clear')
    pass
    
def readfile(path_join,part_explain = 0): #Permet de lire un fichier texte, ici principalement a but d'affichage
    with open(path.join(path.dirname(__file__),path_join),'r') as f: 
        f_split = f.read().split("SUB_PART")#Nous décomposons notre fichier tous les SUB_PART
        print(f_split[part_explain])
    
        
def next_player(P_round):#Gere le passage au joueur suivant 
    cls_screen()#Efface le terminal
    sleep(1)#temps de nettoyer l'ecran
    readfile('..\\ressources\\SaboteurTxt.txt',4)
    print(f"C'est au tour de {P_round[0].name} !\n")
    input("Pressez enter pour continuer, sinon on peut aussi attendre tranquillement\n...")

    
def init_round(extension,P_list):
    #Initialise la map est la position des cartes cachées 
    pos = [[8,-2],[8,0],[8,2]]
    MAP = BoardGame()
    
    #Initialisation des decks
    Deck_ActionChemin = Deck("ACTION_CHEMIN",[extension,False],P_list)
    #connect la carte PEPITE a WIN
    WIN_CARD = Deck_ActionChemin.list_card[29]
    
    #Retire la carte spawn, et les pierre/gold
    MAP.add_card(Deck_ActionChemin.draw_card(30),[0,0],True)
    L = [Deck_ActionChemin.draw_card(27) for i in range(3)]
    shuffle(L)# Permet de mélanger les 3 cartes cachées 
    [MAP.add_card(CARD,POS,True) for CARD,POS in zip(L,pos)]
    
  #  Deck_ActionChemin.list_card=Deck_ActionChemin.list_card[80:105]
    
    #Initialise les autres deck et les mélanges 
    Deck_Role = Deck("ROLE",[extension,extension],P_list)
    Deck_Reward = Deck("REWARD",[extension,extension],P_list)
    Decks = [Deck_ActionChemin,Deck_Role,Deck_Reward]
    [shuffle(x.list_card) for x in Decks]
    
    #Effacement des status, et supression des cartes restantes
    [(player.status.clear(),player.main.clear()) for player in P_list]
    #assignement d'un role a chaque joueur, le deck role est déja mélangé
    for i,player in enumerate(P_list,1) : player.role=Deck_Role.list_card[i]
    
    return Decks,MAP,WIN_CARD

#Gere la répartition des cartes action/chemin entre les joueurs 
def repartition_card(extension,P_list,Deck):
    if extension:
        Deck.list_card = Deck.list_card[9:]#On retire les 10 premières cartes
        [player.main.append(Deck.draw_card()) for player in P_list for i in range(6)]

    else :
        #S il ny a pas l'extension alors:
        #Tous les 2 joueurs, une carte en moins est donnée initialement 
        nb_P_repart = 7 -len(P_list)//2
        [player.main.append(Deck.draw_card()) for player in P_list for i in range(nb_P_repart)]

#Gere la manche en cours 
def run_round(extension,P_round,MAP,Deck_,WIN_CARD):
    #Verifie que la pépite n'est pas trouvé et qu'un joueur a toujours au moins une carte
    first_player = P_round[0].name
    first_turn = True
    while True:
        P_Alive = True
        print(MAP)
        if first_turn: print(f"\n{P_round[0].name}, vous êtes :\n{P_round[0].role}\n")
        while True: #tant qu'un joueur n'as pas joué
            if P_round[0].play(P_round,MAP,extension,Deck_):
                break
        print(MAP)
        if not(P_round[0].get_card(Deck_)):
            if len(P_round[0].main) == 0:
                P_round.pop(0)
                P_Alive = False
            else : print("La pioche de carte est vide.")
        if WIN_CARD.borders[0].flag_loop != None : return True,P_round
        #Une fois que le joueur a joué nous passons au suivant,stocké en position 0
        #Le joueur qui vient de finir sont tour passe en dernière position
        if P_Alive : P_round = P_round[1:] + P_round[:1]
        try:
            if first_player == P_round[0].name : first_turn=False
        except IndexError:
            return False,P_round
        print("\nFIN de votre tour, analyser la MAP et retennez vos cartes si vous le desirez.")
        input("Pressez enter quand vous avez fini pour confirmer la fin de votre tour\n...")
    
        next_player(P_round)

def reward_time(extension,P_list,P_round,status_win,Deck_Reward,MAP):
    """
    P_list va se faire filtrer de manière a conserver uniquement les gagnant du round
    nb_deleted est présent pour eviter de provoquer un décalage d'indice dans la list des joueurs
    """
    nb_deleted = 0
    if not(extension):
        if status_win : #les chercheurs ont gagnés
            Deck_Reward.list_card.sort(key=lambda card: card.pepite, reverse=True)
            if len(P_list)>= 10 :
                Deck_Reward.list_card.append(Deck_Reward.list_card[-1])#s'il y a 10 joueurs
                Deck_Reward.list_card[-1].pepite = "0"
            [P_list.append(P_list.pop(0)) for x in P_list if x != P_round[0]]
            P_list.insert(0, P_list.pop()) #Fait repasser le joueur qui a trouver la pépite, devant
            for i in range(len(P_list)) :
                if P_list[i-nb_deleted].role.name[0] != "C" :
                    del P_list[i-nb_deleted]
                    nb_deleted +=1
            for i,card_reward in enumerate(Deck_Reward.list_card,0):
                if i== len(P_list)-1 : break
                P_list[i].score += int(card_reward.pepite)
                
        else : #les Saboteurs ont gagnés
            for i in range(len(P_list)) :
                if P_list[i-nb_deleted].role.name[0] != "S" : 
                    del P_list[i-nb_deleted]
                    nb_deleted +=1
            nb_pepites = 4-len(P_list)//2
            for player in P_list :
                player.score += int(nb_pepites)
                
    else :
        #Check pour des potentiels voleur
        P_list[0].status.append("Voleur")
        P_voleur = []
        [P_voleur.append(player) for player in P_list if ("Voleur" in player.status)and not("Emprisonnement" in player.status)]
        #DETECTION DES GEMMES GEOLOGUES
        nb_cristaux = 0
        for map_c in MAP._BoardGame__map_ :
            for card in map_c:
                if card !=[] and card.special=="cristaux" : nb_cristaux +=1
            print(card,nb_cristaux)
            
        if status_win : #les Chercheurs gagnent
            if P_round[0].role.name[0] != "C": #C'est un role spécial qui a fait la connection
                pass
            
            
        else : #les saboteurs gagnent
            print('sabo win')
            for n,player in enumerate(P_list,0) :
                if player.role.name[0] != (("S") or ("P")) : #Saboteur or Profiteur
                    print(n)
                    print("enterr",player.role.name[0],player.name)
                    del P_list[i-nb_deleted]
                    nb_deleted +=1
                else : print("SURVIVE",player.name)
            print("OUT")  
            nb_pepites = max(6-len(P_list),1)#Nombre de pépites en fonction du nombre de gagnant
            print("len",len(P_list),"\n")
            [print(player,player.role.name) for player in P_list]
            for n in range(len(P_list)):
                if P_list[n].role.name[0] ==("S"):
                    print("Ajout S",P_list[n].role.name,P_list[n].name)
                    P_list[n].score += int(nb_pepites)
                else : 
                    print("Ajout P",P_list[n].role.name,P_list[n].name)
                    P_list[n].score += int(nb_pepites)-1 #les sabouteurs gagne 1 de moins
                    
                  #p.append(plaer) for list geo list gagnt si score !=0      
        #if player.score == 0 : P_list.remove(player) #Si le score est nul, c'est que le gagnant a rien gagné
        #On va le retirer de la list des gagnant de manière a éviter qu'il puisse se faire voler
        #Tour des voleurs
        print("Voleur",P_voleur)
        if len(P_voleur) != 0 and len(P_list)!=0:
            print("vole")
            for player in P_voleur :
                next_player(P_voleur) #ne peut voler que les joueurs qui viennent de gagner
                print("THIEF TIME hehe\nChoissiez à quel gagnant vous souhaitez voler une pépite :\n")
                [(print('[',i, ']', x.name,"(",x.role.name,')', sep='', end='  ')) for i, x in enumerate(P_list, 1)]
                selected = input_player(1,len(P_list))
                P_list[selected-1].score -= 1 
                player.score +=1
                del P_voleur[0]
                
