'''
Created on Dec 13, 2014

@author: Milos
'''
from textx.metamodel import metamodel_from_file


class Song:
    def interpret(self, model):
        print(" {} \n {} \n {}/{} \n".format(model.header.name,model.header.author,
                                            model.header.tempoup,model.header.tempodown))
        for seq in model.sequences:
            print("{} {}".format(seq.type,seq.name))
            for val in seq.value.chords:
                print val.prefix.chord.base

if __name__ == "__main__":
    robot_mm = metamodel_from_file('grammer/composition.tx', debug=False)
    robot_model = robot_mm.model_from_file('examples/track.song')
    
    music = Song()
    music.interpret(robot_model)