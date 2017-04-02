import numpy as np
import pygame
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_WIDTH = 8
GRID_HEIGHT = 8
RECT_WIDTH = SCREEN_WIDTH / GRID_WIDTH
RECT_HEIGHT = SCREEN_HEIGHT / GRID_HEIGHT

COLORS = np.random.randint(155, size = (1000, 3)) + 100

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class Ant :


    def __init__(self, world, position, species, destination) :
        self.world = world
        self.position = position
        self.species = species
        self.dead = False
        self.color = (COLORS[species][0],COLORS[species][1],COLORS[species][2])
        self.destination = destination
        self.success = False
        self.genes = self.findPath(position, destination)
        self.age = 0
        self.minLength = len(self.genes)

    def mutate(self, genes) :
        randA = np.random.randint(len(genes) + 1)
        randB = np.random.randint(len(genes) + 2)
        if np.random.rand() > 0.5 :
            if np.random.rand() > 0.5 :
                genes.insert(randA, EAST)
                genes.insert(randB, WEST)
            else :
                genes.insert(randA, NORTH)
                genes.insert(randB, SOUTH)
        elif len(self.genes) > self.minLength :
            if NORTH in self.genes and SOUTH in self.genes :
                self.genes.remove(NORTH)
                self.genes.remove(SOUTH)
            elif EAST in self.genes and WEST in self.genes :
                self.genes.remove(EAST)
                self.genes.remove(WEST)

        self.genes = genes

    def findPath(self, position, destination) :
        xDist = destination.position[0] - position[0]
        yDist = position[1] - destination.position[1]

        path = []

        for i in range(abs(xDist)) :
            if abs(xDist) - xDist == 0 : # xDist is positive
                path.append(EAST)
            else :
                path.append(WEST)
        for i in range(abs(yDist)) :
            if abs(yDist) - yDist == 0 : # yDist is positive
                path.append(NORTH)
            else :
                path.append(SOUTH)

        return path

    def kill(self) :
#        for row in self.world :
#            for tile in row :
#                if self in tile :
#                    tile.remove(self)

        position =  self.position
        #self.world[position[0]][position[1]].remove(self)
        for i in range(self.age-1, -1, -1) :
            self.world[position[0]][position[1]].remove(self)
            if self.genes[i] == NORTH :
                position = (position[0], position[1] + 1)
            elif self.genes[i] == EAST :
                position = (position[0] - 1, position[1])
            elif self.genes[i] == SOUTH :
                position = (position[0], position[1] - 1)
            elif self.genes[i] == WEST :
                position = (position[0] + 1, position[1])
            #if self in self.world[position[0]][position[1]] :

            
        self.dead = True

    def moveTo(self, coord) :
            
        # If the coord is going to be out of bounds
        if coord[0] >= GRID_WIDTH or coord[0] < 0 or coord[1] >= GRID_HEIGHT or  coord[1] < 0 :
            self.kill()
            return

        if len(self.world[coord[0]][coord[1]]) == 0 : # this is a valid place to move
            self.position = coord
            self.world[self.position[0]][self.position[1]].append(self)
        else :
            otherAnt = False
            for ant in world[coord[0]][coord[1]] :
                if ant.species != self.species :
                    otherAnt = True

            if otherAnt :
                self.world[coord[0]][coord[1]][0].kill()
                self.kill()
            else :
                self.position = coord
                self.world[self.position[0]][self.position[1]].append(self)

        self.age += 1

    def march(self) :
            nextMove = self.genes[self.age]

            if nextMove == NORTH :
                self.moveTo((self.position[0], self.position[1] - 1))
            elif nextMove == EAST :
                self.moveTo((self.position[0] + 1, self.position[1]))
            elif nextMove == SOUTH :
                self.moveTo((self.position[0], self.position[1] + 1))
            elif nextMove == WEST :
                self.moveTo((self.position[0] - 1, self.position[1]))


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
        #for i in range(1): 
         #   self.newAnt()

    def marchAnts(self) :
        for ant in self.ants :
            if ant.dead :
                self.ants.remove(ant)
                self.newAnt()
                self.ants[-1].mutate(ant.genes)
            elif not ant.success and ant.position == ant.destination.position :
                ant.success = True
#                for i in range(5) :
#                    if len(self.ants) <= self.numAnts :
#                        self.newAnt(ant = ant)
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
nests.append(Nest(world, (int(GRID_WIDTH / 4)-1,int(GRID_HEIGHT/2)), 0))
nests.append(Nest(world, (int(GRID_WIDTH *3/4), int(GRID_HEIGHT /2)), 0))
nests.append(Nest(world, (int(GRID_WIDTH /2), int(GRID_HEIGHT/4)), 1))
nests.append(Nest(world, (int(GRID_WIDTH/2), int(GRID_HEIGHT *3/4)), 1))

nests[0].addConnection(nests[1])
nests[1].addConnection(nests[0])
nests[2].addConnection(nests[3])
nests[3].addConnection(nests[2])

nests[0].newAnt()
nests[2].newAnt()


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
skip_frames = 10000
frame = 0

running = True
while running:
    frame += 1
    # Update everything
    for nest in nests :
        nest.marchAnts()

    # Redraw
    if frame % skip_frames == 0 : # skip drawing frames
        pygame.time.wait(0)
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


