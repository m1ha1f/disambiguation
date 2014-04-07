class Synset:
	NOUN = 'n'
	VERB = 'v'
	ADJECTIVE = 'a'
	ADJECTIVE_SATELLITE = 's'
	ADVERB = 'r'

	def __init__(self, id, text, type):
		self.id = id
		self.text = text

		assert (type in [Synset.NOUN, Synset.VERB, Synset.ADJECTIVE, 
			Synset.ADJECTIVE_SATELLITE, Synset.ADVERB])
		self.type = type

class SynsetCollection:
	def __init__(self, synsetList):
		self.id2synset = {}
		self.text2synset = {}
		for synset in synsetList:
			self.id2synset[synset.id] = synset
			self.text2synset[synset.text] = synset

	def get(self, id):
		return self.id2synset[id]


