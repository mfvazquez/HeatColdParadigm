#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import core, visual, event
import random
import json


class Stimulus:

    def __init__(self, duration, win):
        self.win = win
        self.duration = duration
        self._update = False

    def run(self):
        self.win.flip()
        core.wait(self.duration)

    def needs_update(self):
        return self._update



class Text(Stimulus):

    def __init__(self, duration, win):
        super().__init__(duration, win)
        self._update = True

    def run(self):
        self.stim.draw()
        super().run()
        self._update = True

    def update(self, word):
        self.stim = visual.TextStim(self.win, text=word)
        self._update = False


class TextConstructor():

    @classmethod
    def create(cls, config, win):
        return Text(config["duration"], win)



class Fixation(Stimulus):

    def __init__(self, symbol, duration, win):
        self.stim = visual.TextStim(win, text=symbol)
        super().__init__(duration, win)

    def run(self):
        self.stim.draw()
        super().run()    

class FixationConstructor():

    @classmethod
    def create(cls, config, win):
        return Fixation(config["symbol"], config["duration"], win)



class Blank(Stimulus):

    def __init__(self, duration, win):
        super().__init__(duration, win)

class BlankConstructor():

    @classmethod
    def create(cls, config, win):
        return Blank(config["duration"], win)



class RandomBlank(Blank):

    def __init__(self, range, win):
        duration = random.uniform(range[0], range[1])
        super().__init__(duration, win)

class RandomBlankConstructor():

    @classmethod
    def create(cls, config, win):
        return RandomBlank(config["duration"], win)



class Constructor():

    constructors = {
        "fixation": FixationConstructor,
        "blank": BlankConstructor,
        "random_blank": RandomBlankConstructor,
        "text": TextConstructor
    }

    @classmethod
    def create(cls, config, win):
        return cls.constructors[config["type"]].create(config, win)