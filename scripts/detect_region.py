# La classe connection edge permet de gérer les connections entre
# des objets à une source et de savoir si l'objet regardé est
# connecté à la source voulue

class ConnectionEdge: # Classe de connection entre les objets
    
    def __init__(self, name, flag=None, source=False):
        self.delet = False # permet d'activer ou de désactiver la fonction de suppression
        self.flag = flag # permet de savoir si l'objet est connecté à la source
        self.__source = source # permet de savoir si l'objet est la source
        self.__inputo = [] # liste des objets connectés en input
        self.__outputo = [] # liste des objets connectés en output
        self.__name = name # nom de la connection
    
    # flag_loop et __flag_ permettent de récuperer l'information à quelle source
    # est connectée l'objet concerné d'objet connecté à une source
    @property
    def source(self):
        return self.__source
    
    @source.setter
    def source(self, source):
        self.__source = source
    
    @property
    def name(self):
        return self.__name
    
    # condition propre aux jeux sur les noms de nos objets
    @name.setter
    def name(self, name):
        if name in ['up', 'down', 'right', 'left']: # si le nom est une des quatres direction
            self.__name = name
        else:
            pass
            # print('le nom de l'objet cree ne correspond pas aux different nom attendu, pour retier cette ligne de
            # code, allez : detect_region.py ligne 33')
    
    def __flag_(self, start): # permet de recuperer l'information de la source
        if self.__source:
            return self.flag
        else:
            if self.__inputo:
                if len(self.__inputo) == 1:
                    if start != self.__inputo[0]:
                        return self.__inputo[0].__flag_(start)
        return None
    
    @property
    def flag_loop(self):
        return self.__flag_(self)
    
    # inputo et outputo cree des listes des input/output entre les objets voulue
    # attention lors de son utilisation si plusieurs input sont defini avant d'utiliser
    # la fonction "flag_loop" pour detecter la region de l'objet, il faut 1
    # recontruire les chemins partant de l'objet source
    # pour cela on utilisera la fonction "reconstruc_path"
    
    @property
    def inputo(self):
        return self.__inputo
    
    @inputo.setter
    def inputo(self, obj):
        if self.delet:
            self.__inputo.remove(obj)
        else:
            self.__inputo.append(obj)
    
    @property
    def outputo(self):
        return self.__outputo
    
    @outputo.setter
    def outputo(self, obj):
        if self.delet:
            self.__outputo.remove(obj)
        else:
            self.__outputo.append(obj)
    
    def connect(self, obj): # Permet de connecter deux objets
        self.delet = False
        obj.delet = False
        self.inputo = obj
        obj.outputo = self
    
    # deconnect deux objets
    # pour simplifier l'utilisation de la fonction, nous considérons que si l'utilisateur rentre
    # je veux déconnecter A et B sera la meme chose que déconnecter B et A
    # donc l'ordre n'a plus d'importance lors de l'utilisation de la fonction
    def disconnect(self, obj): # Permet de déconnecter deux objets
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
    
    # permet de détruire l'intégralité de l'objet et ses connexions
    def delete_connection(self):
        [self.disconnect(i) for i in self.inputo]
        [self.disconnect(i) for i in self.outputo]
    
    # à utiliser lorsque l'on déconnecte deux objets si l'on veut recree correctement
    # les chemins jusqu'à l'objet source
    
    def reconstruc_path(self, source_flag):
        in_out = [self.outputo[i] if i < len(self.outputo) else self.inputo[i - len(self.outputo) - 1] for i in
                  range(len(self.outputo) + len(self.inputo))]
        # melange les inputs et les outputs de l'objet et les redefines
        # en fonction de la direction de la source
        # par la suite on isolera la source et considerations que tous les autres ports
        # de l'objet sont des outputs de ce dernier
        # la reconstruction de chemin se base sur le fait que si le prochain
        # segment de chemin est deja connecté à la source recheck on se permet de
        # l'ignorer et de continuer à parcourir les ports de no blocs
        
        for i in in_out:
            i.disconnect(self)
            if i != source_flag:
                
                if i.flag_loop is None or i.flag_loop != self.flag_loop:
                    i.connect(self)
                    i.reconstruc_path(self)
                else:
                    i.outputo = self
                    self.outputo = i
            else:
                self.connect(i)
