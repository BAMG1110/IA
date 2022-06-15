import pygame, pygame.font
import random, math

pygame.font.init()
map_width       = 640
map_height      = 640
obj_size        = 32
rango_rastro    = 8


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
    periferia = [["E", None], ["N", None], ["O", None], ["S", None], ["actual", Todo.objetos[y][x]]]

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
                if p[i][1]:
                    if p[i][1].id == 0:
                        # calcular intensidad segun el origen, Manhattan distance
                        intensidad = (abs(p[i][1].coord[0] - origen[0]) + abs(p[i][1].coord[1] - origen[1])) // obj_size
                        c = (120/rango)*intensidad
                        color = tuple([0, 130-c, 0])
                        temp = Feromona(4, name = "feromona", color = color, coord = p[i][1].coord, rastro = intensidad, origen = origen)
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
        self.clones = []

        self.vel = obj_size
        self.uu = ""

        self.mostrarMapa = False
        self.moving = False
        self.PA = False

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
    
    def movRandom(self):
        per = self.percibir()
        pm = []
        print(f"per {per}")

        
        # si mabby esta sobre la meta, detener
        # if p[4].id == 3:
        #     self.moving = False
        #     return 0

        # posibles movimientos
        for l in per:
            if l[1]:
                if l[1].id == 4:
                    pm.append(l)

        print(f"pm {pm} {len(pm)}")

        # # si se detecta un rastro, elegir el mas cercano
        # for f in fer:
        #     if f[1].rastro < r_min:
        #         r_min = f[1].rastro
        #         fer_min = f


        # if fer_min:
        #     if fer_min[0] == "E":
        #         self.uu = "O"
        #     if fer_min[0] == "N":
        #         self.uu = "S"
        #     if fer_min[0] == "O":
        #         self.uu = "E"
        #     if fer_min[0] == "S":
        #         self.uu = "N"

        #     self.mover(fer_min[0])
        # else:
        #     try:
        #         d = random.sample(lista, k=1)[-1]
        #         if d == "E":
        #             self.uu = "O"
        #         if d == "N":
        #             self.uu = "S"
        #         if d == "O":
        #             self.uu = "E"
        #         if d == "S":
        #             self.uu = "N"

        #         self.mover(d)
        #     except:
        #         print("el unico camino es por donde vengo...")
        #         self.uu = ""

    def movPA(self):
        temp = 45
        temp_list = []
        temp_p = self.percibir()

        # si mabby esta sobre la meta, detener
        if temp_p[4].id == 3:
            self.PA = False
            self.moving = False
            return 0

        # suma de casillas adyacentes a los clones
        for c in range(len(self.clones)):
            p = self.clones[c].percibir()
            for obj in p:
                if obj:
                    if obj.id == 3:
                        self.mover(self.clones[c].direccion)
                        return 0
                    elif obj.id == 4:
                        self.clones[c].suma += obj.rastro
                    else:
                        self.clones[c].suma += (rango_rastro + 1)
                else:
                    self.clones[c].suma += (rango_rastro + 1)
            
            # obtener los clones con la menor suma
            if self.clones[c].suma == temp and self.clones[c].direccion != self.uu:
                temp = self.clones[c].suma
                temp_list.append(self.clones[c].direccion)
            elif self.clones[c].suma < temp and self.clones[c].direccion != self.uu:
                temp = self.clones[c].suma
                temp_list = [self.clones[c].direccion]

        try:
            d = random.sample(temp_list, k=1)[-1]
            if d == "E":
                self.uu = "O"
            if d == "N":
                self.uu = "S"
            if d == "O":
                self.uu = "E"
            if d == "S":
                self.uu = "N"
            self.mover(d)
        except:
            self.uu = ""

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

    def generarClones(self):
        self.clones = []
        chka = checkAround(self.coord)

        if chka[0]:
            if chka[0].id != 2:
                E = Clon(id=5, name="Clon", color=(254,254,0), coord=[(self.coord[0]+obj_size),(self.coord[1])], direccion="E")
                self.clones.append(E)
        if chka[1]:
            if chka[1].id != 2:
                N = Clon(id=5, name="Clon", color=(254,254,0), coord=[(self.coord[0]),(self.coord[1]-obj_size)], direccion="N")
                self.clones.append(N)
        if chka[2]:
            if chka[2].id != 2:
                O = Clon(id=5, name="Clon", color=(254,254,0), coord=[(self.coord[0]-obj_size),(self.coord[1])], direccion="O")
                self.clones.append(O)
        if chka[3]:
            if chka[3].id != 2:
                S = Clon(id=5, name="Clon", color=(254,254,0), coord=[(self.coord[0]),(self.coord[1]+obj_size)], direccion="S")
                self.clones.append(S)

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

        # aumentar percepcion
        if evento == pygame.K_c:
            if self.PA:
                self.PA = False
            else:
                self.PA = True


        # mover random
        if evento == pygame.K_SPACE:
            if self.moving:
                self.moving = False
            else:
                self.moving = True


class Feromona(Materia):
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

class Clon(Materia):
    def __init__(self, id, name, color, coord, direccion):
        super().__init__(id, name, color, coord)
        self.direccion = direccion
        self.suma = 0
    
    def percibir(self):
        x = self.coord[0]//obj_size
        y = self.coord[1]//obj_size

        b = checkBorders(self.coord)
        percibido = [None, None, None, None, None]

        percibido[4] = Todo.objetos[y][x]

        if b[0] and self.direccion != "O":
            E = Todo.objetos[y][x+1]
            if E.id == 0 or E.id == 3 or E.id == 4:
                percibido[0] = E
        if b[1] and self.direccion != "S":
            N = Todo.objetos[y-1][x]
            if N.id == 0 or N.id == 3 or N.id == 4:
                percibido[1] = N
            
        if b[2] and self.direccion != "E":
            O = Todo.objetos[y][x-1]
            if O.id == 0 or O.id == 3 or O.id == 4:
                percibido[2] = O
            
        if b[3] and self.direccion != "N":
            S = Todo.objetos[y+1][x]
            if S.id == 0 or S.id == 3 or S.id == 4:
                percibido[3] = S
            
        
        return percibido
