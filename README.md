# Kicad-Annotator
Python based annotator for Kicad sch files, which groups components by label/type/footprint

It works as follows:

1. Group by label, type, and footprint.<br> ![Table](https://i.imgur.com/6YGpvwM.png)
2. Start with the top left component of each group and file.<br>![Routing](https://i.imgur.com/uqjmNQk.png)
3. Go to the nearest neighbour.


## Why this method?

This is primarily for hand soldering one-sided boards. What I do is print the symbol fields table from kicad, sorted by reference. Then go through with a spool of components one at a time. Ex:

1. R1-**R10** are 10k 0805 resistors. Grab 10 of them and attach them to any R footprint valued R10 or below.
2. R11-R15 are 10 ohm 0805 resistors. Grab 5 of them and attach them to any *unoccupied* R footprint valued R15 or below.
3. Repeat until you reach the end of the list.

This means you don't have to look up each reference for each component. Just look if the reference value is lower than the highest one for that part.

## Install

If you have python 3.8.5+ installed, you can run src/ComponentSorter.py

If you don't, you can run the exe in build.

## How to use

1. Click the big "Select Project File" button.
2. Navigate to your kicad project, and select the project file you want to update. (Note: It will only update the schematic named the same as your project, and any sub-schematics of that)
3. If this is the first time you run this script on that project, backups of the affected schematics will be created with the file extension .csbup. If a backup exists, you will be prompted if you want to overwrite it. Only overwrite a backup once you are sure the current .sch works.
4. If everything worked as it should, your sch file(s) will be annotated. 
5. If you have the schematic open in kicad, close it and open it again.
6. [Opt] PCB files will not be updated. **Verify that your schematic file annotated properly in Kicad**. Then in Pcbnew, clickt he Update PCB from schematic button to update the annotations.


