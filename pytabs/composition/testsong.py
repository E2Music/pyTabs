'''
Created on Dec 13, 2014

@author: Milos
'''
import os
from textx.metamodel import metamodel_from_file
import pytabs
from pytabs.chords.guitarchords import GuitarChordProcessor, chord_command_processor
from pytabs.guitar.guitar_tablature import GuitarNoteProcessor
from pytabs.tablature.tablature import process_tab_string, TablatureProcessor


class Song:
    def interpret(self, model):
        print(" {} \n {} \n {}/{} \n {}".format(model.header.name,model.header.author,
                                            model.header.beatup,model.header.beatdown,
                                            model.header.tempo))
        for seq in model.sequences:
            print("{} {}".format(seq.type,seq.name))
        
            if(seq.value.__class__.__name__=="GuitarChords"):
                gpc = GuitarChordProcessor(guitar_model=seq.value)
                akords = gpc.guitarmodel_interprete()
                
                print akords
            elif(seq.value.__class__.__name__=="Tablature"):
                processor = TablatureProcessor(GuitarNoteProcessor())
                res = processor.process_tablature_model(seq.value)
                print res



if __name__ == "__main__":
    root_dir = os.path.abspath(os.path.dirname(pytabs.__file__))
    robot_mm = metamodel_from_file(root_dir+'/grammer/composition.tx', debug=False)
    robot_mm.register_obj_processors({'BaseExtended': chord_command_processor,
                                      "PrepExtended": chord_command_processor,
                                      "DecorateExtended":chord_command_processor,
                                      "String":process_tab_string})
    
    robot_model = robot_mm.model_from_file('examples/track.song')
    
    music = Song()
    music.interpret(robot_model)