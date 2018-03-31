from fase import *
class textToFaseFactory():
	def createFase(self, file,director):
		self.nuevafase=Fase(director)
		f=open(file,'r')
		linea=f.readline()
		while(linea!=''):
			cachos=linea.split('|')
			if cachos[0]=='j':
				self.readPlayer(cachos[1:])
			if cachos[0]=='d':
				self.readDecorado(cachos[1:])
			if cachos[0]=='e':
				self.readEnemigos(cachos[1:])
			if cachos[0]=='o':
				self.readObjetos(cachos[1:])
			if cachos[0]=='p':
				self.readPlataformas(cachos[1:])
			if cachos[0]=='f':
				self.readFondo(cachos[1:])
			if cachos[0]=='cp':#custcenes primero
				self.readCutscenePrimero(cachos[1:len(cachos)-1])
			if cachos[0]=='cu':#cutscenes despues
				self.readCutsceneUltimo(cachos[1:len(cachos)-1])
			if cachos[0]=='ef':
				self.readEndFase(cachos[1:])
			linea=f.readline()
		return self.nuevafase
	def readEndFase(self,listaValores):
		final=EndFase()
		final.establecerPosicion((int(listaValores[0]),int(listaValores[1])))
		self.nuevafase.setFin(final)
	def readCutscenePrimero(self,listaValores):
		self.nuevafase.cutscenesprimero=(Cutscene(self.nuevafase.director,listaValores))

	def readCutsceneUltimo(self,listaValores):
		self.nuevafase.cutscenesultimo=(Cutscene(self.nuevafase.director,listaValores))
	def readFondo(self,listaValores):
		self.nuevafase.setFondo(listaValores[0],int(listaValores[1]),int(listaValores[2]),float(listaValores[3]))
	def readDecorado(self,listaValores):
		self.nuevafase.setDecorado(listaValores[0],int(listaValores[1]),int(listaValores[2]),float(listaValores[3]))
	def readPlayer(self,listaValores):
		self.nuevafase.setJugador(int(listaValores[0]),int(listaValores[1]))

	def readEnemigos(self,listaValores):
		i=0
		for i in range(0,len(listaValores)):
			subcachos=listaValores[i].split('-')
			if (int(subcachos[0])==1):
				enemigo1 = Sniper()
			if (int(subcachos[0])==2):
				enemigo1 = mob1()
			if (int(subcachos[0])==3):
				enemigo1 = Sniper_Dispara(self.nuevafase.grupoProyectilesEnemigo)
				enemigo1.setgrupoproyEnem(self.nuevafase.grupoSpritesDinamicos,self.nuevafase.grupoSprites)
			if (int(subcachos[0])==4):
				enemigo1 = Tirador_Arriba(self.nuevafase.grupoProyectilesEnemigo)
				enemigo1.setgrupoproyEnem(self.nuevafase.grupoSpritesDinamicos,self.nuevafase.grupoSprites)
			if (int(subcachos[0])==5):
				enemigo1 = Tirador_Abajo(self.nuevafase.grupoProyectilesEnemigo)
				enemigo1.setgrupoproyEnem(self.nuevafase.grupoSpritesDinamicos,self.nuevafase.grupoSprites)
			if (int(subcachos[0])==6):
				enemigo1 = Boss1(self.nuevafase.grupoProyectilesEnemigo,self.nuevafase.director)
				enemigo1.setgrupoproyEnem(self.nuevafase.grupoSpritesDinamicos,self.nuevafase.grupoSprites)
			enemigo1.establecerPosicion((int(subcachos[1]),int( subcachos[2])))
			self.nuevafase.addEnemigo(enemigo1)
	def readObjetos(self,listaValores):
		i=0
		for i in range(0,len(listaValores)):
			subcachos=listaValores[i].split('-')
			if (int(subcachos[0])==1):
				powerup1 = powerupSpeed()
			if (int(subcachos[0])==2):
				powerup1 = powerupBotiquin()
        	powerup1.establecerPosicion((int(subcachos[1]), int(subcachos[2])))
        	self.nuevafase.addPowerUp(powerup1)
	
	def readPlataformas(self,listaValores):
		i=0
		for i in range(0,len(listaValores)):
			subcachos=listaValores[i].split('-')
			plataformaSuelo = Plataforma(pygame.Rect(int(subcachos[0]) ,int(subcachos[1]), int(subcachos[2]),int( subcachos[3])))
			self.nuevafase.addPlataforma(plataformaSuelo)
