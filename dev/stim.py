#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import core, visual, event
import random
import json

# -------------------------------------
#           Stimulus Classes
# -------------------------------------


class Stimulus:
    def __init__(self, win, duration):
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

    def __init__(self, win, duration):
        super().__init__(win, duration)
        self._update = True

    def run(self):
        super().run()
        self._update = True

    def update(self, word):
        self.stim = visual.TextStim(self.win, text=word)
        self._update = False


class Fixation(SimpleDrawableStimulus):

    def __init__(self, win, symbol, duration):
        self.stim = visual.TextStim(win, text=symbol)
        super().__init__(win, duration)


class Blank(Stimulus):

    def __init__(self, win, duration):
        super().__init__(win, duration)


class RandomBlank(Blank):

    def __init__(self, win, range_duration):
        duration = random.uniform(range_duration[0], range_duration[1])
        super().__init__(win, duration)


class Choice(Stimulus):

    def __init__(self, win, duration, choices):
        self.choices = []
        self.keys = []
        for choice in choices:
            self.choices.append(visual.TextStim(
                win, text=choice[0], pos=choice[1]))
            self.keys.append(choice[2])
        super().__init__(win, duration)

    def run(self):
        for choice in self.choices:
            choice.draw()
        self.win.flip()
        event.waitKeys(maxWait = self.duration, keyList = self.keys)


# -------------------------------------
#            Constructor Class
# -------------------------------------


class Constructor():

    stimuli = {
        "fixation": Fixation,
        "blank": Blank,
        "random_blank": RandomBlank,
        "word": Word,
        "choice": Choice
    }

    @classmethod
    def create(cls, config, win):
        return cls.stimuli[config["type"]](win, **config["setup"])
