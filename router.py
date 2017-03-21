import numpy as np
import pygame

class Ant : 

    def __init__(self, position, destination) :
        self.step_length = 10
        self.lifeTime = 1000*np.random.rand()
        self.position = position
        self.destination = destination
        self.connected = False
        self.path = np.array([[position[0],position[1]]])
        self.color = (np.random.rand()*255,np.random.rand()*255,np.random.rand()*255)

    def march(self):
        if not self.connected :
            # Determine if I can connect to the pin with a single step
            destDist = np.sqrt((self.path[-1][0] - self.destination.position[0])**2+(self.path[-1][1] - self.destination.position[1])**2)
            if destDist <= self.step_length :
                nextPos = self.destination.position
                self.connected = True
            else :
                nextPos = [self.path[-1][0]+(1.0 - 2*np.random.rand())*self.step_length,self.path[-1][1]+(1.0 - 2*np.random.rand())*self.step_length]
            self.path = np.append(self.path, [nextPos], axis=0)

class Nest :

    def __init__(self, position, ants) :
        self.position = position
        self.connections = []
        self.ants = ants
        self.myAnts = []

    def addConnection(self, connectedNest) :
        self.connections.append(connectedNest)
        self.ants.append(Ant(self.position,connectedNest))
        self.myAnts.append(self.ants[-1])

    def march(self) :
        for ant in self.myAnts :
            ant.lifeTime -= 1
            # if ant dies add a new one
            if ant.lifeTime <= 0 and not ant.connected :
                # First make a new one
                self.ants.append(Ant(self.position,ant.destination))
                self.myAnts.append(self.ants[-1])
                # Remove dead one
                self.ants.remove(ant)
                self.myAnts.remove(ant)


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
skip_frames = 1000
frame = 0

running = True
while running:
    pygame.time.wait(5)
    # Update everything
    for i in range(skip_frames):
        frame += 1
        for nest in nests :
            nest.march()
        for ant in ants :
            ant.march()

    # Redraw
    pygame.display.set_caption(str(frame))
    screen.fill((0,0,0))
    for ant in ants :
        pygame.draw.lines(screen, ant.color, False, ant.path, 5)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


