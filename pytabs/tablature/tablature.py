'''
Created on Dec 13, 2014

@author: zeljko.bal
'''
from os.path import os
from textx.metamodel import metamodel_from_file
from mingus.containers.NoteContainer import NoteContainer


GRAMMAR_PATH = os.path.dirname(os.path.realpath(__file__)) + "/grammar/"

class TablatureProcessor:
    """
    Processes tablature model.
    """
    
    def __init__(self, process_note, additional_dashes=0):
        """
        Accepts a process_note(note_symbol, mark_symbol) callable  
        that returns an instance of mingus Note or its subclass.
        """
        assert process_note is not None
        self.process_note = process_note
        self.additional_dashes = additional_dashes
    
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
                    string.chars = self._eat_leading_dashes(string.chars, 1)
                
                note_chars_column.append(note_chars)
                
            columns.append(note_chars_column)
                    
            # find maximum note character length
            max_length = len(max(note_chars_column, key=len))
            
            # eat max_length number of dashes from all other strings
            for string, chars in zip(tab_strings_model.strings, note_chars_column):
                # if all chars to eat are '-' eat, else error
                string.chars = self._eat_leading_dashes(string.chars, (max_length - len(chars)) + additional_dashes)
                
    def extract_string_marks(self, tab_strings_model):
        """Extracts the string mark symbol (at the beginning of the string)."""
        if len(tab_strings_model.strings) == 0:
            raise ParsingException("string list empty")
        
        mark_column = [string.mark for string in tab_strings_model.strings]
        
        if not all(len(mark) == len(mark_column[0]) for mark in mark_column):
            raise ParsingException("not all marks are of the same length")
        
        # extract everything up to the first '-'        
        return [mark.split('-', 1)[0] for mark in mark_column]
    
    def _eat_leading_dashes(self, string, n):
        """Remove n number of leading dashes, if non dash character is encountered ParsingException is thrown."""
        if n == 0:
            return string
        elif len(string) == 0:
            raise ParsingException("expected '-'")
        elif not all(c == '-' for c in string[:n]):
            raise ParsingException("expected '-'")
        else:
            return string[n:]
    
    def process_tablature_model(self, tab_model):
        """Processes the tablature model (using note_processor) and returns a list of mingus NoteContainers that represent beats (columns in the tablature) filled with mingus Notes."""
        
        beats = self.extract_note_symbols(tab_model, self.additional_dashes)
        mark_symbols = self.extract_string_marks(tab_model)
        
        # list of NoteContainer instances
        note_containers = []
        
        # for every beat add a NoteContainer
        for beat in beats:
            
            note_container = NoteContainer()
            
            for note_symbol, mark_symbol in zip(beat, mark_symbols):
                
                # process the note_symbol and mark_symbol and get a Note instance
                note = self.process_note(note_symbol, mark_symbol)
                
                # add every note that is not None to note_container
                if note:
                    note_container.add_note(note)
            
            note_containers.append(note_container)
        
        return note_containers

class TablatureParser:
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
    
    def __init__(self, note_processor, tab_grammar_file=None, additional_dashes=0):
        """Initializes metamodel and processor, if metamodel file is not specified initialize with default file."""
        self.processor = TablatureProcessor(note_processor, additional_dashes)
        
        if not tab_grammar_file:
            tab_grammar_file = GRAMMAR_PATH + "tablature.tx"
        
        self.tab_metamodel = metamodel_from_file(tab_grammar_file)
        self.tab_metamodel.register_obj_processors({'String': process_tab_string})
    
    def parse_tablature_string(self, tab_string):
        """Extracts tablature string model (textx) and then parses it."""
        tab_strings_model = self.tab_metamodel.model_from_str(tab_string)
        return self.processor.process_tablature_model(tab_strings_model)

def process_tab_string(tab_string):
    """Process a String object."""
    # remove trailing '||' from chars
    tab_string.chars = tab_string.chars[:-2]
    
class ParsingException(Exception):
    def __init__(self, args):
        super(ParsingException, self).__init__(args)
