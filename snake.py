import pygame, sys
from pygame.math import Vector2
class FRUIT:
    def __init__(self):
        self.x = 5
        self.y = 4
        self.pos = Vector2(self.x,self.y)
    
    
pygame.init()
screen = pygame.display.set_mode((400,500))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.fill((175,215,70))
    pygame.display.update()
    clock.tick(60)