from abc import ABC
from scripts.card import input_player

class Player(ABC):
    
    def __init__(self,name):
        self.score = 0
        self.name = name
        self.role = None
        self.main = []
        self.status = []
        self.carte_max = 5
    
    def __str__ (self):
        Aff = "-"*20 
        return Aff+f"\n name = {self.name}"+f"\n score = {self.score}"+f"\n card = {i.name for i in self.main}"+'\n'+Aff
       
    @property
    def score(self):
        return self.__score
    
    @score.setter
    def score(self,score):
        if score >= 0:
            self.__score = score
        else:
            print("impssible de retirer des point au joueur")
            

class Human(Player):
    
    def __init__(self,name):
        super().__init__(name)
    
    def skip_turn(self):
        if len(self.main) == 0: return True
        return False       



    def del_card (self,quantite = 1):
            if len(self.main) < quantite:
                print('vous n avez pas asser de cartes')
                return False
            for i in range(quantite):
                ID = input("quelle carte voulez vous jouer ?")
                card = self.main[ID-1] 
                if card in self.main:
                    self.main.remove(card)
                else: 
                    print("cette carte n est pas presente dans votre main")


    def ask_pos(self):
        pos = [] 
        while True:
            try:
                pos = input("Taper la position(int) ou vous voulez jouer votre carte, forme :\nX Y\n")
                x,y = pos.split()
                pos = [int(x),int(y)]
                break
            except ValueError:
                print("Valeur Incorrecte")
                continue
        return pos

    
    def __flip_card_(self,ID):
        antipode_d_u = ['down','up']
        antipode_l_r = ['right','left']
        try:
            [CARD.name(antipode_d_u.index(CARD.name)-1)for CARD in self.main[ID-1] if CARD.name in antipode_d_u]
            [CARD.name(antipode_l_r.index(CARD.name)-1)for CARD in self.main[ID-1] if CARD.name in antipode_l_r]   
        except (IndexError,ValueError):
            return False
        return True
        
    def play(self,P_list,MAP):
        
        if len(self.main) == 0:
            print('le joueur n a plus de cartes')
            return True
        print("Voici votre main :")
        [print(f"[{i}] {card.name}") for i,card in enumerate(self.main,1)]
        print("\n")
        card = self.main[input_player(0,len(self.main))-1]

        if len(self.status) != 0 or (len(self.status) ==1 and not(self.status[0]=="voleur")) :
           print("Aie..\nVous êtes affecter par ceci :")
           [print(f"- {status}") for status in self.status]
           
        try:
            if card.__class__.__name__ =='CardChemin':
                if len(self.status)==0 or self.status[0]=='voleur': 
                    ########################################
                    print(f"Vous allez jouer :{print(card)}") ######AFFICHER COMME SI C ETAIT SUR LA MAPPPPPPP
                    print("[1] Continuer\n[2] Retour selection")
                    rep = input_player(1,2)
                    if rep == 1:
                        pos = self.ask_pos()
                        if MAP.add_card(card,pos):
                            self.main.remove(card)
                            return True
                
            if  card.__class__.__name__ == 'CardAction':
                card.arg = [P_list,MAP]
                if card.effect():
                    self.main.remove(card)
                    return True
            return False
        
        except IndexError:
            print("print vous n'avez pas asser de cartes")
            return False


    def get_card(self,Decks):
        if len(self.main) <= self.carte_max:
            card = Decks.draw_card()
            if card:
                self.main.append(card)
                return True
        print('cous avez trop de cartes')
        return False
