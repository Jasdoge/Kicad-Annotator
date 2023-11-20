import pcbnew
import os
import wx
import re

class FpEditor:
	
	
	def __init__(self):
		self.groups = []
		self._refnrs = {}	# ref : nr

	def add(self, footprint):
		# Get ref like C or R with no number
		ref = re.search("[^\-\?\d]*", footprint.GetReference())
		#wx.MessageBox(footprint.GetReference() + " " + ref.group(0))
		if ref:
			ref = ref.group(0)
		else:
			ref = "UNKNOWN"
		# Get footprint name
		ident = footprint.GetFPID().GetUniStringLibItemName()
		# Get value
		value = footprint.GetValue()
		group = self.getGroup(ref, ident, value)
		if not group:
			group = FpGroup(ref, ident, value)
			self.groups.append(group)
		group.add(footprint)
	
	def print(self):
		for group in self.groups:
			wx.MessageBox(" ".join([group.ident, group.value, ":", str(len(group.footprints))]))

	def sort(self):
		# Sort items in groups by x
		for group in self.groups:
			group.sort()
		# Sort the groups themselves
		self.groups = sorted(self.groups, key = lambda x: (x.ref, x.valNum, x.value, x.ident))

	# Gets a group by ref, ident, and value
	def getGroup(self, ref, ident, value):
		for group in self.groups:
			if group.ref == ref and group.ident == ident and group.value == value:
				return group

	# Writes changes to board
	def write(self):
		self._refnrs = {}
		for group in self.groups:
			ref = group.ref		# Get reference label like Q or R or C
			# Create new index if it doesn't exist
			if not ref in self._refnrs:
				self._refnrs[ref] = 1
			start = self._refnrs[ref]
			group.write(start)
			self._refnrs[ref] += len(group.footprints)
			#wx.MessageBox("Group "+group.ref+"."+group.ident+"."+group.value+" has "+str(len(group.footprints))+" entries")

# Group by footprint, reference type, and value
class FpGroup:
	def __init__(self, ref, ident, value):
		self.ref = ref
		self.ident = ident		# Footprint ex R_0603_1608Metric
		self.value = value		# Value ex 100k
		self.footprints = []	# Items to be sorted
		# Try to represent the value as an int
		mul = re.findall("(?<=[0-9\s_-])[^\d\s\.]", value) # Find the first non digit or space preceded by a digit, space, or underscore
		try:
			self.valNum = float(re.compile("^[+-]*([\d\.]+)").match(value).group(1)) # JS/PHP style number conversion. Get the first numbers
		except:
			self.valNum = 0 # No number here
			

		if len(mul):
			m = mul[0]
			if m == "G":
				self.valNum *= 1e9
			elif m == "M":
				self.valNum *= 1e6
			elif m == "k" or m == "K":
				self.valNum *= 1e3
			elif m == "m":
				self.valNum /= 1e3
			elif m == "u" or m == "μ":
				self.valNum /= 1e6
			elif m == "n":
				self.valNum /= 1e9
			elif m == "p":
				self.valNum /= 1e12 # can python do this?
		#wx.MessageBox(str(self.value)+" -> "+str(self.valNum))
		# 0.01uF
	
	def add(self, footprint):
		self.footprints.append(footprint)

	# Sorts from left to right. Could sort better later
	def sort(self):
		self.footprints = sorted(self.footprints, key = lambda x: (x.GetPosition()[0]))

	# Writes footprints
	def write(self, start):
		for footprint in self.footprints:
			ref = self.ref+str(start)
			footprint.SetReference(ref)
			start += 1
		

class SimplePlugin(pcbnew.ActionPlugin):
	def defaults(self):
		self.name = "Hand Solder Annotate"
		self.category = "Annotations"
		self.description = "Groups and sorts annotation by type -> value -> position"
	
	def Run(self):
		footprints = pcbnew.GetBoard().GetFootprints()
		editor = FpEditor()
		for footprint in footprints:
			editor.add(footprint)
		editor.sort()
		editor.write()
		#editor.print()
		pcbnew.Refresh()

SimplePlugin().register()

