import pygame
import random

map_width = 512
map_height = 512

def generarMatriz(t):
    m = []
    for x in range(map_width//32):
        x = []
        for y in range(map_height//32):
            x.append(t)
        m.append(x)
    return m

class Todo:
    objetos = generarMatriz(None)

    @classmethod
    def definirOrigen():
        x,y = pygame.mouse.get_pos()
        pos = [(x//32)*32, (y//32)*32]
        return pos

    @classmethod
    def definirMeta():
        x,y = pygame.mouse.get_pos()
        pos = [(x//32)*32, (y//32)*32]
        return pos

    @classmethod
    def agregarObjeto(cls, obj):
        # cls.objetos[obj.coord[0]][obj.coord[1]]
        x, y = obj.coord[0]//32, obj.coord[1]//32
        cls.objetos[x][y] = obj
    
    @classmethod
    def eliminarObjeto(cls, pos):
        # cls.objetos[obj.coord[0]][obj.coord[1]]
        # print(f"pos: {pos}")
        x, y = pos[0]//32, pos[1]//32
        print("coord", x, y)
        cls.objetos[x][y] = None

    @classmethod
    def verObjetos(cls):
        print("objetos")
        for i in cls.objetos:
            for obj in i:
                if obj:
                    print(f"{obj.descripcion}\n")
        print("@\n")

    @classmethod
    def draw(cls, todo):
        for obj_i in cls.objetos:
            for obj_j in obj_i:
                if obj_j:
                    obj_j.draw(todo)

    @classmethod
    def mouse(cls):
        x,y = pygame.mouse.get_pos()
        pos = [(x//32)*32, (y//32)*32]

        if pygame.mouse.get_pressed()[0] == True:
            return pos, False
        elif pygame.mouse.get_pressed()[2] == True:
            return pos, True
        else:
            return False, False

class Materia():
    def __init__(self, id, name, color, coord, size=[32, 32]):
        self.id = id
        self.name = name
        self.color = color
        self.coord = coord
        self.size = size

    # surface, color, (posicion & dimension)
    def draw(self, ventana):
        size = (self.coord[0], self.coord[1], self.size[0], self.size[1])
        pygame.draw.rect(ventana, self.color, size)

    @property
    def descripcion(self):
        print('id:         \t', self.id)
        print('coordenadas:\t', self.coord[0] // 32, self.coord[1] // 32)
        print('nombre:     \t', self.name)

class SerVivo(Materia):
    def __init__(self, id, name, color, coord, mapa = generarMatriz(0)):
        super().__init__(id, name, color, coord)
        self.mapa = mapa
        self.moving = False
        self.vel = 32

    @property
    def verMapa(self):
        print("mapa")
        for i in self.mapa:
            print(f"{i}")
            
    def checkBorders(self):
        # print(f"x: {x}, y:{y}, coord: {self.coord}, b:{b}")
        x = self.coord[0]
        y = self.coord[1]
        b = [True, True, True, True]
        if x == (map_width) - 32:
            b[0] = False
        if y == 0:
            b[1] = False
        if x == 0:
            b[2] = False
        if y == (map_height) - 32:
            b[3] = False

        return b

    def movRandom(self):
        if self.moving:
            lista = [pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s]
            d = random.sample(lista, k=1)[-1]
            self.accion(d)

    def accion(self, evento):
        # print(f"evento: {evento}")
        b = self.checkBorders()
        coord_x = self.coord[0]
        coord_y = self.coord[1]

        if evento == pygame.K_d and b[0]:
            if not(Todo.objetos[(coord_x+32)//32][coord_y//32]):
                self.coord[0] += self.vel
                self.mapa[coord_y//32][coord_x//32] += 1
        
        if evento == pygame.K_w and b[1]:
            if not(Todo.objetos[(coord_x)//32][(coord_y-32)//32]):
                self.coord[1] -= self.vel
                self.mapa[coord_y//32][coord_x//32] += 1

        if evento == pygame.K_a and b[2]:
            if not(Todo.objetos[(coord_x-32)//32][coord_y//32]):
                self.coord[0] -= self.vel
                self.mapa[coord_y//32][coord_x//32] += 1
        
        if evento == pygame.K_s and b[3]:
            if not(Todo.objetos[(coord_x)//32][(coord_y+32)//32]):
                self.coord[1] += self.vel
                self.mapa[coord_y//32][coord_x//32] += 1

        if evento == pygame.K_i:
            self.descripcion

        if evento == pygame.K_u:
            self.verMapa

        if evento == pygame.K_SPACE:
            if self.moving:
                self.moving = False
            else:
                self.moving = True

        # print(f"x, y: {self.coord[0]}, {self.coord[1]} - {Todo.objetos[(self.coord[0]+32)//32][self.coord[1]//32].descripcion}@\n")
