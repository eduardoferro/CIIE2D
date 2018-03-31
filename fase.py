# -*- coding: utf-8 -*-

import pygame
from personajes import *
from pygame.locals import *
from gestorRecursos import *
from escena import *
# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

VELOCIDAD_SOL = 0.1 # Pixeles por milisegundo

# Los bordes de la pantalla para hacer scroll horizontal
MINIMO_X_JUGADOR = 150
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

# -------------------------------------------------
# Clase Fase

class Fase(Escena):
    def __init__(self,director):

        # Habria que pasarle como parámetro el número de fase, a partir del cual se cargue
        #  un fichero donde este la configuracion de esa fase en concreto, con cosas como
        #   - Nombre del archivo con el decorado
        #   - Posiciones de las plataformas
        #   - Posiciones de los enemigos
        #   - Posiciones de inicio de los jugadores
        #  etc.
        # Y cargar esa configuracion del archivo en lugar de ponerla a mano, como aqui abajo
        # De esta forma, se podrian tener muchas fases distintas con esta clase
        Escena.__init__(self, director)
        # Creamos el decorado y el fondo
       
        self.fondo = Cielo()
        self.decorado=Decorado('decorado.png',1200,300,1)
        # Que parte del decorado estamos visualizando
        self.scrollx = 0
        #  En ese caso solo hay scroll horizontal
        #  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)
        self.grupoProyectilesEnemigo = pygame.sprite.Group()
        self.grupoPowerUps=pygame.sprite.Group()
        self.grupoFinFase=pygame.sprite.Group()
        self.grupoHud=pygame.sprite.Group()
        
        # Creamos los sprites de los jugadores
        self.grupoProyectiles = pygame.sprite.Group()
        self.jugador1 = Jugador(self.grupoProyectiles)
        # self.jugador2 = Jugador(self.grupoProyectiles)
        self.grupoJugadores = pygame.sprite.Group( self.jugador1 )

        # Ponemos a los jugadores en sus posiciones iniciales
        
        # self.jugador2.establecerPosicion((400, 551))

        # Creamos las plataformas del decorado
        # La plataforma que conforma todo el suelo

        # y el grupo con las mismas
        self.grupoPlataformas = pygame.sprite.Group( )

        # Y los enemigos que tendran en este decorado
        

        # Creamos un grupo con los enemigos
        self.grupoEnemigos = pygame.sprite.Group(  )

        # Creamos un grupo con los Sprites que se mueven
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1 )
        # Creamos otro grupo con todos los Sprites
        self.grupoSprites = pygame.sprite.Group( self.jugador1 )
        self.jugador1.setgrupproy(self.grupoSpritesDinamicos,self.grupoSprites)
    def addPlataforma(self,plat):
        self.grupoPlataformas.add(plat)
        self.grupoSprites.add(plat)
    #def setFondo(self,fondo):
    def addHud(self,hud):
        self.grupoSprites.add(hud)
        self.grupoHud.add(hud)
    def addPowerUp(self,powerup):
        self.grupoSprites.add(powerup)
        self.grupoPowerUps.add(powerup)

    def addEnemigo(self,enem):
        self.grupoEnemigos.add(enem)
        self.grupoSpritesDinamicos.add(enem)
        self.grupoSprites.add(enem)

    def setDecorado(self,file,x,y,scrolldelay):
        self.decorado = Decorado(file,x,y,scrolldelay)
    def setFondo(self,file,x,y,scrolldelay):
        self.fondo = Decorado(file,x,y,scrolldelay)
    def setJugador(self,x,y):
        self.jugador1.establecerPosicion((x, y))
    def setFin(self,fin):
        self.grupoSprites.add(fin)
        self.grupoFinFase.add(fin)

    # Devuelve True o False según se ha tenido que desplazar el scroll
    def actualizarScrollOrdenados(self, jugador1):
        # Si ambos jugadores se han ido por ambos lados de los dos bordes
#         if (jugadorIzq.rect.left<MINIMO_X_JUGADOR) and (jugadorDcha.rect.right>MAXIMO_X_JUGADOR):

            # ocamos al jugador que esté a la izquierda a la izquierda de todo
#             jugadorIzq.establecerPosicion((self.scrollx+MINIMO_X_JUGADOR, jugadorIzq.posicion[1]))
            # ocamos al jugador que esté a la derecha a la derecha de todo
#             jugadorDcha.establecerPosicion((self.scrollx+MAXIMO_X_JUGADOR-jugadorDcha.rect.width, jugadorDcha.posicion[1]))

