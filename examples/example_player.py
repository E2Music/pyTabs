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

from os.path import isfile, os

from pytabs.composition.composition import parse_composition_file
from pytabs.player.player import play

BASE_DIR = os.path.dirname(os.path.realpath(__file__))+'/'
SONGS_DIR = BASE_DIR+'songs/'
INSTRUMENTS_DIR = SONGS_DIR+'instruments/'

examples = ['smoke_on_the_water.song']
instrument_dependencies={'Saber_5ths_and_3rds.sf2':'http://www.hammersound.com/cgi-bin/soundlink_download2.pl/Download%20USA;Saber_5ths_and_3rds.rar;724',
                         'Soundfont BassFing.sf2':'http://www.hammersound.com/cgi-bin/soundlink_download2.pl/Download%20USA;BassFing.rar;740',
                         'AJH_Piano.sf2':'http://www.hammersound.com/cgi-bin/soundlink_download2.pl/Download%20USA;AJH_Piano.rar;696'
                         }

def play_examples():

    has_unresolved = False
    for instrument in instrument_dependencies.keys():
        if not isfile(INSTRUMENTS_DIR+instrument):
            url = instrument_dependencies[instrument]
            print('Please download the soundfont: "{instrument}" from {url} and place it in the instruments folder at {instruments_dir}.'.format(instrument=instrument, url=url, instruments_dir=INSTRUMENTS_DIR))
            has_unresolved = True
            
    if not has_unresolved:
        for example in examples:
            composition_model = parse_composition_file(SONGS_DIR+example)
            print("********************************************")
            print("Song: {song_name} by {author}".format(song_name=composition_model.header.name, author=composition_model.header.author))
            print("********************************************")
            play(composition_model)

if __name__ == '__main__':
    play_examples()
