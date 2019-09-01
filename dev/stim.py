#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import core, visual, event
import random
import json

# -------------------------------------
#           Stimulus Classes
# -------------------------------------


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


class SimpleDrawableStimulus(Stimulus):

    def run(self):
        self.stim.draw()
        super().run()


class Word(SimpleDrawableStimulus):

    def __init__(self, duration, win):
        super().__init__(duration, win)
        self._update = True

    def run(self):
        super().run()
        self._update = True

    def update(self, word):
        self.stim = visual.TextStim(self.win, text=word)
        self._update = False


class Fixation(SimpleDrawableStimulus):

    def __init__(self, symbol, duration, win):
        self.stim = visual.TextStim(win, text=symbol)
        super().__init__(duration, win)


class Blank(Stimulus):

    def __init__(self, duration, win):
        super().__init__(duration, win)


class RandomBlank(Blank):

    def __init__(self, range, win):
        duration = random.uniform(range[0], range[1])
        super().__init__(duration, win)


class Choice(Stimulus):

    def __init__(self, duration, choices, win):
        self.choices = []
        for choice in choices:
            self.choices.append(visual.TextStim(win, text=choice))
        super().__init__(duration, win)

    def run(self):
        for choice in self.choices:
            choice.draw()
        super().run()



# -------------------------------------
#            Constructor Classes
# -------------------------------------


class WordConstructor():

    @classmethod
    def create(cls, config, win):
        return Word(config["duration"], win)


class FixationConstructor():

    @classmethod
    def create(cls, config, win):
        return Fixation(config["symbol"], config["duration"], win)


class BlankConstructor():

    @classmethod
    def create(cls, config, win):
        return Blank(config["duration"], win)


class RandomBlankConstructor():

    @classmethod
    def create(cls, config, win):
        return RandomBlank(config["duration"], win)

class ChoiceConstructor():

    @classmethod
    def create(cls, config, win):
        return Choice(config["duration"], config["choices"], win)


class Constructor():

    constructors = {
        "fixation": FixationConstructor,
        "blank": BlankConstructor,
        "random_blank": RandomBlankConstructor,
        "word": WordConstructor,
        "choice": ChoiceConstructor
    }

    @classmethod
    def create(cls, config, win):
        return cls.constructors[config["type"]].create(config, win)
