# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from gestorRecursos import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Movimientos
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4

#Posturas
SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1
SPRITE_SALTANDO = 2

# Velocidades de los distintos personajes
VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5 # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura

VELOCIDAD_SNIPER = 0.12 # Pixeles por milisegundo
VELOCIDAD_SALTO_SNIPER = 0.27 # Pixeles por milisegundo
RETARDO_ANIMACION_SNIPER = 5 # updates que durará cada imagen del personaje
                             # debería de ser un valor distinto para cada postura
# El Sniper camina un poco más lento que el jugador, y salta menos

GRAVEDAD = 0.0006 # Píxeles / ms2

# -------------------------------------------------

# -------------------------------------------------
# Funciones auxiliares
# -------------------------------------------------
# -------------------------------------------------


# -------------------------------------------------
# -------------------------------------------------
# Clases de los objetos del juego
# -------------------------------------------------
# -------------------------------------------------


# -------------------------------------------------
# Clase MiSprite
class MiSprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll   = (0, 0)

    def establecerPosicion(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollDecorado):
        self.scroll = scrollDecorado;
        (scrollx, scrolly) = self.scroll;
        (posx, posy) = self.posicion;
        self.rect.left = posx - scrollx;
        self.rect.bottom = posy - scrolly;

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((posx+incrementox, posy+incrementoy))

    def update(self, tiempo):
        incrementox = self.velocidad[0]*tiempo
        incrementoy = self.velocidad[1]*tiempo
        self.incrementarPosicion((incrementox, incrementoy))



# -------------------------------------------------
# Clases Personaje

#class Personaje(pygame.sprite.Sprite):
class Personaje(MiSprite):
    "Cualquier personaje del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadCarrera, velocidadSalto, retardoAnimacion):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self);
        self.unSaltoSolo=0
        self.direcbala=DERECHA
        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)

        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO
        # Lado hacia el que esta mirando
        self.mirando = IZQUIERDA

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1;
        self.numImagenPostura = 0;
        cont = 0;
        self.coordenadasHoja = [];
        for linea in range(0, 3):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0;

        # En que postura esta inicialmente
        self.numPostura = QUIETO

        # El rectangulo del Sprite
        self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        # Las velocidades de caminar y salto
        self.velocidadCarrera = velocidadCarrera
        self.velocidadSalto = velocidadSalto

        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()


    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def mover(self, movimiento):
        if movimiento == ARRIBA:

            # Si estamos en el aire y el personaje quiere saltar, ignoramos este movimiento
            if self.numPostura == SPRITE_SALTANDO:
                    self.movimiento = self.unSaltoSolo
            else:
                    self.movimiento = ARRIBA
        else:
            if movimiento !=0 :
                self.direcbala=movimiento
            self.unSaltoSolo=movimiento
            self.movimiento = movimiento


    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion#actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0;
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == IZQUIERDA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == DERECHA:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)


    def update(self, grupoPlataformas, tiempo):

        # Las velocidades a las que iba hasta este momento
        (velocidadx, velocidady) = self.velocidad

        # Si vamos a la izquierda o a la derecha
        if (self.movimiento == IZQUIERDA) or (self.movimiento == DERECHA):
            # Esta mirando hacia ese lado
            self.mirando = self.movimiento

            # Si vamos a la izquierda, le ponemos velocidad en esa dirección
            if self.movimiento == IZQUIERDA:
                velocidadx = -self.velocidadCarrera
            # Si vamos a la derecha, le ponemos velocidad en esa dirección
            else:
                velocidadx = self.velocidadCarrera

            # Si no estamos en el aire
            if self.numPostura != SPRITE_SALTANDO:
                # La postura actual sera estar caminando
                self.numPostura = SPRITE_ANDANDO
                # Ademas, si no estamos encima de ninguna plataforma, caeremos
                if pygame.sprite.spritecollideany(self, grupoPlataformas) == None:
                    self.numPostura = SPRITE_SALTANDO

        # Si queremos saltar
        elif self.movimiento == ARRIBA:
            # La postura actual sera estar saltando
            self.numPostura = SPRITE_SALTANDO
            # Le imprimimos una velocidad en el eje y
            velocidady = -self.velocidadSalto

        # Si no se ha pulsado ninguna tecla
        elif self.movimiento == QUIETO:
            # Si no estamos saltando, la postura actual será estar quieto
            if not self.numPostura == SPRITE_SALTANDO:
                self.numPostura = SPRITE_QUIETO
            velocidadx = 0



        # Además, si estamos en el aire
        if self.numPostura == SPRITE_SALTANDO:

            # Miramos a ver si hay que parar de caer: si hemos llegado a una plataforma
            #  Para ello, miramos si hay colision con alguna plataforma del grupo
            plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
            #  Ademas, esa colision solo nos interesa cuando estamos cayendo
            #  y solo es efectiva cuando caemos encima, no de lado, es decir,
            #  cuando nuestra posicion inferior esta por encima de la parte de abajo de la plataforma
            if (plataforma != None) and (velocidady>0) and (plataforma.rect.bottom>self.rect.bottom):
                # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
                #  para poder detectar cuando se cae de ella
                self.establecerPosicion((self.posicion[0], plataforma.posicion[1]-plataforma.rect.height+1))
                # Lo ponemos como quieto
                self.numPostura = SPRITE_QUIETO

                # Y estará quieto en el eje y
                velocidady = 0

            # Si no caemos en una plataforma, aplicamos el efecto de la gravedad
            else:
                velocidady += GRAVEDAD * tiempo

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje
        self.velocidad = (velocidadx, velocidady)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MiSprite.update(self, tiempo)

        return



