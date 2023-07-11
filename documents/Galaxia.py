import pygame, pygame_gui, sys, sqlite3
from boton import Boton
from clases import *
from base import *
from funciones import *
#importe moviepy (pip install moviepy)
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import rotate

#Para crear el .exe instale -> pip install pyinstaller
#Despues Escribi lo siguiente en la terminal: pyinstaller --onefile --noconsole ./documents/Galaxia.py
#Despues movi de la carpeta "dist" el Galaxia.exe a la seccion "main"


pygame.init()

#FPS
FPS = 240
 
 #Cambio el icono de la ventana
icono = pygame.image.load("./documents/assets/img/icono.png")
pygame.display.set_icon(icono)


leaderboard = pygame.image.load("./documents/assets/img/menu/leaderboard.png")


#Se carga el video
video = VideoFileClip("./documents/assets/video/menu/menu_principal.mp4")
video_gameover = VideoFileClip("./documents/assets/video/menu/menu_gameover.mp4")

# Rotación de 90 grados en sentido horario
video = rotate(video, 90)
video_gameover = rotate(video_gameover, 90)


# Reproducir en bucle
video = video.loop(duration=video.duration)
video_gameover = video_gameover.loop(duration=video_gameover.duration)


#Se crea una superficie de pygame
video_surface = pygame.display.set_mode((ANCHO, ALTO))
video_surface_gameover = pygame.Surface((ANCHO, ALTO)).convert()

pantalla = pygame.display.set_mode((ANCHO, ALTO))

#-------------------------------------------------
# Fuente
consolas = pygame.font.match_font('consolas')

def get_font(size):
    return pygame.font.Font("./documents/assets/fuente.ttf", size)

#-------------------------------------------------


