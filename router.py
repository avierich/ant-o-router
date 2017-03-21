import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Ant : 

    def __init__(self, position, destination) :
        self.position = position
        self.destination = destination
        self.connected = False
        self.path = [[np.random.rand(),np.random.rand()],[np.random.rand(),np.random.rand()]]
        self.line = plt.plot([],[])

    def get_line() :
        self.line.set_data(self.path)
        return self.line

class Nest :

    def __init__(self, position, ants) :
        self.position = position
        self.connections = []
        self.ants = ants

    def addConnection(self, connectedNest) :
        self.connections.append(connectedNest)
        self.ants.append(Ant(self.position,connectedNest))

def update_line(num, data, line):
    line.set_data(data[...,:num])
    print(line)
    return line,

def rando_walk(num, data, datatwo, line, linetwo):
    data[0].append(np.random.rand())
    data[1].append(np.random.rand())
    line.set_data(data)
    datatwo[0].append(np.random.rand())
    datatwo[1].append(np.random.rand())
    linetwo.set_data(datatwo)
    return line,linetwo

def step_world(num, ants) :
    lines = []
    for ant in ants :
        lines.append(ant.get_line)

    return lines

fig1 = plt.figure()

# Setup world
ants = []

pins = [(0.5,0.5),(0.8,0.5),(0.5,0.8)]
nests = [Nest((0.2,0.8),ants),Nest((0.8,0.8),ants),Nest((0.2,0.2),ants),Nest((0.8,0.2),ants)]

# Connect pins (This is not a pretty way to acheive this)
nests[0].addConnection(nests[1])
nests[1].addConnection(nests[0])
nests[2].addConnection(nests[3])
nests[3].addConnection(nests[2])


# Show pins
for nest in nests :
    plt.scatter(nest.position[0], nest.position[1])

data = [[],[]]
datatwo = [[],[]]
l, = plt.plot([], [])
ltwo, = plt.plot([], [])
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xlabel('x')
plt.title('test')
line_ani = animation.FuncAnimation(fig1, step_world, 100, fargs=(ants),
    interval=50, blit=False, repeat = False)
#line_ani.save('lines.mp4')
plt.show()