#             return False; # No se ha actualizado el scroll

        # Si el jugador de la izquierda se encuentra más allá del borde izquierdo
        if (jugador1.rect.left<MINIMO_X_JUGADOR):
            desplazamiento = MINIMO_X_JUGADOR - jugador1.rect.left

            # Si el escenario ya está a la izquierda del todo, no lo movemos mas
            if self.scrollx <= 0:
                self.scrollx = 0

                # En su lugar, colocamos al jugador que esté más a la izquierda a la izquierda de todo
                jugador1.establecerPosicion((MINIMO_X_JUGADOR, jugador1.posicion[1]))

                return False; # No se ha actualizado el scroll

            # Si no, es posible que el jugador de la derecha no se pueda desplazar
            #  tantos pixeles a la derecha por estar muy cerca del borde derecho
            elif ((MAXIMO_X_JUGADOR-jugador1.rect.right)<desplazamiento):

                # En este caso, ponemos el jugador de la izquierda en el lado izquierdo
                jugador1.establecerPosicion((jugador1.posicion[0]+desplazamiento, jugador1.posicion[1]))

                return False; # No se ha actualizado el scroll

            # Si se puede hacer scroll a la izquierda
            else:
                # Calculamos el nivel de scroll actual: el anterior - desplazamiento
                #  (desplazamos a la izquierda)
                self.scrollx = self.scrollx - desplazamiento;

                return True; # Se ha actualizado el scroll

        # Si el jugador de la derecha se encuentra más allá del borde derecho
        if (jugador1.rect.right>MAXIMO_X_JUGADOR):

            # Se calcula cuantos pixeles esta fuera del borde
            desplazamiento = jugador1.rect.right - MAXIMO_X_JUGADOR

            # Si el escenario ya está a la derecha del todo, no lo movemos mas
            if self.scrollx + ANCHO_PANTALLA >= self.decorado.rect.right:
                self.scrollx = self.decorado.rect.right - ANCHO_PANTALLA

                # En su lugar, colocamos al jugador que esté más a la derecha a la derecha de todo
                jugador1.establecerPosicion((self.scrollx+MAXIMO_X_JUGADOR-jugador1.rect.width, jugador1.posicion[1]))

                return False; # No se ha actualizado el scroll

            # Si no, es posible que el jugador de la izquierda no se pueda desplazar
            #  tantos pixeles a la izquierda por estar muy cerca del borde izquierdo
            elif ((jugador1.rect.left-MINIMO_X_JUGADOR)<desplazamiento):

                # En este caso, ponemos el jugador de la derecha en el lado derecho
                jugador1.establecerPosicion((jugador1.posicion[0]-desplazamiento, jugador1.posicion[1]))

                return False; # No se ha actualizado el scroll

            # Si se puede hacer scroll a la derecha
            else:

                # Calculamos el nivel de scroll actual: el anterior + desplazamiento
                #  (desplazamos a la derecha)
                self.scrollx = self.scrollx + desplazamiento;

                return True; # Se ha actualizado el scroll

        # Si ambos jugadores están entre los dos límites de la pantalla, no se hace nada
        return False;


    def actualizarScroll(self, jugador1):
        # Se ordenan los jugadores según el eje x, y se mira si hay que actualizar el scroll
        #  if (jugador1.posicion[0]<jugador1.posicion[0]):
        #     cambioScroll = self.actualizarScrollOrdenados(jugador1, jugador1)
        # else:
        cambioScroll = self.actualizarScrollOrdenados(jugador1)

        # Si se cambio el scroll, se desplazan todos los Sprites y el decorado
        if cambioScroll:
            # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
            for sprite in iter(self.grupoSprites):
                sprite.establecerPosicionPantalla((self.scrollx, 0))

            # Ademas, actualizamos el decorado para que se muestre una parte distinta
            self.decorado.update(self.scrollx)
            self.fondo.update(self.scrollx)


    # Se actualiza el decorado, realizando las siguientes acciones:
    #  Se indica para los personajes no jugadores qué movimiento desean realizar según su IA
    #  Se mueven los sprites dinámicos, todos a la vez
    #  Se comprueba si hay colision entre algun jugador y algun enemigo
    #  Se comprueba si algún jugador ha salido de la pantalla, y se actualiza el scroll en consecuencia
    #     Actualizar el scroll implica tener que desplazar todos los sprites por pantalla
    #  Se actualiza la posicion del sol y el color del cielo
    # Ademas, devuelve si se debe parar o no la ejecucion del juego
    def update(self, tiempo):

        # Primero, se indican las acciones que van a hacer los enemigos segun como esten los jugadores
        for enemigo in iter(self.grupoEnemigos):
            enemigo.mover_cpu(self.jugador1)
        for bala in iter(self.grupoProyectiles):
            bala.mover_cpu(self.jugador1)
        for bala in iter(self.grupoProyectilesEnemigo):
            bala.mover_cpu(self.jugador1)
        # Esta operación es aplicable también a cualquier Sprite que tenga algún tipo de IA
        # En el caso de los jugadores, esto ya se ha realizado

        # Actualizamos los Sprites dinamicos
        # De esta forma, se simula que cambian todos a la vez
        # Esta operación de update ya comprueba que los movimientos sean correctos
        #  y, si lo son, realiza el movimiento de los Sprites
        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)
        # Dentro del update ya se comprueba que todos los movimientos son válidos
        #  (que no choque con paredes, etc.)

        # Los Sprites que no se mueven no hace falta actualizarlos,
        #  si se actualiza el scroll, sus posiciones en pantalla se actualizan más abajo
        # En cambio, sí haría falta actualizar los Sprites que no se mueven pero que tienen que
        #  mostrar alguna animación

        # Comprobamos si hay colision entre algun jugador y algun enemigo
        # Se comprueba la colision entre ambos grupos
        # Si la hay, indicamos que se ha finalizado la fase
        #if pygame.sprite.groupcollide(self.grupoJugadores, self.grupoEnemigos, False, False)!={}:
            #return True
        coll=pygame.sprite.groupcollide(self.grupoEnemigos, self.grupoProyectiles, False, True)
        if coll!={}:
            for cosa in coll:
                cosa.vida-=1
                cosa.recibir_dano()
                if cosa.vida<0 :
                	cosa.sonidomuerte.play()
                	cosa.kill()
        coll=pygame.sprite.groupcollide(self.grupoPowerUps, self.grupoJugadores, True, False)
        if coll!={}:
            for up in coll:
                up.efecto(self.jugador1)
                up.sonido.play()
        coll=pygame.sprite.groupcollide(self.grupoJugadores, self.grupoFinFase, True, False)
        if coll!={}:
            self.director.salirEscena()
        coll=pygame.sprite.groupcollide(self.grupoJugadores, self.grupoProyectilesEnemigo, False, True)
        if coll!={}:
            lhud=self.grupoHud.sprites()
            if len(lhud)==0:
                #APILAR CONTINUE
                self.director.salirEscena()
            else:
                lhud[len(lhud)-1].kill()
            # self.jugador2.vida-=1
            #if self.jugador2.vida<0 :
            #    return True
