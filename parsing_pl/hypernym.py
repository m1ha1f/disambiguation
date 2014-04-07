class Hypernym:
	def __init__(self, parent, child):
		self.parent = parent
		self.child = child

class HypernymCollection:
	def __init__(self, hypernymList):
		self.child2parent = {}
		self.parent2children = {}

		for h in hypernymList:
			self.child2parent[h.child] = h.parent
			if h.parent not in self.parent2children:
				self.parent2children[h.parent] = set()
			self.parent2children[h.parent].add(h.child)

	def getParent(self, childId):
		return self.child2parent.get(childId, None)

	def getChildren(self, parentId):
		return self.parent2children[parentId]