'''
Created on Nov 27, 2014

@author: Milos
'''
from types import NoneType

from textx.metamodel import metamodel_from_file


def move_command_processor(move_cmd):
    if move_cmd.number == 0:
        move_cmd.number = ""

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
        
        for c in model.chords:
            if(c.__class__.__name__=="ChordExtended"):
                if(c.suffix):
                    #ima povisilicu ili snizilicu
                    if(c.prefix.decor):
                        #ima molove majeve susove divove itd
                        if(c.prefix.prep):
                            prefixchord = self._prefix_decor_prep(c)
                            suffixchord = self._suffix_decor_prep(c)
                            
                            print("{}/{}".format(prefixchord, suffixchord))
                        #nena nista od toga
                        else:
                            prefixchord = self._prefix_decor_no_prep(c)
                            suffixchord = self._suffix_decor_no_prep(c)
                            
                            print("{}/{}".format(prefixchord, suffixchord))
                            
                    #nema povislicu ili snizilicu
                    else:
                        pass
                        if(c.prefix.prep):
                            prefixchord = self._prefix_no_decor_prep(c)
                            suffixchord = self._suffix_no_decor_prep(c)
                            print("{}/{}".format(prefixchord, suffixchord))
                        else:
                            prefixchord = self._prefix_no_decor_no_prep(c)
                            suffixchord = self._suffix_no_decor_no_prep(c)
                            print("{}/{}".format(prefixchord, suffixchord))
                else:
                    #ima povisilicu ili snizilicu
                    if(c.prefix.decor):
                        
                        #ima molove majeve susove divove itd
                        if(c.prefix.prep):
                            prefixchord = self._prefix_decor_prep(c)
                            print("{}".format(prefixchord))
                        #nena nista od toga
                        else:
                            prefixchord = self._prefix_decor_no_prep(c)
                            print("{}".format(prefixchord)) 
                    #nema povislicu ili snizilicu
                    else:
                        if(c.prefix.prep):
                            prefixchord = self._prefix_no_decor_prep(c)
                            print("{}".format(prefixchord))
                        else:
                            prefixchord = self._prefix_no_decor_no_prep(c)
                            print("{}".format(prefixchord))
            else:
                print("pause {}".format(c.time))



if __name__ == "__main__":
    robot_mm = metamodel_from_file('grammer/chords.tx', debug=False)
    robot_mm.register_obj_processors({'BaseExtended': move_command_processor,
                                      "PrepExtended":move_command_processor,
                                      "DecorateExtended":move_command_processor})
    
    robot_model = robot_mm.model_from_file('examples/rythm.mcx')
    
    music = Music()
    music.interpret(robot_model)