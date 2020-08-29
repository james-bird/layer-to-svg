# layer-to-svg

This is a python script which takes an Inkscape svg file and creates separate svg files for each layer.
Each new file takes the name of the layer.
If a layer called 'background' exists, then that layer is common to all the files produced.

## Usage
* For easy of use, move layer2svg.py to same directory as multi-layered file. Alternatively, pass path to file.
* Run `python3 layer2svg.py multi-layered-file.svg`
* Layers will be created in a new folder

This was script was not written as an Inkscape extension, just a quick way to post-process Inkscape files, often as part of larger scripts.
