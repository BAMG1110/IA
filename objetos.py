import pygame, pygame.font
import random, math

pygame.font.init()
map_width = 640
map_height = 640
obj_size = 32


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
    periferia = [None, None, None, None]

    if b[0]:
        E = Todo.objetos[y][x+1]
        periferia[0] = E
    if b[1]:
        N = Todo.objetos[y-1][x]
        periferia[1] = N
    if b[2]:
        O = Todo.objetos[y][x-1]
        periferia[2] = O
    if b[3]:
        S = Todo.objetos[y+1][x]
        periferia[3] = S
    
    return periferia

def generarMatriz():
    matriz = []
    for i in range(map_width//obj_size):
        fila = []
        for j in range(map_height//obj_size):
            coordenada = [j*obj_size, i*obj_size]
            fila.append(Materia(0, "Nada", (0,0,0), coordenada))
        matriz.append(fila)
    
    return matriz

class Materia():
    def __init__(self, id, name, color, coord, size=[obj_size, obj_size], rastro = 0):
        self.id = id
        self.name = name
        self.color = color
        self.coord = coord
        self.size = size
        self.rastro = rastro
    
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

    def generarRastro(self, rango, origen = None):
        coord = self.coord
        if not(origen):
            origen = self.coord
        
        p = checkAround(coord)
        z = []

        if self.rastro < rango:
            # Este
            if p[0]:
                if p[0].id == 0:
                    # calcular intensidad segun el origen, Manhattan distance
                    intensidad = (abs(p[0].coord[0] - origen[0]) + abs(p[0].coord[1] - origen[1])) // obj_size
                    c = (120/rango)*intensidad
                    color = tuple([0, 130, 0])
                    temp = feromona(4, name = "feromona", color = color, coord = p[0].coord, rastro = intensidad, origen = origen)
                    Todo.agregarObjeto(temp)
                    z.append(temp)
            # Norte
            if p[1]:
                if p[1].id == 0:
                    # calcular intensidad segun el origen, Manhattan distance
                    intensidad = (abs(p[1].coord[0] - origen[0]) + abs(p[1].coord[1] - origen[1])) // obj_size
                    c = (120/rango)*intensidad
                    color = tuple([0, 130, 0])
                    temp = feromona(4, name = "feromona", color = color, coord = p[1].coord, rastro = intensidad, origen = origen)
                    Todo.agregarObjeto(temp)
                    z.append(temp)
            # Oeste
            if p[2]:
                if p[2].id == 0:
                    # calcular intensidad segun el origen, Manhattan distance
                    intensidad = (abs(p[2].coord[0] - origen[0]) + abs(p[2].coord[1] - origen[1])) // obj_size
                    c = (120/rango)*intensidad
                    color = tuple([0, 130, 0])
                    temp = feromona(4, name = "feromona", color = color, coord = p[2].coord, rastro = intensidad, origen = origen)
                    Todo.agregarObjeto(temp)
                    z.append(temp)
            # Sur
            if p[3]:
                if p[3].id == 0:
                    # calcular intensidad segun el origen, Manhattan distance
                    intensidad = (abs(p[3].coord[0] - origen[0]) + abs(p[3].coord[1] - origen[1])) // obj_size
                    c = (120/rango)*intensidad
                    color = tuple([0, 130, 0])
                    temp = feromona(4, name = "feromona", color = color, coord = p[3].coord, rastro = intensidad, origen = origen)
                    Todo.agregarObjeto(temp)
                    z.append(temp)

            for ad in z:
                print(ad.rastro)
                ad.generarRastro(rango, origen)


class Todo:
    objetos = generarMatriz()
    meta_actual = False

    @classmethod
    def agregarObjeto(cls, obj):
        x, y = obj.coord[0]//obj_size, obj.coord[1]//obj_size
        cls.objetos[y][x] = obj

    @classmethod
    def eliminarObjeto(cls, pos):
        x, y = pos[0]//obj_size, pos[1]//obj_size
        cls.objetos[y][x] = Materia(0, "Nada", (0,0,0), [x, y])

    @classmethod
    def verObjetos(cls):
        for obj in cls.objetos:
            print(obj)
        print("\n")

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

     
class SerVivo(Materia):
    def __init__(self, id, name, color, coord, mapa = generarMatriz()):
        super().__init__(id, name, color, coord)
        self.mapa = mapa
        self.mostrarMapa = False
        self.moving = False
        self.vel = obj_size
        self.ultima_ubicacion = ""

    def defOrigen(self):
        Todo.eliminarObjeto(self.coord)
        x,y = pygame.mouse.get_pos()
        pos = [(x//obj_size)*obj_size, (y//obj_size)*obj_size]
        self.coord = pos

    def verMapa(self, ventana):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[0])):
                Font=pygame.font.SysFont('timesnewroman',  15)
                l=Font.render(str(self.mapa[j][i]), False, (254,254,254), (0,0,0))
                ventana.blit(l, (i*obj_size + (obj_size / 4), j*obj_size + (obj_size / 4)))
    
    def movRandom(self):
        if self.moving:
            lista = ["E", "N", "O", "S"]
            d = random.sample(lista, k=1)[-1]
            
            if d != self.ultima_ubicacion:
                if d == "E":
                    self.ultima_ubicacion = "O"
                elif d == "O":
                    self.ultima_ubicacion = "E"
                elif d == "N":
                    self.ultima_ubicacion = "S"
                elif d == "S":
                    self.ultima_ubicacion = "N"

                print(d, self.ultima_ubicacion)
                self.accion(d)

    def percibir(self):
        x = self.coord[0]//obj_size
        y = self.coord[1]//obj_size

        b = checkBorders(self.coord)
        percibido = [None, None, None, None]

        if b[0]:
            E = Todo.objetos[y][x+1]
            if E.id == 0:
                percibido[0] = E
        if b[1]:
            N = Todo.objetos[y-1][x]
            if N.id == 0:
                percibido[1] = N
        if b[2]:
            O = Todo.objetos[y][x-1]
            if O.id == 0:
                percibido[2] = O
        if b[3]:
            S = Todo.objetos[y+1][x]
            if S.id == 0:
                percibido[3] = S
        
        return percibido

    def mover(self, direccion):
        if direccion == "E":
            self.coord[0] += self.vel
            # lugar visitado, subir contador en el mapa
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1
        if direccion == "N":
            self.coord[1] -= self.vel
            # lugar visitado, subir contador en el mapa
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1
        if direccion == "O":
            self.coord[0] -= self.vel
            # lugar visitado, subir contador en el mapa
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1
        if direccion == "S":
            self.coord[1] += self.vel
            # lugar visitado, subir contador en el mapa
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1
        
    def accion(self, evento):
        p = self.percibir()
        print("@: ", evento, p)

        if evento == pygame.K_d and p[0]:
            self.mover("E")
        if evento == pygame.K_w and p[1]:
            self.mover("N")
        if evento == pygame.K_a and p[2]:
            self.mover("O")
        if evento == pygame.K_s and p[3]:
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

        
        # mover random
        if evento == pygame.K_SPACE:
            if self.moving:
                self.moving = False
            else:
                self.moving = True


class feromona(Materia):
    def __init__(self, id, name, color, coord, rastro, origen):
        super().__init__(id, name, color, coord)
        self.rastro = rastro
        self.origen = origen

    def draw(self, ventana):
        Font=pygame.font.SysFont('timesnewroman',  15)
        l=Font.render(str(self.rastro), False, (254,254,254), self.color)
        x = self.coord[0] + (obj_size / 4)
        y = self.coord[1] + (obj_size / 4)

        size = (self.coord[0], self.coord[1], self.size[0], self.size[1])
        pygame.draw.rect(ventana, self.color, size)
        ventana.blit(l, (x, y))
