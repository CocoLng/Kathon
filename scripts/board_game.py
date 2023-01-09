class BoardGame:
    
    def __init__(self):
        # initialise une carte de X = 0 y = 0
        self.__map_ = [[[]]]
        self.decalage = [0, 0]
        self.pos_spe = []
        self.liste_spe = ['PIERRE', 'PEPITE']
    
    @property
    def MAP(self):
        return self.__map_
    
    def __str__(self):
        aff = ""
        ma_lenx = len(f"{self.decalage[0]}") if len(f"{self.decalage[0]}") > len(f"{len(self.__map_)}") else len(
            f"{len(self.__map_)}")
        ma_leny = len(f"{self.decalage[1]}") if len(f"{self.decalage[1]}") > len(f"{len(self.__map_[0])}") else len(
            f"{len(self.__map_[0])}")
        
        if ma_lenx < 4:
            ma_lenx = 3
        aff_barre = "|" + " " * ma_leny + "|"
        aff_barreb = "+" + "-" * ma_leny + '+'
        
        for j in range(len(self.__map_)):
            x = len(f"{j + self.decalage[0]}")
            aff_barre += " " + " " * ((ma_lenx - x) // 2 + (ma_lenx - x) % 2) + f"{j + self.decalage[0]}" + " " * (
                    (ma_lenx - x) // 2) + " "
            aff_barreb += "-" * (ma_lenx - x + (ma_lenx - x) % 2) * 2 + '-'
        aff_barre = aff_barreb + '\n' + aff_barre + "\n" + aff_barreb
        
        for i in range(len(self.__map_[0])):
            y = len(f"{i + self.decalage[1]}")
            aff1 = "|" + " " * ma_leny + "|"
            aff2 = "|" + " " * ma_leny + "|"
            aff3 = "|" + " " * ((ma_leny - y) // 2 + (ma_leny - y) % 2) + f"{i + self.decalage[1]}" + " " * (
                    (ma_leny - y) // 2) + "|"
            aff4 = "|" + " " * ma_leny + "|"
            aff5 = "|" + " " * ma_leny + "|"
            
            for j in range(len(self.__map_)):
                if not self.__map_[j][i]:
                    
                    aff1 += "     "
                    aff2 += "     "
                    aff3 += "     "
                    aff4 += "     "
                    aff5 += "     "
                
                else:
                    aff1 += self.__map_[j][i].aff[0]
                    aff2 += self.__map_[j][i].aff[1]
                    aff3 += self.__map_[j][i].aff[2]
                    aff4 += self.__map_[j][i].aff[3]
                    aff5 += self.__map_[j][i].aff[4]
            
            aff += aff1 + "\n" + aff2 + "\n" + aff3 + "\n" + aff4 + "\n" + aff5 + "\n"
        return aff_barre + "\n" + aff
    
    # permet de verifier si la carte posé est en accord avec les regles de conection de cartes
    # permet de verifier si la carte poser est en acord avec les regles de conection de cartes
    def detect(self, card):
        flag = []
        for i in self.__map_[-self.decalage[0]][-self.decalage[1]].borders:
            i.reconstruc_path(i)
            if not card.borders[0].flag_loop in flag:
                flag.append(card.borders[0].flag_loop)
        
        for posl in self.pos_spe:
            self.__map_[posl[0] - self.decalage[0]][posl[1] - self.decalage[1]].effect()
            if not (card.borders[0].flag_loop in flag):
                flag.append(card.borders[0].flag_loop)
        
        return flag
    
    def card_set(self, card, pos):
        card_p = []
        borders_to_connect = []
        
        antipode_d_u = ['down', 'up']
        antipode_l_r = ['right', 'left']
        
        flag = False
        
        for x_y in [-1, 1]:
            print(x_y)
            if 0 <= pos[0] + x_y < len(self.__map_):
                try:
                    
                    INTE1 = [True if I.name == antipode_l_r[(x_y + 1) // 2] else False for I in
                             self.__map_[pos[0] + x_y][pos[1]].borders]
                    INTE = [True if I.name == antipode_l_r[(x_y - 1) // 2] else False for I in card.borders]
                    
                    if (True in INTE) == (True in INTE1):
                        
                        card_p.append(self.__map_[pos[0] + x_y][pos[1]].borders[INTE1.index(True)])
                        borders_to_connect.append(card.borders[INTE.index(True)])
                        
                        if self.__map_[pos[0] + x_y][pos[1]].borders[INTE1.index(True)].flag_loop is not None:
                            flag = True
                    else:
                        if not (self.__map_[pos[0] + x_y][pos[1]].special in self.liste_spe):
                            print('Probleme lors de la connection des cartes en X')
                            return False
                except(AttributeError, IndexError, ValueError):
                    pass
            
            if 0 <= pos[1] + x_y < len(self.__map_[0]):
                try:
                    
                    INTE1 = [True if I.name == antipode_d_u[(x_y + 1) // 2] else False for I in
                             self.__map_[pos[0]][pos[1] + x_y].borders]
                    INTE = [True if I.name == antipode_d_u[(x_y - 1) // 2] else False for I in card.borders]
                    if (True in INTE) == (True in INTE1):
                        
                        card_p.append(self.__map_[pos[0]][pos[1] + x_y].borders[INTE1.index(True)])
                        borders_to_connect.append(card.borders[INTE.index(True)])
                        
                        if self.__map_[pos[0]][pos[1] + x_y].borders[INTE1.index(True)].flag_loop is not None:
                            flag = True
                    else:
                        if not (self.__map_[pos[0]][pos[1] + x_y].special in self.liste_spe):
                            print('Probleme lors de la connection des cartes en Y')
                            return False
                except(AttributeError, IndexError, ValueError):
                    pass
        
        if not flag:
            print('Non connecté au start')
            return False
        
        for x_y in [-1, 1]:
            if 0 <= pos[0] + x_y < len(self.__map_):
                if self.__map_[pos[0] + x_y][pos[1]]:
                    self.__map_[pos[0] + x_y][pos[1]].reveal = True
            if 0 <= pos[1] + x_y < len(self.__map_[0]):
                if self.__map_[pos[0]][pos[1] + x_y]:
                    self.__map_[pos[0]][pos[1] + x_y].reveal = True
        
        for exterieur, interieur in zip(card_p, borders_to_connect):
            interieur.secu_connect(exterieur)
        
        self.__map_[pos[0]][pos[1]] = card
        
        for i in self.__map_[-self.decalage[0]][-self.decalage[1]].borders:
            i.reconstruc_path(i)
        
        if card.special == "START":
            self.pos_spe.insert(0, [pos[0] + self.decalage[0], pos[1] + self.decalage[1]])
        if card.special == "DOOR":
            self.pos_spe.append([pos[0] + self.decalage[0], pos[1] + self.decalage[1]])
        
        for posl in self.pos_spe:
            self.__map_[posl[0] - self.decalage[0]][posl[1] - self.decalage[1]].effect()
        
        return True
        
        # permet de suprimer des cartes a une positon precise si il reussi renvoi True sinon False
    
    def del_card(self, pos):
        pos = [po - deca for deca, po in zip(self.decalage, pos)]
        if self.__map_[pos[0]][pos[1]]:
            # on regrade si la carte a un attribut special que l'on ne peut pas detruire
            if self.__map_[pos[0]][pos[1]].special in ["PIERRE", 'PEPITE'] or self.__map_[pos[0]][
                pos[1]].name == "ENTREE":
                print("Vous ne pouvez pas detruire une carte special")
                return False
            else:
                # si elle est destructible on demande a la carte de ce deconnecter
                self.__map_[pos[0]][pos[1]].delete()
                self.__map_[pos[0]][pos[1]] = []
                
                for i in self.__map_[-self.decalage[0]][-self.decalage[1]].borders:
                    # apres avoir rajouté la carte il reconstruit le chemin en partant des
                    # #sources pour etre sur que les portes soit bien connecté
                    i.reconstruc_path(i)
                i = 0
                # ici on stock l indice des source contenue dans la map pour pouvoir les recuper facilement
                for posl in self.pos_spe:
                    i += 0
                    if self.__map_[posl[0] - self.decalage[0]][posl[1] - self.decalage[1]]:
                        self.__map_[posl[0] - self.decalage[0]][posl[1] - self.decalage[1]].effect()
                    else:
                        self.pos_spe.pop(i)
                        i -= 1
            return True
        else:
            return False
    
    # permet de rajouter des cartes a une position precise
    # si la carte est en dehors de la map deja cree
    # des lignes/colonnes ou les deux seront ajouté pour pouvoir placer la carte
    
    def add_card(self, card, pos, admin=False):
        
        # on ajoute le decalage de l'indice zeros pour que l'on puisse avoir des valeure negative dans les positions
        pos[0] = pos[0] - self.decalage[0]
        pos[1] = pos[1] - self.decalage[1]
        
        # si elle est a l exterieur nous devont ettendre la carte
        a = pos[0]
        b = pos[1]
        
        # on verifie la taille de la map par rapport a la position demande
        # si la position demande est en dehors de la map alors Xa/Ya = True
        # cela indique que l'on vas agrandir la map soit sur l axe des X soit Y ou les deux
        if -1 < pos[0] < len(self.__map_) + 1 and -1 <  pos[1] > len(self.__map_[0]) + 1 or admin:
            if len(self.__map_) <= pos[0] or pos[0] < 0:
                Xa = True
            else:
                Xa = False

            if len(self.__map_[0]) <= pos[1] or pos[1] < 0:
                Ya = True
            else:
                Ya = False

            # on regarde si la position ou l on veux poser la carte est deja prise
            if not Xa and not Ya:
                if not (self.__map_[pos[0]][pos[1]] == []):
                    print("Carte deja presente")
                    return False

            else:
                # Xa et Ya nous donne l information sur si on est a l'exterieur
                # en x ou en y donc soit rajouter une/des ligne(s) ou une/des colonne(s)

                if Xa:
                    # Xa activé donc on on va augmenter la map sur l axe des X
                    L = len(self.__map_[0])

                    # on regarde si l'indice cherché est  negatif si il est negatif on agrandi la map en fesant un insert
                    # a l indice 0 sinon un append on recupere en meme temps l information de combien de case on doit
                    # agrandir la map
                    if pos[0] >= 0:
                        Xlen = pos[0] - len(self.__map_) + 1

                    else:
                        a = 0
                        Xlen = abs(pos[0])
                        self.decalage[0] += pos[0]

                    # on une colonne soit au debut de la carte soit a la fin
                    [self.__map_.append([]) if a > 0 else self.__map_.insert(0, []) for _ in range(Xlen)]

                    # si des case en X sont rajouter on doit rajouter des cases sur l axe Y afin que notre carte soit carré
                    for k in range(len(self.__map_)):
                        if len(self.__map_[k]) < L:
                            [self.__map_[k].append([]) if pos[1] > i else self.__map_[k].insert(0, []) for i in range(L)]

                if Ya:
                    # on regarde si l'indice cherché est  negatif si il est negatif on agrandi la map en fesant un insert
                    # a l indice 0 sinon un append on recupere en meme temps l information de combien de case on doit
                    # agrandir la map
                    if pos[1] >= 0:
                        Ylen = pos[1] - len(self.__map_[0]) + 1
                    else:
                        b = 0
                        Ylen = abs(pos[1])
                        self.decalage[1] += pos[1]

                    # on rajoute une ligne soit en haut de la __map soit en bas de la __map
                    for j in range(len(self.__map_)):
                        [self.__map_[j].append([]) if b > 0 else self.__map_[j].insert(0, []) for _ in range(Ylen)]

            # apres avoir mis a jour la taille de la map on vas ranger la carte dans notre tableau on regarde si on est
            # en mod admin si oui on poseras la carte sans ondition sinon on regarderais si la carte est possable
        if not admin:
                # cette methode permet d ajouter la carte à la map
                if self.card_set(card, [a, b]):
                    print('La pose de carte est reussite!')
                    return True
                
                return False
        else:
            self.__map_[a][b] = card
        return True
    
    def current(self, pos):
        pos = [po - deca for deca, po in zip(self.decalage, pos)]
        return self.__map_[pos[0]][pos[1]]
