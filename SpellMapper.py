# Caitlin McElwee, April 2019

# This class is to define what a spell is, which is to say, an object consisting of 
# the spell's name, its level, and its school

class Spell(object):
	name = "default"
	level = -1
	school = "default"
	
	def __init__(self,name,level,school):
		self.name = name
		self.level = level
		self.school = school

	def __repr__(self):
		# Get the right suffix for the level 
		suffix = 'st' if self.level == 1 else 'nd' if self.level == 2 else 'rd' if self.level == 3 else 'th'
		return f'{self.name}'#, {self.level}{suffix}-level {self.school}'
		# return f'{self.school} {self.level}'	# testing line used for testing correct edges
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# This script is to load spells into a program and then output a spell map of them

import networkx as nx
import matplotlib.pyplot as plt
import random

# Import file containing all the random effects
file = open("PreparedSpells.txt","r")

# Declare & initialize collection
spells = []

print("File opened, importing ... ", end='')

# Load all spells into collection
for line in file:
	spellLine = line.strip().split(',')
	spells.append(Spell(spellLine[0],int(spellLine[1]),spellLine[2]))
file.close()
print("Done !")

# Now we initialize a graph and add every spell to it as nodes
G=nx.Graph()
for spell in spells:
	G.add_node(spell)
# end for
print("All spells added to graph")

# We need to add an edge for each connection that needs to be there. Let's store a backup of spells for repeating
copyOfSpells = spells.copy
# Randomize the collection so as to, on every run, have the chance of a new map
random.shuffle(spells)
# Seperate the spells out by level
spellsByLevel = [[],[],[],[],[],[],[],[],[],[]]	# prepare to hold ten levels of spells (0-9)
for spell in spells:
	spellsByLevel[spell.level].append(spell)

spellsByLevel = [level for level in spellsByLevel if level]	# Clear empty levels (no spells prepared at that level)
print("All spells sorted")
for level in spellsByLevel:					# for each level of spell
	for i in range(len(level) - 1):			# for eah spell of current level
		G.add_edge(level[i],level[i+1])		# connect current spell to the next spell of same level, in a chain

while spells != []:				# while there are spells left to connect
	currentSpell = spells[0]	# grab the first spell
	for spell in spells:		# for every spell in the collection
								# if this spell is of the same school and is one level higher or lower than currentSpell
		if (currentSpell.school == spell.school) and (abs(currentSpell.level - spell.level) == 1):	
			G.add_edge(currentSpell,spell)	# add an edge between these two
	del spells[0]

print("Nodes of graph: ")
print(G.nodes())
print("Edges of graph: ")
print(G.edges())


nx.draw(G,with_labels=True)
plt.savefig("simple_path.png") # save as png
plt.show() # display
