import os, sys
from fileEditor import DebugError, run as writeFiles
import tkinter as tk
from tkinter import font, filedialog, messagebox

rootWindow = tk.Tk()
rootWindow.rowconfigure(0, weight=1)
rootWindow.columnconfigure(0, weight=1)
#rootWindow.rowconfigure(0, weight=1)
#rootWindow.columnconfigure(0, weight=1)
rootWindow.title("KiCad Annotator")
rootWindow.geometry("300x100")

buttonFont = font.Font(size=20)

def fileButtonClicked():
	print("Clicked button")
	filepath = filedialog.askopenfilename(title="Select Kicad project file", filetypes=[("kicad project files","*.pro")])
	if not filepath:
		return

	filedir = os.path.dirname(os.path.realpath(filepath))
	filename = os.path.splitext(os.path.basename(os.path.realpath(filepath)))[0]
	try:
		stats = writeFiles(filedir, filename+".sch", True)
		text = "Update complete:\n  - Files updated: "+str(stats["files"])+"\n  - Components updated: "+str(stats["comp"])
		if stats["bup"]:
			text = text+"\n\nBackups have been made, with .csbup appended to the file name."
		text = text+"\n\nNOTE: Only .sch files have been updated. Any PCB files will need to be updated by you.\nNOTE: If your .sch file is open you will need to close and re-open it to see the changes."
		messagebox.showinfo(title="Operation complete!", message=text)
	except DebugError as e:
		messagebox.showerror(message=str(e))
	except:
		messagebox.showerror(message="Unknown error occurred, try running from the command line")



fileButton = tk.Button(rootWindow, text="Select Project File", command=fileButtonClicked)
fileButton["font"] = buttonFont
fileButton.grid(column=0, row=0)





rootWindow.mainloop()