

import numpy as np
import math
from ..miniworld import MiniWorldEnv, Room
from ..entity import Box, TextFrame, CifarFrame
import time
import random 
import string

class OneRoomNoisyTv(MiniWorldEnv):
    """
    Environment in which the goal is to go to a red box
    placed randomly in one big room.
    """

    def __init__(self, size=10, noisy_tv=True, **kwargs):
        assert size >= 2
        self.size = size
        self.noisy_tv=noisy_tv
        super().__init__(
            max_episode_steps=180,
            **kwargs
        )
        self.action_space = spaces.Discrete(self.actions.move_forward+2)

    def _gen_world(self):
        room = self.add_rect_room(
            min_x=0,
            max_x=self.size,
            min_z=0,
            max_z=self.size
        )

        if self.noisy_tv:
            self.tv = CifarFrame(
                pos=[self.size/2, 1.5, self.size-0.1],
                dir=math.pi/2,
                str = ''
            )
            # self.text = TextFrame(
            #     pos=[self.size/2, 1.5, self.size-0.1],
            #     dir=math.pi/2,
            #     str = ''.join(random.choice(self.letters) for i in range((self.num_letters)))
            # )
            self.entities.append(self.tv)



        self.box = self.place_entity(Box(color='red'))
        self.place_agent()

    def step(self, action):
        obs, reward, done, info = super().step(action)

        if self.noisy_tv and action ==self.actions.toggle:
            # self.text.str = ''.join(random.choice(self.letters) for i in range((self.num_letters)))
            # self.text.randomize(None,None)
            self.tv.randomize(None,None)
            del self.entities[-1]
            self.entities.append(self.tv)



        if self.near(self.box):
            reward += self._reward()
            done = True


        return obs, reward, done, info

