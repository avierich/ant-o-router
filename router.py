import numpy as np
import pygame

class Ant : 

    def __init__(self, position, destination) :
        self.step_length = 15
        self.position = position
        self.destination = destination
        self.connected = False
        self.path = np.array([[position[0],position[1]]])
        self.color = (np.random.rand()*255,np.random.rand()*255,np.random.rand()*255)

    def march(self):
        self.path = np.append(self.path, [[self.path[-1][0]+(1.0 - 2*np.random.rand())*self.step_length,self.path[-1][1]+(1.0 - 2*np.random.rand())*self.step_length]], axis=0)

class Nest :

    def __init__(self, position, ants) :
        self.position = position
        self.connections = []
        self.ants = ants

    def addConnection(self, connectedNest) :
        self.connections.append(connectedNest)
        self.ants.append(Ant(self.position,connectedNest))



# Setup world
ants = []
nests = [Nest((100,100),ants),Nest((400,100),ants),Nest((100,400),ants),Nest((400,400),ants)]

# Connect pins (This is not a pretty way to acheive this)
nests[0].addConnection(nests[1])
nests[1].addConnection(nests[0])
nests[2].addConnection(nests[3])
nests[3].addConnection(nests[2])

pygame.init()
screen = pygame.display.set_mode((640,480))
skip_frames = 1

running = True
while running:
    pygame.time.wait(5)
    # Update everything
    for i in range(skip_frames):
        for ant in ants :
            ant.march()

    # Redraw
    screen.fill((0,0,0))
    for ant in ants :
        pygame.draw.lines(screen, ant.color, False, ant.path, 5)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


