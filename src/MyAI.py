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

class MyAI(Agent):

    def __init__(self):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        self._has_gold = False
        self._breadcrumbs = []

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction(self, stench, breeze, glitter, bump, scream):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        if self._has_gold:
            if not self._breadcrumbs:
                return Agent.Action.CLIMB
            # Backtrack
            return self._breadcrumbs.pop()

        if glitter:
            self._has_gold = True

            # Turn around
            self._breadcrumbs.append(Agent.Action.TURN_LEFT)
            self._breadcrumbs.append(Agent.Action.TURN_LEFT)
            return Agent.Action.GRAB

        selected_action = self.__actions[random.randrange(len(self.__actions))]
        if selected_action == Agent.Action.TURN_LEFT:
            self._breadcrumbs.append(Agent.Action.TURN_RIGHT)
        elif selected_action == Agent.Action.TURN_RIGHT:
            self._breadcrumbs.append(Agent.Action.TURN_LEFT)
        elif selected_action == Agent.Action.FORWARD:
            self._breadcrumbs.append(Agent.Action.FORWARD)

        return selected_action

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

    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
