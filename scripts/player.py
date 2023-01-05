from abc import ABC

class Player(ABC):
    
    def __init__(self,name):
        self.score = 0
        self.name = name
        self.role = None
        self.__main = []
        self.status = []
        self.__carte_max = 5
        self.card_number = 0
    
    def __str__ (self):
        Aff = "-"*20 
        return Aff+f"\n name = {self.name}"+f"\n score = {self.score}"+f"\n card = {self.__main}"+'\n'+Aff
       
    @property    
    def add_card(self):
        return self.__main
    
    @add_card.setter
    def add_card(self,carte):
        self.__main.append(carte) if len(self.__main) < self.__carte_max else print("deffauser, car trop de cartes")        
        
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
        self.__main = []
    
    def skip_turn(self):
        if self.card_number == 0: return True
        return False       
    
    def __flip_card_(self,ID):
        antipode_d_u = ['down','up']
        antipode_l_r = ['right','left']
        try:
            [CARD.name(antipode_d_u.index(CARD.name)-1)for CARD in self.__main[ID-1] if CARD.name in antipode_d_u]
            [CARD.name(antipode_l_r.index(CARD.name)-1)for CARD in self.__main[ID-1] if CARD.name in antipode_l_r]   
        except (IndexError,ValueError):
            return False
        return True
        
    def play_card(self,MAP,Pl_lt):
        ID = input("quelle carte voulez vous jouer ?")
        try:
            
            card = self.__main[ID-1]    
            if isinstance(card,'CardChemin'):
                if self.__status == []: 
                    if MAP.card_setable():
                        MAP.add_card(card,False)
                        self.__main.remove(card)
                        self.card_number = len(self.__main)
                        return True
                
            if isinstance(card,'CardAction'):
                card.P_list = Pl_lt
                if card.effect():
                    self.__main.remove(card)
                    self.card_number = len(self.__main)
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
                card = self.__main[ID-1] 
                if card in self.__main:
                    self.__main.remove(card)
                else: 
                    return print("cette carte n est pas presente dans votre main")
           
    def get_card(self,card):
        if len(self.__main) <= self.__carte_max:
            self.__main.append(card)
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