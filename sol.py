import pygame


class Sol(pygame.sprite.Sprite):

	def __init__(self, image):

		super().__init__()
		self.rect = pygame.Rect(0,470,1100,170)
		self.image = image

	def afficher(self, surface):

		surface.blit(self.image, self.rect)

		#pygame.draw.rect(surface, (0,255,0), self.rect)