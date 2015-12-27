#!/usr/bin/env python

import sys, os, subprocess, copy

if len(sys.argv) == 1:
	print """
usage: renamefonts.py <font files to rename>

This script requires FontTools/TTX to extract the font name from the font file itself, which is obviously highly important to the script's operation.

You can rename as many font files as you like. Separate them with spaces only, not commas. On OS X, it's easiest to simply drag all your files into Terminal from the Finder.

Font format can be ttf (TrueType), or otf (OpenType). FontTools/TTX apparently also works with Type 1 fonts, but I haven't tested this.
"""

FNULL = open(os.devnull, 'w')

TTFList = sys.argv
TTFList.remove(__file__)

ConvertToTTX = []
ConvertToTTX = copy.copy(TTFList)
ConvertToTTX.insert(0, 'ttx')

try:
    subprocess.call(ConvertToTTX, stdout=FNULL, stderr=subprocess.STDOUT)
except OSError as e:
    print """
This script requires FontTools/TTX to extract the font name from the font file itself, which is obviously highly important to the script's operation.

Your system does not appear to have FontTools/TTX installed.
Check if it's installed, and if not, install it.
If it is installed, but the script still fails, check if it's added to the path.
"""
fileList = [os.path.splitext(i)[0] for i in TTFList]

lookup = '<namerecord nameID="4"'

for fNum, file in enumerate(fileList):
    myFile = open(file + '.ttx')
    fileLines = myFile.readlines()
    myFile.close()
    extension = os.path.splitext(TTFList[fNum])[1]
    directory = os.path.split(TTFList[fNum])[0]
    for lNum, line in enumerate(fileLines):
        if lookup in line:
            nameLine = fileLines[lNum + 1]
            newFileName = nameLine.strip() + extension
            os.rename(file + extension, os.path.join(directory, newFileName))
            break

for file in fileList:
	os.remove(file + '.ttx')

print "\nFiles have been renamed successfully."
