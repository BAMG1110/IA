import pygame, numpy
from objetos import *
from NN import *

# funcionamiento del entorno

if __name__ == "__main__":
    run = True
    ventana = pygame.display.set_mode((map_width, map_height))
    clock = pygame.time.Clock()

    # Red neuronal
    X = []
    y = np.array([0, 0, 0, 0, 0, 0, 0, 0])

    capa_1 = Layer_Dense((len(Todo.objetos)*len(Todo.objetos[0])), 8)
    capa_2 = Layer_Dense(8, 8)

    act_1 = Activation_ReLU()
    act_2 = Activation_Softmax()

    # objetos
    mabby = SerVivo(id=1, name="mabby", color=(255,0,255), coord=[64, 64])
    Todo.objetos[5][5] = Materia(3, "Meta", (0,255,0), [320, 320])
    Todo.meta_actual = [320, 320]
    ventana.fill((0,0,0))

    for i in Todo.objetos:
        for j in i:
            j.calc_costo()
            X.append(round(j.costo))

    a = obtenerCostoAdyacentes(mabby.percibir())
    m = min(i for i in a if i > 0)
    print("Position:", a.index(m))
    print("Value:", m)

    y[a.index(m)] = 1

    # >>>>>>>>>>>>>>>
    # secuencia
    capa_1.forward(X)
    act_1.forward(capa_1.output)
    capa_2.forward(act_1.output)
    act_2.forward(capa_2.output)

    print("X\n", X)
    print("y\n", y)
    print("capa_1\n", capa_1.output)
    print("act_1\n", act_1.output)
    print("capa_2\n", capa_2.output)
    print("act_2\n", act_2.output)

    # Obtener SSR x resultado
    # Obtener b, wn x 


    # >>>>>>>>>>>>>>>

    while run:
        # time delay _& fps
        pygame.time.delay(300)
        clock.tick(200)

        # eventos
        for e in pygame.event.get():
            # cerrar ventana
            if e.type == pygame.QUIT:
                run = False

            # escuchar teclado
            elif e.type == pygame.KEYDOWN:
                try:
                    key = getattr(e, 'key')
                    if key == pygame.K_m:
                        Todo.verMatrizObjetos()
                    elif key == pygame.K_n:
                        Todo.verObjeto()
                    elif key == pygame.K_b:
                        datos()
                    
                    # guardar y borrar mapa
                    elif key == pygame.K_v:
                        guardarMapa()
                        borrarMapa()

                    # cargar mapas 1-3
                    elif key == pygame.K_1:
                        borrarMapa()
                        cargarMapa('data_1.pickle')
                    elif key == pygame.K_2:
                        borrarMapa()
                        cargarMapa('data_2.pickle')
                    elif key == pygame.K_3:
                        borrarMapa()
                        cargarMapa('data_3.pickle')
                    elif key == pygame.K_4:
                        borrarMapa()
                        cargarMapa('data_4.pickle')
                    elif key == pygame.K_5:
                        borrarMapa()
                        cargarMapa('data_5.pickle')
                    elif key == pygame.K_6:
                        borrarMapa()
                        cargarMapa('data_6.pickle')
                    elif key == pygame.K_0:
                        borrarMapa()
                        cargarMapa('data_n.pickle')

                    # definir meta
                    elif key == pygame.K_p:
                        Todo.defMeta()
                    else:
                        mabby.accion(key)
                except:
                    pass
            
            # escuchar mouse
            Todo.mouse()


        # update
        Todo.draw(ventana)
        
        mabby.draw(ventana)
        
        # A*
        if mabby.buscarMeta:
            mabby.buscarMeta = mabby.Astar()
        
        if mabby.mostrarMapa:
            mabby.verMapa(ventana)

        Todo.drawGrid(ventana)
        
        pygame.display.update()
    
    pygame.quit()

