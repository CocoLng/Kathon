# la classe connection edge permet de gerer les connections entre 
# des objets a une sources et de savoir si l'objet regarde est 
# connecté a la source voulue

class ConnectionEdge:
    
    def __init__(self,name,flag=None,source=False):
            self.delet = False
            self.__flag = flag
            self.__source = source 
            self.__inputo = []
            self.__outputo = []
            self.is_check = False
            self.__name = name
            self.WARNING = 0
    
    #def __str__(self):
     #   return self.name
            
# flag_loop et __flag_ pemettent de recuperer l'information a quelle source
# est connecté l'objet concerné d'objet connecté a une source
    @property
    def source(self):
        return self.__source
    @source.setter
    def source(self,source):
        self.__source = source
    @property
    def name(self):
        return self.__name
    
    #condition propre au jeux sur les nom de nos objets
    @name.setter
    def name(self,name):
        if name in ['up','down','right','left']:
            self.__name = name
        else:
            pass
            #print('le nom de l objet cree ne correspond pas aux different nom attendu, pour retier cette ligne de code aller: detect_region.py ligne 33')
        
    def __flag_(self,start):
        if self.__source:
            return self.__flag
        else:
            if self.__inputo != []:
                if len(self.__inputo) == 1 :
                    if start != self.__inputo[0]: 
                        return self.__inputo[0].__flag_(start)
        return None
                
    @property
    def flag_loop(self): 
        return self.__flag_(self)
    

# inputo et outputo cree des listes des input/output entre les objets voulue
# attention lors de sont utilisation si plusieures input sont defini avant d'utiliser 
# la fonction "flag_loop" pour detecter la region de l'objet, il faut 1
# recontruire les chemins partant de l'objet source
# pour cela on utliserat la fonction "reconstruc_path"

    @property
    def inputo(self):
        return self.__inputo
    
    @inputo.setter
    def inputo(self,obj):
        if self.delet:
            self.__inputo.remove(obj)
        else:
            self.__inputo.append(obj)
        
    @property
    def outputo(self):
        return self.__outputo
    
    @outputo.setter
    def outputo(self,obj):
        if self.delet:
            self.__outputo.remove(obj)
        else:
            self.__outputo.append(obj)
            
            
            
# connect deux objets        
    def connect(self,obj):  
        self.delet = False
        obj.delet = False
        self.inputo = obj  
        obj.outputo = self
        
        
# deconnect deux objets
# pour simplifier l'utilisation de la fonction nous considerons que si l'utilisateur rentre
# je veux deconnecter A et B serat la meme chose que deconnecter B et A 
# donc l'odre n'a plus d'importance lors de lutilisation de la fonction 
    def disconnect(self,obj):
        self.delet = True
        obj.delet = True
        try:
            self.inputo = obj
            obj.outputo = self    
        except ValueError:
            try:
                self.outputo = obj
                obj.inputo = self 
            except ValueError:
                pass
        self.delet = False
        obj.delet = False
                
 #permet dedetruire l'integraliter de l'objet et ses connections               
    def delete_connection(self):
        in_out = [self.outputo[i] if i < len(self.outputo) else self.inputo[i-len(self.outputo)] for i in range(len(self.outputo)+len(self.inputo))]
        [self.disconnect(i) for i in in_out]

        
# a utiliser lorsque l'on deconnecte deux objet si l'on veux recree correctement
# les chemins j'usqua l'objet source
    
    def reconstruc_path(self,source_flag):
        if not(self.is_check):
            in_out = [self.outputo[i] if i < len(self.outputo) else self.inputo[i-len(self.outputo)-1] for i in range(len(self.outputo)+len(self.inputo))]
            # melange les input et les output de l'objet et les redefinies
            # en fonction de la direction de la source
            # par la suite on isoleras la source et considererons que tous les autres ports
            # de l'objet sont des output de ce dernier si il a plus d'une output on serat sur un noeud
            # le programe commnceras par explorer une direction de ce noeud une fois l'exploration de la ligne terminé
            # nous retournons sur le noeud et explorons une autre direction
            self.is_check = True   
            
            for i in in_out:
                if i.WARNING == 0:
                    if not(i.is_check): 
                        if not(i.source):
                            if i != source_flag:
                                print(self.name,i.name)
                                #on verifie si l'objet suivent a deja ete verifier par le programme  
                                # on detruit les chemins existent &aavant de 
                                # les reconnecter a fin d'eviter une copie des input/output dans l'objet
                                self.disconnect(i)
                                i.connect(self)
                                #si il ne la pas ete on continue la recontruction de chemin
                                i.reconstruc_path(self)
                                    
                            else:
                                # si on detect que 'i' correspond a la source on indique on programe
                                # que l'on veut que 'i' soit l'input de notre objet
                                self.disconnect(i)
                                if not(self.source):
                                    self.connect(i)
                                else:
                                    i.connect(self)
                        else:
                            
                            if i == source_flag:
                                self.disconnect(i)
                                self.connect(i)
                            else:
                                if self != i:    
                                    self.disconnect(i)
                                    self.outputo = i
                                    i.outputo = self
                    else:
                        if self in i.inputo:
                            self.disconnect(i)
                            self.outputo = i
                            i.outputo = self
                        self.WARNING += 1

                else:
                    i.WARNING -= 1  
        if self.WARNING > 0:
            self.WARNING -= 1
        # permet de gerer les fin de lignes conecter a des noeuds
        if self.WARNING == 0:
            self.is_check = False

        
# cette classe serat utilisé afin de gere entre sorti des 
# cartes chemins ainssi que leurs connections intern
