# Kicad-Annotator
Python based annotator for Kicad sch files, which groups components by label/type/footprint

It works as follows:

1. Group by label, type, and footprint.<br> ![Table](https://i.imgur.com/6YGpvwM.png)
2. Start with the top left component of each group and file.<br>![Routing](https://i.imgur.com/uqjmNQk.png)
3. Go to the nearest neighbour.





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


