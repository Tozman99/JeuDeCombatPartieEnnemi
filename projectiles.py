import pygame


class Projectile(pygame.sprite.Sprite):

	def __init__(self, x, y , taille, direction, image):

		super().__init__()
		self.x = x
		self.y = y
		self.taille = taille
		self.direction = direction
		self.image = image
		self.rect = pygame.Rect(self.x, self.y, self.taille[0], self.taille[1])

	def afficher(self, surface, delta_temps):
		"""

		:param surface:
		:param delta_temps:
		Affiche l'image en fonction du delta_temps
		"""

		if delta_temps > 2:
			self.image = pygame.transform.scale(self.image, (30, 30))

		surface.blit(self.image, self.rect)

	def mouvement(self, vitesse):
		"""

		:param vitesse:
		Augmente la position en x du projectile
		"""

		self.rect.x += ( vitesse * self.direction)


class Slash(pygame.sprite.Sprite):

	def __init__(self, x, y, taille, image):

		super().__init__()
		self.x = x
		self.y = y
		self.taille = taille
		self.image = image
		self.rect = pygame.Rect(self.x, self.y, self.taille[0], self.taille[1])

	def afficher(self, surface):

		surface.blit(self.image, self.rect)

	def mouvement(self, vitesse):
		"""

		:param vitesse:
		Augmente la position en x du slash
		"""

		self.rect.x += vitesse

