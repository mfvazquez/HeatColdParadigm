#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import core, visual, monitors
import json
import stim


if __name__ == "__main__":

    with open("paradigm.json") as paradigm_config:
        config = json.load(paradigm_config)

    if "window" in config:
        print("Loading custom setup...")
        setup = config["window"]
        win = visual.Window(**setup, monitor='testMonitor', units='deg')
    else:
        print("Loading default setup...")
        win = visual.Window(monitor='testMonitor', units='deg')

    stimuli = []
    for stimulus_conf in config["trial"]:
        stimuli.append(stim.Constructor.create(stimulus_conf, win))


    for stimulus in stimuli:
        if stimulus.needs_update():
            stimulus.update("some word")
        stimulus.run()

    win.close()
    core.quit()
