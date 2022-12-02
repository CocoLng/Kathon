
class BordGame:
    
    def __init__(self):
        self.map_ = [[]]
        
    def card_setable(self,card,pos):
        chemin = card
        X = [self.map_[pos[0]+ ind - 2][pos[1]].chemin[ind - 2] if ind%2 != 0 else self.map_[pos[0]][pos[1] + ind - 1].chemin[ind - 2] for ind in range(len(chemin))]

        c = [True if i == j  else False for i,j in zip(chemin,X)]
        
        if False in c:
            return False
        return True
   
    
    def del_card(self,pos):
        self.map_[pos[0]][pos[1]] = []
       
    def add_card(self,card,pos):

        if len(self.map_) <= pos[0] or pos[0] < 0 :Xa = True 
        else: Xa = False
        
        if len(self.map_[0]) <= pos[1] or pos[1] < 0:Ya = True 
        else: Ya = False
        
        if not(Xa) and not(Ya): 
            
            if  self.map_[pos[0]][pos[1]] == []:
                 self.map_[pos[0]][pos[1]] = card
                
            else: print("carte deja presente")
            
        else:
            a = pos[0]
            b = pos[1]
            if Xa:
                L = len(self.map_[0])
                if pos[0] >= 0:
                    Xlen = pos[0]-len(self.map_) 
                else:
                    a = 0
                    Xlen = pos[0]+1
                    
                [self.map_.append([]) if a > 0 else self.map_.insert(0,[]) for i in range(abs(Xlen)+1)]

                for k in range(len(self.map_)):   
                        if len(self.map_[k]) < L:
                            [self.map_[k].append([]) if pos[1] > i else self.map_[k].insert(0,[]) for i in range(L)]  

            if Ya:
                if pos[1] >= 0:
                    Ylen = pos[1]-len(self.map_[0])
                else:
                    b = 0
                    Ylen = pos[1]+1
                    
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