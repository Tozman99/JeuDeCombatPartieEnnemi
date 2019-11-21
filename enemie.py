import pygame

class Enemie(pygame.sprite.Sprite):

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
		self.a_attaque = False
		self.tir_autorise = 2
		self.direction = 2
		self.etat = 'vivant'
		self.index = 0
		self.enemy_vivant = [pygame.Rect(48, 4, 57, 43)]
		self.enemy_mort = [
			pygame.Rect(7, 185, 32, 31),
			pygame.Rect(141, 246, 23, 26),
			pygame.Rect(171, 243, 17, 31),
			pygame.Rect(190, 239, 29, 40)

		]
		self.enemy_attaque = [
			pygame.Rect(2, 129, 42, 47),
			pygame.Rect(53, 136, 34, 43),
			pygame.Rect(93, 102, 61, 73),
			pygame.Rect(162, 101, 60, 74),
			pygame.Rect(230, 102, 59, 72)
		]


	def afficher(self, surface, dict):

		self.index += 1

		if self.index >= len(dict[self.etat]):
			self.index = 0

		if self.etat == 'attaque' and self.index == 4:
			self.index = 3

		image = dict[self.etat][self.index]

		surface.blit(image, self.rect)
		pygame.draw.rect(surface, (0, 255, 255), self.rect, 1)



	def image_liste(self, image, dict):

			for image_debout in self.enemy_vivant:

				image_rect = self.enemy_vivant.pop(0)
				image_joueur = image.subsurface(image_rect)
				image_joueur = pygame.transform.scale(image_joueur, (88, 60))
				self.enemy_vivant.append(image_joueur)

			dict['vivant'] = self.enemy_vivant


			for image_attaque in self.enemy_attaque:
				rect_joueur = self.enemy_attaque.pop(0)
				image_joueur = image.subsurface(rect_joueur)
				image_joueur = pygame.transform.scale(image_joueur, (88, 60))
				self.enemy_attaque.append(image_joueur)

			dict['attaque'] = self.enemy_attaque


			return dict
