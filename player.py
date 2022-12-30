from Card import *
from board_game import *

class Player(ABC):
    
    def __init__(self,name):
        self.score = 0
        self.name = name
        self.__main = []
        self.status = []
        self.__carte_max = 5
    
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
        


class IA(Player):
    
    def __init__(self,name):
        super().__init__(name)
        self.__main = []



class Human(Player):
    
    def __init__(self,name):
        super().__init__(name)
        self.__main = []
    
    def skip_turn(self):
        if self.__main == []: return True
        return False
  
        
  
    def play_card(self,MAP,Pl_lt):
        ID = input("quelle carte voulez vous jouer ?")
        try:
            
            card = self.__main[ID-1]    
            if hasattr(CardChemins,card):
                if self.__status == []: 
                    if MAP.card_setable():
                        MAP.add_card(card,False)
                        self.__main.remove(card)
                        return True
                
            if hasattr(CardAction,card):
                card.P_list = Pl_lt
                if card.effect():
                    self.__main.remove(card)
                    return True
                
            return False
        
        except IndexError:
            print("print vous n'avez pas asser de cartes")
            return False
  

            
    def del_card (self,card):
        
            if card in self.__main:
                self.__main.remove(card)
            else: 
               return print("cette carte n est pas presente dans votre main")

