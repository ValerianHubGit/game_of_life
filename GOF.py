import time
import pygame
import numpy as np

#Set Variables
width = 1000
height = 1000
FPS = 30
size = 10
alive_color = (210, 210, 210)
unalive_color= (25, 25, 25)

def draw(screen, cells):
    screen.fill(unalive_color)
    for row, col in np.ndindex(cells.shape):
        if cells[row,col]:
            pygame.draw.rect(screen, alive_color, (row*size, col*size, size-1, size-1))

def update(cells):
    updated_cells=np.zeros((cells.shape[0], cells.shape[1]))
    for row, col in np.ndindex(cells.shape):
        no_neighbours=np.sum(cells[row-1:row+2,col-1:col+2])-cells[row, col]
        #Remains alive?
        if cells[(row,col)] and no_neighbours in [2,3]:
            updated_cells[(row, col)] = 1
        #Rises from unalive?
        elif (not cells[(row,col)]) and no_neighbours == 3:
            updated_cells[(row,col)] = 1
    return updated_cells

def init_grid(rows, cols, random=True):
    if random:
        return np.random.choice([0,1], size=(rows, cols), p=[0.8, 0.2])
    return  np.zeros((rows, cols)) 

#kreiere Pygame-Screen mit Grid und Klickbaren Feldern zum Alive/Unalive - Triggern
def main():
    #alive cells get a 1, unalive cells get 0, initialize (randomly?)
    cells=init_grid(width//size, height//size, True)

    pygame.init()
    screen=pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game of Life")

    clock=pygame.time.Clock()

    running=False
    #öffne Fenster
    while True:
        #Core Mechanic
        clock.tick(FPS)
        if running:
            cells=update(cells)
        draw(screen, cells)        
        pygame.display.update()
        
        #Inputs
        for event in pygame.event.get():
            #Schließen
            if event.type==pygame.QUIT:
                pygame.quit()
                return
            #Pausieren
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    running= not running
            #Manual Draw on click-event
            if event.type==pygame.MOUSEBUTTONDOWN:
                loc = pygame.mouse.get_pos()
                prior_value=cells[loc[0]//size, loc[1]//size]
                new_value=1 if prior_value==0 else 0
                cells[(loc[0]//size, loc[1]//size)]=new_value
                pygame.display.update()                

#apparently notwendig um nicht bei Import pygame ständig auszuführen
if __name__=="__main__":
    main()