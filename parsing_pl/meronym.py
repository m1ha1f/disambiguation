class Meronym:
	MEMBER = 1
	SUBSTANCE = 2
	PART = 3


	def __init__(self, part, whole, type):
		self.part = part
		self.whole = whole

		assert(type in [Meronym.MEMBER, Meronym.SUBSTANCE, Meronym.PART])
		self.type = type

class MeronymCollection:
	def __init__(self, meronymlist):
		self.part2whole = {}
		self.whole2parts = {}

		for m in meronymlist:
			self.part2whole[m.part] = m.whole

			if m.whole not in self.whole2parts:
				self.whole2parts[m.whole] = set()
			self.whole2parts[m.whole].add(m.part)

	def getWhole(self, partId):
		return self.part2whole.get(partId, None)

	def getParts(self, wholeId):
		return self.whole2parts[wholeId]
		