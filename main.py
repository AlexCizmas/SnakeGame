import pygame
import time
from pygame.locals import *
import random

marime = 40
Culoare_fundal = (110, 110, 5)

#Crearea clasei obiectului mar, desenarea si miscarea acestuia
class Mar:
    def __init__(self, ecran_parinte):
        self.ecran_parinte = ecran_parinte
        self.image = pygame.image.load("resurse/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def desenare(self):
        self.ecran_parinte.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def misca(self):
        self.x = random.randint(0,24) * marime
        self.y = random.randint(0, 19) * marime

#Crearea clasei sarpe, miscarea acestuia si marirea lungimii
class Sarpe():
    def __init__(self, ecran_parinte):
        self.ecran_parinte = ecran_parinte
        self.image = pygame.image.load("resurse/bloc.jpg").convert()
        self.directie = 'jos'

        self.lungime = 1
        self.x = [40]
        self.y =[40]

    def misca_stanga(self):
        self.directie = 'stanga'

    def misca_dreapta(self):
        self.directie = 'dreapta'

    def misca_sus(self):
        self.directie = 'sus'

    def misca_jos(self):
        self.directie = 'jos'

    def misca(self):
        for i in range(self.lungime - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]


        if self.directie == 'sus':
            self.y[0] -= marime
        if self.directie == 'jos':
            self.y[0] += marime
        if self.directie == 'stanga':
            self.x[0] -= marime
        if self.directie == 'dreapta':
            self.x[0] += marime

        self.desenare()

    def desenare(self):
        for i in range(self.lungime):
            self.ecran_parinte.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def marire_lungime(self):
        self.lungime += 1
        self.x.append(-1)
        self.y.append(-1)

class Joc:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game!")

        pygame.mixer.init()
        self.muzica_fundal()

        self.suprafata = pygame.display.set_mode((1000, 800))
        self.sarpe = Sarpe(self.suprafata)
        self.sarpe.desenare()
        self.mar = Mar(self.suprafata)
        self.mar.desenare()

    def muzica_fundal(self):
        pygame.mixer.music.load('resurse/muzica_fundal.mp3')
        pygame.mixer.music.play(-1, 0)

    def sunet(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resurse/lovire.mp3")
        elif sound_name =='ding':
            sound = pygame.mixer.Sound("resurse/ring.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.sarpe = Sarpe(self.suprafata)
        self.mar = Mar(self.suprafata)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + marime:
            if y1 >= y2 and y1 < y2 + marime:
                return True
        return False

    def incarcare_background(self):
        bg = pygame.image.load('resurse/background.png')
        self.suprafata.blit(bg, (0,0))

    def start(self):
        self.incarcare_background()
        self.sarpe.misca()
        self.mar.desenare()
        self.scor()
        pygame.display.flip()


        for i in range(self.sarpe.lungime):
            if self.is_collision(self.sarpe.x[i], self.sarpe.y[i], self.mar.x, self.mar.y):
                self.sunet('ding')
                self.sarpe.marire_lungime()
                self.mar.misca()

        for i in range(3, self.sarpe.lungime):
            if self.is_collision(self.sarpe.x[0], self.sarpe.y[0], self.sarpe.x[i], self.sarpe.y[i]):
                self.sunet('crash')
                raise"Collision occured"

        if not (0 <= self.sarpe.x[0] <= 1000 and 0 <= self.sarpe.y[0] <= 800):
            self.sunet("crash")
            raise "hit the boundry error"

    #Crearea unei functii care mentine scorul
    def scor(self):
        font = pygame.font.SysFont('arial', 30)
        scor = font.render(f"Score: {self.sarpe.lungime}", True, (255, 255, 255))
        self.suprafata.blit(scor, (450, 10))

    def ai_pierdut(self):
        self.incarcare_background()
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render(f"Ai pierdut, scorul final este {self.sarpe.lungime}", True, (255, 255, 255))
        self.suprafata.blit(line1, (200, 300))
        line2 = font.render("Pentru a juca din nou, apasati tasta Enter.", True, (255, 255, 255))
        line3 = font.render("Pentru a iesi, apasati escape!", True, (255, 255, 255))
        self.suprafata.blit(line2, (200, 350))
        self.suprafata.blit(line3, (200, 400))
        pygame.mixer.music.pause()
        pygame.display.flip()


    def Pornire(self):
        functionare = True
        pauza = False
        while functionare:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        functionare = False
                    if event.key == K_RETURN:
                        pauza = False
                    if not pauza:
                        if event.key == K_UP:
                            self.sarpe.misca_sus()

                        if event.key == K_DOWN:
                            self.sarpe.misca_jos()

                        if event.key == K_LEFT:
                            self.sarpe.misca_stanga()

                        if event.key == K_RIGHT:
                            self.sarpe.misca_dreapta()

                elif event.type == QUIT:
                    functionare = False
            try:
                if not pauza:
                    self.start()
            except Exception as e:
                self.ai_pierdut()
                pauza = True
                self.reset()
            time.sleep(.1)


if __name__== '__main__':
    joc = Joc()
    joc.Pornire()

