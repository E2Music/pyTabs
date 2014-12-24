'''
Created on Dec 12, 2014

@author: zeljko.bal
'''
from os.path import os

from mingus.containers.Note import Note
from textx.metamodel import metamodel_from_file

import pytabs


GRAMMAR_PATH = os.path.abspath(os.path.dirname(pytabs.__file__))+'/grammar/'

class TabNote(Note, object):
    """Mingus Note with additional parameters."""
    def __init__(self, name= 'C', octave = 4, dynamics = {}, pm = False):
        super(TabNote, self).__init__(name, octave, dynamics)
        self.pm = pm

class GuitarNoteProcessor:
    def __init__(self, tab_note_grammar_file=None):
        """Initializes note metamodel, if file is not specified initialize with default file."""
        if not tab_note_grammar_file:
            tab_note_grammar_file = GRAMMAR_PATH + "guitar_tab_note.tx"
        
        self.tab_note_metamodel = metamodel_from_file(tab_note_grammar_file)
    
    def _note_num_from_fret(self, fret, string_height):
        """Calculates a note number."""
        # base is the lowest E-0
        base = 3 * 12
        # frets from base to empty string
        string = {"e":28,
                  "B":23,
                  "G":19,
                  "D":14,
                  "A":9,
                  "E":4,
                  }[string_height]
        return base + string + int(fret)
    
    def __call__(self, note_symbol, mark_symbol):
        """Processes a note based on note_symbol and string mark_symbol, returns a Note instance."""
        note_model = self.tab_note_metamodel.model_from_str(note_symbol)
        
        # skip rests
        if note_model == '-':
            return None
        
        note_num = self._note_num_from_fret(note_model.fret, mark_symbol)
        note = TabNote(pm=note_model.pm)
        note.from_int(note_num)
        
        return note
