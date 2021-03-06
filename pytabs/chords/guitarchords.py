#    PyTabs - Simplified music notation DSL, interpreter and player.
#    Copyright (C) 2014, Milos Simic
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
Created on Nov 27, 2014

@author: Milos
'''
import os
from mingus.containers import NoteContainer
from mingus.core.chords import from_shorthand
from textx.metamodel import metamodel_from_file
import pytabs
from types import NoneType


GRAMMAR_PATH = os.path.abspath(os.path.dirname(pytabs.__file__))+'/grammar/'

DEFAULT_CHORD_DURATION = 4
DEFAULT_EMPTY_NUMBER = ""

class Music:

    def _prefix_decor_prep(self, c):
        prefixret = "".join([c.prefix.chord.base,str(c.prefix.chord.number),
                             c.prefix.decor.name,str(c.prefix.decor.number),
                             c.prefix.prep.name,str(c.prefix.prep.number)])
        return prefixret
    
    def _suffix_decor_prep(self, c):
        suffixret = "".join([c.suffix.chord.base,str(c.suffix.chord.number),
                             c.suffix.decor.name,str(c.suffix.decor.number),
                             c.suffix.prep.name,str(c.suffix.prep.number)])
        return suffixret
    
    def _prefix_decor_no_prep(self, c):
        prefixret = "".join([c.prefix.chord.base,str(c.prefix.chord.number),
                             c.prefix.decor.name,str(c.prefix.decor.number)])
        return prefixret
    
    def _suffix_decor_no_prep(self, c):
        suffixret = "".join([c.suffix.chord.base,str(c.suffix.chord.number),
                             c.suffix.decor.name,str(c.suffix.decor.number)])
        return suffixret
    
    def _prefix_no_decor_prep(self, c):
        prefixret = "".join([c.prefix.chord.base,str(c.prefix.chord.number),
                             c.prefix.prep.name,str(c.prefix.prep.number)])
        return prefixret
    
    def _suffix_no_decor_prep(self, c):
        suffixret = "".join([c.suffix.chord.base,str(c.suffix.chord.number),
                             c.suffix.prep.name,str(c.suffix.prep.number)])
        return suffixret
    
    def _prefix_no_decor_no_prep(self, c):
        prefixret = "".join([c.prefix.chord.base,str(c.prefix.chord.number)])
        
        return prefixret
    
    def _suffix_no_decor_no_prep(self, c):
        suffixret = "".join([c.suffix.chord.base,str(c.suffix.chord.number)])
        
        return suffixret
    
    def _add_note(self, note_name):
        """
        Metoda koja na osnovu imena akorda vraca NoteContainer iz imena. Ova
        metoda je direktno zavisna od pogloge tj mingusa u ovoj verziji!
        """
        
        n = NoteContainer()
        n.add_notes(from_shorthand(note_name))
        
        return n
    
    def _interval_time(self, chord):
        """
        Metoda koja proverava da li je zadat interval za duzinu trajanja akorda.
        Ako je zadata vrednost uzima je, ako nije vraca neku default vrednost
        """
        
        return chord.duration.time if type(chord.duration) is not NoneType else DEFAULT_CHORD_DURATION
    
    def interpret(self, model):
        chords = []
        
        for c in model.value:
            if(c.__class__.__name__=="ChordExtended"):
                if(c.suffix):
                    #ima povisilicu ili snizilicu
                    if(c.prefix.decor):
                        #ima molove majeve susove divove itd
                        if(c.prefix.prep):
                            prefixchord = self._prefix_decor_prep(c)
                            suffixchord = self._suffix_decor_prep(c)
                            container = (self._add_note("{}/{}".format(prefixchord, suffixchord)),self._interval_time(c))
                            chords.append(container)
                        #nena nista od toga
                        else:
                            prefixchord = self._prefix_decor_no_prep(c)
                            suffixchord = self._suffix_decor_no_prep(c)
                            container = (self._add_note("{}/{}".format(prefixchord, suffixchord)),self._interval_time(c))
                            chords.append(container)
                    #nema povislicu ili snizilicu
                    else:
                        pass
                        if(c.prefix.prep):
                            prefixchord = self._prefix_no_decor_prep(c)
                            suffixchord = self._suffix_no_decor_prep(c)
                            container = (self._add_note("{}/{}".format(prefixchord, suffixchord)),self._interval_time(c))
                            chords.append(container)
                        else:
                            prefixchord = self._prefix_no_decor_no_prep(c)
                            suffixchord = self._suffix_no_decor_no_prep(c)
                            container = (self._add_note("{}/{}".format(prefixchord, suffixchord)),self._interval_time(c))
                            chords.append(container)
                else:
                    #ima povisilicu ili snizilicu
                    if(c.prefix.decor):
                        #ima molove majeve susove divove itd
                        if(c.prefix.prep):
                            prefixchord = self._prefix_decor_prep(c)
                            container = (self._add_note("{}".format(prefixchord)), self._interval_time(c))
                            chords.append(container)
                        #nena nista od toga
                        else:
                            prefixchord = self._prefix_decor_no_prep(c)
                            container = (self._add_note("{}".format(prefixchord)), self._interval_time(c))
                            chords.append(container)
                    #nema povislicu ili snizilicu
                    else:
                        if(c.prefix.prep):
                            prefixchord = self._prefix_no_decor_prep(c)
                            container = (self._add_note("{}".format(prefixchord)), self._interval_time(c))
                            chords.append(container)
                        else:
                            prefixchord = self._prefix_no_decor_no_prep(c)
                            container = (self._add_note("{}".format(prefixchord)), self._interval_time(c))
                            chords.append(container)
            else:
                pause = PauseChord(duration=c.time)
                container = (pause, pause.duration)
                chords.append(container)
        
        self.akordi = [x for x in chords]

class PauseChord(object):
    """
        Class that represent a pose Chord. 
        Args (int) duration :duration of time how long pause will last
    """
    
    def __init__(self,duration):
        self.value = None
        self.duration = duration
        self.name = "Pause"
        
    def __str__(self, *args, **kwargs):
        return "{}".format(self.name)
    
    def __repr__(self, *args, **kwargs):
        return  self.__str__()

def chord_command_processor(move_cmd):
    """
    Procesor koji ce u slucaju da se pojavi akord bez pridruzene INT vrednosti, 
    prebaciti 0 u prazan string. Na ovaj nacin mingus moze da svira samo akord.
        
    Args:move_cmd model koji se proverava
        
    """
    if move_cmd.number == 0:
        move_cmd.number = DEFAULT_EMPTY_NUMBER

def chord_interval_processor(move_cmd):
    """
    Procesor koji ce u slucaju da je interval trajanja akorda ostavljen na 0
    prebaciti na 4, Razlog tome je posto mingus ocekuje neku vrednost koliko
    traje akord ceo ton, pola,osminu,cetrtinu,....
    
    Args:move_cmd model koji se proverava
    
    """
    if move_cmd.time == 0:
        move_cmd.time = DEFAULT_CHORD_DURATION

class GuitarChordProcessor(object):
    """
        Class that will take file where chords are and/or take model of chords
        Args:
            (string):guitar_chords_grammar_file where grammer that
            represent chords is
            guitar_model (textx model):model to process 
    """
    
    def __init__(self, guitar_chords_grammar_file=None, guitar_model = None):
        
        if not guitar_chords_grammar_file:
            guitar_chords_grammar_file = GRAMMAR_PATH +'chords.tx'
        
        self.guitar_chords_mm = metamodel_from_file(guitar_chords_grammar_file, debug=False)
        self.guitar_chords_mm.register_obj_processors({'BaseExtended': chord_command_processor,
                                      "PrepExtended":chord_command_processor,
                                      "DecorateExtended":chord_command_processor,
                                      "ChordDuration":chord_interval_processor})
        self.guitar_chords_model = guitar_model
        #guitar_chords_model = guitar_chords_mm.model_from_file('examples/rythm.mcx')
            
    def guitarchords_model_from_file(self, file_path):
        """
            Read sample from file and trasport it to metamodel in text
            Args:
                file_path (string):path where sample is
        """
        
        self.guitar_chords_model = self.guitar_chords_mm.model_from_file(file_path)
        
    def guitarchords_model_from_str(self, model_str):
        """
            Read sample from string and trasport it to metamodel in text
            Args:
                file_path (string):string of sample
        """
        
        self.guitar_chords_model = self.guitar_chords_mm.model_from_str(model_str)
        
    def guitarmodel_interprete(self):
        """
            For a givem metamodel prepare model by iterate trough metamodel
        """
        
        music = Music()
        music.interpret(self.guitar_chords_model)
        
        return music.akordi


    
if __name__ == "__main__":
    
    root_dir = os.path.abspath(os.path.dirname(pytabs.__file__))
    gpc = GuitarChordProcessor()
    gpc.guitarchords_model_from_file('examples/rythm2.mcx')
    akords = gpc.guitarmodel_interprete()
    
    for b in akords:
        print b
    
