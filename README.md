# PyTabs

PyTabs is a DSL (Domain Specific Language) for simplified music notation and composition description. The projet includes an interpreter that creates an object model of a composition based on the provided description and a player that renders music based on that model, all of which is accessable through a simple GUI.

In PyTabs language you can describe a composition which is composed of several segments played sequentially. Each segment consists of one or more sequences that are played together. Each sequence is played by a specified instrument and described in one of supported notations. Currently PyTabs supports guitar and keyboard tablatures and guitar chords and it can easily be extended to support other notations.

An example of a composition in PyTabs language can be found in examples/songs/smoke_on_the_water.song .

## Technical description

PyTabs is implemented in python programming language, it uses [textX] python library to define the language grammar and interpret compositions creating a python object model. The model obtained from textX is then interpreted for each notation and transformed to a composition model that uses [mingus] note container objects for note representation. This model can then be played using the [FluidSynth] library wrapper provided in mingus. FluidSynth uses [SoundFont] samples to play the music, so different soundfonts can be used to play different instrument in the same composition.

## Installation

####Requirements:
- python v2.7
- [textX]
```sh
$ pip install textX
```
- [mingus]
```sh
$ pip install mingus
```
- [PySide] (for GUI)
```sh
$ pip install PySide
```
- [FluidSynth] a dll should be placed in PATH, you can compile it yourself from [FluidSynth source] or download one from here http://svn.drdteam.org/zdoom/fluidsynth.7z (ofcourse download at your own risk, link found via stackoverflow).

After installing all the requirements you can download or clone and start using the PyTabs project.

## Getting started

To run the example song you can simply run the play_examples.py sceipt in the root directory of the project.
```sh
$ python play_examples.py
```
The first time you run it, it will tell you to download the necessary soundfont files and where to place them. After that you can run it again and you should be able to hear the music. The example can be found at examples/songs/smoke_on_the_water.song . 

You can also start the GUI by running pytabs\gui\startApp.py script. Enter a valid composition description in PyTabs language such as the one provided in the example and click the play button to play the composition.

License
----
PyTabs is a free and opensource project licensed under [GPLv3].

[textX]:https://github.com/igordejanovic/textX
[mingus]:https://code.google.com/p/mingus/
[PySide]:http://qt-project.org/wiki/PySide
[FluidSynth]:http://www.fluidsynth.org/
[FluidSynth source]:http://sourceforge.net/projects/fluidsynth/files/fluidsynth-1.1.3/
[SoundFont]:http://en.wikipedia.org/wiki/SoundFont
[GPLv3]:http://www.gnu.org/licenses/
