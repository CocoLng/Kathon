from abc import ABC, abstractmethod 


class Player(ABC):
    
    def __init__(self,name):
        self.score = 0
        self.name = name
        self.__main = []
        self.statu = []
        self.__carte_max = 5
    
    def __str__ (self):
        Aff = "-"*20 
        return Aff+f"\n name = {self.name}"+f"\n score = {self.score}"+f"\n card = {self.__main}"+'\n'+Aff
       
    @property    
    def pick_card(self):
        return self.__main
    
    @pick_card.setter
    def pick_card(self,carte):
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

    def play_card(self):
            return input("ou voulez vous poser votre carte ?")
    
    def sel_choice(self):
            return input("quelle action voulez vous faire ?")
       
    def del_card (self,card):
        
            if card in self.main:
                self.__main.remove(card)
            else: 
               return print("cette carte n est pas presente dans votre main")

"""
le score doit etre une input qui ne fonctione pas sur spider

"""
