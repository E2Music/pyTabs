'''
Created on Nov 27, 2014

@author: Milos
'''
"""
    Procesor koji ce u slucaju da se pojavi akord bez pridruzene INT vrednosti, 
    prebaciti 0 u prazan string. Na ovaj nacin mingus moze da svira samo akord.
    
    Args:move_cmd model koji se proverava
    
"""
import os
from types import NoneType

from textx.metamodel import metamodel_from_file


def move_command_processor(move_cmd):
    if move_cmd.number == 0:
        move_cmd.number = ""

"""
    Klasa koja opisuje model akorada koji se dobijaju parsiranjem ulaznog
    fajla na osnovu zadate gramatike
"""
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
                            
                            print("{}/{}".format(prefixchord, suffixchord))
                            chords.append("{}/{}".format(prefixchord, suffixchord))
                        #nena nista od toga
                        else:
                            prefixchord = self._prefix_decor_no_prep(c)
                            suffixchord = self._suffix_decor_no_prep(c)
                            
                            print("{}/{}".format(prefixchord, suffixchord))
                            chords.append("{}/{}".format(prefixchord, suffixchord))
                    #nema povislicu ili snizilicu
                    else:
                        pass
                        if(c.prefix.prep):
                            prefixchord = self._prefix_no_decor_prep(c)
                            suffixchord = self._suffix_no_decor_prep(c)
                            
                            print("{}/{}".format(prefixchord, suffixchord))
                            chords.append("{}/{}".format(prefixchord, suffixchord))
                        else:
                            prefixchord = self._prefix_no_decor_no_prep(c)
                            suffixchord = self._suffix_no_decor_no_prep(c)
                            
                            print("{}/{}".format(prefixchord, suffixchord))
                            chords.append("{}/{}".format(prefixchord, suffixchord))
                else:
                    #ima povisilicu ili snizilicu
                    if(c.prefix.decor):
                        
                        #ima molove majeve susove divove itd
                        if(c.prefix.prep):
                            prefixchord = self._prefix_decor_prep(c)
                            
                            print("{}".format(prefixchord))
                            chords.append("{}".format(prefixchord))
                        #nena nista od toga
                        else:
                            prefixchord = self._prefix_decor_no_prep(c)
                            
                            print("{}".format(prefixchord)) 
                            chords.append("{}".format(prefixchord))
                    #nema povislicu ili snizilicu
                    else:
                        if(c.prefix.prep):
                            prefixchord = self._prefix_no_decor_prep(c)
                            
                            print("{}".format(prefixchord))
                            chords.append("{}".format(prefixchord))
                        else:
                            prefixchord = self._prefix_no_decor_no_prep(c)
                            print("{}".format(prefixchord))
                            chords.append("{}".format(prefixchord))
            else:
                print("pause {}".format(c.time))


GRAMMAR_PATH = os.path.dirname(os.path.realpath(__file__)) + "/grammar/"

class GuitarChordProcessor(object):
    def __init__(self, guitar_chords_grammar_file=None):
        
        if not guitar_chords_grammar_file:
            guitar_chords_grammar_file = GRAMMAR_PATH + "chords.tx"
        
        self.guitar_chords_mm = metamodel_from_file(guitar_chords_grammar_file, debug=False)
        self.guitar_chords_mm.register_obj_processors({'BaseExtended': self.chord_command_processor,
                                      "PrepExtended":move_command_processor,
                                      "DecorateExtended":move_command_processor})
        #guitar_chords_model = guitar_chords_mm.model_from_file('examples/rythm.mcx')
        
    
    def chord_command_processor(self,move_cmd):
        """
        Procesor koji ce u slucaju da se pojavi akord bez pridruzene INT vrednosti, 
        prebaciti 0 u prazan string. Na ovaj nacin mingus moze da svira samo akord.
        
        Args:move_cmd model koji se proverava
        
        """
        if move_cmd.number == 0:
            move_cmd.number = ""
            
    def guitarchords_model_from_file(self, file_path):
        #'examples/rythm.mcx'
        self.guitar_chords_model = self.guitar_chords_mm.model_from_file(file_path)
        
    def guitarmodel_interprete(self):
        music = Music()
        music.interpret(self.guitar_chords_model)
    
if __name__ == "__main__":
    robot_mm = metamodel_from_file('grammer/chords.tx', debug=False)
    robot_mm.register_obj_processors({'BaseExtended': move_command_processor,
                                      "PrepExtended":move_command_processor,
                                      "DecorateExtended":move_command_processor})
    
    robot_model = robot_mm.model_from_file('examples/rythm.mcx')
    
    music = Music()
    music.interpret(robot_model)