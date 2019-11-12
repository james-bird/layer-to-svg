#! /usr/bin/python3
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

try:
	listoflayers.remove('background')
except ValueError:
	print("No background")
for counter in range(len(listoflayers)):
	james=listoflayers[:]
	temp_tree = copy.deepcopy(tree)
	del james[counter]
	print(james)
	temp_root = temp_tree.getroot()
	for g in temp_root.findall('{http://www.w3.org/2000/svg}g'):
		name = g.get('{http://www.inkscape.org/namespaces/inkscape}label')
		if name in james:
			temp_root.remove(g)
	temp_tree.write(os.path.join(export_folder,listoflayers[counter]+'.svg'))