import pygame
from random import randint
from math import sqrt

tam_telaX = 660
tam_telaY = 750
white = (255,255,255)

tela = pygame.display.set_mode((tam_telaX, tam_telaY))
clock = pygame.time.Clock()
run = True

class Bola:
    def __init__(self, x, y, vx, vy, raio, m):

        if x + raio > tam_telaX or y + raio > tam_telaY:
            self.x = x - raio
            self.y = y - raio
        elif x - raio < 0 or y - raio < 0:
            self.x = x + raio
            self.y = y + raio
        else:
            self.x = x
            self.y = y

        self.vx = vx
        self.vy = vy
        self.raio = raio
        self.cor = (randint(115,150), randint(115,150),randint(115,150))
        self.m = m
    def moveBola(self):
        self.x += self.vx
        self.y += self.vy
    def colisoesParede(self):
        if self.x + self.raio >= tam_telaX or self.x - self.raio <= 0:
            self.vx = - self.vx
            self.x += self.vx
        if self.y + self.raio >= tam_telaY or self.y - self.raio <= 0:
            self.vy = - self.vy
            self.y += self.vy
    def checaColisao(bola1, bola2):
        distancia = sqrt((bola1.x - bola2.x)**2 + (bola1.y - bola2.y)**2)
        if (bola1.raio + bola2.raio >= distancia):
            aux = bola1.vx
            bola1.vx = (bola1.m - bola2.m)/ (bola1.m + bola2.m) * bola1.vx + 2*bola2.m/ (bola1.m + bola2.m) * bola2.vx 
            bola2.vx = (bola2.m - bola1.m) * bola2.vx/ (bola1.m + bola2.m) + 2*bola1.m * aux/ (bola1.m + bola2.m)
            aux = bola1.vy
            bola1.vy = (bola1.m - bola2.m) * bola1.vy/ (bola1.m + bola2.m) + 2*bola2.m * bola2.vy/ (bola1.m + bola2.m)
            bola2.vy = (bola2.m - bola1.m) * bola2.vy/ (bola1.m + bola2.m) + 2*bola1.m * aux/ (bola1.m + bola2.m)

    def descolaBolas (bola1, bola2):
        distancia = sqrt((bola1.x - bola2.x)**2 + (bola1.y - bola2.y)**2)

        if distancia <= (bola1.raio + bola2.raio):
            dx = bola1.x - bola2.x
            dy = bola1.y - bola2.y

            erro = (bola1.raio + bola2.raio) - distancia

            erro_x = (dx*erro)/distancia
            erro_y = (dy*erro)/distancia

            bola1.x += erro_x/2
            bola1.y += erro_y/2

            bola2.x -= erro_x/2
            bola1.y -= erro_y/2
    def descolaParede(bola):

        if bola.x - bola.raio < 0:
            erro = bola.raio-bola.x
            bola.x += erro

        elif bola.x + bola.raio > tam_telaX:
            erro = bola.raio-(tam_telaX- bola.x)
            bola.x -= erro

        if bola.y - bola.raio < 0:
            erro = bola.raio-bola.y
            bola.y += erro

        elif bola.y + bola.raio > tam_telaY:
            erro = bola.raio-(tam_telaY-bola.y)
            bola.y -= erro

n_bolas = int(input("n_bolas"))

bolas = []

for i in range(n_bolas):
    bolas.append(Bola(randint(0, tam_telaX), 
                      randint(0, tam_telaY), 
                      randint(-5, 5), 
                      randint(-5, 5), 
                      randint(18, 35),
                      randint(2,15)))

while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    tela.fill(white)

    for i in range(n_bolas):
        pygame.draw.circle(tela, bolas[i].cor, (bolas[i].x, bolas[i].y), bolas[i].raio)
    
        Bola.colisoesParede(bolas[i])
        Bola.descolaParede(bolas[i])

        for j in range(i):
            if j != i:
                Bola.checaColisao(bolas[i], bolas[j])
                Bola.descolaBolas(bolas[i], bolas[j])

        Bola.moveBola(bolas[i])
        
    pygame.display.update()
pygame.quit()

''' A = np.sqrt(x_initial**2 + (v0 / omega)**2)  # Amplitude calculada a partir da posição inicial e velocidade inicial
phi = np.arcsin(-v0/A*omega)# Fase inicial baseada em x_initial e v0
#np.arctan2(-v0 / (A * omega), x_initial / A)'''