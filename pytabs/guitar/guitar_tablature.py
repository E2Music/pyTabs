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

'''
Created on Dec 12, 2014

@author: zeljko.bal
'''
from os.path import os
from textx.metamodel import metamodel_from_file

from mingus.containers.Note import Note
from mingus.containers.NoteContainer import NoteContainer
from mingus.containers.Track import Track

from pytabs.tablature.tablature import TablatureProcessor


GRAMMAR_PATH = os.path.dirname(os.path.realpath(__file__)) + "/grammar/"

class TabNote(Note, object):
    """Mingus Note with additional parameters."""
    def __init__(self, name= 'C', octave = 4, dynamics = {}, pm = False):
        super(TabNote, self).__init__(name, octave, dynamics)
        self.pm = pm

class GuitarNoteProcessor:
    """Processor for a single guitar note."""
    def __init__(self, tab_note_grammar_file=None, default_duration=4):
        """Initializes note metamodel, if file is not specified initialize with default file."""
        if not tab_note_grammar_file:
            tab_note_grammar_file = GRAMMAR_PATH + "guitar_tab_note.tx"
        
        self.tab_note_metamodel = metamodel_from_file(tab_note_grammar_file)
        self.default_duration = default_duration
    
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
            if mark_symbol == 'R':
                return self.default_duration
            else:
                return None
        
        # just return the number if rythm string
        if mark_symbol == 'R':
            return int(note_symbol)
        
        note_num = self._note_num_from_fret(note_model.fret, mark_symbol)
        note = TabNote(pm=note_model.pm)
        note.from_int(note_num)
        
        return note
    
class GuitarTabProcessor:
    """Processor for a guitar tab textx model."""
    def __init__(self, default_duration=4, additional_dashes=0):
        self.processor = TablatureProcessor(process_note=GuitarNoteProcessor(default_duration=default_duration), 
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
