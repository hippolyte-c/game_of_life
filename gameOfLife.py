import pygame
import time
import threading
from multiprocessing import Process


FOND = (250, 250, 250)
CELL = (100, 100, 100)

RATIO = 10
SIZE_W = 800
SIZE_T = SIZE_W//RATIO


pygame.init()
fen = pygame.display.set_mode((SIZE_W,SIZE_W))
fen.fill(FOND)
pygame.display.flip()


def click(tablo, x, y):
    tablo[x][y] = not tablo[x][y]
    if(tablo[x][y]):
        pygame.draw.rect(fen, CELL, (x*RATIO, y*RATIO, RATIO, RATIO))
    else:
        pygame.draw.rect(fen, FOND, (x*RATIO, y*RATIO, RATIO, RATIO))
    pygame.display.flip()

    return tablo


def play(tablo):
    nvTablo = [[None for x in range(SIZE_T)] for y in range(SIZE_T)]

    for x in range(SIZE_T):
        for y in range(SIZE_T):
            nbv = 0
            if(tablo[x][y]):
                nbv = -1
            for a in range((x-1), (x+2)):
                for b in range(y-1, y+2):
                    if(a >= 0 and b >= 0):
                        try:
                            if(tablo[a][b]):
                                nbv += 1
                        except IndexError as e:
                            pass

            if(nbv in [2, 3] and tablo[x][y]):
                nvTablo[x][y] = True
                pygame.draw.rect(fen, CELL, (x*RATIO, y*RATIO, RATIO, RATIO))
            elif(nbv == 3 and not tablo[x][y]):
                nvTablo[x][y] = True
                pygame.draw.rect(fen, CELL, (x*RATIO, y*RATIO, RATIO, RATIO))
            else:
                nvTablo[x][y] = False
                pygame.draw.rect(fen, FOND, (x*RATIO, y*RATIO, RATIO, RATIO))

    pygame.display.flip()
    return nvTablo



if __name__ == '__main__':

    tablo = [[None for x in range(SIZE_T)] for y in range(SIZE_T)]

    start = time.time()

    running = True
    jeu = False

    while running:
        for event in pygame.event.get():
            if(event.type == pygame.MOUSEBUTTONUP and event.button == 1):   #clic gauche
                x, y = pygame.mouse.get_pos()
                tablo = click(tablo, x//RATIO, y//RATIO)

            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_SPACE):
                    jeu = not jeu

                if(event.key == pygame.K_c):
                    tablo = [[None for x in range(SIZE_T)] for y in range(SIZE_T)]
                    fen.fill(FOND)
                    pygame.display.flip()

            if(event.type == pygame.QUIT):
                pygame.quit()
                exit()

        if(jeu and time.time() - start > 1):
            tablo = play(tablo)
            start = time.time()
