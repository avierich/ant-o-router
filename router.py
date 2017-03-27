import numpy as np
import pygame
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
GRID_WIDTH = 100
GRID_HEIGHT = 70
RECT_WIDTH = SCREEN_WIDTH / GRID_WIDTH
RECT_HEIGHT = SCREEN_HEIGHT / GRID_HEIGHT

COLORS = np.random.randint(155, size = (1000, 3)) + 100


class Ant :

    def __init__(self, world, position, species, destination) :
        self.world = world
        self.position = position
        self.species = species
        self.dead = False
        self.color = (COLORS[species][0],COLORS[species][1],COLORS[species][2])
        self.genes = np.random.randint(4294967295)
        self.random = np.random.RandomState(self.genes)
        self.destination = destination
        self.success = False

    def kill(self) :
        for row in self.world :
            for tile in row :
                if self in tile :
                    tile.remove(self)
        self.dead = True

    def moveTo(self, coord) :
        self.position = coord

        if len(self.world[coord[0]][coord[1]]) == 0 :
            self.world[self.position[0]][self.position[1]].append(self)
        else :
            otherAnt = False
            for ant in world[coord[0]][coord[1]] :
                if ant.species != self.species :
                    otherAnt = True

            if otherAnt :
                self.world[coord[0]][coord[1]][0].kill()
                self.kill()

    def march(self) :
        direction = np.array(self.destination.position) - np.array(self.position)
        direction = direction/np.sqrt(np.sum(direction**2))

        if self.random.rand() < 0.5 :
            # move in the x direction
            if self.random.rand() < 0.5 and self.position[0] > 0 : # move to the left
                self.moveTo((self.position[0] - 1, self.position[1]))
            elif self.position[0] < GRID_WIDTH - 1 :
                self.moveTo((self.position[0] + 1,  self.position[1]))
        else :
            # move in the y direction
            if self.random.rand() < 0.5 and self.position[1] > 0 :
                self.moveTo((self.position[0], self.position[1] - 1))
            elif self.position[1] < GRID_HEIGHT - 1 :
                self.moveTo((self.position[0], self.position[1] + 1))


class Nest :
    def __init__(self, world, position, species) :
        self.world = world
        self.position = position
        self.connections = []
        self.ants = []
        self.species = species
        self.numAnts = 100

    def newAnt(self, ant = 'null') :
        self.ants.append(Ant(self.world, self.position, self.species, self.connections[0]))
        if ant != 'null' :
            self.ants[-1].random = np.random.RandomState(ant.genes)
            self.ants[-1].genes = ant.genes

    def addConnection(self, connectedNest) :
        self.connections.append(connectedNest)
        for i in range(1): 
            self.newAnt()

    def marchAnts(self) :
        for ant in self.ants :
            if ant.dead :
                self.ants.remove(ant)
                self.newAnt()
            elif not ant.success and ant.position == ant.destination.position :
                print('successful ant!! '+str(ant.species) +'  ' + str(ant.genes))
                ant.success = True
                for i in range(5) :
                    if len(self.ants) <= self.numAnts :
                        self.newAnt(ant = ant)
            elif not ant.success :
                ant.march()

# Setting everything up and run

world = []
for i in range(GRID_WIDTH) :
    col = []
    for j in range(GRID_HEIGHT) :
        col.append([])
    world.append(col)


# Add some pins
#world[20][35].append(1)
#world[80][35].append(1)

nests = []
nests.append(Nest(world, (20, 20), 0))
nests.append(Nest(world, (80, 20), 0))
nests.append(Nest(world, (20, 50), 1))
nests.append(Nest(world, (80, 50), 1))

nests[0].addConnection(nests[1])
nests[1].addConnection(nests[0])
nests[2].addConnection(nests[3])
nests[3].addConnection(nests[2])


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
skip_frames = 1000
frame = 0

running = True
while running:
    frame += 1
    # Update everything
    for nest in nests :
        nest.marchAnts()

    # Redraw
    if frame % skip_frames == 0 : # skip drawing frames
        pygame.time.wait(1)
        pygame.display.set_caption(str(frame))
        screen.fill((0,0,0))
        for x in range(len(world)) :
            for y in range(len(world[0])) :
                if len(world[x][y]) > 0 and isinstance(world[x][y][0], Ant):
                    pygame.draw.rect(screen, world[x][y][0].color, (x*RECT_WIDTH, y*RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT), 0)
                elif 1 in world[x][y] :
                    pygame.draw.rect(screen, (255, 0, 0), (x*RECT_WIDTH, y*RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT), 0)

        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


