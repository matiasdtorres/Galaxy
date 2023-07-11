import pygame
import sqlite3
from colores import *

def mostrar_barra_vida(pantalla, x, y, jugador):
    largo = 200
    ancho = 26
    calculo_barra = int((jugador.hp / 100) * largo)
    borde = pygame.Rect(x, y, largo, ancho)
    vida = pygame.Rect(x, y, calculo_barra, ancho)
    pygame.draw.rect(pantalla, WHITE, borde, 2)
    pygame.draw.rect(pantalla, GREEN, vida)
    warning = pygame.image.load('./documents/assets/img/warning.png').convert()
    warning.set_colorkey(BLACK)
    if jugador.hp < 30:
        pantalla.blit(pygame.transform.scale(warning,(26,26)), (1020,15))

def mostrar_vidas(pantalla,x,vidas,jugador):
    pantalla.blit(pygame.transform.scale(jugador.image,(30,30)), (1220,40))
    pantalla.blit(pygame.transform.scale(jugador.image,(30,30)), (1140,40))
    pantalla.blit(pygame.transform.scale(jugador.image,(30,30)), (1060,40))
    cruz = pygame.image.load('./documents/assets/img/cruz.png').convert()
    cruz.set_colorkey(BLACK)
    if jugador.vidas == 2:
        pantalla.blit(pygame.transform.scale(cruz,(25,25)), (1223,40))
    if jugador.vidas == 1:
        pantalla.blit(pygame.transform.scale(cruz,(25,25)), (1223,40))
        pantalla.blit(pygame.transform.scale(cruz,(25,25)), (1143,40))
    if jugador.vidas == 0:
        pantalla.blit(pygame.transform.scale(cruz,(25,25)), (1223,40))
        pantalla.blit(pygame.transform.scale(cruz,(25,25)), (1143,40))
        pantalla.blit(pygame.transform.scale(cruz,(25,25)), (1063,40))


def mostrar_puntos(pantalla,fuente,texto,color, dimensiones, x, y):
	tipo_letra = pygame.font.Font(fuente,dimensiones)
	superficie = tipo_letra.render(texto,True, color)
	rectangulo = superficie.get_rect()
	rectangulo.center = (x, y)
	pantalla.blit(superficie,rectangulo)
        
def leer_db():
    conexion = sqlite3.connect('./documents/database/db.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM puntuacion ORDER BY score DESC LIMIT 7")
    jugadores = cursor.fetchall()
    
    lista_jugadores = []
    posicion = 1
    for jugador in jugadores:
        dict = {
            'posicion': posicion,
            'nick': jugador[1],
            'score': jugador[2]
        }
        lista_jugadores.append(dict)
        posicion += 1
    conexion.close()
    return lista_jugadores

def mostrar_leaderboard(pantalla):
    fuente = "./documents/assets/fuente.ttf"
    color = WHITE  # Color blanco
    dimensiones = 28  # Tamaño de la fuente
    x = pantalla.get_width() // 2  # Posicion x centrada en la pantalla
    y = 140 # Posicion y centrada en la pantalla

    puntuaciones = leer_db()

    for puntuacion in puntuaciones:
        texto = f"{puntuacion['posicion']}  -   {puntuacion['nick']}  -  Puntuacion: {puntuacion['score']}"
        mostrar_puntos(pantalla, fuente, texto, color, dimensiones, x, y)
        y += 70  # Ajusta este valor para espaciar las puntuaciones en pantalla