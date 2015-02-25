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
Created on Dec 13, 2014

@author: Milos
'''
import os

from textx.metamodel import metamodel_from_file

import pytabs
from pytabs.chords.guitarchords import GuitarChordProcessor, chord_command_processor, chord_interval_processor
from pytabs.guitar.guitar_tablature import GuitarNoteProcessor
from pytabs.tablature.tablature import TablatureProcessor
from pytabs.keyboards.keyboard_tablature import KeyboardNoteProcessor

class Song:
    def interpret(self, model):
        print(" {} \n {} \n {}/{} \n {}".format(model.header.name,model.header.author,
                                            model.header.beatup,model.header.beatdown,
                                            model.header.tempo))
        print "---------"*4
         
        for sf in model.imports.soundfonts:
            print "{} {}".format(sf.name, sf.path)
        
        print "---------"*4
        
        for seq in model.sequences:
            print("{} {}".format(seq.type,seq.name))
            if(seq.value.__class__.__name__=="GuitarChords" and seq.type == "guitar-rhythm"):
                gpc = GuitarChordProcessor(guitar_model=seq.value)
                akords = gpc.guitarmodel_interprete()
                
                print akords
            elif(seq.value.__class__.__name__=="Tablature" and seq.type == "guitar-solo"):
                processor = TablatureProcessor(GuitarNoteProcessor())
                res = processor.process_tablature_model(seq.value)
                print res
            
            elif(seq.value.__class__.__name__=="Tablature" and seq.type == "keyboards"):
                processor = TablatureProcessor(KeyboardNoteProcessor)
                res = processor.process_tablature_model(seq.value)
                print res
        
        print "---------"*4
        
        for segment in model.segments:
            print segment.name
            
        print "---------"*4
        
        for track in model.timeline.tracks:
            for part in track.segmentlist:
                print("{} {}".format(part.sequence.name,
                                     part.soundfont.name))

        print "---------"*4

if __name__ == "__main__":
    root_dir = os.path.abspath(os.path.dirname(pytabs.__file__))
    robot_mm = metamodel_from_file(root_dir+'/grammar/composition.tx', debug=False)
    robot_mm.register_obj_processors({'BaseExtended': chord_command_processor,
                                      "PrepExtended": chord_command_processor,
                                      "DecorateExtended":chord_command_processor,
                                      "ChordDuration":chord_interval_processor})
    
    robot_model = robot_mm.model_from_file('examples/track.song')
    
    music = Song()
    music.interpret(robot_model)
