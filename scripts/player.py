from abc import ABC

class Player(ABC):
    
    def __init__(self,name):
        self.score = 0
        self.name = name
        self.role = None
        self.main = []
        self.status = []
        self.__carte_max = 5
        self.card_number = 0
    
    def __str__ (self):
        Aff = "-"*20 
        return Aff+f"\n name = {self.name}"+f"\n score = {self.score}"+f"\n card = {self.main}"+'\n'+Aff
       
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
        if self.card_number == 0: return True
        return False       
    
    def __flip_card_(self,ID):
        antipode_d_u = ['down','up']
        antipode_l_r = ['right','left']
        try:
            [CARD.name(antipode_d_u.index(CARD.name)-1)for CARD in self.main[ID-1] if CARD.name in antipode_d_u]
            [CARD.name(antipode_l_r.index(CARD.name)-1)for CARD in self.main[ID-1] if CARD.name in antipode_l_r]   
        except (IndexError,ValueError):
            return False
        return True
        
    def play_card(self,MAP,Pl_lt):
        ID = input("quelle carte voulez vous jouer ?")
        try:
            
            card = self.main[ID-1]    
            if isinstance(card,'CardChemin'):
                if self.__status == []: 
                    if MAP.card_setable():
                        MAP.add_card(card,False)
                        self.main.remove(card)
                        self.card_number = len(self.main)
                        return True
                
            if isinstance(card,'CardAction'):
                card.P_list = Pl_lt
                if card.effect():
                    self.main.remove(card)
                    self.card_number = len(self.main)
                    return True
                
            return False
        
        except IndexError:
            print("print vous n'avez pas asser de cartes")
            return False


    def del_card (self,quantite = 1):
            if self.card_number < quantite:
                print('vous n avez pas asser de cartes')
                return False
            for i in range(quantite):
                ID = input("quelle carte voulez vous jouer ?")
                card = self.main[ID-1] 
                if card in self.main:
                    self.main.remove(card)
                else: 
                    return print("cette carte n est pas presente dans votre main")
           
    def get_card(self,card):
        if len(self.main) <= self.__carte_max:
            self.main.append(card)
            return True
        print('cous avez trop de cartes')
        return False


def ask_pos(self):
    X = [] 
    while True:
        try:
            X = input("a quelle pisiton voulez vous jouer votre carte x y\n")
            x,y = X.split()
            P = [int(x),int(y)]
            break
        except (KeyboardInterrupt,ValueError):
            print("pas les bonnes valeurs")
    return P