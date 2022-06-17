import pygame, pygame.font
import random, math

pygame.font.init()
map_width = 384
map_height = 384
obj_size = 32
iteraciones = 100


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
        for i in range(4):
            if self.rastro < rango:
                if p[i]:
                    if p[i].id == 0:
                        # calcular intensidad segun el origen, Manhattan distance
                        intensidad = (abs(p[i].coord[0] - origen[0]) + abs(p[i].coord[1] - origen[1])) // obj_size
                        c = (120/rango)*intensidad
                        color = tuple([0, 130-c, 0])
                        temp = feromona(4, name = "feromona", color = color, coord = p[i].coord, rastro = intensidad, origen = origen)
                        Todo.agregarObjeto(temp)
                        z.append(temp)

        for ad in z:
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
        cls.objetos[y][x] = Materia(0, "Nada", (0,0,0), [x*obj_size, y*obj_size])

    @classmethod
    def verObjetos(cls):
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
        self.mapa = self.generarMapa()

        self.vel = obj_size
        self.uu = ""
        self.iter_count = 0
        self.origen = [0, 0]

        self.mostrar_mapa = False
        self.moving = False
        self.seguir_camino = False
        

    def defOrigen(self):
        x,y = pygame.mouse.get_pos()
        pos = [(x//obj_size)*obj_size, (y//obj_size)*obj_size]
        self.coord = pos

    def generarMapa(self):
        matriz = []
        for i in range(map_width//obj_size):
            fila = []
            for j in range(map_height//obj_size):
                fila.append(0)
            matriz.append(fila)
        
        return matriz

    def verMapa(self, ventana):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[0])):
                Font=pygame.font.SysFont('timesnewroman',  15)
                l=Font.render(str(self.mapa[j][i]), False, (254,254,254), (0,0,0))
                ventana.blit(l, (i*obj_size + (obj_size / 4), j*obj_size + (obj_size / 4)))
    
    def movRandom(self):
        lista_dir = []
        p = self.percibir()
        
        if p[4].id == 3:
            # mover a mabby al origen
            print(self.iter_count)
            self.iter_count += 1
            self.coord = [0, 0]
            if self.iter_count == iteraciones:
                self.uu = ""
                self.mostrar_mapa = True
                self.moving = False
                self.seguir_camino = True
            return 0

        if p[0] and self.uu != "E":
            lista_dir.append(["E", p[0]])
        if p[1] and self.uu != "N":
            lista_dir.append(["N", p[1]])
        if p[2] and self.uu != "O":
            lista_dir.append(["O", p[2]])
        if p[3] and self.uu != "S":
            lista_dir.append(["S", p[3]])

        try:
            d = random.sample(lista_dir, k=1)[-1]

            if d[0] == "E":
                self.uu = "O"
            if d[0] == "N":
                self.uu = "S"
            if d[0] == "O":
                self.uu = "E"
            if d[0] == "S":
                self.uu = "N"

            self.mover(d[0])
        except:
            self.uu = ""

    def seguirCamino(self):
        lista_dir = []
        p = self.percibir()
        temp = 0

        if p[4].id == 3:
            self.seguir_camino = False
            self.iter_count = 0
            return 0

        if p[0] and self.uu != "E":
            lista_dir.append(["E", self.mapa[p[0].coord[1]//obj_size][p[0].coord[0]//obj_size]])
        else:
            lista_dir.append(None)
        if p[1] and self.uu != "N":
            lista_dir.append(["N", self.mapa[p[1].coord[1]//obj_size][p[1].coord[0]//obj_size]])
        else:
            lista_dir.append(None)
        if p[2] and self.uu != "O":
            lista_dir.append(["O", self.mapa[p[2].coord[1]//obj_size][p[2].coord[0]//obj_size]])
        else:
            lista_dir.append(None)
        if p[3] and self.uu != "S":
            lista_dir.append(["S", self.mapa[p[3].coord[1]//obj_size][p[3].coord[0]//obj_size]])
        else:
            lista_dir.append(None)

        for t in lista_dir:
            if t:
                temp = t
                break

        for i in range(4):
            if lista_dir[i]:
                if p[i].id == 3:
                    temp = lista_dir[i]
                    break
                elif temp[1] > lista_dir[i][1]:
                    temp = lista_dir[i]

        if temp[0] == "E":
            self.uu = "O"
        if temp[0] == "N":
            self.uu = "S"
        if temp[0] == "O":
            self.uu = "E"
        if temp[0] == "S":
            self.uu = "N"

        self.mover(temp[0])

    def percibir(self):
        x = self.coord[0]//obj_size
        y = self.coord[1]//obj_size
        pos_actual = Todo.objetos[y][x]

        b = checkBorders(self.coord)
        percibido = [None, None, None, None, pos_actual]

        if b[0]:
            E = Todo.objetos[y][x+1]
            if E.id == 0 or E.id == 3 or E.id == 4:
                percibido[0] = E
        if b[1]:
            N = Todo.objetos[y-1][x]
            if N.id == 0 or N.id == 3 or N.id == 4:
                percibido[1] = N
        if b[2]:
            O = Todo.objetos[y][x-1]
            if O.id == 0 or O.id == 3 or O.id == 4:
                percibido[2] = O
        if b[3]:
            S = Todo.objetos[y+1][x]
            if S.id == 0 or S.id == 3 or S.id == 4:
                percibido[3] = S
        
        return percibido

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

        if evento == pygame.K_d and p[0]:
            self.mover("E")
        if evento == pygame.K_w and p[1]:
            self.mover("N")
        if evento == pygame.K_a and p[2]:
            self.mover("O")
        if evento == pygame.K_s and p[3]:
            self.mover("S")

        # mapa
        if evento == pygame.K_u:
            if self.mostrar_mapa:
                self.mostrar_mapa = False
            else:
                self.mostrar_mapa = True
        
        # descripcion
        if evento == pygame.K_i:
            self.descripcion
        
        # definir punto de origen
        if evento == pygame.K_o:
            self.defOrigen()

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

    # def draw(self, ventana):
    #     Font=pygame.font.SysFont('timesnewroman',  15)
    #     l=Font.render(str(self.rastro), False, (254,254,254), self.color)
    #     x = self.coord[0] + (obj_size / 4)
    #     y = self.coord[1] + (obj_size / 4)

    #     size = (self.coord[0], self.coord[1], self.size[0], self.size[1])
    #     pygame.draw.rect(ventana, self.color, size)
    #     ventana.blit(l, (x, y))
