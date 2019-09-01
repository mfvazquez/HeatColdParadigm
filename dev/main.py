#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import core, visual, monitors
import json
import stim
import sys


if __name__ == "__main__":

    with open("../data/paradigm.json") as paradigm_config:
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
        stimulus = stim.Constructor.create(stimulus_conf, win)
        if "exit_key" in config:
            stimulus.set_exit_key(config["exit_key"])
        stimuli.append(stimulus)

    print("{0} stimulus created successfully".format(len(stimuli)))
    print("Loading words sequence...")

    for stimulus in stimuli:

        if stimulus.needs_update():
            stimulus.update("some word")

        if not stimulus.run():
            print("Exit key pressed. Leaving application...")
            win.close()
            core.quit()
            sys.exit()


    win.close()
    core.quit()
