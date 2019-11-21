import pygame


class Joueur(pygame.sprite.Sprite):

	def __init__(self, x, y, taille):

		super().__init__()
		self.x = x
		self.y = y
		self.taille = taille
		self.rect = pygame.Rect(self.x, self.y, self.taille[0], self.taille[1])
		self.saut = 0
		self.saut_montee = 0
		self.saut_descente = 5
		self.nombre_de_saut = 0
		self.a_sauter = False
		self.a_tire = False
		self.tir_autorise = 1
		self.direction = 2
		self.joueur_debout = [pygame.Rect(119, 0, 16, 33)]
		self.joueur_bouge = [
			pygame.Rect(114, 80, 27, 33),
			pygame.Rect(154, 81, 25, 30),
			pygame.Rect(196, 82, 21, 31),
			pygame.Rect(235, 81, 24, 33),
			pygame.Rect(273, 81, 28, 32),
			pygame.Rect(313, 81, 25, 31),
			pygame.Rect(359, 80, 18, 33),

		]
		self.joueur_mort = [
			pygame.Rect(7, 185, 32, 31),
			pygame.Rect(141, 246, 23, 26),
			pygame.Rect(171, 243, 17, 31),
			pygame.Rect(190, 239, 29, 40)
		]
		self.joueur_attaque = [
			pygame.Rect(118, 41, 22, 32),
			pygame.Rect(155, 41, 23, 32),
			pygame.Rect(196, 41, 23, 31),
			pygame.Rect(236, 41, 22, 32),
			pygame.Rect(268, 40, 38, 32),
			pygame.Rect(268, 40, 38, 32),
			pygame.Rect(309, 41, 36, 32),
			pygame.Rect(349, 40, 35, 32),

		]
		self.etat = 'debout'
		self.index = 0


	def mouvement(self, vitesse):
		"""
		Crée le mouvement de droite à gauche
		:param vitesse:

		"""

		self.rect.x += vitesse

	def afficher(self, surface, dict):
		"""
		Affiche le joueur
		:param surface:

		"""
		self.index += 1

		if self.index >= len(dict[self.etat]):
			self.index = 0

		if self.etat == 'attaque' and self.index == 7:
			self.index = 6

		image = dict[self.etat][self.index]

		if self.direction == -1:
			image = pygame.transform.flip(image, True, False)

		surface.blit(image, self.rect)
		pygame.draw.rect(surface, (0, 255, 255), self.rect, 1)

	def sauter(self):
		"""
		Decrite la trajectoire du saut du joueur
		"""

		if self.a_sauter:

			if self.saut_montee >= 10:
				self.saut_descente -= 1
				self.saut = self.saut_descente

			else:

				self.saut_montee += 1
				self.saut = self.saut_montee

			if self.saut_descente < 0 :
				self.saut_montee = 0
				self.saut_descente = 5
				self.a_sauter = False

		self.rect.y = self.rect.y - (10 * (self.saut / 2))

	def convertir_rect_surface(self, image, dict):
		"""
		Convertir les rectangle en surface et les stockez dans un dict 

		:param image:
		:param dict:
		:return: dict
		"""

		for image_debout in self.joueur_debout:

			joueur_rectangle_supprime = self.joueur_debout.pop(0)
			image_joueur = image.subsurface(joueur_rectangle_supprime)
			image_joueur = pygame.transform.scale(image_joueur, (32, 64))
			self.joueur_debout.append(image_joueur)

		dict['debout'] = self.joueur_debout

		for image_mouvement in self.joueur_bouge:
			image_rect = self.joueur_bouge.pop(0)
			image_joueur = image.subsurface(image_rect)
			image_joueur = pygame.transform.scale(image_joueur, (32, 64))
			self.joueur_bouge.append(image_joueur)

		dict['bouger'] = self.joueur_bouge

		for image_attaque in self.joueur_attaque:
			rect_joueur = self.joueur_attaque.pop(0)
			image_joueur = image.subsurface(rect_joueur)
			image_joueur = pygame.transform.scale(image_joueur, (32, 64))
			self.joueur_attaque.append(image_joueur)

		dict['attaque'] = self.joueur_attaque

		for image_mort in self.joueur_mort:
			rect_joueur = self.joueur_mort.pop(0)
			image_joueur = image.subsurface(rect_joueur)
			image_joueur = pygame.transform.scale(image_joueur, (32, 64))
			self.joueur_mort.append(image_joueur)

		dict['mort'] = self.joueur_mort

		return dict