# -------------------------------------------------
# Clase Jugador

class Jugador(Personaje):
    "Cualquier personaje del juego"
    def __init__(self,grupoproy):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self,'Jugador.png','coordJugador.txt', [6, 12, 6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR);
        self.grupoProyectiles=grupoproy
        self.vida=3
        self.delaydisp=pygame.time.get_ticks()
    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha,disparo, disparoArriba):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if teclasPulsadas[disparo] or teclasPulsadas[disparoArriba]:
            if (pygame.time.get_ticks()-self.delaydisp)>300:
                self.delaydisp=pygame.time.get_ticks()
                if teclasPulsadas[disparo]:
                    p=Proyectil(self.direcbala)
                if teclasPulsadas[disparoArriba]:
                    p=Proyectil(ARRIBA)
                p.establecerPosicion((self.posicion[0],self.posicion[1]))
                p.scroll=self.scroll
                #p.posicion=self.posicion
                self.grupoProyectiles.add(p)#Personaje.mover(self,ARRIBA)
                self.grupoDinam.add(p)
                self.grupoSprites.add(p)
            if (not teclasPulsadas[derecha]) and (not teclasPulsadas[izquierda]):
                Personaje.mover(self,QUIETO)
            if teclasPulsadas[izquierda]:
                Personaje.mover(self,IZQUIERDA)
            if teclasPulsadas[derecha]:
                Personaje.mover(self,DERECHA)
        elif teclasPulsadas[arriba]:
            Personaje.mover(self,ARRIBA)
        elif teclasPulsadas[izquierda]:
            Personaje.mover(self,IZQUIERDA)
        elif teclasPulsadas[derecha]:
            Personaje.mover(self,DERECHA)
        else:
            Personaje.mover(self,QUIETO)

    def setgrupproy(self,grupdinam,grupsprit):
        self.grupoDinam=grupdinam
        self.grupoSprites=grupsprit
# -------------------------------------------------
# Clase NoJugador

