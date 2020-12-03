#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import core, visual, monitors, logging
import json
import sys
import csv
import os

# Path to this file
script_path = os.path.abspath(os.path.dirname(__file__))
# Adds dev dir to import custom modules
sys.path.append(os.path.join(script_path, "../dev"))

import stim

def csv_read(file, delimiter):
    with open(file, encoding="utf8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=delimiter)
        csv_list = list(readCSV)
    return csv_list

def txt_read(file):
    with open(file, 'r', encoding="utf8") as txtfile:
        content = txtfile.read()
    return content


if __name__ == "__main__":

    # Loads paradigm configuration
    paradigm_file = os.path.join(script_path, "../data/paradigm.json")
    with open(paradigm_file) as paradigm_config:
        config = json.load(paradigm_config)

    # Prepares log file
    log_dir = os.path.join(script_path, "../log")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_file = os.path.join(script_path, "../log/data.log")
    logging.LogFile(log_file, level=logging.INFO, filemode='w')

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
    for block_info in config["sequence"]:

        if block_info["type"] == "instruction":
            instruction_file = os.path.join(script_path, "../data/", block_info["file"])
            content = txt_read(instruction_file)

        elif block_info["type"] == "trial":
            words_file = os.path.join(script_path, "../data/", block_info["file"])
            content = csv_read(words_file, ',')
        
        else:
            raise Exception('Unknow block type: {}'.format(bloc_info["type"]))

        block_info["content"] = content

    # Runs the paradigm
    block_number = 1
    for block in config["sequence"]:
        print(block["type"])
        if block["type"] == "instruction" and not stim.Instruction(win, block["content"], config["exit_key"]).run():
            logging.log(level=logging.INFO, msg="Exit key pressed. Leaving application.")
            logging.flush()
            win.close()
            core.quit()
            sys.exit()

        elif block["type"] == "trial":

            logging.log(level=logging.INFO, msg="running block {0}.".format(block_number))
            for (word, word_code) in block["content"]:

                for stimulus in stimuli:

                    if stimulus.needs_update():
                        stimulus.update(word)

                    if not stimulus.run():
                        logging.log(level=logging.INFO, msg="Exit key pressed. Leaving application.")
                        logging.flush()
                        win.close()
                        core.quit()
                        sys.exit()
            block_number += 1
            logging.flush()

    logging.log(level=logging.INFO, msg="Leaving application.")
    win.close()
    core.quit()
