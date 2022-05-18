import pygame
from objetos import *

if __name__ == "__main__":
    run = True
    todo = pygame.display.set_mode((map_width, map_height))
    clock = pygame.time.Clock()

    # objetos
    mabby = SerVivo(1, "mabby")

    todo.fill((0,0,0))
    # mapa.draw(todo)

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
                    mabby.accion(key)
                except:
                    pass
                  

        # update
        mabby.checkBoundaries()
        mabby.movRandom()
        todo.fill((0,0,0))
        mabby.draw(todo, (255,255,255))
        pygame.display.update()
    
    pygame.quit()

