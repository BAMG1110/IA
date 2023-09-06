import pygame, pygame.font
import random, math
import pickle

pygame.font.init()

obj_size        = 16
map_width       = obj_size*40
map_height      = obj_size*40

#nombre del mapa a guardar
nmg = 'data_n.pickle'


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
    periferia = [["E", None], ["NE", None], ["N", None], ["NO", None], ["O", None], ["SO", None], ["S", None], ["SE", None]]

    if b[0]:
        E = ["E", Todo.objetos[y][x+1]]
        periferia[0] = E

    if b[1]:
        N = ["N", Todo.objetos[y-1][x]]
        periferia[2] = N

    if b[2]:
        O = ["O", Todo.objetos[y][x-1]]
        periferia[4] = O

    if b[3]:
        S = ["S", Todo.objetos[y+1][x]]
        periferia[6] = S

    if b[0] and b[1]:
        E = ["NE", Todo.objetos[y-1][x+1]]
        periferia[1] = E

    if b[1] and b[2]:
        O = ["NO", Todo.objetos[y-1][x-1]]
        periferia[3] = O

    if b[2] and b[3]:
        S = ["SO", Todo.objetos[y+1][x-1]]
        periferia[5] = S

    if b[3] and b[0]:
        S = ["SE", Todo.objetos[y+1][x+1]]
        periferia[7] = S
    
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
    print(f"siguiente: {Nodo.open_list[0]}\nabiertos:\n{Nodo.open_list}")

def obtenerCostoAdyacentes(p):
    adyacentes = []
    for i in p:
        if i[1]:
            adyacentes.append(0)
        else:
            adyacentes.append(1)
    return adyacentes


