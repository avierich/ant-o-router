import numpy as np
import pygame
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_WIDTH = 40
GRID_HEIGHT = 40
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
        self.age = 0
        self.coords = []
        self.direction = NORTH


    def kill(self) :
        for pos in self.coords :
            self.world[pos[0]][pos[1]].remove(self)

        self.dead = True

    def move(self, direction) :
        if direction == NORTH :
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == EAST :
            self.position = (self.position[0] + 1, self.position[1])
        elif direction == SOUTH :
            self.position = (self.position[0], self.position[1] + 1)
        elif direction == WEST :
            self.position = (self.position[0] - 1, self.position[1])

        self.direction = direction
        self.world[self.position[0]][self.position[1]].append(self)

    def otherAnt(self, coord) :
        return len(self.world[coord[0]][coord[1]]) > 0 and self.world[coord[0]][coord[1]][0].species != self.species

    def canMove(self, direction) :
        if direction == NORTH : 
            return self.direction != SOUTH and self.position[1] > 1 and not self.otherAnt((self.position[0], self.position[1] - 2)) and not self.otherAnt((self.position[0] - 1, self.position[1] - 2)) and not self.otherAnt((self.position[0] + 1, self.position[1] - 2))
        elif direction == EAST :
            return self.direction != WEST and self.position[0] < GRID_WIDTH - 2 and not self.otherAnt((self.position[0] + 2, self.position[1])) and not self.otherAnt((self.position[0] + 2, self.position[1] + 1)) and not self.otherAnt((self.position[0] + 2, self.position[1] - 1))
        elif direction == SOUTH :
            return self.direction != NORTH and self.position[1] < GRID_HEIGHT - 2 and not self.otherAnt((self.position[0], self.position[1] + 2)) and not self.otherAnt((self.position[0] + 1, self.position[1] + 2)) and not self.otherAnt((self.position[0] - 1, self.position[1] + 2))
        elif direction == WEST :
            return self.direction != EAST and self.position[0] > 1 and not self.otherAnt((self.position[0] - 2, self.position[1])) and not self.otherAnt((self.position[0] - 2, self.position[1] + 1)) and not self.otherAnt((self.position[0] - 2, self.position[1] - 1))
        else :
            return False

    def march(self) :
        direction = np.array([self.destination.position[0] - self.position[0], self.destination.position[1] - self.position[1]])
        direction = direction / np.sqrt(np.sum(direction**2))

        # Which way do I want to go most?
        primaryDirection = -1
        secondaryDirection = -1
        if np.abs(direction[0]) > np.abs(direction[1]) :
            if direction[0] > 0 :
                primaryDirection = EAST
            else :
                primaryDirection = WEST

            if direction[1] > 0 :
                secondaryDirection = SOUTH
            else :
                secondaryDirection = NORTH
        else :
            if direction[1] > 0 :
                primaryDirection = SOUTH
            else :
                primaryDirection = NORTH

            if direction[0] > 0 :
                secondaryDirection = EAST
            else :
                secondaryDirection = WEST

        teriaryDirection = self.direction
        # Lets go for it
        if self.canMove(primaryDirection) :
            self.move(primaryDirection)
        elif self.canMove(secondaryDirection) :
            self.move(secondaryDirection)
        elif self.canMove(teriaryDirection) :
            self.move(teriaryDirection)
            

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
nests.append(Nest(world, (int(GRID_WIDTH / 4),int(GRID_HEIGHT/2)), 0))
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
skip_frames = 1
frame = 0

running = True
while running:
    frame += 1
    # Update everything
    for nest in nests :
        nest.marchAnts()

    # Redraw
    if frame % skip_frames == 0 : # skip drawing frames
        pygame.time.wait(200)
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


