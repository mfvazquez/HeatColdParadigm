#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import core, visual, monitors
import json
import stim
import sys
import csv
import os.path


def csv_read(file, delimiter):
    with open(file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=delimiter)
        csv_list = list(readCSV)
    return csv_list


if __name__ == "__main__":

    # Path to this file
    script_path = os.path.abspath(os.path.dirname(__file__))

    # Loads paradigm configuration
    paradigm_file = os.path.join(script_path, "../data/paradigm.json")
    with open(paradigm_file) as paradigm_config:
        config = json.load(paradigm_config)

    # Opens the window
    if "window" in config:
        print("Loading custom setup...")
        setup = config["window"]
        win = visual.Window(**setup, monitor='testMonitor', units='deg')
    else:
        print("Loading default setup...")
        win = visual.Window(monitor='testMonitor', units='deg')

    # Creates the stimulus
    stimuli = []
    for stimulus_conf in config["trial"]:
        stimulus = stim.Constructor.create(stimulus_conf, win)
        if "exit_key" in config:
            stimulus.set_exit_key(config["exit_key"])
        stimuli.append(stimulus)

    print("{0} stimulus created successfully".format(len(stimuli)))
    print("Loading words sequence...")

    # Loads the words
    blocks = []
    for block_file in config["sequence"]:
        words_file = os.path.join(script_path, "../data/", block_file)
        blocks.append(csv_read(words_file, ','))

    # Runs the paradigm
    block_number = 1
    for block in blocks:
        print("running block {0}...".format(x))
        for (word, word_code) in block:

            for stimulus in stimuli:

                if stimulus.needs_update():
                    stimulus.update(word)

                if not stimulus.run():
                    print("Exit key pressed. Leaving application...")
                    win.close()
                    core.quit()
                    sys.exit()
        block_number += 1

    win.close()
    core.quit()
