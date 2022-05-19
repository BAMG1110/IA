import pygame
from objetos import *

def mouse():
    x,y = pygame.mouse.get_pos()
    pos = [x//32, y//32]

    if pygame.mouse.get_pressed()[0] == True:
        return pos
    else:
        return False


def crearObjeto(pos):
    return Materia(2, "Algun tipo de piedra", pos)

if __name__ == "__main__":
    run = True
    todo = pygame.display.set_mode((map_width, map_height))
    clock = pygame.time.Clock()

    # objetos
    mabby = SerVivo(1, "mabby")
    objetos = []

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
            
            # escuchar mouse
            mouse_pos = mouse()
            if mouse_pos:
                print(len(objetos), "\n")
                objetos.append(crearObjeto(mouse_pos))

                  

        # update
        # mabby.movRandom()
        

        todo.fill((0,0,0))
        # mabby.draw(todo, (255,0,255))
        
        pygame.display.update()
    
    pygame.quit()

