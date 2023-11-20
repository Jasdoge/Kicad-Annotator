import shlex, re, math, shutil, os
from tkinter import messagebox

def debug(verbose, *text):
	if not verbose:
		return
	print(*text)

class DebugError(Exception):
	pass

filecache = {}

#helper functions
def findClosestEntry(entries, base):
		dist = 0
		closest = None
		for entry in entries:
			if ("_done" in entry and entry["_done"]) or entry["file"] != base["file"] or base == entry:
				continue
			d = math.sqrt(math.pow(entry["x"]-base["x"], 2)+math.pow(entry["y"]-base["y"], 2))
			if closest == None or d < dist:
				dist = d
				closest = entry
		return closest


targetIterator = 0 #Annotation sequence nr
def assignTarget(component, verbose = False):
	global targetIterator, filecache
	targetIterator = targetIterator +1
	component["_done"] = True
	debug(verbose, "            Assigning component "+component["val"]+" ("+component["uuid"]+") value "+str(targetIterator))
	
	row = component["lnr"]
	file = filecache[component["file"]]
	
	titleline = shlex.split(file[row])
	newid = component["id"]+str(targetIterator)
	oldid = component["oldid"]
	titleline[2] = newid
	# +1 because editor is 1 based and file is 0 based
	debug(verbose, "            Replace title line ("+str(row+1)+") with ", " ".join(titleline), "old:"+oldid, "new:"+newid)
	file[row] = " ".join(titleline)+"\n"

	# Encapsulate because all sub properties need the id in quotes
	newid = '"'+newid+'"'
	oldid = '"'+oldid+'"'

	
	# Search through lines and replace
	for i in range(100):
		line = file[row+i+1]
		#if component["id"]+str(targetIterator) == "R6":
		#	debug(verbose, "!! Row: "+str(row+i+1)+" Search: "+oldid+" in  : "+line+" >> "+str(oldid in line))
			
		if line.startswith("$EndComp"):
			break	
		if oldid in line:
			line = line.replace(oldid, newid)
			file[row+i+1] = line
			debug(verbose, "            Replace sub line ("+str(row+i+2)+") with "+line)
	#debug(verbose, "Line: "+file.readline())



