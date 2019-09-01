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
        self._watch_exit = False

    def run(self):
        self.win.flip()

        if not self._watch_exit:
            core.wait(self.duration)
        else:
            keys = event.waitKeys(maxWait=self.duration, keyList=self.exit_key)
            if keys and self.exit_key in keys:
                return False

        return True

    def needs_update(self):
        return self._update

    def set_exit_key(self, exit_key):
        self.exit_key = exit_key
        self._watch_exit = True


class SimpleDrawableStimulus(Stimulus):

    def run(self):
        self.stim.draw()
        return super().run()


class Word(SimpleDrawableStimulus):

    def __init__(self, win, duration):
        super().__init__(win, duration)
        self._update = True

    def run(self):
        self._update = True
        return super().run()

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

        if not self._watch_exit:
            keys = self.keys
        else:
            keys = self.keys + [self.exit_key]

        keys_pressed = event.waitKeys(maxWait=self.duration, keyList=keys)
        if keys_pressed and self.exit_key in keys_pressed:
            return False

        return True


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
