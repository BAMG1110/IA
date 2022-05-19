import pygame
import random

map_width = 512
map_height = 512

class Todo:
    objetos = []

    @classmethod
    def agregarObjeto(cls, obj):
        cls.objetos.append(obj)

    @classmethod
    def info(cls):
        print(f"objetos en el mapa:\n{cls.objetos}")

    @classmethod
    def draw(cls, todo):
        for obj in cls.objetos:
            obj.draw()

class Materia():
    def __init__(self, id, name, color, coord=[160, 160], size=[32, 32]):
        self.id = id
        self.name = name
        self.color = color
        self.coord = coord
        self.size = size

    # surface, color, (posicion & dimension)
    def draw(self, todo):
        size = (self.coord[0], self.coord[1], self.size[0], self.size[1])
        pygame.draw.rect(todo, self.color, size)

    @property
    def descripcion(self):
        print('id:         \t', self.id)
        print('coordenadas:\t', self.coord[0] // 32, self.coord[1] // 32)
        print('nombre:     \t', self.name)

class SerVivo(Materia):
    def __init__(self, id, name, color):
        super().__init__(id, name, color)
        self.moving = False
        self.vel = 32

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
        lista = [pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s]
        d = random.sample(lista, k=1)[-1]
        self.accion(d)

    def accion(self, evento):
        # print(f"evento: {evento}")
        b = self.checkBorders()
        if evento == pygame.K_d and b[0]:
            self.coord[0] += self.vel
        if evento == pygame.K_w and b[1]:
            self.coord[1] -= self.vel
        if evento == pygame.K_a and b[2]:
            self.coord[0] -= self.vel
        if evento == pygame.K_s and b[3]:
            self.coord[1] += self.vel

        if evento == pygame.K_i:
            self.descripcion

        if evento == pygame.K_SPACE:
            self.moving = True
        if evento == pygame.K_m:
            self.moving = False
    
