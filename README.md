# Kicad-Annotator - Updated to work as a PCB Plugin!
KiCad now has support for update schematic from PCB. 

It annotates in the following order:

1. Reference (Alphabetical)
2. Value (Numeric where possible)
3. Footprint (Alphabetical)
4. X Position (Numeric)

Example of a sort

![Table](https://i.gyazo.com/d136dec244d2e7cf218fb618de396ef4.png)

On the board (10k 0603 resistor group)
![10k Resistors](https://i.gyazo.com/71dd07f165c1b0ab3800ec80c1472d17.png)

## Why this method?

This is primarily for hand soldering one-sided boards. What I do is print the symbol fields table from kicad. Then go through with a spool of components one at a time. Ex:

1. R1-**R10** are 10k 0805 resistors. Grab 10 of them and attach them to any R footprint valued R10 or below. Start from the left. If you soldered R2 and the next component you see is R4, you know that R3 is between R2 and R4 on the X axis.
2. R11-**R15** are 10 ohm 0805 resistors. Grab 5 of them and attach them to any *unoccupied* R footprint valued R15 or below.
3. Repeat until you reach the end of the list.

This means you don't have to look up each reference for each component. Just look if the reference value is lower or equal to the highest value for that part.

## Install / Usage

1. Download HandSolderAnnotate.py from this repo.
2. Put it in your KiCad plugin directory (on windows that's under Documents/KiCad/<version>/scripting/plugins)
3. Open the PCB editor and go to Tools > External Plugins > Refresh Plugins.
4. Go back to the same menu and Click Hand Solder Annotate to annotate your board. 

