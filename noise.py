import pygame
from objetos import *
# funcionamiento del entorno

if __name__ == "__main__":
    run = True
    ventana = pygame.display.set_mode((map_width, map_height))
    clock = pygame.time.Clock()

    # objetos
    mabby = SerVivo(id=1, name="mabby", color=(255,0,255))

    ventana.fill((0,0,0))

    while run:
        # time delay _& fps
        pygame.time.delay(60)
        clock.tick(10)

        # eventos
        for e in pygame.event.get():
            # cerrar ventana
            if e.type == pygame.QUIT:
                run = False

            # escuchar teclado
            elif e.type == pygame.KEYDOWN:
                try:
                    key = getattr(e, 'key')
                    if pygame.K_o == key:
                        Todo.verObjetos()
                    else:
                        mabby.accion(key)
                except:
                    pass
            
            # escuchar mouse
            mouse_pos = Todo.mouse()
            if mouse_pos:
                obj = Materia(2, "algun tipo de piedra", (255, 0, 0), mouse_pos)
                Todo.agregarObjeto(obj)

        # update
        ventana.fill((0,0,0))

        mabby.movRandom()
        mabby.draw(ventana)
        Todo.draw(ventana)
        
        pygame.display.update()
    
    pygame.quit()

