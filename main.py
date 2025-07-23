import pygame
import pygame as pg

print('Setup Start')
pg.init()
window = pg.display.set_mode(size=(600, 480))
print('Setup End')

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            print('Quitting...')
            pg.quit()
            quit()
