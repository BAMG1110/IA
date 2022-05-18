import pygame
import random

map_width = 512
map_height = 512

class Materia():
    def __init__(self, id, name, coord=[32, 32], size=[32, 32]):
        self.id = id
        self.name = name
        self.coord = coord
        self.size = size

    # surface, color, (posicion & dimension)
    def draw(self, todo, color=(0, 0, 0)):
        size = (self.coord[0], self.coord[1], self.size[0], self.size[1])
        pygame.draw.rect(todo, color, size)

    @property
    def descripcion(self):
        print('id:         \t', self.id)
        print('coordenadas:\t', self.coord[0] // 32, self.coord[1] // 32)
        print('nombre:     \t', self.name)

class SerVivo(Materia):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.moving = False
        self.vel = 32

    def checkBoundaries(self):
        x = self.coord[0]
        y = self.coord[1]
        b = [True, True, True, True]
        # print(f"x: {x}, y:{y}, coord: {self.coord}, b:{b}")
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

        if evento == pygame.K_d:
            self.coord[0] += self.vel
        if evento == pygame.K_w:
            self.coord[1] -= self.vel
        if evento == pygame.K_a:
            self.coord[0] -= self.vel
        if evento == pygame.K_s:
            self.coord[1] += self.vel

        if evento == pygame.K_i:
            self.descripcion

        if evento == pygame.K_SPACE:
            self.moving = True
        if evento == pygame.K_m:
            self.moving = False
    
