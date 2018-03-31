#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
import pygame
import director
from director import *
from menu import Menu

if __name__ == '__main__':

    # Inicializamos la libreria de pygame
    pygame.init()
    pygame.mixer.pre_init(44100,16,2,4096)
    pygame.mixer.init()
    # Creamos el director
    director = Director()
    # Creamos la escena con la pantalla inicial
    escena = Menu(director)
    # Le decimos al director que apile esta escena
    director.apilarEscena(escena)
    # Y ejecutamos el juego
    director.ejecutar()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
