import pygame
import random

map_width = 512
map_height = 512
obj_size = 16

def generarMatriz(t):
    m = []
    for x in range(map_width//obj_size):
        x = []
        for y in range(map_height//obj_size):
            x.append(t)
        m.append(x)
    return m

class Todo:
    objetos = generarMatriz(None)
    meta_actual = False

    @classmethod
    def agregarObjeto(cls, obj):
        # cls.objetos[obj.coord[0]][obj.coord[1]]
        x, y = obj.coord[0]//obj_size, obj.coord[1]//obj_size
        cls.objetos[x][y] = obj
    
    @classmethod
    def verObjetos(cls):
        print("objetos")
        for i in cls.objetos:
            for obj in i:
                if obj:
                    print(f"{obj.descripcion}\n")
        print("@\n")

    @classmethod
    def eliminarObjeto(cls, pos):
        # cls.objetos[obj.coord[0]][obj.coord[1]]
        # print(f"pos: {pos}")
        x, y = pos[0]//obj_size, pos[1]//obj_size
        cls.objetos[x][y] = None

    @classmethod
    def defMeta(cls):
        x,y = pygame.mouse.get_pos()
        pos = [(x//obj_size)*obj_size, (y//obj_size)*obj_size]

        if cls.meta_actual != pos:
            try:
                cls.eliminarObjeto(cls.meta_actual)
            except:
                pass
            cls.meta_actual = pos

        obj = Materia(3, "Meta", (0, 255, 0), cls.meta_actual)
        cls.agregarObjeto(obj)

    @classmethod
    def draw(cls, todo):
        for obj_i in cls.objetos:
            for obj_j in obj_i:
                if obj_j:
                    obj_j.draw(todo)

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

    # surface, color, (posicion & dimension)
    def draw(self, ventana):
        size = (self.coord[0], self.coord[1], self.size[0], self.size[1])
        pygame.draw.rect(ventana, self.color, size)

    @property
    def descripcion(self):
        print('id:         \t', self.id)
        print('coordenadas:\t', self.coord[0] // obj_size, self.coord[1] // obj_size)
        print('nombre:     \t', self.name)

class SerVivo(Materia):
    def __init__(self, id, name, color, coord, mapa = generarMatriz(0)):
        super().__init__(id, name, color, coord)
        self.mapa = mapa
        self.moving = False
        self.vel = obj_size

    
    def defOrigen(self):
        x,y = pygame.mouse.get_pos()
        pos = [(x//obj_size)*obj_size, (y//obj_size)*obj_size]
        self.coord = pos

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
        if x == (map_width) - obj_size:
            b[0] = False
        if y == 0:
            b[1] = False
        if x == 0:
            b[2] = False
        if y == (map_height) - obj_size:
            b[3] = False

        return b

    def movRandom(self):
        if self.moving:
            lista = [pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s]
            d = random.sample(lista, k=1)[-1]
            self.accion(d)

    def accion(self, evento):
        # print(f"evento: {evento}")
        # print(f"x, y: {self.coord[0]}, {self.coord[1]} - {Todo.objetos[(self.coord[0]+obj_size)//32][self.coord[1]//32].descripcion}@\n")
        b = self.checkBorders()
        coord_x = self.coord[0]
        coord_y = self.coord[1]

        # meta alcanzada
        # wasd
        if evento == pygame.K_d and b[0]:
            obj_der = Todo.objetos[(coord_x+obj_size)//obj_size][coord_y//obj_size]
            if not(obj_der):
                self.coord[0] += self.vel
                self.mapa[coord_y//obj_size][coord_x//obj_size] += 1
            elif obj_der.id == 3:
                self.coord[0] += self.vel
                self.moving = False
        
        if evento == pygame.K_w and b[1]:
            obj_arriba = Todo.objetos[(coord_x)//obj_size][(coord_y-obj_size)//obj_size]
            if not(obj_arriba):
                self.coord[1] -= self.vel
                self.mapa[coord_y//obj_size][coord_x//obj_size] += 1
            elif obj_arriba.id == 3:
                self.coord[1] -= self.vel
                self.moving = False


        if evento == pygame.K_a and b[2]:
            obj_izq = Todo.objetos[(coord_x-obj_size)//obj_size][coord_y//obj_size]
            if not(obj_izq):
                self.coord[0] -= self.vel
                self.mapa[coord_y//obj_size][coord_x//obj_size] += 1
            elif obj_izq.id == 3:
                self.coord[0] -= self.vel
                self.moving = False

        if evento == pygame.K_s and b[3]:
            obj_abajo = Todo.objetos[(coord_x)//obj_size][(coord_y+obj_size)//obj_size]
            if not(obj_abajo):
                self.coord[1] += self.vel
                self.mapa[coord_y//obj_size][coord_x//obj_size] += 1
            elif obj_abajo.id == 3:
                self.coord[1] += self.vel
                self.moving = False

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

