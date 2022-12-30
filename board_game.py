class BordGame:
    
    def __init__(self):
        #initialise une carte de X = 0 y = 0
        self.__map_ = [[[]]]
        self.__decalage = [0,0]
    
    def __str__(self):
        aff = ""
        ma_lenx =  len(f"{self.__decalage[0]}") if len(f"{self.__decalage[0]}") > len(f"{len(self.__map_)}") else len(f"{len(self.__map_)}")
        ma_leny =  len(f"{self.__decalage[1]}") if len(f"{self.__decalage[1]}") > len(f"{len(self.__map_[0])}") else len(f"{len(self.__map_[0])}")

        if ma_lenx < 4:
            ma_lenx =3
        aff_barre = " " *(ma_leny+2)
        for j in range(len(self.__map_)):
            x = len(f"{j+self.__decalage[0]}")
            aff_barre += "|"+" "*((ma_lenx-x)//2+(ma_lenx-x)%2) +f"{j+self.__decalage[0]}"+" "*((ma_lenx-x)//2)+"|"

            
            
        for i in range(len(self.__map_[0])):
            y = len(f"{i+self.__decalage[1]}")
            aff1 ="|" + " "*ma_leny+"|"
            aff2 ="|"+" "*((ma_leny-y)//2+(ma_leny-y)%2) +f"{i+self.__decalage[1]}"+" "*((ma_leny-y)//2)+"|"
            aff3 ="|"+" "*ma_leny+"|"

            for j in range(len(self.__map_)):
            
                chemin = self.__map_[j][i]
                if chemin != []:
                    aff1 += "( " + ("|" if chemin[0] else " ") + " )"
                    aff2 += ("--" if chemin[1] else "( ") +"+"+ ("--" if chemin[3] else " )")
                    aff3 += "( " + ("|" if chemin[2] else " ") + " )"
                else:
                    aff1 +="(   )"
                    aff2 +="(   )"
                    aff3 +="(   )"
                    
            aff += aff1 + "\n" + aff2 + "\n" + aff3 + "\n"
        return aff_barre+"\n"+aff
    
    
    def ask_pos(self):
        X = [] 
        while True:
            try:
                X = input("a quelle pisiton voulez vous jouer votre carte x y\n")
                x,y = X.split()
                P = [int(x),int(y)]
                break
            except ValueError:
                print("pas les bonnes valeurs")
        return P
    

    
    #permet de verifier si la carte poser est en accord avec les regles de conection de cartes
    def card_setable(self,card):
        pos = self.ask_pos()
        chemin = card.chemin
        X = [self.__map_[pos[0]+ ind - 2][pos[1]].chemin[ind - 2] if ind%2 != 0 else self.__map_[pos[0]][pos[1] + ind - 1].chemin[ind - 2] for ind in range(len(chemin))]
        c = [True if i == j  else False for i,j in zip(chemin,X)]
        
        if False in c:
            return False
        return True
    #
    def flag_spread(self):
        card_to_spread = []
        row = 0
        col = 0
        self.__map_.index()
        while True:
            
            break             
        return True 
   
    
    #permet de suprimer des cartes a une positon precise si il reussi renvoi True sinon False
    def del_card(self):
        pos = self.ask_pos()
        if self.__map_[pos[0]][pos[1]] != []:
            if self.__map_[pos[0]][pos[1]].special:
                print("vous ne pouvez pas detruire une carte special")
            else:  
                self.__map_[pos[0]][pos[1]] = []
            return True
        else:
            return False
   
 
   #permet de rajouter des carte a une position precise 
   #si la carte est en dehors de la __map deja cree 
   #des lignes/colonnes ou les deux seront ajouté pour pouvoir placer la carte
   
    def add_card(self,card,admin):
        
        pos = self.ask_pos()
        if not(admin):
           if not(self.card_setable(pos)):
               return False
        #on verifie si la carte est en dehors de la __map"
        #debut verification"
        pos[0] = pos[0]-self.__decalage[0]
        pos[1] = pos[1]-self.__decalage[1]
        print(pos)
        if len(self.__map_) <= pos[0] or pos[0] < 0 :Xa = True 
        else: Xa = False
        
        if len(self.__map_[0]) <= pos[1] or pos[1] < 0:Ya = True 
        else: Ya = False
        #fin verification"
           
        #si elle est a l interieur de la carte crée on peut la rajouter
        if not(Xa) and not(Ya): 
            
            if  self.__map_[pos[0]][pos[1]] == []:
                 self.__map_[pos[0]][pos[1]] = card
                
            else: print("carte deja presente")
                
        else:
        #si elle est a l exterieur nous devont ettendre la carte
            a = pos[0]
            b = pos[1]
        #Xa et Ya nous donne l information sur si on est a l'exteriur en x ou en y donc soit rajouter une/des ligne(s) ou une/des colonne(s)
        #ici Xa donc rajout de case sur X
            if Xa:
               
                L = len(self.__map_[0])
                if pos[0] >= 0:
                    Xlen = pos[0]-len(self.__map_)+1
                else:
                    a = False
                    Xlen = abs(pos[0])
                    self.__decalage[0] += pos[0]


                #on une colonne soit a gauche de la carte soit a la fin 
                [self.__map_.append([]) if a>0 else self.__map_.insert(0,[]) for i in range(Xlen)]
                
                #si des case en X sont rajouter on doit rajouter des cases sur l axe Y afin que notre carte soit carré
                for k in range(len(self.__map_)):   
                        if len(self.__map_[k]) < L:
                            [self.__map_[k].append([]) if pos[1] > i else self.__map_[k].insert(0,[]) for i in range(L)]  
        #ici Xa donc rajout de case sur Y
            if Ya:
          
                if pos[1] >= 0:
                    Ylen = pos[1]-len(self.__map_[0])+1
                else:
                    b = 0
                    Ylen = abs(pos[1])
                    self.__decalage[1] += pos[1]

                #on rajoute une ligne soit en haut de la __map soit en bas de la __map
                for j in range(len(self.__map_)):
                    [self.__map_[j].append([]) if b>0 else self.__map_[j].insert(0,[]) for i in range(Ylen)]  
            
            self.__map_[a][b] = card  
            print( self.__decalage)
            return True
            
            
            
######################################################################################                                                                                    #                                                                                                                 *
#                                        TEST                                        #               *
######################################################################################

mab = BordGame()
C1 = [True,True,True,True]
C2 = [True,True,True,False]

mab.add_card(C1,True)
mab.add_card(C1,True)






print(mab)
