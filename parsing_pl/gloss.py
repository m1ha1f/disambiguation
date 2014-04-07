class Gloss:
	def __init__(self, id, gloss):
		self.id = id
		self.gloss = gloss

class GlossCollection:
	def __init__(self, glossList):
		self.id2gloss = {}
		for gloss in glossList:
			self.id2gloss[gloss.id] = gloss.gloss

	def get(self, id):
		return self.id2gloss[id]