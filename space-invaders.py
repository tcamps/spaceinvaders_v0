import pygame

# Inicialización de Pygame
pygame.init()

# CONSTANTES
ANCHO = 800
ALTO = 600
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# CONSTANTES ESTADOS JUEGO
ESTADO_JUGANDO = 1
ESTADO_GANADO = 2
ESTADO_GAMEOVER = 3

# Variable estado actual del juego
estado_actual_juego = ESTADO_JUGANDO

# Inicializacion de la superfície de dibujo
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders versión 0")

# Creamos sprite de la nave
nave = pygame.sprite.Sprite()
nave.image = pygame.image.load("imagenes/nave.png")
# Obtenemos el rectángulo de la nave
nave.rect = nave.image.get_rect()
# Situamos la nave en la parte inferior y al centro
nave.rect.centerx = ANCHO / 2
nave.rect.bottom = ALTO

# Creamos el sprite del disparo de la nave
# Solo puede haber un disparo a la vez
# Por defecto, se posiciona fuera de pantalla y al disparar entre en la zona de juego
disparo_nave = pygame.sprite.Sprite()
disparo_nave.image = pygame.image.load("imagenes/disparo_nave.png")
disparo_nave.rect = disparo_nave.image.get_rect()
disparo_nave.rect.bottom = 0

# Creamos los aliens. Los guardaremos un un grupo de Sprites
aliens = pygame.sprite.Group()
# Calculamos la separación entre aliens. Cada alien ocupa 50 pixels
aliens_por_fila = 10
separacion_entre_aliens = (ANCHO - (50 * aliens_por_fila)) / (aliens_por_fila + 1)
for i in range(aliens_por_fila):
    alien = pygame.sprite.Sprite()
    alien.image = pygame.image.load("imagenes/alien1.png")
    alien.rect = alien.image.get_rect()
    alien.rect.x = (alien.rect.width * i) + (separacion_entre_aliens * (i + 1))
    alien.rect.top = 10
    aliens.add(alien)

# Dirección en la que se mueven los aliens horizontalmente:
# izquierda (-1) o derecha (1)
movimiento_horizontal = -1

# Creamos textos de "HAS GANADO" y "GAME OVER"
fuente_txt_final = pygame.font.Font(None, 60)
txt_ganado = fuente_txt_final.render("HAS GANADO!!", 0, NEGRO)
txt_gameover = fuente_txt_final.render("GAME OVER!!", 0, NEGRO)

# Bucle principal del juego
jugando = True
while jugando:
    # Comprovamos los eventos
    # Comprovamos si se ha pulsado el botón de cerrar la ventana
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
        # Evento de pulsación de tecla. En este caso no sirve dejar la tecla siempre pulsada
        if event.type == pygame.KEYUP:
            # Se pulsa espacio y el disparo no está actualmente en juego
            if event.key == pygame.K_SPACE and disparo_nave.rect.bottom <= 0:
                disparo_nave.rect.centerx = nave.rect.centerx
                disparo_nave.rect.bottom = nave.rect.top

    # Controlamos las pulsaciones de teclas. En este caso se permite dejar pulsado
    # Izquierda y derecha
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and nave.rect.left > 0:
        nave.rect.x -= 3
    if keys[pygame.K_RIGHT] and nave.rect.right < ANCHO:
        nave.rect.x += 3

    if estado_actual_juego == ESTADO_JUGANDO:
        # Comprovamos colisión de disparo con alguna nave
        if pygame.sprite.spritecollide(disparo_nave, aliens, True):
            disparo_nave.rect.bottom = 0 # Sacamos disparo de zona de juego
            # Comprovamos si aun hay naves
            if len(aliens.sprites()) == 0:
                estado_actual_juego = ESTADO_GANADO


        # Movemos los aliens
        movimento_vertical = 0
        for alien in aliens.sprites():
            if ((movimiento_horizontal < 0 and alien.rect.left <= 0) or
                (movimiento_horizontal > 0 and alien.rect.right >= ANCHO)):
                movimento_vertical = 5
                movimiento_horizontal *= -1
                break

        for alien in aliens.sprites():
            alien.rect.y += movimento_vertical
            alien.rect.x += movimiento_horizontal


        # Comprovamos si aliens tocan nave o han llegado al fondo
        if pygame.sprite.spritecollide(nave, aliens, False):
            estado_actual_juego = ESTADO_GAMEOVER

        # Movemos el disparo de la nave si está en juego
        if disparo_nave.rect.bottom > 0:
            disparo_nave.rect.y -= 5

        # Se pinta el fondo de la ventana
        # Esto borra los posibles elementos que teníamos anteriormente
        ventana.fill(BLANCO)

        # Dibujamos la nave
        ventana.blit(nave.image, nave.rect)

        # Dibujamos el disparo de la nave
        ventana.blit(disparo_nave.image, disparo_nave.rect)

        # Dibujamos el grupo de sprites que contiene los aliens
        aliens.draw(ventana)
    elif estado_actual_juego == ESTADO_GANADO:
        ventana.blit(txt_ganado, ((ANCHO / 2) - (txt_ganado.get_width() / 2), (ALTO / 2) - (txt_ganado.get_height() / 2)))
    elif estado_actual_juego == ESTADO_GAMEOVER:
        ventana.blit(txt_gameover, ((ANCHO / 2) - (txt_gameover.get_width() / 2), (ALTO / 2) - (txt_gameover.get_height() / 2)))

    # Todos los elementos del juego se vuelven a dibujar
    pygame.display.flip()

    # Controlamos la frecuencia de refresco (FPS)
    pygame.time.Clock().tick(60)

pygame.quit()
