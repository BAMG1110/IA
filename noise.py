import pygame
from objetos import *

# funcionamiento del entorno

if __name__ == "__main__":
    run = True
    ventana = pygame.display.set_mode((map_width, map_height))
    clock = pygame.time.Clock()

    # objetos
    mabby = SerVivo(id=1, name="mabby", color=(255,0,255), coord=[0, 0])
    raiz = Nodo(5, "Nodo Raiz", (0,0,200), mabby.coord, None)
    Nodo.open.append(raiz)

    ventana.fill((0,0,0))

    while run:
        # time delay _& fps
        pygame.time.delay(30)
        clock.tick(30)

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
                    elif key == pygame.K_p:
                        Todo.defMeta()
                    else:
                        mabby.accion(key)
                except:
                    pass
            
            # escuchar mouse
            Todo.mouse()
                
        # A*
        if len(Nodo.open) > 0:
            Nodo.aStar()

        # update
        ventana.fill((0,0,0))

        Todo.draw(ventana)
        
        mabby.draw(ventana)
        
        if mabby.mostrarMapa:
            mabby.verMapa(ventana)

        Todo.drawGrid(ventana)
        
        pygame.display.update()
    
    pygame.quit()

