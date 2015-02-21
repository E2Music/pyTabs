'''
Created on Feb 10, 2015

@author: Bojana
'''
from os.path import os
from textx.metamodel import metamodel_from_file

from mingus.containers.Note import Note
from mingus.containers.NoteContainer import NoteContainer
from mingus.containers.Track import Track
from pytabs.tablature.tablature import TablatureProcessor

GRAMMAR_PATH = os.path.dirname(os.path.realpath(__file__)) + "/grammar/"

class KeyboardNoteProcessor:
    """Processor for a single keyboard note."""
    def __init__(self, tab_note_grammar_file=None, default_duration=4):
        """Initializes note metamodel, if file is not specified initialize with default file."""
        if not tab_note_grammar_file:
            tab_note_grammar_file = GRAMMAR_PATH + "keyboard_tab_note.tx"
        
        self.tab_note_metamodel = metamodel_from_file(tab_note_grammar_file)
        self.default_duration = default_duration
    
    def _note_num_from_key(self, key, note_height):
        """Calculates a note number."""
        octave = int(key) * 12
        
        note = { "c":0, "C":1, "d":2, "D":3, "e":4, "f":5, "F":6, "g":7, "G":8, "a":9, "A":10, "b":11}[note_height]

        return note + octave
    
    def __call__(self, note_symbol, mark_symbol):
        """Processes a note based on note_symbol and string mark_symbol, returns a Note instance."""
        note_model = self.tab_note_metamodel.model_from_str(note_symbol)
        
        # skip rests
        if note_model == '-':
            if mark_symbol == 'R':
                return self.default_duration
            else:
                return None
        
        # just return the number if rythm string
        if mark_symbol == 'R':
            return int(note_symbol)
        
        note_num = self._note_num_from_key(mark_symbol,note_model.key)
        note = Note()
        note.from_int(note_num)
        
        return note
    
class KeyboardTabProcessor:
    """Processor for a keyboard tab textx model."""
    def __init__(self, default_duration=4, additional_dashes=0):
        self.processor = TablatureProcessor(process_note=KeyboardNoteProcessor(default_duration=default_duration), 
                                            additional_dashes=additional_dashes, 
                                            container_type=list)
        self.default_duration = default_duration
    
    def process(self, tabs_model):
        """Processes the model and returns a mingus Track."""
        beats = self.processor.process_tablature_model(tabs_model)
        track = Track()
        
        for beat in beats:
            if tabs_model.strings[0].mark == 'R':
                track.add_notes(NoteContainer(beat[1:]), beat[0])
            else:
                track.add_notes(NoteContainer(beat), self.default_duration)
        
        return track
