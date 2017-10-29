# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

import random
from Agent import Agent

def print_map(m):
    for x in m:
        for y in x:
            print(y, end=' ')
        print()

class MyAI(Agent):

    def __init__(self):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        self._has_gold = False
        self._wumpus_alive = True
        self._wump_cords = set()
        self._stench_found = False
        self._breadcrumbs = []
        self._facing = 'R'
        self._stack = [(0,0)]
        self._visited = set()
        self._map = [[ MyAI.__marks['NULL'] for i in range(10) ] for i in range(4)]
        self._map[0][0] = MyAI.__marks['SAFE']
        self._x = 0
        self._y = 0
        self._backtracking = False
        self._turning_around = False

        # map bounds
        self._x_bound = 3
        self._y_bound = 9

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def _update_facing(self, action):
        if action == Agent.Action.TURN_LEFT or action == Agent.Action.TURN_RIGHT:
            self._facing = MyAI.__face_change[self._facing][action]
        elif action == Agent.Action.FORWARD:
            if self._facing == 'L':
                self._x -= 1
            elif self._facing == 'R':
                self._x += 1
            elif self._facing == 'D':
                self._y -= 1
            else:
                self._y += 1
        return action

    def _backtrack(self):
        if len(self._breadcrumbs) == 0:
            return Agent.Action.CLIMB
        if not self._backtracking:
            self._backtracking = True
            self._turning_around = True
            return self._update_facing(Agent.Action.TURN_LEFT)
        if self._turning_around:
            self._turning_around = False
            return self._update_facing(Agent.Action.TURN_LEFT)
        return self._update_facing(self._breadcrumbs.pop())

    def _go_adjacent(self, direction):
        print(self._facing, 'want to go', direction)
        if self._facing == direction:
            self._breadcrumbs.append(Agent.Action.FORWARD)
            return self._update_facing(Agent.Action.FORWARD)
        if self._facing == 'L':
            if direction == 'U':
                self._breadcrumbs.append(Agent.Action.TURN_LEFT)
                return self._update_facing(Agent.Action.TURN_RIGHT)
            else:
                self._breadcrumbs.append(Agent.Action.TURN_RIGHT)
                return self._update_facing(Agent.Action.TURN_LEFT)
        if self._facing == 'R':
            if direction == 'U':
                self._breadcrumbs.append(Agent.Action.TURN_RIGHT)
                return self._update_facing(Agent.Action.TURN_LEFT)
            else:
                self._breadcrumbs.append(Agent.Action.TURN_LEFT)
                return self._update_facing(Agent.Action.TURN_RIGHT)
        if self._facing == 'U':
            if direction == 'L':
                self._breadcrumbs.append(Agent.Action.TURN_RIGHT)
                return self._update_facing(Agent.Action.TURN_LEFT)
            else:
                self._breadcrumbs.append(Agent.Action.TURN_LEFT)
                return self._update_facing(Agent.Action.TURN_RIGHT)
        if self._facing == 'D':
            if direction == 'R':
                self._breadcrumbs.append(Agent.Action.TURN_RIGHT)
                return self._update_facing(Agent.Action.TURN_LEFT)
            else:
                self._breadcrumbs.append(Agent.Action.TURN_LEFT)
                return self._update_facing(Agent.Action.TURN_RIGHT)

    def getAction(self, stench, breeze, glitter, bump, scream):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        # debug
        if self._backtracking:
            print('BACKTRACKING')
        print(self._stack)
        print(self._visited)
        print(self._breadcrumbs)

        if self._has_gold:
            return self._backtrack()

        if glitter:
            self._has_gold = True
            return Agent.Action.GRAB

        if bump:
            if self._facing == 'R':
                self._x_bound = self._x
            else:
                self._y_bound = self._y
            self._stack.pop()
            self._breadcrumbs.pop()

        while True:
            # find next stack top where it is not in visited i.e find next node to expand
            print(self._x, self._y)
            while (len(self._stack) != 0 and (self._stack[-1] in self._visited or self._stack[-1][0] > self._x_bound or self._stack[-1][1] > self._y_bound)):
                self._stack.pop()
            if len(self._stack) == 0:
                return self._backtrack()

            to_expand = self._stack[-1]

            # expand if on coordinate otherwise backtrack till on coordinate
            if (self._x, self._y) == to_expand:
                self._stack.pop()
                self._visited.add(to_expand)
                safe = True
                if self._x != self._x_bound:
                    print('checking right')
                    adj = self._map[self._x+1][self._y]
                    if breeze and adj != MyAI.__marks['SAFE']:
                        self._map[self._x+1][self._y] = MyAI.__marks['PIT']
                        safe = False
                    if not self._stench_found and stench and adj != MyAI.__marks['SAFE']:
                        self._map[self._x+1][self._y] = MyAI.__marks['WUMP']
                        self._wump_cords.add((self._x+1, self._y))
                        safe = False
                    if safe:
                        self._map[self._x+1][self._y] = MyAI.__marks['SAFE']
                        self._stack.append((self._x+1, self._y))

                if self._y != self._y_bound:
                    adj = self._map[self._x][self._y+1]
                    if breeze and adj != MyAI.__marks['SAFE']:
                        self._map[self._x][self._y+1] = MyAI.__marks['PIT']
                        safe = False
                    if not self._stench_found and stench and adj != MyAI.__marks['SAFE']:
                        self._map[self._x][self._y+1] = MyAI.__marks['WUMP']
                        self._wump_cords.add((self._x, self._y+1))
                        safe = False
                    if safe:
                        self._map[self._x][self._y+1] = MyAI.__marks['SAFE']
                        self._stack.append((self._x, self._y+1))

                if self._x != 0:
                    adj = self._map[self._x-1][self._y]
                    if breeze and adj != MyAI.__marks['SAFE']:
                        self._map[self._x-1][self._y] = MyAI.__marks['PIT']
                        safe = False
                    if not self._stench_found and stench and adj != MyAI.__marks['SAFE']:
                        self._map[self._x-1][self._y] = MyAI.__marks['WUMP']
                        self._wump_cords.add((self._x-1, self._y))
                        safe = False
                    if safe:
                        self._map[self._x-1][self._y] = MyAI.__marks['SAFE']
                        self._stack.append((self._x-1, self._y))

                if self._y != 0:
                    adj = self._map[self._x][self._y-1]
                    if breeze and adj != MyAI.__marks['SAFE']:
                        self._map[self._x][self._y-1] = MyAI.__marks['PIT']
                        safe = False
                    if not self._stench_found and stench and adj != MyAI.__marks['SAFE']:
                        self._map[self._x][self._y-1] = MyAI.__marks['WUMP']
                        self._wump_cords.add((self._x, self._y-1))
                        safe = False
                    if safe:
                        self._map[self._x][self._y-1] = MyAI.__marks['SAFE']
                        self._stack.append((self._x, self._y-1))
            else:
                x, y = to_expand
                if self._x == x or self._y == y:
                    self._backtracking = False
                    if x - self._x == 1:
                        return self._go_adjacent('R')
                    if x - self._x == -1:
                        return self._go_adjacent('L')
                    if y - self._y == 1:
                        return self._go_adjacent('U')
                    if y - self._y == -1:
                        return self._go_adjacent('D')
                else:
                    return self._backtrack()

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================



    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================

    __actions = [
        Agent.Action.TURN_LEFT,
        Agent.Action.TURN_RIGHT,
        Agent.Action.FORWARD,
    ]

    __marks = {
        'NULL': -1,
        'SAFE': 0,
        'PIT': 1,
        'WUMP': 2
    }

    __face_change = {
        'L' : {
            Agent.Action.TURN_LEFT : 'D',
            Agent.Action.TURN_RIGHT : 'U'
        },
        'R' : {
            Agent.Action.TURN_LEFT : 'U',
            Agent.Action.TURN_RIGHT : 'D'
        },
        'U' : {
            Agent.Action.TURN_LEFT : 'L',
            Agent.Action.TURN_RIGHT : 'R'
        },
        'D' : {
            Agent.Action.TURN_LEFT : 'R',
            Agent.Action.TURN_RIGHT : 'L'
        },
    }


    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
