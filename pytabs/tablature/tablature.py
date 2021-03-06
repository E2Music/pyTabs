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
Created on Dec 13, 2014

@author: zeljko.bal
'''
from os.path import os

from mingus.containers import NoteContainer
from textx.metamodel import metamodel_from_file
import pytabs


GRAMMAR_PATH = os.path.abspath(os.path.dirname(pytabs.__file__))+'/grammar/'

class TablatureProcessor:
    """
    Processes tablature model.
    """
    
    def __init__(self, process_note, additional_dashes=0, container_type=NoteContainer):
        """
        Accepts a process_note(note_symbol, mark_symbol) callable  
        that returns a recognised object that can be stored in a container_type (NoteContainer by default).
        A number of additional dashes can be ignored following each note, specified by additional_dashes parameter.
        """
        assert process_note is not None
        self.process_note = process_note
        self.additional_dashes = additional_dashes
        self.container_type = container_type
    
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
            raise ParsingException("expected '-' at: "+string)
        elif not all(c == '-' for c in string[:n]):
            raise ParsingException("expected '-' at: "+string)
        else:
            return string[n:]
    
    def process_tablature_model(self, tab_model):
        """Processes the tablature model (using note_processor) and returns a list of mingus NoteContainers that represent beats (columns in the tablature) filled with mingus Notes."""
        
        beats = self.extract_note_symbols(tab_model, self.additional_dashes)
        mark_symbols = self.extract_string_marks(tab_model)
        
        # list of container_type instances
        container_list = []
        
        # for every beat add a container
        for beat in beats:
            
            container = self.container_type()
            
            for note_symbol, mark_symbol in zip(beat, mark_symbols):
                
                # process the note_symbol and mark_symbol and get a Note instance
                note = self.process_note(note_symbol, mark_symbol)
                
                # add every note that is not None to container
                if note:
                    container += [note]
            
            container_list.append(container)
        
        return container_list

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
    
    def parse_tablature_string(self, tab_string):
        """Extracts tablature string model (textx) and then parses it."""
        tab_strings_model = self.tab_metamodel.model_from_str(tab_string)
        return self.processor.process_tablature_model(tab_strings_model)

class ParsingException(Exception):
    def __init__(self, args):
        super(ParsingException, self).__init__(args)
