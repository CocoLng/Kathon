from abc import ABC
from scripts.card import input_player



def options():
    print("\n[0] /!\ Quitte le programme")
    print("[-1] Rappel de votre role")
    print("[-2] Passer votre tour")

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
                print("Vous n'avez pas asser de cartes")
                return False
            for i in range(quantite):
                print("Quelle carte voulez vous défausser ?")
                card = self.main[input_player(1,len(self.main))-1]
                if card in self.main:
                    print(f"\nVous avez defausser {card.name}")
                    self.main.remove(card)
                    return True
                else: 
                    print("Cette carte n est pas presente dans votre main")
                    return False


    def ask_pos(self):
        pos = [] 
        while True:
            try:
                pos = input("Taper la position(int) ou vous voulez jouer votre carte, forme(taper stop pour annuler) :\nX Y\n")
                if pos.upper() == "STOP" : 
                    print("\n")
                    return False
                x,y = pos.split()
                pos = [int(x),int(y)]
                break
            except ValueError:
                print("Valeur Incorrecte")
                continue
        return pos

    
    def __flip_card_(self,card):
        antipode_d_u = ['down','up']
        antipode_l_r = ['right','left']
        try:
            [porte.name(antipode_d_u.index(porte.name)-1)for porte in card.borders if porte.name in antipode_d_u]
            [porte.name(antipode_l_r.index(porte.name)-1)for porte in card.borders if porte.name in antipode_l_r]   
        except (IndexError,ValueError):
            return False
        return True
        
    def play(self,P_list,MAP):
        
        if len(self.status) != 0 or (len(self.status) ==1 and not(self.status[0]=="voleur")) :
           print("Aie..\nVous êtes affecter par ceci :")
           [print(f"- {status}") for status in self.status]
           print("Ceci va vous empechez de posez des cartes chemins tant que vous ne vous en débarrasé pas\n")
        
        print("Voici votre main :")
        [print(f"[{i}] {card.name}") for i,card in enumerate(self.main,1)]
        options()
        card = input_player(-2,len(self.main))
        
           
        try:
            
            if card>0:
                card = self.main[card-1]
            else :
                if card == -1 : 
                    print(f"\nRappel, vous êtes un :\n{self.role}\n")
                    return False
                else : 
                    return self.del_card()
                
            if card.__class__.__name__ =='CardChemin':
                if len(self.status)==0 or self.status[0]=='voleur': 
                    ########################################
                    print(f"Vous allez jouer :{print(card)}")
                    print("[1] Continuer\n[2] Tourner la carte\n[3] Retour selection")
                    rep = input_player(1,3)
                    while True:
                        if rep == 1:
                            pos = self.ask_pos()
                            if pos and MAP.add_card(card,pos):
                                self.main.remove(card)
                                return True
                        elif rep == 2:
                            if self.__flip_card_(card): 
                                rep=1    
                        return False
                                
            if card.__class__.__name__ == 'CardAction':
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