#        coll=pygame.sprite.groupcollide( self.grupoProyectiles,self.grupoEnemigos, False, False)
#        if coll!={}:
#            for cosa in coll:
#                cosa.vida-=1
#                if cosa.vida<=0 :
#                    cosa.kill()
        # Actualizamos el scroll
        self.actualizarScroll(self.jugador1)

        # Actualizamos el fondo:
        #  la posicion del sol y el color del cielo
        #self.fondo.update(tiempo)

        # No se debe parar la ejecucion
        return False


    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.fondo.dibujar(pantalla)
        # Después el decorado
        self.decorado.dibujar(pantalla)
        # Luego los Sprites
        self.grupoSprites.draw(pantalla)


    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_c, K_v)
        # self.jugador2.mover(teclasPulsadas, K_w,  K_s,    K_a,    K_d,K_e)
        # No se sale del programa
        return False

# -------------------------------------------------
# Clase Plataforma

#class Plataforma(pygame.sprite.Sprite):
class Plataforma(MiSprite):
    def __init__(self,rectangulo):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = pygame.Surface((0, 0))


# -------------------------------------------------
# Clase Cielo

class Cielo:
    def __init__(self):
       pass
    def update(self, tiempo):
        pass

    def dibujar(self,pantalla):
        pass


# -------------------------------------------------
# Clase Decorado

class Decorado:
    def __init__(self,file,x,y,scrolldelay):
        self.imagen = GestorRecursos.CargarImagen(file, -1)
        self.imagen = pygame.transform.scale(self.imagen, (x, y))
        self.scrolldelay=scrolldelay
        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA
        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx*self.scrolldelay
        

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)
# -------------------------------------------------
# Clase Cutscene   
class Cutscene(Fase):
    def __init__(self, director,limagenes):

        self.delay = pygame.time.get_ticks()
        Escena.__init__(self, director)
        self.image = Image(director,limagenes)
        self.init=False
    def update(self, tiempo):
        self.image.update(tiempo)
        
    def dibujar(self, pantalla):
        self.image.dibujar(pantalla)
        if self.init==False:
            self.delay = pygame.time.get_ticks()
            self.init=True


    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        if teclasPulsadas[K_c]:
            if(pygame.time.get_ticks()-self.delay)>1000 and self.init==True:
                #print ('PULSADO',self,self.image.count,pygame.time.get_ticks()-self.delay)
                self.delay = pygame.time.get_ticks()
                self.image.advance()

# -------------------------------------------------
# Clase Image

class Image:
    def __init__(self,director,limagenes):
        self.imagen = GestorRecursos.CargarImagen(limagenes[0], -1)
        self.imagen = pygame.transform.scale(self.imagen, (800, 600))
        self.count = 1
        self.director = director
        self.limagenes=limagenes
        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def change(self, img):
        self.imagen = GestorRecursos.CargarImagen(img, -1)

    def advance(self):
        if self.count<len(self.limagenes):
            self.change(self.limagenes[self.count])
            self.count+=1
        else:
            self.director.salirEscena()
        

    def update(self, scrollx):
        self.rectSubimagen.left = 0

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)

