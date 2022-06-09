import pygame
from objetos import *

# funcionamiento del entorno

if __name__ == "__main__":
    run = True
    ventana = pygame.display.set_mode((map_width, map_height))
    clock = pygame.time.Clock()

    # objetos
    mabby = SerVivo(id=1, name="mabby", color=(255,0,255), coord=[160, 160])
    print(obj_size)

    ventana.fill((0,0,0))

    while run:
        # time delay _& fps
        # pygame.time.delay(2)
        # clock.tick(Todo.clock_tick)

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
                        Todo.verObjetos()
                    elif key == pygame.K_o:
                        mabby.defOrigen()
                    elif key == pygame.K_p:
                        meta = Todo.defMeta()
                        meta.generarRastro(10)
                    else:
                        mabby.accion(key)
                except:
                    pass
            
            # escuchar mouse
            Todo.mouse()
                
                    

        # update
        ventana.fill((0,0,0))

        Todo.draw(ventana)
        mabby.draw(ventana)
        if mabby.mostrarMapa:
            mabby.verMapa(ventana)

        # if mabby.seguir_camino:
        #     mabby.seguir_camino()
        
        if mabby.moving:
            mabby.movRandom()

        Todo.drawGrid(ventana)
        
        pygame.display.update()
    
    pygame.quit()

