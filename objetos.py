import pygame
import random

map_width = 512
map_height = 512
obj_size = 32

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
    if x == (map_width) - obj_size:
        b[0] = False
    if y == 0:
        b[1] = False
    if x == 0:
        b[2] = False
    if y == (map_height) - obj_size:
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
    def verTodo(cls):
        print("Todo")
        for obj in cls.objetos:
            try:
                print(obj)
            except:
                pass

    @classmethod
    def eliminarObjeto(cls, pos):
        # cls.objetos[obj.coord[0]][obj.coord[1]]
        # print(f"pos: {pos}")
        x, y = pos[1]//obj_size, pos[0]//obj_size
        cls.objetos[x][y] = 0

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

        return Materia(3, "Meta", (0, 255, 0), cls.meta_actual)
        

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
    
    def __repr__(self):
        return f"{self.id}"

    # surface, color, (posicion & dimension)
    def draw(self, ventana):
        size = (self.coord[0], self.coord[1], self.size[0], self.size[1])
        pygame.draw.rect(ventana, self.color, size)

    @property
    def descripcion(self):
        print('id:         \t', self.id)
        print('coordenadas:\t', self.coord[0] // obj_size, self.coord[1] // obj_size)
        print('nombre:     \t', self.name)

    def generarFeromonas(self, coord, inten):
        p = [[0, obj_size], [-obj_size, 0], [0, -obj_size], [obj_size, 0]]
        b = checkBorders(coord)
        color = tuple([100-inten, 0, 120-inten])
        
        for i in p:
            zipped_lists = zip(i, coord)
            sum = [a + b for (a, b) in zipped_lists]
            ñ = [sum[1]//obj_size, sum[0]//obj_size]

            if (sum[0] >= 0 and sum[0] <= map_width-obj_size) and (sum[1] >= 0 and sum[1] <= map_width-obj_size):
                # print(ñ, Todo.objetos[sum[1]//obj_size][sum[0]//obj_size])

                if not(Todo.objetos[sum[1]//obj_size][sum[0]//obj_size] != 0):
                    if inten < 10:
                        temp = feromona(4, name = "feromona", color = color, coord = sum, origen = coord, intensidad = inten)
                        Todo.agregarObjeto(temp)
                        self.generarFeromonas(sum, inten+1)
                else:
                    # si hay otro objeto
                    pass
            else:
                pass

class SerVivo(Materia):
    def __init__(self, id, name, color, coord, mapa = generarMatriz(0)):
        super().__init__(id, name, color, coord)
        self.mapa = mapa
        self.moving = False
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

    def movRandom(self):
        if self.moving:
            # lista = [pygame.K_d, pygame.K_e, pygame.K_w, pygame.K_q, pygame.K_a, pygame.K_z, pygame.K_x, pygame.K_c]
            lista = [pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_x]
            d = random.sample(lista, k=1)[-1]
            self.accion(d)

    def percibir(self):
        coord_x = self.coord[0]
        coord_y = self.coord[1]
        try:
            obj_0 = Todo.objetos[coord_y//obj_size][(coord_x+obj_size)//obj_size]
        except:
            obj_0 = None
        try:
            obj_1 = Todo.objetos[(coord_y-obj_size)//obj_size][(coord_x+obj_size)//obj_size]
        except:
            obj_1 = None
        try:
            obj_2 = Todo.objetos[(coord_y-obj_size)//obj_size][(coord_x)//obj_size]
        except:
            obj_2 = None
        try:
            obj_3 = Todo.objetos[(coord_y-obj_size)//obj_size][(coord_x-obj_size)//obj_size]
        except:
            obj_3 = None
        try:
            obj_4 = Todo.objetos[coord_y//obj_size][(coord_x-obj_size)//obj_size]
        except:
            obj_4 = None
        try:
            obj_5 = Todo.objetos[(coord_y+obj_size)//obj_size][(coord_x-obj_size)//obj_size]
        except:
            obj_5 = None
        try:
            obj_6 = Todo.objetos[(coord_y+obj_size)//obj_size][(coord_x)//obj_size]
        except:
            obj_6 = None
        try:
            obj_7 = Todo.objetos[(coord_y+obj_size)//obj_size][(coord_x+obj_size)//obj_size]
        except:
            obj_7 = None

        percepcion = [obj_0, obj_1, obj_2, obj_3, obj_4, obj_5, obj_6, obj_7]

        return percepcion, coord_x, coord_y

    def accion(self, evento):
        Todo.eliminarObjeto(self.coord)
        b = checkBorders(self.coord)
        p, x, y = self.percibir()
        # print(f"bordes:     {b}")
        # print(f"percepcion: {p}")

        # Este & Noreste
        if evento == pygame.K_d and b[0]:
            # print(f"0 - obj_E: {p[0]}")
            if p[0] == 0:
                self.coord[0] += self.vel
                self.mapa[y//obj_size][x//obj_size] += 1
            elif p[0].id == 3:
                self.coord[0] += self.vel
                self.moving = False

        if evento == pygame.K_e and b[0] and b[1]:
            # print(f"1 - obj_NE: {p[1]}")
            if p[1] == 0:
                self.coord[0] += self.vel
                self.coord[1] -= self.vel
                self.mapa[y//obj_size][x//obj_size] += 1
            elif p[1].id == 3:
                self.coord[0] += self.vel
                self.coord[1] -= self.vel
                self.moving = False
        
        # Norte & Noroeste
        if evento == pygame.K_w and b[1]:
            # print(f"2 - obj_N: {p[2]}")
            if p[2] == 0:
                self.coord[1] -= self.vel
                self.mapa[y//obj_size][x//obj_size] += 1
            elif p[2].id == 3:
                self.coord[1] -= self.vel
                self.moving = False

        if evento == pygame.K_q and b[1] and b[2]:
            # print(f"3 - obj_NO: {p[3]}")
            if p[3] == 0:
                self.coord[0] -= self.vel
                self.coord[1] -= self.vel
                self.mapa[y//obj_size][x//obj_size] += 1
            elif p[3].id == 3:
                self.coord[0] -= self.vel
                self.coord[1] -= self.vel
                self.moving = False

        # Oeste & Suroeste
        if evento == pygame.K_a and b[2]:
            # print(f"4 - obj_O: {p[4]}")
            if p[4] == 0:
                self.coord[0] -= self.vel
                self.mapa[y//obj_size][x//obj_size] += 1
            elif p[4].id == 3:
                self.coord[0] -= self.vel
                self.moving = False
        
        if evento == pygame.K_z and b[2] and b[3]:
            # print(f"5 - obj_SO: {p[5]}")
            if p[5] == 0:
                self.coord[0] -= self.vel
                self.coord[1] += self.vel
                self.mapa[y//obj_size][x//obj_size] += 1
            elif p[5].id == 3:
                self.coord[0] -= self.vel
                self.moving = False
        
        # Sur & Sureste
        if evento == pygame.K_x and b[3]:
            # print(f"6 - obj_S: {p[6]}")
            if p[6] == 0:
                self.coord[1] += self.vel
                self.mapa[y//obj_size][x//obj_size] += 1
            elif p[6].id == 3:
                self.coord[0] -= self.vel
                self.moving = False
        
        if evento == pygame.K_c and b[3] and b[0]:
            # print(f"7 - obj_SO: {p[7]}")
            if p[7] == 0:
                self.coord[0] += self.vel
                self.coord[1] += self.vel
                self.mapa[y//obj_size][x//obj_size] += 1
            elif p[7].id == 3:
                self.coord[0] -= self.vel
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

class feromona(Materia):
    def __init__(self, id, name, color, coord, origen, intensidad = 0):
        super().__init__(id, name, color, coord)
        self.origen = origen
        self.intensidad = intensidad