class Materia():
    def __init__(self, id, name, color, coord, size=[obj_size, obj_size]):
        self.id = id
        self.name = name
        self.color = color
        self.coord = coord
        self.size = size

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
        Nodo.open_list = []
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
            obj = Materia(2, "algun tipo de obstaculo", (255, 0, 0), pos)
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

    def __repr__(self):
        return f"{self.id}"

    def defOrigen(self):
        x,y = Todo.mouse()
        pos = [x, y]
        self.coord = pos

    def verMapa(self, ventana):
        for i in range(len(Todo.objetos)):
            for j in range(len(Todo.objetos[0])):
                Font=pygame.font.SysFont('timesnewroman',  15)
                l=Font.render(str(Todo.objetos[j][i]), False, (254,254,254), (0,0,0))
                ventana.blit(l, (i*obj_size + (obj_size / 4), j*obj_size + (obj_size / 4)))

    def percibir(self):
        p = checkAround(self.coord)

        if p[0][1]:
            if p[0][1].id == 2:
                p[0] = ["E", None]

        if p[2][1]:
            if p[2][1].id == 2:
                p[2] = ["N", None]

        if p[4][1]:
            if p[4][1].id == 2:
                p[4] = ["O", None]

        if p[6][1]:
            if p[6][1].id == 2:
                p[6] = ["S", None]
        
        if p[1][1]:
            if not(p[0][1]) and not(p[2][1]) or p[1][1].id == 2:
                p[1] = ["NE", None]

        if p[3][1]:
            if not(p[2][1]) and not(p[4][1]) or p[3][1].id == 2:
                p[3] = ["NO", None]

        if p[5][1]:
            if not(p[4][1]) and not(p[6][1]) or p[5][1].id == 2:
                p[5] = ["SO", None]

        if p[7][1]:
            if not(p[6][1]) and not(p[0][1]) or p[7][1].id == 2:
                p[7] = ["SE", None]

        return p

    def mover(self, direccion):
        if direccion == "E":
            self.coord[0] += self.vel
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1
        if direccion == "NE":
            self.coord[0] += self.vel
            self.coord[1] -= self.vel
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1
        if direccion == "N":
            self.coord[1] -= self.vel
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1
        if direccion == "NO":
            self.coord[0] -= self.vel
            self.coord[1] -= self.vel
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1
        if direccion == "O":
            self.coord[0] -= self.vel
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1
        if direccion == "SO":
            self.coord[0] -= self.vel
            self.coord[1] += self.vel
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1
        if direccion == "S":
            self.coord[1] += self.vel
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1
        if direccion == "SE":
            self.coord[0] += self.vel
            self.coord[1] += self.vel
            self.mapa[self.coord[1]//obj_size][self.coord[0]//obj_size] += 1

    def accion(self, evento):
        p = self.percibir()
        # print("@: ", evento, p)

        if evento == pygame.K_d and p[0][1]:
            self.mover("E")
        if evento == pygame.K_e and p[1][1]:
            self.mover("NE")
        if evento == pygame.K_w and p[2][1]:
            self.mover("N")
        if evento == pygame.K_q and p[3][1]:
            self.mover("NO")
        if evento == pygame.K_a and p[4][1]:
            self.mover("O")
        if evento == pygame.K_z and p[5][1]:
            self.mover("SO")
        if evento == pygame.K_x and p[6][1]:
            self.mover("S")
        if evento == pygame.K_c and p[7][1]:
            self.mover("SE")

        # descripcion
        if evento == pygame.K_i:
            print(self.percibir())
        
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
            x,y = self.coord
            raiz = Nodo(5, "Nodo raiz", (0,0,200), [x, y], None, 0, 0)
            raiz.calc_peso()
            print(f"l {raiz.l}, g {raiz.g}")
            Nodo.origen = raiz
            Nodo.open_list.append(raiz)
            Todo.objetos[raiz.coord[1]//obj_size][raiz.coord[0]//obj_size] = raiz
            self.buscarMeta = True

    def Astar(self):
        Nodo.open_list = sorted(Nodo.open_list, key=lambda obj: obj.g)
        datos()
        current = Nodo.open_list.pop(0)

        ngb = current.checkNgb()

        for _, n in ngb:
            if n:
                x,y = n.coord
                # se agregan nodos a los espacios vecinos
                if n.id == 3:
                    current.ngb.append(n)
                elif n.id == 0:
                    nodo = Nodo(4, "nodo", (0,0,100), [x, y], current)
                    current.ngb.append(nodo)
                    Todo.objetos[y//obj_size][x//obj_size] = nodo
                elif n.id == 4 and n.visited == False:
                    current.ngb.append(n)

        for k in current.ngb:

            if k.id == 3:
                current.color = (0,100,0)
                self.crear_path(current)
                return False

            tmp_l, tmp_g = k.calc_pesos(current)

            if (current.l + tmp_l) < k.l:
                k.l = current.l + tmp_l
                k.g = tmp_g + k.l
                k.parent = current
                Nodo.open_list.append(k)


        current.visited = True

        return True


    def crear_path(self, nodo):
        if nodo.parent:
            nodo.parent.color = (0,100,0)
            self.crear_path(nodo.parent)


class Nodo(Materia):
    open_list = []
    nodo_final = None
    contador = 0

    def __init__(self, id, name, color, coord, parent, l=float('inf'), g=float('inf')):
        super().__init__(id, name, color, coord)
        self.parent = parent
        self.ngb = []
        self.visited = False
        self.l = l
        self.g = g
    
    def draw(self, ventana):
        Font=pygame.font.SysFont('timesnewroman',  11)
        # lg=Font.render(str(f"g:{round(self.g, 4)}"), False, (255,255,255), self.color)
        # ll=Font.render(str(f"l:{round(self.l, 4)}"), False, (255,255,255), self.color)
        x = self.coord[0] + 2
        y = self.coord[1]

        size = (self.coord[0], self.coord[1], self.size[0], self.size[1])
        pygame.draw.rect(ventana, self.color, size)
        # ventana.blit(lg, (x, y))
        # ventana.blit(ll, (x, y+18))
        if self.parent:
            px, py = self.parent.coord[0]//obj_size, self.parent.coord[1]//obj_size
            lp=Font.render(str(f"{px},{py}"), False, (255,255,255), self.color)
            ventana.blit(lp, (x, y+15))

    def __repr__(self):
        return f"nodo [{self.coord[0]//obj_size}, {self.coord[1]//obj_size}]"
    
    def checkNgb(self):
        p = checkAround(self.coord)

        if p[0][1]:
            if p[0][1].id == 2:
                p[0] = ["E", None]
        if p[2][1]:
            if p[2][1].id == 2:
                p[2] = ["N", None]
        if p[4][1]:
            if p[4][1].id == 2:
                p[4] = ["O", None]
        if p[6][1]:
            if p[6][1].id == 2:
                p[6] = ["S", None]
        if p[1][1]:
            if not(p[0][1]) and not(p[2][1]) or p[1][1].id == 2:
                p[1] = ["NE", None]
        if p[3][1]:
            if not(p[2][1]) and not(p[4][1]) or p[3][1].id == 2:
                p[3] = ["NO", None]
        if p[5][1]:
            if not(p[4][1]) and not(p[6][1]) or p[5][1].id == 2:
                p[5] = ["SO", None]
        if p[7][1]:
            if not(p[6][1]) and not(p[0][1]) or p[7][1].id == 2:
                p[7] = ["SE", None]

        return p

    def calc_peso(self):
        x, y = self.coord[0]//obj_size, self.coord[1]//obj_size

        if self.parent:
            px, py = self.parent.coord[0]//obj_size, self.parent.coord[1]//obj_size
            self.l = math.sqrt((px-x)**2 + (py-y)**2)
        mx, my = Todo.meta_actual[0]//obj_size, Todo.meta_actual[1]//obj_size
        self.g = math.sqrt((mx-x)**2 + (my-y)**2)

    def calc_pesos(self, origen):
        x, y = self.coord[0]//obj_size, self.coord[1]//obj_size
        nx, ny = origen.coord[0]//obj_size, origen.coord[1]//obj_size
        mx, my = Todo.meta_actual[0]//obj_size, Todo.meta_actual[1]//obj_size
        return math.sqrt((nx-x)**2 + (ny-y)**2), math.sqrt((mx-x)**2 + (my-y)**2)






    
