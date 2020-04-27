import os
import sys
import time
import msvcrt
from readchar import readkey, key
from itertools import product, count
from collections import deque
import numpy as np

class Map:
    def __init__(self):
        
        self.grid = np.array([0 for _ in range(108)]).reshape(9,12)
        for x, y in product(range(3,6), range(0,3)):
            self.grid[x,y] = 1
        for x, y in product(range(3,6), range(3,6)):
            self.grid[x,y] = 2
        for x, y in product(range(0,3), range(6,9)):
            self.grid[x,y] = 5
        for x, y in product(range(3,6), range(9,12)):
            self.grid[x,y] = 4
        for x, y in product(range(6,9), range(6,9)):
            self.grid[x,y] = 6
        for x, y in product(range(3,6), range(6,9)):
            self.grid[x,y] = 3

        N = iter(range(9))

        # for x, y in product(range(0,3), range(6,9)):
            # self.grid[x,y] = next(N)

    def __str__(self):

        return str(self.grid)

    def __repr__(self):

        return self.__class__.__name__+'()'

    def left_piece(self, counter=None):

        d = list(self.grid[:,6])
        t = []
        for i in self.grid[3:6,2]:
            t.append(i)
        t = t[::-1]
        for i in t:
            d.append(i)
        d = deque(d)
        if counter is None:
            d.rotate(3)
        else:
            d.rotate(-3)
        d = list(d)
        for i in range(3,6):
            self.grid[i,2] = d[-1]
            del d[-1]
        for i in range(9):
            self.grid[i,6] = d[i]

        if counter:
            self.grid[np.ix_([3,4,5],[3,4,5])] = np.rot90(self.grid[np.ix_([3,4,5],[3,4,5])])
        else:
            self.grid[np.ix_([3,4,5],[3,4,5])] = np.rot90(self.grid[np.ix_([3,4,5],[3,4,5])], -1)

    def right_piece(self, counter=None):

        d = list(self.grid[:,8])
        t = []
        for i in self.grid[3:6,0]:
            t.append(i)
        t = t[::-1]
        for i in t:
            d.append(i)
        d = deque(d)
        if counter is None:
            d.rotate(-3)
        else:
            d.rotate(3)
        d = list(d)
        for i in range(3,6):
            self.grid[i,0] = d[-1]
            del d[-1]
        for i in range(9):
            self.grid[i,8] = d[i]

        if counter:
            self.grid[np.ix_([3,4,5],[9,10,11])] = np.rot90(self.grid[np.ix_([3,4,5],[9,10,11])], -1)
        else:
            self.grid[np.ix_([3,4,5],[9,10,11])] = np.rot90(self.grid[np.ix_([3,4,5],[9,10,11])])

    def top_piece(self, counter=None):

        d = list(self.grid[3,:])
        d = deque(d)
        if counter is None:
            d.rotate(-3)
        else:
            d.rotate(3)
        d = list(d)
        self.grid[3,:] = d

        if counter:
            self.grid[np.ix_([0,1,2],[6,7,8])] = np.rot90(self.grid[np.ix_([0,1,2],[6,7,8])])
        else:
            self.grid[np.ix_([0,1,2],[6,7,8])] = np.rot90(self.grid[np.ix_([0,1,2],[6,7,8])], -1)

    def bottom_piece(self, counter=None):

        d = list(self.grid[5,:])
        d = deque(d)
        if counter is None:
            d.rotate(3)
        else:
            d.rotate(-3)
        d = list(d)
        self.grid[5,:] = d

        if counter:
            self.grid[np.ix_([6,7,8],[6,7,8])] = np.rot90(self.grid[np.ix_([6,7,8],[6,7,8])])
        else:
            self.grid[np.ix_([6,7,8],[6,7,8])] = np.rot90(self.grid[np.ix_([6,7,8],[6,7,8])], -1)

    def front_piece(self, counter=None):

        if counter:
            self.grid[np.ix_([2,3,4,5,6],[5,6,7,8,9])] = np.rot90(self.grid[np.ix_([2,3,4,5,6],[5,6,7,8,9])])
        else:
            self.grid[np.ix_([2,3,4,5,6],[5,6,7,8,9])] = np.rot90(self.grid[np.ix_([2,3,4,5,6],[5,6,7,8,9])], -1)

    def back_piece(self, counter=None):

        if counter:
            self.grid[np.ix_([3,4,5],[0,1,2])] = np.rot90(self.grid[np.ix_([3,4,5],[0,1,2])], -1)
            self.grid[0,6:9], self.grid[3:6,11], self.grid[8,6:9], self.grid[3:6,3] = self.grid[3:6,11].copy(), self.grid[8,6:9].copy(), self.grid[3:6,3].copy(), self.grid[0,6:9].copy()
        else:
            self.grid[np.ix_([3,4,5],[0,1,2])] = np.rot90(self.grid[np.ix_([3,4,5],[0,1,2])])
            self.grid[0,6:9], self.grid[3:6,11], self.grid[8,6:9], self.grid[3:6,3] = self.grid[3:6,11].copy(), self.grid[8,6:9].copy(), self.grid[3:6,3].copy(), self.grid[0,6:9].copy()
    def move(self, alg):

        moves = alg.split()
        for i in moves:
            if i == 'L':
                self.left_piece()
            elif i == 'l' or i == "L'":
                self.left_piece(counter=True)
            elif i == 'R':
                self.right_piece()
            elif i == 'r' or i == "R'":
                self.right_piece(counter=True)
            elif i == 'U':
                self.top_piece()
            elif i == 'u' or i == "U'":
                self.top_piece(counter=True)
            elif i == 'D':
                self.bottom_piece()
            elif i == 'd' or i == "D'":
                self.bottom_piece(counter=True)
            elif i == 'F':
                self.front_piece()
            elif i == 'f' or i == "F'":
                self.front_piece(counter=True)
            elif i == 'B':
                self.back_piece()
            elif i == 'b' or i == "B'":
                self.back_piece(counter=True)

    # def interactive(self):

    #     import time
    #     LEFT = key.LEFT
    #     left = []
    #     RIGHT = key.RIGHT
    #     right = []
    #     UP = key.UP
    #     up = []
    #     DOWN = key.DOWN
    #     down = []
    #     while True:
    #         char = readkey()
    #         ts = time.perf_counter_ns()
    #         if char == UP:
    #             te = time.perf_counter_ns() - ts
    #             up.append(te)
    #             avg = sum(up)/len(up)
    #             print(f"UP {avg:.02f} nanoseconds")
    #         if char == DOWN:
    #             te = time.perf_counter_ns() - ts
    #             down.append(te)
    #             avg = sum(down)/len(down)
    #             print(f"DOWN {avg:.02f} nanoseconds")
    #         if char == LEFT:
    #             te = time.perf_counter_ns() - ts
    #             left.append(te)
    #             avg = sum(left)/len(left)
    #             print(f"LEFT {avg:.02f} nanoseconds")
    #         if char == RIGHT:
    #             te = time.perf_counter_ns() - ts
    #             right.append(te)
    #             avg = sum(right)/len(right)
    #             print(f"RIGHT {avg:.02f} nanoseconds")

m = Map()
while True:
    os.system('cls')
    print(m)
    sequence = input(">>> ")
    m.move(sequence)