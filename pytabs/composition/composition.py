'''
Created on Dec 25, 2014

@author: zeljko.bal
'''
from os.path import os
from textx.metamodel import metamodel_from_file

from mingus.containers.Track import Track

import pytabs
from pytabs.chords.guitarchords import chord_command_processor, \
    chord_interval_processor, GuitarChordProcessor
from pytabs.guitar.guitar_tablature import GuitarTabProcessor


GRAMMAR_PATH = os.path.abspath(os.path.dirname(pytabs.__file__))+'/grammar/'

def parse_composition_file(composition_file_path):
      
    composition_mm = metamodel_from_file(GRAMMAR_PATH + 'composition.tx', debug=False)
    composition_mm.register_obj_processors({'BaseExtended': chord_command_processor,
                                      "PrepExtended": chord_command_processor,
                                      "DecorateExtended":chord_command_processor,
                                      "ChordDuration":chord_interval_processor,
                                      "SongSequence":process_sequence,
                                      "Program":process_instruments,
                                      })
    
    return composition_mm.model_from_file(composition_file_path)

def process_sequence(sequence):
    processor = {
                 "guitar-solo":process_guitar_tabs,
                 "guitar-rhythm":process_chords,
                }[sequence.type]
    
    sequence.value = processor(sequence.value)

def process_guitar_tabs(tabs_model):
    return GuitarTabProcessor().process(tabs_model)

def process_chords(chords_model):
    processor = GuitarChordProcessor(guitar_model=chords_model)
    chords = processor.guitarmodel_interprete()
    
    track = Track()
    
    for chord,duration in chords:
        track.add_notes(chord, duration)
    
    return track

def process_instruments(program):
    program.imports = {instrument.name:instrument.path for instrument in program.imports.soundfonts}
    
    