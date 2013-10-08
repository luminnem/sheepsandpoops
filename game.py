import pygame as py
from pygame.locals import *
from random import randrange


class Wheat(object):
	def __init__(self, pos, img):
		self.x , self.y = pos
		self.img = img
	def render(self, screen):
		screen.blit(self.img, (self.x, self.y))
		
		
class Player(object):
	def __init__(self):
		self.img = [py.image.load("sheep.png"), py.image.load("sheep_1.png")]
		self.poop = py.image.load("poop.png")
		self.sheeps = [Sheep(self.img, self.poop)]
		self.wheat = []
		self.poops = []
		self.wimg = py.image.load("wheat.png")
		self.allowc = True
		self.nw = 5
		self.ns = 0
		self.d = 1 * 1000 * 60
		self.ps = 0
		self.tp = 0
		
	def render(self, screen):
		for sheep in self.sheeps:
			sheep.render(screen)
			sheep.update(self.wheat, self.poops)
			if sheep.hungry <= 0:
				self.sheeps.remove(sheep)
		for wheat in self.wheat:
			wheat.render(screen)
		for p in self.poops:
			p.render(screen)
			
	def update(self):
		mouse = py.mouse.get_pressed()
		mx, my = py.mouse.get_pos()
		if mouse[0] == 1:
			for sh in self.poops:
				if mx > sh.x + 11 or my > sh.y + 11 or mx + 1 < sh.x or my + 1 < sh.y:
					pass
				else:
					self.poops.remove(sh)
					self.ps += 1
					self.allowc = False
					self.tp += 1
							
			if self.allowc and self.nw > 0:
				self.wheat.append(Wheat(py.mouse.get_pos(), self.wimg))
				self.allowc = False
				self.nw -= 1
				
			if self.ps / 2 >= 1:
				self.nw += (self.ps / 2)*2
				self.ps = 0
		else:
			self.allowc = True
		self.spawn()
			
	def spawn(self):
		if py.time.get_ticks() - self.ns > self.d:
			self.ns = py.time.get_ticks()
			self.sheeps.append(Sheep(self.img, self.poop))
			
			

class Poop(object):
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.img = img
	def render(self, screen):
		screen.blit(self.img, (self.x, self.y))
		
class Sheep(object):
	def __init__(self, s, p):
		self.x, self.y = 0, 0
		self.vx, self.vy = 0, 0
		self.img = s
		self.poop = p
		self.frame = 0
		self.delay = 250
		self.time = 0
		self.poops = []
		self.hungry = 9
		self.ht = 0
		self.dx, self.dy = 0, 0
		self.od = True
		self.speed = 1
		self.pt = 0
		
	def render(self, screen):
		screen.blit(self.img[self.frame], (self.x, self.y))
		for p in self.poops:
			p.render(screen)
		
	def update(self, wheat, poops):
		self.animation()
		self.hungryt()
		self.ai(wheat, poops)
		self.x += self.vx
		self.y += self.vy
		if self.x < 0:
			self.x = 0
		elif self.x > 740:
			self.x = 740
		if self.y < 0:
			self.y = 0
		elif self.y > 550:
			self.y = 550
		
	def ai(self, wheat, poops):
		self.pooptimer(poops)
		
		if self.hungry < 10:
			for w in wheat:
				self.dx = w.x
				self.dy = w.y
				self.od = False
			
		if self.od and len(wheat) == 0:
			self.dx = randrange(0, 740)
			self.dy = randrange(0, 550)
			self.od = False
			
			
		if not self.od:
			if self.x < self.dx:
				self.vx = self.speed
			elif self.x > self.dx:
				self.vx = -self.speed
				
			else:
				self.vx = 0
				
			if self.y < self.dy:
				self.vy = self.speed
			elif self.y > self.dy:
				self.vy = -self.speed
			else:
				self.vy = 0
				
			if self.x == self.dx and self.y == self.dy:
				if self.hungry <= 10 and len(wheat) > 0:
					self.hungry += 3
					del wheat[-1]
				self.od = True
		
	def pooptimer(self, poops):
		if py.time.get_ticks() - self.pt > 10000:
			self.pt = py.time.get_ticks()
			poops.append(Poop(self.x, self.y, self.poop))
			
	def hungryt(self):
		if py.time.get_ticks() - self.ht > 5000:
			self.ht = py.time.get_ticks()
			self.hungry -= 1
			
	def animation(self):
		if py.time.get_ticks() - self.time > self.delay:
			self.time = py.time.get_ticks()
			self.frame+=1
			if self.frame > 1:
				self.frame = 0

def main():
	py.init()
	screen = py.display.set_mode((800, 600))
	py.display.set_caption("Poop mania")
	
	exit = False
	clear = (75, 188, 75)
	FPS = py.time.Clock()
	font = py.font.Font("a song for jennifer.ttf", 20)
	
	
	player = Player()
	while not exit:
		screen.fill(clear)
		for event in py.event.get():
			if event.type == QUIT:
				exit = True
				
		FPS.tick(60)
		if len(player.sheeps) > 0:
			score = font.render("Total poops: "+str(player.tp), 1, (255, 255, 255))
			wheat = font.render("Wheat: "+str(player.nw)+" / "+"Poops: "+str(player.ps), 1, (255, 255, 255))
			sheeps = font.render("Sheeps: "+str(len(player.sheeps))+"/ 'til next sheep "+str(60-(py.time.get_ticks()-player.ns)/1000), 1, (255, 255, 255))
			screen.blit(score, (20, 20))
			screen.blit(wheat, (20, 40))
			screen.blit(sheeps, (20, 60))
			player.update()
			player.render(screen)
		else:
			end = font.render("All your sheeps have bead.", 1, (255, 255, 255))
			end_2 = font.render("You got "+str(player.tp)+" poops.", 1, (255, 255, 255))
			end_3 = font.render("Please close the window and re-open it to play again.", 1, (255, 255, 255))
			screen.blit(end, (200, 200))
			screen.blit(end_2, (200, 220))
			screen.blit(end_3, (200, 240))
		py.display.update()
	return 0
	
if __name__ == "__main__":
	main()
