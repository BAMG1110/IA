import pygame, pygame.font
import random, math

map_width = 640
map_height = 640
obj_size = 32

pygame.font.init()

def generarMatriz(t):
    m = []
    for x in range(map_width//obj_size):
        x = []
        for y in range(map_height//obj_size):
            x.append(t)
        m.append(x)
    return m

def checkBorders(coord):
    x = coord[0]
    y = coord[1]
    b = [True, True, True, True]
    if x == (map_width - obj_size):
        b[0] = False
    if y - obj_size < 0:
        b[1] = False
    if x - obj_size < 0:
        b[2] = False
    if y == (map_height - obj_size):
        b[3] = False

    return b

class Todo:
    objetos = generarMatriz(0)
    meta_actual = False

    @classmethod
    def agregarObjeto(cls, obj):
        # cls.objetos[obj.coord[0]][obj.coord[1]]
        x, y = obj.coord[1]//obj_size, obj.coord[0]//obj_size
        cls.objetos[x][y] = obj

    @classmethod
    def eliminarObjeto(cls, pos):
        # cls.objetos[obj.coord[0]][obj.coord[1]]
        # print(f"pos: {pos}")
        x, y = pos[1]//obj_size, pos[0]//obj_size
        cls.objetos[x][y] = 0

    @classmethod
    def obtenerObjeto(cls, coord):
        obj = cls.objetos[coord[1]//obj_size][coord[0]//obj_size]
        return obj

    @classmethod
    def defMeta(cls):
        x,y = pygame.mouse.get_pos()
        pos = [(x//obj_size)*obj_size, (y//obj_size)*obj_size]

        if cls.meta_actual != pos:
            try:
                cls.eliminarObjeto(cls.meta_actual)
                for obj in cls.objetos:
                    for ob in obj:
                        try:
                            if ob.id == 4:
                                cls.eliminarObjeto(ob.coord)
                        except:
                            pass
            except:
                pass
            cls.meta_actual = pos
        return Materia(3, "comida", (0,254,0), cls.meta_actual)
    
    @classmethod
    def verTodo(cls):
        print("Todo")
        for obj in cls.objetos:
            try:
                print(obj)
            except:
                pass

        return Materia(3, "Meta", (0, 255, 0), cls.meta_actual)
        
    @classmethod
    def draw(cls, todo):
        for obj_i in cls.objetos:
            for obj_j in obj_i:
                if obj_j:
                    obj_j.draw(todo)

    @classmethod
    def drawGrid(cls, todo):
        fw = map_width // obj_size
        fh = map_height // obj_size
        x = 0
        y = 0
        for l in range(fw):
            x = x + obj_size
            y = y + obj_size

            pygame.draw.line(todo, (55,55,55), (x, 0), (x, map_width))
            pygame.draw.line(todo, (55,55,55), (0, y), (map_height, y))

    @classmethod
    def mouse(cls):
        x,y = pygame.mouse.get_pos()
        pos = [(x//obj_size)*obj_size, (y//obj_size)*obj_size]

        if pygame.mouse.get_pressed()[0] == True:
            obj = Materia(2, "algun tipo de piedra", (255, 0, 0), pos)
            cls.agregarObjeto(obj)
        elif pygame.mouse.get_pressed()[2] == True:
            cls.eliminarObjeto(pos)


class Materia():
    def __init__(self, id, name, color, coord, size=[obj_size, obj_size]):
        self.id = id
        self.name = name
        self.color = color
        self.coord = coord
        self.size = size
    
    def __repr__(self):
        return f"{self.id}"

    def draw(self, ventana):
        size = (self.coord[0], self.coord[1], self.size[0], self.size[1])
        pygame.draw.rect(ventana, self.color, size)

    @property
    def descripcion(self):
        print('id:         \t', self.id)
        print('coordenadas:\t', self.coord[0] // obj_size, self.coord[1] // obj_size)
        print('nombre:     \t', self.name)

    def generarRastro(self, rango, coord = None):
        p = [[obj_size, 0], [0, -obj_size], [-obj_size, 0], [0, obj_size]]
        z = []
        if not(coord):
            coord = self.coord

        for i in p:
            zipped_lists = zip(i, coord)
            sum = [a + b for (a, b) in zipped_lists]

            # obtener adyacentes validos
            if (sum[0] >= 0 and sum[0] <= map_width-obj_size) and (sum[1] >= 0 and sum[1] <= map_width-obj_size):
                if not(Todo.objetos[sum[1]//obj_size][sum[0]//obj_size] != 0):
                    # calcular intensidad segun el origen, Manhattan distance
                    intensidad = (abs(sum[0] - self.coord[0]) + abs(sum[1] - self.coord[1])) // obj_size

                    # print(f"temp: {intensidad} rango: {rango} - {intensidad <= rango}")
                    if intensidad <= rango:
                        # c = intensidad*10 if intensidad*10 <= 120 else 120
                        c = (120/rango)*intensidad
                        color = tuple([0, 130-(c), 0])
                        temp = feromona(4, name = "feromona", color = color, coord = sum, origen = coord, intensidad = intensidad)
                        Todo.agregarObjeto(temp)
                        self.generarRastro(rango, sum)
                    

class SerVivo(Materia):
    def __init__(self, id, name, color, coord, mapa = generarMatriz(0)):
        super().__init__(id, name, color, coord)
        self.mapa = mapa
        self.buscando = False
        self.vel = obj_size

    def defOrigen(self):
        Todo.eliminarObjeto(self.coord)
        x,y = pygame.mouse.get_pos()
        pos = [(x//obj_size)*obj_size, (y//obj_size)*obj_size]
        self.coord = pos

    @property
    def verMapa(self):
        print("mapa")
        for i in self.mapa:
            print(f"{i}")

    def buscarComida(self):
        if self.buscando:
            # lista = [pygame.K_d, pygame.K_e, pygame.K_w, pygame.K_q, pygame.K_a, pygame.K_z, pygame.K_x, pygame.K_c]
            lista = [pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_x]
            d = random.sample(lista, k=1)[-1]
            self.accion(d)

    def percibir(self):
        x = self.coord[0]
        y = self.coord[1]

        E = Todo.obtenerObjeto([x+obj_size, y])
        N = Todo.obtenerObjeto([x, y-obj_size])
        O = Todo.obtenerObjeto([x-obj_size, y])
        S = Todo.obtenerObjeto([x, y+obj_size])
    
        percibido = {}
        b = checkBorders(self.coord)

        if b[0]:
            if E != 0:
                if E.id != 2:
                    percibido["E"] = [E, True]
                else:
                    percibido["E"] = [E, False]
            else:
                percibido["E"] = [E, True]
        else:
            percibido["E"] = ["NO EXISTE", False]

        if b[1]:
            if N != 0:
                if N.id != 2:
                    percibido["N"] = [N, True]
                else:
                    percibido["N"] = [N, False]
            else:
                percibido["N"] = [N, True]
        else:
            percibido["N"] = ["NO EXISTE", False]

        if b[2]:
            if O != 0:
                if O.id != 2:
                    percibido["O"] = [O,True]
                else:
                    percibido["O"] = [E,False]
            else:
                percibido["O"] = [O, True]
        else:
            percibido["O"] = ["NO EXISTE", False]

        if b[3]:
            if S != 0:
                if S.id != 2:
                    percibido["S"] = [S,True]
                else:
                    percibido["S"] = [S,False]
            else:
                percibido["S"] = [S, True]
        else:
            percibido["S"] = ["NO EXISTE", False]


        # print(percibido)
        return percibido

    def mover(self, direccion):
        print(direccion)
        if direccion == "E":
            self.coord[0] += self.vel
        if direccion == "N":
            self.coord[1] -= self.vel
        if direccion == "O":
            self.coord[0] -= self.vel
        if direccion == "S":
            self.coord[1] += self.vel
        

    def accion(self, evento):
        print("@: ", evento)
        p = self.percibir()

        if evento == pygame.K_d and p["E"][1]:
            self.mover("E")
        if evento == pygame.K_w and p["N"][1]:
            self.mover("N")
        if evento == pygame.K_a and p["O"][1]:
            self.mover("O")
        if evento == pygame.K_s and p["S"][1]:
            self.mover("S")

        # descripcion
        if evento == pygame.K_i:
            self.descripcion
        
        # mapa
        if evento == pygame.K_u:
            self.verMapa
        
        # mover random
        if evento == pygame.K_SPACE:
            if self.moving:
                self.moving = False
            else:
                self.moving = True


class feromona(Materia):
    def __init__(self, id, name, color, coord, origen, intensidad = 0):
        super().__init__(id, name, color, coord)
        self.origen = origen
        self.intensidad = intensidad

    # def draw(self, ventana):
    #     Font=pygame.font.SysFont('timesnewroman',  15)
    #     l=Font.render(str(self.intensidad), False, (254,254,254), self.color)
    #     x = self.coord[0] + (obj_size / 4)
    #     y = self.coord[1] + (obj_size / 4)

    #     size = (self.coord[0], self.coord[1], self.size[0], self.size[1])
    #     pygame.draw.rect(ventana, self.color, size)
    #     ventana.blit(l, (x, y))
