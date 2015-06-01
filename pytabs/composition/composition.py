#    PyTabs - Simplified music notation DSL, interpreter and player.
#    Copyright (C) 2014, Zeljko Bal
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from mingus.containers import NoteContainer

'''
Created on Dec 25, 2014

@author: zeljko.bal
'''
from os.path import os

from mingus.containers import Track
from textx.metamodel import metamodel_from_file

import pytabs
from pytabs.chords.guitarchords import chord_command_processor, \
    chord_interval_processor, GuitarChordProcessor, PauseChord
from pytabs.guitar.guitar_tablature import GuitarTabProcessor
from pytabs.keyboards.keyboard_tablature import KeyboardTabProcessor


GRAMMAR_PATH = os.path.abspath(os.path.dirname(pytabs.__file__))+'/grammar/'

def get_composition_metamodel(script_dir):
    composition_mm = metamodel_from_file(GRAMMAR_PATH + 'composition.tx', debug=False)
    composition_mm.register_obj_processors({'BaseExtended': chord_command_processor,
                                      "PrepExtended": chord_command_processor,
                                      "DecorateExtended":chord_command_processor,
                                      "ChordDuration":chord_interval_processor,
                                      "SongSequence":process_sequence,
                                      "Program":lambda program: process_instruments(program, script_dir),
                                      })
    return composition_mm

def parse_composition_file(composition_file_path):
    composition_mm = get_composition_metamodel(script_dir=os.path.dirname(composition_file_path))
    return composition_mm.model_from_file(composition_file_path)

def parse_composition_string(composition_string, script_dir):
    composition_mm = get_composition_metamodel(script_dir=script_dir)
    return composition_mm.model_from_str(composition_string)

def process_sequence(sequence):
    processor = {
                 "guitar-solo":process_guitar_tabs,
                 "guitar-rhythm":process_chords,
                 "keyboards":process_keyboard_tabs,
                }[sequence.type]
    
    sequence.value = processor(sequence.value)

def process_keyboard_tabs(tabs_model):
    return KeyboardTabProcessor().process(tabs_model)

def process_guitar_tabs(tabs_model):
    return GuitarTabProcessor().process(tabs_model)

def process_chords(chords_model):
    processor = GuitarChordProcessor(guitar_model=chords_model)
    chords = processor.guitarmodel_interprete()
    
    track = Track()
    
    for chord,duration in chords:
        if isinstance(chord, PauseChord):
            track.add_notes(NoteContainer(), duration)
        else:
            track.add_notes(chord, duration)
    
    _change_track_octave(track, -1)
    
    return track

def process_instruments(program, composition_file_path_dir):
    imports = {}
    for instrument in program.imports.soundfonts:
        path_prefix = ''
        if not os.path.isabs(instrument.path):
            path_prefix = composition_file_path_dir
        imports[instrument.name] = path_prefix+'/'+instrument.path
    
    program.imports = imports
    
def _change_track_octave(track, n):
    if n == 0:
        return
    for _ in range(abs(n)):
        for bar in track.bars:
            for note in bar.bar[0][2]:
                if n > 0:
                    note.octave_up()
                else:
                    note.octave_down()
    
    