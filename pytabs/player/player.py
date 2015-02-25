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
Created on Dec 25, 2014

@author: zeljko.bal
'''
from threading import Thread

from mingus.midi import fluidsynth


class PlayerThread(Thread):
    def __init__(self, track, tempo, instrument):
        
        self.sequencer = fluidsynth.FluidSynthSequencer()
        self.sequencer.start_audio_output()
        self.sequencer.load_sound_font(instrument)
        self.sequencer.fs.program_reset()
        
        def execute():
            self.sequencer.play_Track(track, 1, tempo)
        
        super(PlayerThread, self).__init__(target=execute)

def play(composition_model):
    
    segments = []
    
    # create threads
    for segment_model in composition_model.timeline.tracks:
        segment = []
        
        for sequence_model in segment_model.segmentlist:
            segment.append(PlayerThread(sequence_model.sequence.value, composition_model.header.tempo, composition_model.imports[sequence_model.soundfont.name]))
        
        segments.append(segment)
    
    # play threads segment by segment
    for segment in segments:
        for t in segment:
            t.start()
        
        for t in segment:
            t.join()
