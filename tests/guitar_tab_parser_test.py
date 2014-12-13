'''
Created on Dec 12, 2014

@author: zeljko.bal
'''
from textx.exceptions import TextXSyntaxError
import unittest

from mingus.containers import Note

from pytabs.guitar.guitar_tablature import GuitarNoteProcessor
from pytabs.tablature.tablature import TablatureParser, ParsingException


class Test(unittest.TestCase):

    def setUp(self):
              
        self.parser = TablatureParser(GuitarNoteProcessor())
        
        self.test_tab_empty = """
        e|-0-||
        B|-0-||
        G|-0-||
        D|-0-||
        A|-0-||
        E|-0-||
        """
        
        self.test_tab_frets = """
        e|-1-||
        B|-2-||
        G|-3-||
        D|-4-||
        A|-5-||
        E|-6-||
        """
        
        self.test_tab_pm = """
        e|-0pm-||
        B|-0---||
        G|-0pm-||
        D|-0---||
        A|-0pm-||
        E|-0---||
        """
        
        self.test_tab_rests = """
        e|-0-||
        B|---||
        G|-0-||
        D|---||
        A|-0-||
        E|---||
        """
        
        self.test_tab_end_with_dash = """
        e|-0-||
        B|-10||
        G|-0-||
        D|-0-||
        A|-0-||
        E|-0-||
        """
        
        self.test_tab_equal_length = """
        e|-0-||
        B|-1-||
        G|-0-5-||
        D|-0-||
        A|-0-6-||
        E|-0-||
        """
        
        self.test_tab_missplaced_note = """
        e|-0-7--4-||
        B|-1--5-5-||
        G|-0-53-6-||
        D|-0-6--7-||
        A|-0-6--4-||
        E|-0---7--||
        """
        
        self.test_tab_multiple_columns = """
        e|-0-7--4-||
        B|-5-5--5-||
        G|-0-53-6-||
        D|-0-6--7-||
        A|-0-6--4-||
        E|-0----7-||
        """
    
    def test_empty(self):    
        note_container = self.parser.parse_tablature_string(self.test_tab_empty)[0]
        self.assertEquals(note_container[0], Note('E-3'))
        self.assertEquals(note_container[1], Note('A-3'))
        self.assertEquals(note_container[2], Note('D-4'))
        self.assertEquals(note_container[3], Note('G-4'))
        self.assertEquals(note_container[4], Note('B-4'))
        self.assertEquals(note_container[5], Note('E-5'))
        
    def test_frets(self):
        note_container = self.parser.parse_tablature_string(self.test_tab_frets)[0]
        self.assertEquals(note_container[0], Note('A#-3'))
        self.assertEquals(note_container[1], Note('D-4'))
        self.assertEquals(note_container[2], Note('F#-4'))
        self.assertEquals(note_container[3], Note('A#-4'))
        self.assertEquals(note_container[4], Note('C#-5'))
        self.assertEquals(note_container[5], Note('F-5'))
    
    def test_pm(self):
        note_container = self.parser.parse_tablature_string(self.test_tab_pm)[0]
        self.assertFalse(note_container[0].pm)
        self.assertTrue(note_container[1].pm)
        self.assertFalse(note_container[2].pm)
        self.assertTrue(note_container[3].pm)
        self.assertFalse(note_container[4].pm)
        self.assertTrue(note_container[5].pm)
    
    def test_equal_length(self):
        with self.assertRaises(ParsingException):
            self.parser.parse_tablature_string(self.test_tab_equal_length)
    
    def test_missplaced_note(self):
        with self.assertRaises(ParsingException):
            self.parser.parse_tablature_string(self.test_tab_missplaced_note)
    
    def test_end_with_dash(self):
        with self.assertRaises(TextXSyntaxError):
            self.parser.parse_tablature_string(self.test_tab_end_with_dash)
    
    def test_rests(self):
        note_container = self.parser.parse_tablature_string(self.test_tab_rests)[0]
        self.assertEquals(note_container[0], Note('A-3'))
        self.assertEquals(note_container[1], Note('G-4'))
        self.assertEquals(note_container[2], Note('E-5'))
        self.assertEquals(len(note_container), 3)
        
    def test_multiple_columns(self):
        self.assertEquals(len(self.parser.parse_tablature_string(self.test_tab_multiple_columns)), 3)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()