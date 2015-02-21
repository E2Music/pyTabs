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

