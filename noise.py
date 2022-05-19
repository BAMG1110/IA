import pygame
from objetos import *
# funcionamiento del entorno
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
    mabby = SerVivo(id=1, name="mabby", color=(255,0,255))

    todo.fill((0,0,0))

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
                obj = Materia(2, "algun tipo de piedra", mouse_pos)
                Todo.agregarObjeto(obj)
                Todo.info()

                  

        # update
        mabby.movRandom()
        

        todo.fill((0,0,0))
        mabby.draw(todo)
        
        pygame.display.update()
    
    pygame.quit()

