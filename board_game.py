
class BordGame:
    
    def __init__(self):
        #initialise une carte de X = 0 y = 0
        self.map_ = [[]]
    
    
    #permet de verifier si la carte poser est en acord avec les regles de conection de cartes
    def card_setable(self,card,pos):
        chemin = card
        X = [self.map_[pos[0]+ ind - 2][pos[1]].chemin[ind - 2] if ind%2 != 0 else self.map_[pos[0]][pos[1] + ind - 1].chemin[ind - 2] for ind in range(len(chemin))]

        c = [True if i == j  else False for i,j in zip(chemin,X)]
        
        if False in c:
            return False
        return True
   
    #permet de suprimer des cartes a une positon precise si il reussi renvoi True sinon False
    def del_card(self,pos):
        
        if self.map_[pos[0]][pos[1]] != []:    
            self.map_[pos[0]][pos[1]] = []
            return True
        else:
            return False
   
 
   #permet de rajouter des carte a une position precise 
   #si la carte est en dehors de la map deja cree 
   #des lignes/colonnes ou les deux seront ajouté pour pouvoir placer la carte
   
    def add_card(self,card,pos):

        #on verifie si la carte est en dehors de la map"
        #debut verification"
        if len(self.map_) <= pos[0] or pos[0] < 0 :Xa = True 
        else: Xa = False
        
        if len(self.map_[0]) <= pos[1] or pos[1] < 0:Ya = True 
        else: Ya = False
        #fin verification"
        
        
        #si elle est a l interieur de la carte crée on peut la rajouter
        if not(Xa) and not(Ya): 
            
            if  self.map_[pos[0]][pos[1]] == []:
                 self.map_[pos[0]][pos[1]] = card
                
            else: print("carte deja presente")
                
        else:
        #si elle est a l exterieur nous devont ettendre la carte
            a = pos[0]
            b = pos[1]
        #Xa et Ya nous donne l information sur si on est a l'exteriur en x ou en y donc soit rajouter une/des ligne(s) ou une/des colonne(s)
        #ici Xa donc rajout de case sur X
            if Xa:
                L = len(self.map_[0])
                if pos[0] >= 0:
                    Xlen = pos[0]-len(self.map_) 
                else:
                    a = 0
                    Xlen = pos[0]+1
                #on une colonne soit a gauche de la carte soit a la fin 
                [self.map_.append([]) if a > 0 else self.map_.insert(0,[]) for i in range(abs(Xlen)+1)]
                
                #si des case en X sont rajouter on doit rajouter des cases sur l axe Y afin que notre carte soit carré
                for k in range(len(self.map_)):   
                        if len(self.map_[k]) < L:
                            [self.map_[k].append([]) if pos[1] > i else self.map_[k].insert(0,[]) for i in range(L)]  
        #ici Xa donc rajout de case sur Y
            if Ya:
                if pos[1] >= 0:
                    Ylen = pos[1]-len(self.map_[0])
                else:
                    b = 0
                    Ylen = pos[1]+1
                #on rajoute une ligne soit en haut de la map soit en bas de la map
                for j in range(len(map_)):
                    [self.map_[j].append([]) if b > 0 else self.map_[j].insert(0,[]) for i in range(abs(Ylen)+1)]  
            
            self.map_[a][b] = card  
"""
*******************************************************************************************************************
*                                                                                                                 *
*                                                                                                                 *
*                                                      TEST                                                       *
*                                                                                                                 *
*                                                                                                                 *
*******************************************************************************************************************
"""
map_ = [[]]
mab = BordGame(map_)

mab.add("C1",[0,0])
mab.add("C2",[0,0])
mab.add("C3",[0,0])
mab.add("C4",[0,0])
mab.add("C5",[0,0])
mab.add("C6",[0,0])


print(mab.map_)
del(mab)