# Takes the base sheet and runs it and any subsheets
def run(rootPath, rootFile, verbose = False):
	global filecache, targetIterator
	targetIterator = 0
	subfiles = [
		rootFile
	]
	entries = []

	filecache = {}
	stats = {
		"files" : 0,	# files updated
		"comp" : 0,		# total components updated
		"bup" : False
	}
	


	for filename in subfiles:
		filename = rootPath+"/"+filename
		debug(verbose, "Opening file: "+filename)
		
		if not os.path.isfile(filename):
			raise DebugError("SCH file not found: "+filename) 

		linenr = 0
		with open(filename) as file:
			filecache[filename] = file.readlines()

		bupfile = filename+".csbup"
		bupExists = os.path.isfile(bupfile)
		if not bupExists or messagebox.askyesno(title="Backup?", default="no", message="Existing backup found, would you like to overwrite it?\n(Only recommended after verifying that your existing schematic file works)"):

			debug(verbose, "making backup:", bupfile)
			stats["bup"] = True
			shutil.copyfile(filename, bupfile)

		while linenr < len(filecache[filename]):
			line = filecache[filename][linenr]

			if line.startswith("$Comp"):
				linenr = linenr+1
				l = filecache[filename][linenr]

				if l.startswith("L "):
					spl = shlex.split(l)
					if spl[-1][0] != "#":	# Hashtag is used in power

						fulluuid = ""
						uuid = ""
						line = linenr
						x = 0
						y = 0
						val = ""
						footprint = ""

						# Read until the next component
						for i in range(50):
							linenr = linenr+1
							l = filecache[filename][linenr]

							if l.startswith("$EndComp"):
								break
							
							if l.startswith("U"):
								spl = shlex.split(l)
								uuid = spl[3]

							if l.startswith("P "):
								spl = shlex.split(l)
								x = int(spl[1])
								y = int(spl[2])

							# This is where the item label is stored
							if l.startswith("F 0 "):
								spl = shlex.split(l)
								fulluuid = id = spl[2]
								endpos = re.search("[0-9\?]", id)
								if endpos == None:
									endpos = -1
								else:
									endpos = endpos.start()
								id = id[0:endpos]

							if l.startswith("F 1 "):
								spl = shlex.split(l)
								val = spl[2]

							if l.startswith("F 2 "):
								spl = shlex.split(l)
								footprint = spl[2]

							if l.startswith("AR Path="):
								endpos = re.search("Ref=", l)
								if endpos != None:
									endpos = endpos.start()+5
									id = l[endpos:]
									endpos = re.search("[0-9\?]", id)
									if endpos == None:
										endpos = -1
									else:
										endpos = endpos.start()
									id = id[:endpos]

						if not id:
							debug(verbose, "ERROR! Component ID missing for "+uuid)
							continue

						print("Detected: "+id+" on line "+str(line))					
						entries.append({
							"id" : id,
							"oldid" : fulluuid,
							"lnr" : line,
							"x" : x,
							"y" : y,
							"file" : filename,
							"val" : val,
							"uuid" : uuid,
							"footprint" : footprint
						})


			elif line.startswith("$Sheet"):
				for i in range(50):
					linenr = linenr+1
					l = filecache[filename][linenr]

					if l.startswith("F1 "):
						spl = shlex.split(l)
						if not spl[1] in subfiles:
							subfiles.append(spl[1])
						break
					if l.startswith("$EndSheet"):
						break

			linenr = linenr+1

	#entries = sorted(entries, key = lambda i: (i["id"], i["val"], i["file"]))

	

	debug(verbose, "\n== FOUND "+str(len(entries))+" COMPONENTS IN "+str(len(filecache))+" FILES ==\n\n")
	stats["comp"] = len(entries)
	stats["files"] = len(filecache)


	# group by id
	grouped = {}
	for entry in entries:
		if not entry["id"] in grouped:
			grouped[entry["id"]] = []
		grouped[entry["id"]].append(entry)

	

	for group in grouped:
		debug(verbose, "\n\n== Group "+group+" ("+str(len(grouped[group]))+")\n")

		targetIterator = 0		# Reset the annotation nr within this group of components

		#sort by lowest distance from top left, making Y matter double
		grouped[group] = sorted(grouped[group], key = lambda i: (i["y"]+i["x"]*2))

		#split into subgroups based on val
		subgroups = {}
		for entry in grouped[group]:
			vfp = entry["val"]+"$$"+entry["footprint"] #value with footprint
			if not vfp in subgroups:
				subgroups[vfp] = []
			subgroups[vfp].append(entry)

		for subgroup in subgroups:
			debug(verbose, "   == Subgroup: "+subgroup+" ("+str(len(subgroups[subgroup]))+")")


			filesplit = {}	# split by file
			for component in subgroups[subgroup]:
				if not component["file"] in filesplit:
					filesplit[component["file"]] = []
				filesplit[component["file"]].append(component)

			for file in filesplit:
				debug(verbose, "        == Components for file: "+file)

				##debug(verbose, filesplit[file])
				components = filesplit[file]
				target = components[0]
				assignTarget(target, verbose)
				while True:
					target = findClosestEntry(components, target)
					if not target:
						break
					assignTarget(target, verbose)

			#start at the top left
			#debug(verbose, "        First entry: ")
			#debug(verbose, entries[0])


	for file in filecache:
		with open(file, "w+") as f:
			f.writelines(filecache[file])
			debug(verbose, "Wrote", file)

	return stats

		# Now we have a list where the first value should be #1. 
		# Gotta figure out how to sort the rest tho


