import pygame
from objetos import *

# funcionamiento del entorno

if __name__ == "__main__":
    run = True
    ventana = pygame.display.set_mode((map_width, map_height))
    clock = pygame.time.Clock()

    # objetos
    mabby = SerVivo(id=1, name="mabby", color=(255,0,255), coord=[0, 0])
    Todo.objetos[19][19] = Materia(3, "Meta", (0,255,0), [608, 608])
    Todo.meta_actual = [608, 608]
    ventana.fill((0,0,0))
    
    while run:
        # time delay _& fps
        # pygame.time.delay(30)
        clock.tick(60)

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

