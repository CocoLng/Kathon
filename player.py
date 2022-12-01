from abc import ABC, abstractmethod 


class Player(ABC):
    
    def __init__(self,name,score):
        self.score = score
        self.name = name
        self.__main = []
        self.statu = []
        self._carte_max = 5
        
       
    @property    
    def tirer_carte(self):
        return self.__main
    
    @tirer_carte.setter
    def tirer_carte(self,carte):
        self.__main.append(carte) if len(self.__main) <= self.__carte_max else print("deffauser, car trop de cartes")        
        
    @property
    def score(self):
        return self.__score
    @score.setter
    def score(self,score):
        if score > 0:
            self.__score = score
        else:
            print("impssible de retirer des point au joueur")
        


class IA(Player):
    
    def __init__(self,name):
        super().__init__(name)
        self.__main = []



class Humain(Player):
    
    def __init__(self,name,score):
        super().__init__(name,score)
        self.__main = []

    def poser_carte(self):
            return input("ou voulez vous poser votre carte ?")
    
    def selec_choice(self):
            return input("quelle action voulez vous faire ?")
       
    def supp_carte (self,place):
        try:
            del self.__main[place-1]
            
        except:
            if place != int :
               return print("erreur emplacement de carte invalide")
            else: 
               return print("erreur lors de la supression de carte")

"""
le score doit etre une input qui ne fonctione pas sur spider

"""