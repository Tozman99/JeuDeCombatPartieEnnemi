import pygame
import sys, time
from pygame.sprite import Group
from joueur import Joueur
from sol import Sol
from projectiles import Projectile, Slash
from plateforme import Plateforme
from enemie import Enemie



class Jeu:

	def __init__(self):

		self.ecran = pygame.display.set_mode((1100, 600))
		pygame.display.set_caption('Jeu De Combat')
		self.jeu_encours = True
		self.joueur_x, self.joueur_y = 600, 100
		self.taille = [32, 64]
		self.joueur_vitesse_x = 0
		self.joueur = Joueur(self.joueur_x, self.joueur_y, self.taille)
		self.enemie_x, self.enemie_y = 100, 400
		self.enemie_taille = [88, 60]
		self.image_enemie = pygame.image.load('knight.png')
		self.enemie = Enemie(self.enemie_x, self.enemie_y, self.enemie_taille)
		self.image_arriere_plan = pygame.image.load('PC Computer - RPG Maker VX Ace - Battle Background Overlays 33.png')
		self.arriere_plan_rect = [34, 34, 574, 214]
		self.image_ciel_bleu = self.image_arriere_plan.subsurface(self.arriere_plan_rect)
		self.image_ciel_bleu = pygame.transform.scale(self.image_ciel_bleu, (1100, 600))
		self.image_sol_plat = pygame.image.load('Game Boy Advance - Sonic Advance - Background Elements 1.gif')
		self.image_sol_rect = [542, 3693, 373, 117]
		self.image_sol = self.image_sol_plat.subsurface(self.image_sol_rect)
		self.image_sol = pygame.transform.scale(self.image_sol, (1100, 170))
		self.image_plat_rect = [535, 3689, 379, 123]
		self.image_plat = self.image_sol_plat.subsurface(self.image_plat_rect)
		self.image_plat = pygame.transform.scale(self.image_plat, (300, 50))
		self.sol = Sol(self.image_sol)
		self.gravite = (0, 10)
		self.resistance = (0, 0)
		self.rect = pygame.Rect(0, 0, 1100, 600)
		self.collision_sol = False
		self.horloge = pygame.time.Clock()
		self.fps = 30
		self.projectile_groupe = Group()
		self.t1, self.t2 = 0, 0
		self.delta_temps = 0
		self.image_joueur = pygame.image.load('WonderSwan WSC - RockmanEXE WS - MegaManEXE Heat Style.png')
		self.image_joueur_rect = pygame.Rect(124, 453, 8, 8)
		self.image_boule_de_feu = self.image_joueur.subsurface(self.image_joueur_rect)
		self.plateforme_groupe = Group()
		self.plateforme_liste_rect = [
			pygame.Rect(0, 300, 300, 50), pygame.Rect(800, 300, 300, 50),
			pygame.Rect(400, 150, 300, 50)
		]
		self.slash_groupe = Group()
		self.slash_image_rect = pygame.Rect(108, 232, 24, 43)
		self.image_slash = self.image_enemie.subsurface(self.slash_image_rect)
		self.image_slash = pygame.transform.scale(self.image_slash, (30, 30))

	def boucle_principale(self):
		"""
		Boucle principale du jeu

		"""
		dictionnaire_vide_joueur = {}
		dictionnaire_images_joueur = self.joueur.convertir_rect_surface(self.image_joueur, dictionnaire_vide_joueur)
		dictionnaire_vide_enemie = {}
		dictionnaire_images_enemie = self.enemie.image_liste(self.image_enemie, dictionnaire_vide_enemie)

		while self.jeu_encours:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RIGHT:
						self.joueur_vitesse_x = 10
						self.joueur.direction = 1
						self.joueur.etat = 'bouger'

					if event.key == pygame.K_LEFT:
						self.joueur_vitesse_x = -10
						self.joueur.direction = -1
						self.joueur.etat = 'bouger'


					if event.key == pygame.K_UP:
						self.joueur.a_sauter = True
						self.joueur.nombre_de_saut += 1

					if event.key == pygame.K_p:
						self.t1 = time.time()
						self.joueur.etat = 'attaque'

					if event.key == pygame.K_e:
						self.enemie.a_attaque = True
						self.enemie.etat = 'attaque'

				if event.type == pygame.KEYUP:
					if event.key == pygame.K_RIGHT:
						self.joueur_vitesse_x = 0
						self.joueur.etat = 'debout'

					if event.key == pygame.K_LEFT:

						self.joueur_vitesse_x = 0
						self.joueur.etat = 'debout'


					if event.key == pygame.K_p:
						self.t2 = time.time()
						self.joueur.a_tire = True
						self.joueur.etat = 'debout'

					if event.key == pygame.K_e:
						self.enemie.etat = 'vivant'



			if self.sol.rect.colliderect(self.joueur.rect):
				self.resistance = (0, -10)
				self.collision_sol = True
				self.joueur.nombre_de_saut = 0

			else:
				self.resistance = (0, 0)

			if self.joueur.a_sauter and self.collision_sol:
				if self.joueur.nombre_de_saut < 2:
					self.joueur.sauter()

			if self.joueur.a_tire:
				if len(self.projectile_groupe) < self.joueur.tir_autorise and self.delta_temps > 0.05:
					projectile = Projectile(self.joueur.rect.x + 20, self.joueur.rect.y - 5, [10, 10], self.joueur.direction,
					                            self.image_boule_de_feu)
					self.projectile_groupe.add(projectile)
					self.joueur.a_tire = False

			if self.enemie.a_attaque:

				if len(self.slash_groupe) < self.enemie.tir_autorise:
					slash = Slash(self.enemie.rect.x + 20, self.enemie.rect.y - 5, [30, 30], self.image_slash)
					self.slash_groupe.add(slash)
					self.enemie.a_attaque = False


			for projectile in self.projectile_groupe:
				projectile.mouvement(50)
				if projectile.rect.right >= self.rect.right or projectile.rect.left <= self.rect.left:
					self.projectile_groupe.remove(projectile)

			for slash in self.slash_groupe:
				slash.mouvement(50)
				if slash.rect.right >= self.rect.right or slash.rect.left <= self.rect.left:
					self.slash_groupe.remove(slash)


			for rectangle in self.plateforme_liste_rect:
				plateforme = Plateforme(rectangle, self.image_plat)
				self.plateforme_groupe.add(plateforme)
				if self.joueur.rect.midbottom[1] // 10 * 10 == plateforme.rect.top \
						and self.joueur.rect.colliderect(rectangle):
					self.resistance = (0, -10)
					self.joueur.nombre_de_saut = 0

			self.delta_temps = self.t2 - self.t1
			self.joueur.mouvement(self.joueur_vitesse_x)
			self.gravite_jeu()
			self.joueur.rect.clamp_ip(self.rect)
			self.ecran.fill((255, 255, 255))
			self.ecran.blit(self.image_ciel_bleu, self.rect)
			self.joueur.afficher(self.ecran, dictionnaire_images_joueur)
			self.enemie.afficher(self.ecran, dictionnaire_images_enemie)
			self.sol.afficher(self.ecran)
			for plateforme in self.plateforme_groupe:
				plateforme.afficher(self.ecran)

			for slash in self.slash_groupe:
				slash.afficher(self.ecran)
			for projectile in self.projectile_groupe:
				projectile.afficher(self.ecran, self.delta_temps)
			pygame.draw.rect(self.ecran, (255, 0, 0), self.rect, 1)
			self.horloge.tick(self.fps)
			pygame.display.flip()

	def gravite_jeu(self):
		"""
		Gére la gravité pour chaque élément
		"""

		self.joueur.rect.y += self.gravite[1] + self.resistance[1]


if __name__ == '__main__':
	pygame.init()
	Jeu().boucle_principale()
	pygame.quit()
