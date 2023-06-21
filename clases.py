import pygame
import random
from colores import *

pygame.mixer.init()

nave = pygame.image.load("./assets/ferpa01.png")
sonidomisil = pygame.mixer.Sound('./assets/sounds/misil.mp3')

#Tamaño de pantalla
ALTO = 720
ANCHO = 1280

# Creacion de grupos
jugador_sprites = pygame.sprite.Group()
enemigos_facilitos = pygame.sprite.Group()
enemigos_normalitos = pygame.sprite.Group()
misiles = pygame.sprite.Group()
meteorito = pygame.sprite.Group()
misiles_enemigos = pygame.sprite.Group()


class Jugador(pygame.sprite.Sprite):
    # Sprite del jugador
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # Rectangulo (Jugador)
        self.image = nave
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(BLACK)
        # Obtiene el rectangulo (sprite)
        self.rect = self.image.get_rect()
        
        self.radious = 25.5

        # Centro el rectangulo (sprite)
        self.rect.center = (ANCHO / 2, ALTO // 1.2)
        # Velocidad del personaje (inicial)
        self.vel_x = 0

        #Disparo
        self.tiempo = 140
        self.ultimo_disparo = pygame.time.get_ticks()
        #HP
        self.hp = 100
        #Vidas
        self.vidas = 3

    def update(self):
        # Velocidad predeterminada vuelta del bucle si no pulsas nada
        self.vel_x = 0

        # Devuelve una lista, con las teclas pulsadas
        teclas = pygame.key.get_pressed()
        # Si pulsas izquierda
        if teclas[pygame.K_LEFT]:
            self.vel_x = -9.5
        # Si pulsas derecha
        if teclas[pygame.K_RIGHT]:
            self.vel_x = 9.5
        # Si pulsas espacio
        if teclas[pygame.K_SPACE]:
            ahora = pygame.time.get_ticks()
            if ahora - self.ultimo_disparo > self.tiempo:
                self.disparo()
                self.ultimo_disparo = ahora

        # Actualiza la velocidad
        self.rect.x += self.vel_x

        # Si el jugador se sale de la pantalla
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.left < 0:
            self.rect.left = 0
    
    def disparo(self):
        misil = Disparos(self.rect.centerx, self.rect.top, True)
        misiles.add(misil)
        jugador_sprites.add(misil)
        sonidomisil.play()


class Malo(pygame.sprite.Sprite):
    # Sprite del jugador
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # Rectangulo (Jugador)
        self.image = pygame.image.load("./assets/img/enemigos/normalito.png").convert()
        self.image = pygame.transform.scale(self.image, (59, 59))
        self.image.set_colorkey(BLACK)
        # Obtiene el rectangulo (sprite)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = -self.rect.width
        self.velo_y = random.randrange(2, 5)

        # Disparo
        self.tiempo_entre_disparos = random.randrange(1000, 2500)  # Intervalo de 300 milisegundos entre disparos
        self.ultimo_disparo = pygame.time.get_ticks()  # Momento del último disparo


    def update(self):
        self.rect.y += self.velo_y
        if self.rect.top > ALTO:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = -self.rect.width
            # ANCHO
            self.velo_y = random.randrange(2, 5)

        # Verificar si ha pasado suficiente tiempo para disparar automáticamente
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.tiempo_entre_disparos:
            self.disparo()
            self.ultimo_disparo = ahora

    def disparo(self):
        misilMalo = Disparos_Enemigos(self.rect.centerx, self.rect.top)
        misiles_enemigos.add(misilMalo)
        #sonidomisil.play()
    

class Malo2(pygame.sprite.Sprite):
    # Sprite del jugador
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # Rectangulo (Jugador)
        self.image = pygame.image.load("./assets/img/enemigos/facilito.png").convert()
        self.image = pygame.transform.scale(self.image, (45, 45))
        self.image.set_colorkey(BLACK)
        # Obtiene el rectangulo (sprite)
        self.rect = self.image.get_rect()
        
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = -self.rect.width
        self.velo_y = random.randrange(2, 5)

    def update(self):
        
        self.rect.y += self.velo_y
        if self.rect.top > ALTO:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = -self.rect.width
            # ANCHO
            self.velo_y = random.randrange(2, 5)



class Disparos(pygame.sprite.Sprite):
    def __init__(self, x, y, jugador):
        super().__init__()
        self.image = pygame.image.load("./assets/img/misil.png").convert()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.jugador = jugador #Booleano que determina si es jugador o enemigo
        self.rect.centerx = x
        if self.jugador:
            self.rect.bottom = y
        else:
            self.rect.bottom = y + 40
    
    def update(self):
        if self.jugador:
            self.rect.y -= 5
        else:
            self.rect.y += 5
        if self.rect.bottom < 0:
            self.kill()

class Disparos_Enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./assets/img/misil_enemigo.png").convert()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 40
        self.rect.centerx = x
    
    def update(self):
        self.rect.y += 5
        if self.rect.bottom < 0:
            self.kill()

class Meteoritos(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_random = random.randrange(3)
        if self.image_random == 0:
            self.image = pygame.transform.scale(pygame.image.load("./assets/img/enemigos/meteorito.jpg").convert(),(80,80))
            self.radius = 40
        if self.image_random == 1:
            self.image = pygame.transform.scale(pygame.image.load("./assets/img/enemigos/meteorito.jpg").convert(),(50,50))
            self.radius = 25
        if self.image_random == 2:
            self.image = pygame.transform.scale(pygame.image.load("./assets/img/enemigos/meteorito.jpg").convert(),(20,20))
            self.radius = 10
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = -self.rect.width
        self.velo_y = random.randrange(3, 7)

    def update(self):
        self.rect.y += self.velo_y
        if self.rect.top > ALTO:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = -self.rect.width
            # ANCHO
            self.velo_y = random.randrange(3, 7)