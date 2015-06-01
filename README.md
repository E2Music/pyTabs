#<img src="https://raw.githubusercontent.com/E2Music/pyTabs/afcb14757df8b9c051750909fcc00a47a44c142f/logo.jpg" width="100"/> PyTabs

PyTabs is a DSL (Domain Specific Language) for simplified music notation and composition description. The projet includes an interpreter that creates an object model of a composition based on the provided description and a player that renders music based on that model, all of which is accessable through a simple GUI.

In PyTabs language you can describe a composition which is composed of several segments played sequentially. Each segment consists of one or more sequences that are played together. Each sequence is played by a specified instrument and described in one of supported notations. Currently PyTabs supports guitar and keyboard tablatures and guitar chords and it can easily be extended to support other notations.

An example of a composition in PyTabs language can be found in examples/songs/smoke_on_the_water.song . Here is the example with marked composition sections:

![song example screenshot](https://raw.githubusercontent.com/E2Music/pyTabs/afcb14757df8b9c051750909fcc00a47a44c142f/screens/song_example_scheme.png) 

## Technical description

PyTabs is implemented in python programming language, it uses [textX] python library to define the language grammar and interpret compositions creating a python object model. The model obtained from textX is then interpreted for each notation and transformed into a composition model that uses [mingus] note container objects for note representation. This model can then be played using the [FluidSynth] library wrapper provided in mingus. FluidSynth uses [SoundFont] samples to play the music, so different soundfonts can be used to play different instrument in the same composition.

## Installation

####Requirements:
- python v2.7
- [textX] v0.3.1
```sh
$ pip install textX
```
- [mingus] v0.5.0
```sh
$ pip install mingus
```
- [PySide] (for GUI) v1.2.2
```sh
$ pip install PySide
```
- [FluidSynth] 
    - Windows: fluidsynth.dll should be placed in PATH or in PyTabs lib directory (will be added to PATH when running start scripts), you can compile it yourself from [FluidSynth source] or download one from here http://svn.drdteam.org/zdoom/fluidsynth.7z (ofcourse download at your own risk, link found via stackoverflow).
    - Linux (not tested): for package installation see [FluidSynth downloads] or compile it yourself from [FluidSynth source]

After installing all the requirements you can download or clone and start using the PyTabs project.

## Getting started

To run the example song you can simply run the play_examples script in the root directory of the project.
The first time you run it, it will tell you to download the necessary soundfont files and where to place them. After that you can run it again and you should be able to hear the music. The example can be found at examples/songs/smoke_on_the_water.song . 

You can also start the GUI by running the start_gui script in the root directory. Enter a valid composition description in PyTabs language such as the one provided in the example (you can click the 'new' button and choose to open the example file) and click the 'play' button to play the composition.

![gui screenshot](https://raw.githubusercontent.com/E2Music/pyTabs/afcb14757df8b9c051750909fcc00a47a44c142f/screens/gui_screen.png)

You can also check out the grammar definitions in pytabs/grammar. They are easy to understand and can help you write your own compositions.

In order to import your own soundfonts just place the .sf2 files into examples/songs/instruments and add an import statement in the import section of your composition. It should look like:
```
my_instrument_name "instruments/myInstrument.sf2"
```

License
----
PyTabs is a free and opensource project licensed under [GPLv3].

[textX]:https://github.com/igordejanovic/textX
[mingus]:https://code.google.com/p/mingus/
[PySide]:http://qt-project.org/wiki/PySide
[FluidSynth]:http://www.fluidsynth.org/
[FluidSynth source]:http://sourceforge.net/projects/fluidsynth/files/fluidsynth-1.1.3/
[FluidSynth downloads]:http://sourceforge.net/p/fluidsynth/wiki/Download/
[SoundFont]:http://en.wikipedia.org/wiki/SoundFont
[GPLv3]:http://www.gnu.org/licenses/
