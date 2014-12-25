'''
Created on Dec 25, 2014

@author: zeljko.bal
'''

from os.path import isfile

from pytabs.composition.composition import parse_composition_file
from pytabs.player.player import play


INSTRUMENTS_DIR = "instruments/"
SONGS_DIR = "songs/"

examples = ['smoke_on_the_water.song']
instrument_dependencies={'Saber_5ths_and_3rds.sf2':'http://www.hammersound.com/cgi-bin/soundlink_download2.pl/Download%20USA;Saber_5ths_and_3rds.rar;724',
                         'Soundfont BassFing.sf2':'http://www.hammersound.com/cgi-bin/soundlink_download2.pl/Download%20USA;BassFing.rar;740'
                         }

has_unresolved = False
for instrument in instrument_dependencies.keys():
    if not isfile(INSTRUMENTS_DIR+instrument):
        url = instrument_dependencies[instrument]
        print("Please download the soundfont: {instrument} from {url} and place it in the instruments folder.".format(instrument=instrument, url=url))
        has_unresolved = True
        
if not has_unresolved:
    for example in examples:
        composition_model = parse_composition_file(SONGS_DIR+example)
        print("********************************************")
        print("Song: {song_name} by {author}".format(song_name=composition_model.header.name, author=composition_model.header.author))
        print("********************************************")
        play(composition_model)
