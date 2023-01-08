# la classe connection edge permet de gerer les connections entre 
# des objets a une sources et de savoir si l'objet regarde est 
# connecté a la source voulue

class ConnectionEdge:

    def __init__(self, name, flag=None, source=False):
        self.delet = False
        self.flag = flag
        self.__source = source
        self.__inputo = []
        self.__outputo = []
        self.is_check = False
        self.__name = name
        self.WARNING = 0

    # def __str__(self):
    #   return self.name

    # flag_loop et __flag_ pemettent de recuperer l'information a quelle source
    # est connecté l'objet concerné d'objet connecté a une source
    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, source):
        self.__source = source

    @property
    def name(self):
        return self.__name

    # condition propre au jeux sur les nom de nos objets
    @name.setter
    def name(self, name):
        if name in ['up', 'down', 'right', 'left']:
            self.__name = name
        else:
            pass
            # print('le nom de l objet cree ne correspond pas aux different nom attendu, pour retier cette ligne de
            # code aller: detect_region.py ligne 33')

    def __flag_(self, start):
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
    # attention lors de sont utilisation si plusieures input sont defini avant d'utiliser
    # la fonction "flag_loop" pour detecter la region de l'objet, il faut 1
    # recontruire les chemins partant de l'objet source
    # pour cela on utliserat la fonction "reconstruc_path"

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

    # connect deux objets
    def connect(self, obj):
        self.delet = False
        obj.delet = False
        self.inputo = obj
        obj.outputo = self

    # deconnect deux objets
    # pour simplifier l'utilisation de la fonction nous considerons que si l'utilisateur rentre
    # je veux deconnecter A et B serat la meme chose que deconnecter B et A
    # donc l'odre n'a plus d'importance lors de lutilisation de la fonction
    def disconnect(self, obj):
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

    # permet dedetruire l'integraliter de l'objet et ses connections
    def delete_connection(self):
        [self.disconnect(i) for i in self.inputo]
        [self.disconnect(i) for i in self.outputo]

    # a utiliser lorsque l'on deconnecte deux objet si l'on veux recree correctement
    # les chemins j'usqua l'objet source

    def reconstruc_path(self, source_flag):
        in_out = [self.outputo[i] if i < len(self.outputo) else self.inputo[i - len(self.outputo) - 1] for i in
                  range(len(self.outputo) + len(self.inputo))]
        # melange les input et les output de l'objet et les redefinies
        # en fonction de la direction de la source
        # par la suite on isoleras la source et considererons que tous les autres ports
        # de l'objet sont des output de ce dernier
        # la recontstruction de chemin ce base sur le fait que si le prochaine
        # segment de chemin est deja connecté a la source recheché on ce permet de
        # l'ignorer et de continuer a parcourir les ports de no blocs

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