def jugar():
    
    reloj = pygame.time.Clock()
    fondo = pygame.image.load("./documents/assets/img/fondo.jpg")
    pygame.display.set_caption("Jugando...")

    # Bucle principal
    ejecutando = True
    
    # Sistema de puntuaciones
    puntuacion = 0

    jugador = Jugador()
    jugador_sprites.add(jugador)

    pygame.mixer.init()

    tiempo = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Variables del temporizador
    total_segundos = 120  # 2 minutos
    frame_count = 0

    hit = pygame.mixer.Sound('./documents/assets/sounds/hit.mp3')

    
    while ejecutando:

        # Logica del temporizador
        tiempo.tick(60)
        frame_count += 1

        if frame_count == 60:  # Actualiza el temporizador cada segundo
            total_segundos -= 1
            frame_count = 0

        if total_segundos <= 0:
        # si el temporizador es 0, detener el bucle del juego
            ejecutando = False
            jugador_sprites.empty()
            enemigos_facilitos.empty()
            enemigos_normalitos.empty()
            misiles.empty()
            misiles_enemigos.empty()
            meteorito.empty()
            gameover(puntuacion)
    

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                # Actualizar

        if not meteorito:
            for x in range(random.randrange(11) + 4):
                meteoritos = Meteoritos()
                meteorito.add(meteoritos)
        
        if not enemigos_facilitos:
            for x in range(random.randrange(7) + 5):
                enemigof = Malo2()
                enemigos_facilitos.add(enemigof)
        
        if not enemigos_normalitos:
            for x in range(random.randrange(12) + 7):
                enemigo = Malo()
                enemigos_normalitos.add(enemigo)
    

        jugador_sprites.update()
        enemigos_facilitos.update()
        enemigos_normalitos.update()
        misiles.update()
        misiles_enemigos.update()
        meteorito.update()
        
        
        # Colisiones
        colision_M_meteorito = pygame.sprite.groupcollide(meteorito,misiles,True,True,pygame.sprite.collide_circle)

        if colision_M_meteorito:
            puntuacion += 5

        #-------------------------------------------------------------------------------------------------------------------------
        colision_M_Facilitos = pygame.sprite.groupcollide(enemigos_facilitos,misiles,True,True,pygame.sprite.collide_circle)

        if colision_M_Facilitos:
            puntuacion += 10
        #-------------------------------------------------------------------------------------------------------------------------
        

        #-------------------------------------------------------------------------------------------------------------------------
        colision_M_Normalitos = pygame.sprite.groupcollide(enemigos_normalitos,misiles,True,True,pygame.sprite.collide_circle)

        if colision_M_Normalitos:
            puntuacion += 15
            hit.play()
        #-------------------------------------------------------------------------------------------------------------------------


        #-------------------------------------------------------------------------------------------------------------------------
        colision_MisilEnemigos_Facilitos = pygame.sprite.groupcollide(jugador_sprites,misiles_enemigos,False,True,pygame.sprite.collide_circle)

        if colision_MisilEnemigos_Facilitos:
            jugador.hp -= 25
        #-------------------------------------------------------------------------------------------------------------------------


        #-------------------------------------------------------------------------------------------------------------------------
        colision_P_Meteorito = pygame.sprite.groupcollide(jugador_sprites, meteorito,False,True,pygame.sprite.collide_circle)

        if colision_P_Meteorito:
            jugador.hp -= 15
            if puntuacion >= 0:
                puntuacion -= 5
                if puntuacion < 0:
                    puntuacion = 0
        #-------------------------------------------------------------------------------------------------------------------------


        #-------------------------------------------------------------------------------------------------------------------------
        colision_P_facilitos = pygame.sprite.groupcollide(jugador_sprites, enemigos_facilitos,False,True,pygame.sprite.collide_circle)

        if colision_P_facilitos:
            jugador.hp -= 15
            if puntuacion >= 0:
                puntuacion -= 10
                if puntuacion < 0:
                    puntuacion = 0
        #-------------------------------------------------------------------------------------------------------------------------


        #-------------------------------------------------------------------------------------------------------------------------
        colision_P_Normalitos = pygame.sprite.groupcollide(jugador_sprites, enemigos_normalitos,False,True,pygame.sprite.collide_circle)
                    
        if colision_P_Normalitos:
            jugador.hp -= 30
            if puntuacion >= 0:
                puntuacion -= 15
                if puntuacion < 0:
                    puntuacion = 0
        #-------------------------------------------------------------------------------------------------------------------------
        

        #-------------------------------------------------------------------------------------------------------------------------

        cruz = pygame.image.load('./documents/assets/img/cruz.png').convert()
        
        if jugador.hp <= 0 and jugador.vidas == 3:
            jugador.kill()
            jugador = Jugador()
            jugador_sprites.add(jugador)
            jugador.vidas = 2

        if jugador.vidas == 2:
            if jugador.hp <= 0:
                jugador.kill()
                jugador = Jugador()
                jugador_sprites.add(jugador)
                jugador.vidas = 1
        
        if jugador.vidas == 1:
            if jugador.hp <= 0:
                jugador.kill()
                jugador = Jugador()
                jugador_sprites.add(jugador)
                jugador.vidas = 0
        
        if jugador.vidas == 0:
            if jugador.hp <= 0:
                jugador.kill()
                jugador.hp = 0

        if jugador.hp <= 0:
            ejecutando = False
            jugador_sprites.empty()
            enemigos_facilitos.empty()
            enemigos_normalitos.empty()
            misiles.empty()
            misiles_enemigos.empty()
            meteorito.empty()
            gameover(puntuacion)


        
        # Dibujar / renderizar
        pantalla.blit(fondo, (0, 0))

        jugador_sprites.draw(pantalla)
        enemigos_facilitos.draw(pantalla)
        enemigos_normalitos.draw(pantalla)
        misiles.draw(pantalla)
        meteorito.draw(pantalla)
        misiles_enemigos.draw(pantalla)

        texto_tiempo = font.render("Tiempo restante: {:02d}:{:02d}".format(total_segundos // 60, total_segundos % 60), True, WHITE)
        text_rect = texto_tiempo.get_rect(center=(150, 30))

        
        #Dibujo el texto
        mostrar_puntos(pantalla,consolas,str(puntuacion), WHITE, 40, ANCHO // 2, 40)
        mostrar_barra_vida(pantalla, 1055, 15, jugador)
        mostrar_vidas(pantalla, 0, 15, jugador)
        pantalla.blit(texto_tiempo, text_rect)
        
        # Despues de dibujar todo, flip
        pygame.display.flip()
        reloj.tick(FPS)

def gameover(puntuacion):
    pygame.display.set_caption("Ingrese Usuario")
    texto_ingresado = ""
    nombre_ingresado = False
    font = pygame.font.SysFont("Cambria", 75)
    rect_texto = pygame.Rect(456,538,10,72)
    en_pos = False


    while True:
        # Obtén el fotograma actual del video y conviértelo a una imagen de Pygame
        frame_gameover = video_gameover.get_frame(pygame.time.get_ticks() / 1000)
        frame_gameover = pygame.surfarray.make_surface(frame_gameover)
        # Dibuja el fotograma en la superficie de Pygame
        video_surface_gameover.blit(frame_gameover, (0, 0))

        # Dibuja la superficie de Pygame en la ventana
        pantalla.blit(video_surface_gameover, (0, 0))


        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_texto.collidepoint(evento.pos):
                    en_pos = True
                else:
                    en_pos = False

            if evento.type == pygame.KEYDOWN:
                if en_pos and not nombre_ingresado:  # Solo permitir entrada de texto si no se ha ingresado un nombre
                    if evento.key == pygame.K_BACKSPACE:
                        texto_ingresado = texto_ingresado[0:-1]
                    elif evento.key == pygame.K_RETURN:  # Comprobar si se presiona la tecla Enter
                        nombre_ingresado = True  # Establecer la bandera en True para indicar que se ha ingresado un nombre
                        insertar_score(texto_ingresado,puntuacion)
                        main_menu()
                    else:
                        texto_ingresado += evento.unicode


        if en_pos and not nombre_ingresado:
            color_actual = GRAY
        else:
            color_actual = GRAY10

        pygame.draw.rect(pantalla,color_actual, rect_texto)

        superficie_texto = font.render(texto_ingresado, True,(255,255,255))
        pantalla.blit(superficie_texto,rect_texto)

        rect_texto.w = max(368,superficie_texto.get_width() + 10)

        pygame.display.flip()
    
def ranking():
    pygame.display.set_caption("Mirando Ranking...")
    pantalla.blit(leaderboard, (0, 0))
    mostrar_leaderboard(pantalla)
    while True:
        posicion_mouse = pygame.mouse.get_pos()


        VOLVER = Boton(image=None, pos=(640, 630), 
                            text_input="VOLVER", font=get_font(50), base_color=WHITE, hovering_color=YELLOW1)

        VOLVER.changeColor(posicion_mouse)
        VOLVER.update(pantalla)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if VOLVER.checkForInput(posicion_mouse):
                    main_menu()

        pygame.display.update()

def main_menu():
    pygame.display.set_caption("Bienvenido")
    while True:
        #Obtén el fotograma actual del video y conviértelo a una imagen de Pygame
        frame = video.get_frame(pygame.time.get_ticks() / 1000)
        frame = pygame.surfarray.make_surface(frame)
        #Dibuja el fotograma en la superficie de Pygame
        video_surface.blit(frame, (0, 0))

        #Dibuja la superficie de Pygame en la ventana
        pantalla.blit(video_surface, (0, 0))

        posicion_mouse = pygame.mouse.get_pos()

        BOTON_JUGAR = Boton(image=pygame.image.load("./documents/assets/img/menu/jugar.png"), pos=(640, 250), 
                            text_input=" ", font=get_font(70), base_color=WHITE, hovering_color=WHITE)
        BOTON_RANKING = Boton(image=pygame.image.load("./documents/assets/img/menu/ranking.png"), pos=(640, 400), 
                            text_input=" ", font=get_font(70), base_color=WHITE, hovering_color=WHITE)
        BOTON_SALIR = Boton(image=pygame.image.load("./documents/assets/img/menu/salir.png"), pos=(640, 550), 
                            text_input=" ", font=get_font(70), base_color=WHITE, hovering_color=WHITE)

        for boton in [BOTON_JUGAR, BOTON_RANKING, BOTON_SALIR]:
            boton.changeColor(posicion_mouse)
            boton.update(pantalla)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BOTON_JUGAR.checkForInput(posicion_mouse):
                    jugar()
                if BOTON_RANKING.checkForInput(posicion_mouse):
                    ranking()
                if BOTON_SALIR.checkForInput(posicion_mouse):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

main_menu()