class NoJugador(Personaje):
    "El resto de personajes no jugadores"
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion):
        # Primero invocamos al constructor de la clase padre con los parametros pasados
        Personaje.__init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion);
        self.quieto=False
        self.vida=3
        self.danodelay=pygame.time.get_ticks()
    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion por defecto, este metodo deberia de ser implementado en las clases inferiores
    #  mostrando la personalidad de cada enemigo
    def update (self, grupoPlataformas, tiempo):
        if (pygame.time.get_ticks()-self.danodelay)>400:
            self.quieto=False
        if not self.quieto:
            Personaje.update( self,grupoPlataformas, tiempo)
    def mover_cpu(self, jugador1):
        # Por defecto un enemigo no hace nada
        #  (se podria programar, por ejemplo, que disparase al jugador por defecto)

        return
    def recibir_dano(self):
        if (pygame.time.get_ticks()-self.danodelay)>600:
            self.danodelay=pygame.time.get_ticks()
            self.vida-=1
            self.quieto=True

        return
# -------------------------------------------------
# Clase Sniper

class Sniper(NoJugador):
    "El enemigo 'Sniper'"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Sniper.png','coordSniper.txt', [5, 10, 6], VELOCIDAD_SNIPER, VELOCIDAD_SALTO_SNIPER, RETARDO_ANIMACION_SNIPER);
        self.vida=5
    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
   
    def mover_cpu(self, jugador1):
        if self.quieto==True :
            return
        else:
            # Movemos solo a los enemigos que esten en la pantalla
            if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:

                # Por ejemplo, intentara acercarse al jugador mas cercano en el eje x
                # Miramos cual es el jugador mas cercano
                # if abs(jugador1.posicion[0]-self.posicion[0])<abs(jugador2.posicion[0]-self.posicion[0]):
                jugadorMasCercano = jugador1
                # else:
                #     jugadorMasCercano = jugador2
                # Y nos movemos andando hacia el
                if jugadorMasCercano.posicion[0]<self.posicion[0]:
                    Personaje.mover(self,IZQUIERDA)
                else:
                    Personaje.mover(self,DERECHA)

            # Si este personaje no esta en pantalla, no hara nada
            else:
                Personaje.mover(self,QUIETO)
            
class Proyectil(Personaje):
    "El proyectil del enemigo"
    def __init__(self,direccion):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self,'disparo.png','coordSniper.txt', [5, 10, 6], 0.3, VELOCIDAD_SALTO_SNIPER, RETARDO_ANIMACION_SNIPER);
        self.direcc=direccion
        self.vida=1
        self.lifetime=pygame.time.get_ticks()
    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):
        #print (pygame.time.get_ticks()-self.lifetime)
        if (pygame.time.get_ticks()-self.lifetime)>1800:
            #print self, self.lifetime, pygame.time.get_ticks()
            self.kill()
        else:
            #self.lifetime-=pygame.time.get_ticks()
            Personaje.mover(self,self.direcc)

    def update(self, grupoPlataformas, tiempo):

        # Las velocidades a las que iba hasta este momento
        (velocidadx, velocidady) = self.velocidad

        # Si vamos a la izquierda o a la derecha
        if (self.movimiento == IZQUIERDA) or (self.movimiento == DERECHA):
            # Esta mirando hacia ese lado
            self.mirando = self.movimiento

            # Si vamos a la izquierda, le ponemos velocidad en esa dirección
            if self.movimiento == IZQUIERDA:
                velocidadx = -self.velocidadCarrera
            # Si vamos a la derecha, le ponemos velocidad en esa dirección
            else:
                velocidadx = self.velocidadCarrera

            # Si no estamos en el aire
            if self.numPostura != SPRITE_SALTANDO:
                # La postura actual sera estar caminando
                self.numPostura = SPRITE_ANDANDO
                # Ademas, si no estamos encima de ninguna plataforma, caeremos
                if pygame.sprite.spritecollideany(self, grupoPlataformas) == None:
                    self.numPostura = SPRITE_SALTANDO

        # Si queremos saltar
        elif self.movimiento == ARRIBA:
            # La postura actual sera estar saltando
            self.numPostura = SPRITE_SALTANDO
            # Le imprimimos una velocidad en el eje y
            velocidady = -self.velocidadSalto
        elif self.movimiento == ABAJO:
            # La postura actual sera estar saltando
            self.numPostura = SPRITE_SALTANDO
            # Le imprimimos una velocidad en el eje y
            velocidady = self.velocidadSalto

        # Si no se ha pulsado ninguna tecla
        elif self.movimiento == QUIETO:
            # Si no estamos saltando, la postura actual será estar quieto
            if not self.numPostura == SPRITE_SALTANDO:
                self.numPostura = SPRITE_QUIETO
            velocidadx = 0



        # Además, si estamos en el aire
        # Actualizamos la imagen a mostrar
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje
        self.velocidad = (velocidadx, velocidady)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MiSprite.update(self, tiempo)

        return


