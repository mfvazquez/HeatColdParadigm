#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import core, visual
import json
import stim


if __name__ == "__main__":

    with open("example.json") as paradigm_config:
        config = json.load(paradigm_config)

    win = visual.Window([800, 600], monitor='testMonitor', units='deg')


    stimuli = []
    for stimulus_conf in config["trial"]:
        stimuli.append(stim.Constructor.create(stimulus_conf, win))


    for stimulus in stimuli:
        if stimulus.needs_update():
            stimulus.update("some word")
        stimulus.run()

    win.close()
    core.quit()
