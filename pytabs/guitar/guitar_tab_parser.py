'''
Created on Dec 12, 2014

@author: zeljko.bal
'''
from os.path import os
from textx.metamodel import metamodel_from_file

from mingus.containers.Note import Note
from mingus.containers.NoteContainer import NoteContainer

class TabNote(Note, object):
    """Mingus Note sa dodatnim gitarskim parametrima."""
    def __init__(self, name= 'C', octave = 4, dynamics = {}, pm = False):
        super(TabNote, self).__init__(name, octave, dynamics)
        self.pm = pm

class ParsingException(Exception):
    def __init__(self, args):
        super(ParsingException, self).__init__(args)

class GuitarTabParser:
    """
    Parses tablatures in form of:
    e|-0-----10-3-||
    B|-------1--1-||
    G|-12pm-----6-||
    D|-2-----9--0-||
    A|-2-----3--2-||
    E|------------||
    
    All notes must be separated by a dash '-' and they can be of arbitrary length (with parameters),
    every note must be followed by additional dashes for the length of the longest note in a column,
    all strings must be of equal length and each one must start with '|-' and end with '-||'
    """
    
    def __init__(self, tab_grammar_file=None, tab_note_grammar_file=None):
        """Initializes metamodels, if files are not specified initialize with default files."""
        # initialize textx metamodels
        if not tab_grammar_file or not tab_note_grammar_file:
            directory = os.path.dirname(os.path.realpath(__file__))
            prefix = directory + "/grammar/"
            if not tab_grammar_file:
                tab_grammar_file = prefix + "guitar_tab.tx"
            if not tab_note_grammar_file:
                tab_note_grammar_file = prefix + "guitar_tab_note.tx"
        self.init_metamodels(tab_grammar_file, tab_note_grammar_file)
    
    def init_metamodels(self, tab_grammar_file, tab_note_grammar_file):
        """Initializes metamodels with grammars specified in tab_grammar_file and tab_note_grammar_file."""
        if tab_grammar_file:
            self.tab_metamodel = metamodel_from_file(tab_grammar_file)
        if tab_note_grammar_file:
            self.tab_note_metamodel = metamodel_from_file(tab_note_grammar_file)
    
    def extract_strings(self, tab_string):
        """Extracts guitar tablature model (textx) from a tab_string."""
        tab_strings_model = self.tab_metamodel.model_from_str(tab_string)
        
        # remove trailing '||'
        for string in tab_strings_model.strings:
            string.chars = string.chars[:-2]
        
        return tab_strings_model
    
    def extract_note_symbols(self, tab_strings_model, additional_dashes=0):
        """Extracts note characters from tab_strings_model and place them in a list of beat columns."""
        if len(tab_strings_model.strings) == 0:
            raise ParsingException("string list empty")
        
        if any(len(string.chars) == 0 for string in tab_strings_model.strings):
            raise ParsingException("there are empty strings")
        
        if not all(len(string.chars) == len(tab_strings_model.strings[0].chars) for string in tab_strings_model.strings):
            raise ParsingException("not all strings are of the same length")
        
        if not all(string.chars[-1] == '-' for string in tab_strings_model.strings):
            raise ParsingException("not all strings end with '-'")
        
        columns = []
        
        while True:
            
            # if nothing left to parse it's the end
            if len(tab_strings_model.strings[0].chars) == 0:
                return columns
            
            note_chars_column = []
            
            for string in tab_strings_model.strings:
                # characters before the first '-' go to note_chars, others go to string.chars
                note_chars, string.chars = string.chars.split('-', 1)
                
                # if it is a pause set note_chars to '-' and eat another '-' because split() didn't
                if note_chars == '':
                    note_chars = '-'
                    self._eat_dashes(string, 1)
                
                note_chars_column.append(note_chars)
                
                # recognise a note using textx
                
            columns.append(note_chars_column)
                    
            # find maximum note character length
            max_length = len(max(note_chars_column, key=len))
            
            # eat max_length number of dashes from all other strings
            for string, chars in zip(tab_strings_model.strings, note_chars_column):
                # if all chars to eat are '-' eat, else error
                self._eat_dashes(string, (max_length - len(chars)) + additional_dashes)
    
    def _eat_dashes(self, string, n):
        """Remove n number of leading dashes, if non dash character is encountered ParsingException is thrown."""
        if n == 0:
            return
        elif len(string.chars) == 0:
            raise ParsingException("expected '-'")
        elif not all(c == '-' for c in string.chars[:n]):
            raise ParsingException("expected '-'")
        else:
            string.chars = string.chars[n:]
    
    def parse_note(self, tab_note_symbol):
        """Create a tab_note_model (textx) from a tab_note_symbol string."""
        return self.tab_note_metamodel.model_from_str(tab_note_symbol)
    
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
    
    def parse_tablature_string(self, tab_string):
        """Extracts tablature string model and then parses it."""
        tab_strings_model = self.extract_strings(tab_string)
        return self.parse_tablature_model(tab_strings_model)
    
    def parse_tablature_model(self, tab_model):
        """Parses the tablature string model and returns a list of mingus NoteContainers that represent beats (columns in the tablature) filled with TabNotes."""
        
        tab_note_symbols = self.extract_note_symbols(tab_model)
        
        ret = []
        
        # for every beat add a NoteContainer
        for beat in tab_note_symbols:
            
            note_container = NoteContainer()
            
            # add every note to note_container
            for note_symbol, string in zip(beat, tab_model.strings):
                
                note_model = self.parse_note(note_symbol)
                
                # skip rests
                if note_model == '-':
                    continue
                
                note_num = self._note_num_from_fret(note_model.fret, string.height)
                note = TabNote(pm=note_model.pm)
                note.from_int(note_num)
                note_container.add_note(note)
            
            ret.append(note_container)
        
        return ret
    