class PowerUp(Personaje):
    "PowerUp para el personaje"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self,'disparo.png','coordSniper.txt', [5, 10, 6], 0.3, VELOCIDAD_SALTO_SNIPER, RETARDO_ANIMACION_SNIPER);
    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):
        return
    def efecto(self,jugador1):
        print "PowerUp"
        return


class EndFase(Personaje):
    "PowerUp para el personaje"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self,'EndFase.png','coordEndFase.txt', [5, 10, 6], 0.3, VELOCIDAD_SALTO_SNIPER, RETARDO_ANIMACION_SNIPER);
    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):
        return
    def efecto(self):
        #director.salirFase()
        return
#--------------------------------------------------------------

class Sniper_Dispara(Sniper):
    "Enemigo 'Sniper' que solo nos dispara"
    def __init__(self,grupoproyEnem):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Sniper.png','coordSniper.txt', [5, 10, 6], VELOCIDAD_SNIPER, VELOCIDAD_SALTO_SNIPER, RETARDO_ANIMACION_SNIPER);
        self.vida=5
        self.grupoProyectilesEnemigo=grupoproyEnem
        self.delaydisp=pygame.time.get_ticks()

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
   
    def mover_cpu(self, jugador1):
        if self.quieto==True :
            return
        else:
            # Disparan solo los enemigos que esten en la pantalla
            if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:
                self.mover(QUIETO)
                if (pygame.time.get_ticks()-self.delaydisp)>300:
                    self.delaydisp=(pygame.time.get_ticks())*1.2
                    jugadorMasCercano = jugador1
                    if jugadorMasCercano.posicion[0]<self.posicion[0]:
                        self.disparar(IZQUIERDA) 
                        self.mover(IZQUIERDA)
                    else:
                        self.disparar(DERECHA)
                        self.mover(DERECHA)
            # Si este personaje no esta en pantalla, no hara nada
            else:
                Personaje.mover(self,QUIETO)

    def disparar(self,direccion):
        p=Proyectil(direccion)
        p.establecerPosicion((self.posicion[0],self.posicion[1]))
        p.scroll=self.scroll 
        self.grupoProyectilesEnemigo.add(p)
        self.grupoDinam.add(p)
        self.grupoSprites.add(p)

    def setgrupoproyEnem(self,grupdinam,grupsprit):
        self.grupoDinam=grupdinam
        self.grupoSprites=grupsprit


class Tirador_Arriba(Sniper_Dispara):
    "Enemigo que no se mueve, nos dispara desde abajo"
    def __init__(self,grupoproyEnem):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Sniper.png','coordSniper.txt', [5, 10, 6], VELOCIDAD_SNIPER, VELOCIDAD_SALTO_SNIPER, RETARDO_ANIMACION_SNIPER);
        self.vida=3
        self.grupoProyectilesEnemigo=grupoproyEnem
        self.delaydisp=pygame.time.get_ticks()

    def mover_cpu(self, jugador1):
        if self.quieto==True :
            return
        else:
            # Disparan solo los enemigos que esten en la pantalla
            if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:
                if (pygame.time.get_ticks()-self.delaydisp)>300:
                    self.delaydisp=(pygame.time.get_ticks())*1.2
                    jugadorMasCercano = jugador1
                    p=Proyectil(ARRIBA)
                    p.establecerPosicion((self.posicion[0],self.posicion[1]))
                    p.scroll=self.scroll 
                    self.grupoProyectilesEnemigo.add(p)
                    self.grupoDinam.add(p)
                    self.grupoSprites.add(p)           
            # Si este personaje no esta en pantalla, no hara nada
            else:
                Personaje.mover(self,QUIETO)    

    def setgrupoproyEnem(self,grupdinam,grupsprit):
        self.grupoDinam=grupdinam
        self.grupoSprites=grupsprit

