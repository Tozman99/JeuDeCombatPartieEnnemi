import pygame


class Plateforme(pygame.sprite.Sprite):

	def __init__(self, rect, image):

		super().__init__()
		self.rect = rect
		self.image = image

	def afficher(self, surface):

		#pygame.draw.rect(surface, (0, 255, 0), self.rect)
		surface.blit(self.image, self.rect)