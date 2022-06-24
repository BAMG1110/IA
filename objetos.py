import pygame, pygame.font
import random, math
import pickle

pygame.font.init()
map_width       = 640
map_height      = 640
obj_size        = 32
rango_rastro    = 8
#nombre del mapa a guardar
nmg     = 'data_n.pickle'


def checkBorders(coord):
    x = coord[0]
    y = coord[1]
    b = [True, True, True, True]
    if x+obj_size >= map_width:
        b[0] = None
    if y - obj_size < 0:
        b[1] = None
    if x - obj_size < 0:
        b[2] = None
    if y+obj_size >= map_height:
        b[3] = None

    return b

def checkAround(coord):
    x = coord[0]//obj_size
    y = coord[1]//obj_size

    b = checkBorders(coord)
    periferia = [["E", None], ["N", None], ["O", None], ["S", None]]

    if b[0]:
        E = ["E", Todo.objetos[y][x+1]]
        periferia[0] = E
    if b[1]:
        N = ["N", Todo.objetos[y-1][x]]
        periferia[1] = N
    if b[2]:
        O = ["O", Todo.objetos[y][x-1]]
        periferia[2] = O
    if b[3]:
        S = ["S", Todo.objetos[y+1][x]]
        periferia[3] = S
    
    return periferia

def generarMatriz(x = None):
    matriz = []

    if not(x):
        for i in range(map_width//obj_size):
            fila = []
            for j in range(map_height//obj_size):
                coordenada = [j*obj_size, i*obj_size]
                fila.append(Materia(0, "Nada", (0,0,0), coordenada))
            matriz.append(fila)
    else:
        for i in range(map_width//obj_size):
            fila = []
            for j in range(map_height//obj_size):
                coordenada = [j*obj_size, i*obj_size]
                fila.append(x)
            matriz.append(fila)
    
    return matriz

def guardarMapa():
    data = Todo.objetos
    with open(nmg, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def cargarMapa(nombre):
    with open(nombre, 'rb') as f:
        Todo.objetos = pickle.load(f)

def borrarMapa():
    Todo.objetos = generarMatriz()
    
def datos():
    print(f"\nmeta actual: {Todo.meta_actual}")
    print(f"abiertos: {Nodo.opened}")
    print(f"analizados: {Nodo.closed} len {len(Nodo.closed)}\n")


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


class Todo:
    objetos = generarMatriz()
    meta_actual = False

    @classmethod
    def agregarObjeto(cls, obj):
        x, y = obj.coord[0]//obj_size, obj.coord[1]//obj_size
        cls.objetos[y][x] = obj

    @classmethod
    def eliminarObjeto(cls, pos):
        x, y = pos[0], pos[1]
        cls.objetos[y//obj_size][x//obj_size] = Materia(0, "Nada", (0,0,0), [x, y])
    
    @classmethod
    def verObjeto(cls):
        x,y = Todo.mouse()
        obj = cls.objetos[y//obj_size][x//obj_size]
        print(obj.descripcion)

    @classmethod
    def verMatrizObjetos(cls):
        for obj in cls.objetos:
            print(obj)
        print("\n")

    @classmethod
    def defMeta(cls):
        x, y = cls.mouse()
        for fila in cls.objetos:
            for obj in fila:
                if obj.id == 3:
                    cls.objetos[obj.coord[1]//obj_size][obj.coord[0]//obj_size] = Materia(0, "Nada", (0,0,0), [obj.coord[0], obj.coord[1]])
                if obj.id == 4:
                    cls.objetos[obj.coord[1]//obj_size][obj.coord[0]//obj_size] = Materia(0, "Nada", (0,0,0), [obj.coord[0], obj.coord[1]])

        cls.objetos[y//obj_size][x//obj_size] = Materia(3, "Meta", (0,255,0), [x, y])
        cls.meta_actual = [x, y]
        return cls.objetos[y//obj_size][x//obj_size]
        
    @classmethod
    def draw(cls, todo):
        for i in cls.objetos:
            for j in i:
                j.draw(todo)

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

        return pos

     
class SerVivo(Materia):
    def __init__(self, id, name, color, coord):
        super().__init__(id, name, color, coord)
        self.mapa = generarMatriz(0)
        self.vel = obj_size

        self.mostrarMapa = False
        self.buscarMeta = False

    def defOrigen(self):
        x,y = Todo.mouse()
        pos = [x, y]
        self.coord = pos

    def verMapa(self, ventana):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[0])):
                Font=pygame.font.SysFont('timesnewroman',  15)
                l=Font.render(str(self.mapa[j][i]), False, (254,254,254), (0,0,0))
                ventana.blit(l, (i*obj_size + (obj_size / 4), j*obj_size + (obj_size / 4)))

    def percibir(self):
        p = checkAround(self.coord)

        if p[0][1]:
            if p[0][1].id == 2:
                p[0] = ["E", None]

        if p[1][1]:
            if p[1][1].id == 2:
                p[1] = ["N", None]

        if p[2][1]:
            if p[2][1].id == 2:
                p[2] = ["O", None]

        if p[3][1]:
            if p[3][1].id == 2:
                p[3] = ["S", None]

        return p

    def mover(self, direccion):
        if direccion == "E":
            self.coord[0] += self.vel
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1
        if direccion == "N":
            self.coord[1] -= self.vel
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1
        if direccion == "O":
            self.coord[0] -= self.vel
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1
        if direccion == "S":
            self.coord[1] += self.vel
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1

    def accion(self, evento):
        p = self.percibir()
        print("@: ", evento, p)

        if evento == pygame.K_d and p[0][1]:
            self.mover("E")
        if evento == pygame.K_w and p[1][1]:
            self.mover("N")
        if evento == pygame.K_a and p[2][1]:
            self.mover("O")
        if evento == pygame.K_s and p[3][1]:
            self.mover("S")

        # descripcion
        if evento == pygame.K_i:
            self.descripcion
        
        # mapa
        if evento == pygame.K_u:
            if self.mostrarMapa:
                self.mostrarMapa = False
            else:
                self.mostrarMapa = True

        # definir origen
        if evento == pygame.K_o:
            self.defOrigen()

        # inciar A*
        if evento == pygame.K_SPACE:
            if self.buscarMeta:
                self.buscarMeta = False
            else:
                self.buscarMeta = True


class Nodo(Materia):
    pass