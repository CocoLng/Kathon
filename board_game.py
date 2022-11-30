"""
project pyhton 2022 M1
"""


class game_bord:
    ### ID = identiter de l'objet
    ### pose = position ou l on veux poser la carte
    def __init__(self):
        self.map_ = [[[]]]
        self.init = True
        self.tableau_carte = ''
                    
        
    def __str__(self):
        
        for i in range(len(self.map_[0])):
            tab1 = ""
            tab2 = ""
            tab3 = ""
            for j in range(len(self.map_)):
                if self.map_[j][i] != []:        
                    tab1 += "( " + ("|" if self.map_[j][i].bordures[0] == 1 else ' ') + ' )'  
                    tab2 += ("--" if self.map_[j][i].bordures[1] == 1 else '( ') +'x'+ ('--' if self.map_[j][i].bordures[3] == 1 else ' )')  
                    tab3 += "( " + ("|" if self.map_[j][i].bordures[2] == 1 else ' ') + ' )'      
                else:
                    tab1 += '(   )'
                    tab2 += '(   )'  
                    tab3 += '(   )'  
                    
            self.tableau_carte =  self.tableau_carte  + '\n' + tab1 +'\n'+ tab2 +'\n'+ tab3
   
        return(print(self.tableau_carte))
        
        
        
    def del_connection(self,pose):
        if self.map_[pose[0]][pose[1]] != []:
            self.map_[pose[0]][pose[1]] = []
        else:
            return print("il n'y a pas de carte a supprimer")
        


    def connection(self,pose,carte,ID):
        
        ## genere les conections entre les carte une case a 8 ports 4 entrant 4 sortant 
        ## ils permettent de savoir si les chemins sont detaché et qu'elle equipe a gagné 
        ## la manche
        decalagex = 0
        decalagey = 0        
        verife = [-1,1]
        for i in verife:
           
            try:
                ## verification en x
                ##carte_cote = map_[x][y]  
                if pose[0]+i < 0:    
                    self.map_.insert(0,[[]*len(self.map_[0])])
                    decalagex = 1
                
                carte_cote_x = self.map_[pose[0] + i + decalagex][pose[1] + decalagey]

                if carte_cote_x != []:
                    if  carte.bordures[i+2] != carte_cote_x.bordures[i] and carte_cote_x.bordures[i] != []:
                        return print("vous pouvez pas poser la carte")

            except:
                self.map_.append([]) 
                for i in range(len(self.map_[0])):
                    self.map_[len(self.map_)-1].append([])                 


        for i in verife:
            try:
                ## verification en y
                ##carte_cote = map_[x][y]    
                if pose[1]+i < 0:  
                    for i in range(len(self.map_)):
                        self.map_[i].insert(0,[])
                        decalagey = 1
                    
                carte_cote_y = self.map_[pose[0] + decalagex] [pose[1]+ i + decalagey]

                if carte_cote_y != []:
                    if  carte.bordures[i+1] != carte_cote_y.bordures[i+3] and  carte_cote_y.bordures[i+3] != '':
                        return print("vous pouvez pas poser la carte") 
            except:
                for i in range(len(self.map_)):
                    self.map_[i].append([])
                
        self.map_[pose[0]+ decalagex][pose[1]+ decalagey] = carte
     
   
    @property
    def MAP(self):
        return self.map_


class card:
    def __init__(self,bordure):
        self.bordure = bordure
        self.A = []
    
    @property
    def bordures(self):
        return self.bordure
    
    """test run"""
    
C1 = card([1,1,1,1]) 
C2 = card([1,1,1,1]) 
C3 = card([1,0,0,0]) 
C4 = card([1,1,0,0]) 
C5 = card([0,0,0,0]) 
map_ = game_bord()

map_.connection([0,0],C1,0)


map_.connection([2,3],C5,0)
map_.__str__()

del(map_)
map_.__str__()