class Tirador_Abajo(Sniper_Dispara):
    "Enemigo que no se mueve, nos dispara desde arriba"
    def __init__(self,grupoproyEnem):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Sniper.png','coordSniper.txt', [5, 10, 6], VELOCIDAD_SNIPER, VELOCIDAD_SALTO_SNIPER, RETARDO_ANIMACION_SNIPER);
        self.vida=3
        self.grupoProyectilesEnemigo=grupoproyEnem
        self.delaydisp=pygame.time.get_ticks()

    def mover_cpu(self, jugador1):
        if self.quieto==True :
            return
        else:
            # Disparan solo los enemigos que esten en la pantalla
            if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:
                if (pygame.time.get_ticks()-self.delaydisp)>300:
                    self.delaydisp=(pygame.time.get_ticks())*1.2
                    jugadorMasCercano = jugador1
                    p=Proyectil(ABAJO)
                    p.establecerPosicion((self.posicion[0],self.posicion[1]))
                    p.scroll=self.scroll 
                    self.grupoProyectilesEnemigo.add(p)
                    self.grupoDinam.add(p)
                    self.grupoSprites.add(p)           
            # Si este personaje no esta en pantalla, no hara nada
            else:
                Personaje.mover(self,QUIETO)    

    def setgrupoproyEnem(self,grupdinam,grupsprit):
        self.grupoDinam=grupdinam
        self.grupoSprites=grupsprit
#Diferentes enemigos
class mob1(NoJugador):
    "El enemigo 'Sniper'"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'mob1pix.png','coordSniper.txt', [5, 10, 6], VELOCIDAD_SNIPER, VELOCIDAD_SALTO_SNIPER, RETARDO_ANIMACION_SNIPER);
        self.vida=2
    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
   
    def mover_cpu(self, jugador1):
        if self.quieto==True :
            return
        else:
            # Movemos solo a los enemigos que esten en la pantalla
            if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:

                # Por ejemplo, intentara acercarse al jugador mas cercano en el eje x
                # Miramos cual es el jugador mas cercano
                # if abs(jugador1.posicion[0]-self.posicion[0])<abs(jugador2.posicion[0]-self.posicion[0]):
                jugadorMasCercano = jugador1
                # else:
                #     jugadorMasCercano = jugador2
                # Y nos movemos andando hacia el
                if jugadorMasCercano.posicion[0]<self.posicion[0]:
                    Personaje.mover(self,IZQUIERDA)
                else:
                    Personaje.mover(self,DERECHA)

            # Si este personaje no esta en pantalla, no hara nada
            else:
                Personaje.mover(self,QUIETO)
#--------------------------------------------------------------
#Diferentes power ups

class powerupSpeed(PowerUp):
    "PowerUp para el personaje"
    def __init__(self):
        Personaje.__init__(self,'powerup.png','coordSniper.txt', [5, 10, 6], 0.3, VELOCIDAD_SALTO_SNIPER, RETARDO_ANIMACION_SNIPER);
    def efecto(self,jugador1):
        return
class powerupBotiquin(PowerUp):
    "PowerUp para el personaje"
    def __init__(self):
        Personaje.__init__(self,'powerupBotiquin.png','coordSniper.txt', [5, 10, 6], 0.3, VELOCIDAD_SALTO_SNIPER, RETARDO_ANIMACION_SNIPER);
    def efecto(self,jugador1):
        jugador1.vida=3
        return

