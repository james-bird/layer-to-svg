#! /usr/bin/env python
import xml.etree.ElementTree as ET
import os
import copy
import sys

export_folder = os.path.splitext(sys.argv[1])[0]
tree = ET.parse(sys.argv[1])
root = tree.getroot()
listoflayers=[]
for g in root.findall('{http://www.w3.org/2000/svg}g'):
	name = g.get('{http://www.inkscape.org/namespaces/inkscape}label')
	listoflayers.append(name)
print(listoflayers)


if not os.path.exists(export_folder):
	os.makedirs(export_folder)

# remove background layers
background_layers = [l for l in listoflayers if "background" in l]
if len(background_layers) == 0:
	print("No background")
for layer in background_layers:
	listoflayers.remove(layer)

for counter in range(len(listoflayers)):
	lname = listoflayers[counter]
	if len( lname ) == 1:
		lname = 'char_' + str(ord( lname ))
	james=listoflayers[:]
	temp_tree = copy.deepcopy(tree)
	del james[counter]
	temp_root = temp_tree.getroot()
	for g in temp_root.findall('{http://www.w3.org/2000/svg}g'):
		name = g.get('{http://www.inkscape.org/namespaces/inkscape}label')
		if name in james:
			temp_root.remove(g)
		else:
			style = g.get('style')
			if type(style) is str:
				style = style.replace( 'display:none', 'display:inline' )
				g.set('style', style)
	temp_tree.write( os.path.join( export_folder, lname +'.svg' ) )
