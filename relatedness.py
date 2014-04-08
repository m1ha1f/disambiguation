from nltk.corpus import wordnet as wn
from overlap import glossOverlap

HYPE = 'hypernymy'
HYPO = 'hyponymy'
GLOSS = 'gloss'
MERONYMY = 'meronymy'

def getRelationGloss(synset, r):
	synsets = []
	if r == HYPE:
		synsets = synset.hypernyms()
	elif r == HYPO:
		synsets = synset.hyponyms()
	elif r == GLOSS:
		synsets = [synset]
	elif r == MERONYMY:
		synsets = synset.member_meronyms() + synset.part_meronyms() + synset.substance_meronyms()
	else:
		#to do: add other relations if necessary
		raise Exception("Unknown relation %s" % r)

	glosses = [x.definition for x in synsets]
	return " ".join(glosses)

def testRelationGloss():
	synset = wn.synset('unpleasant_woman.n.01')
	gloss = getRelationGloss(synset, HYPO)

	#print gloss

	assert('ugly' in gloss)
	assert('ill-tempered' in gloss)
	assert('woman' in gloss)
	assert('scolding' in gloss)
	assert('nagging' in gloss)
	assert('malicious' in gloss)
	assert('unattractive' in gloss)
	assert('unpleasant' in gloss)
	assert('cruel' in gloss)

def relatedness(synset1, synset2, relpairs):
	ret = 0
	for (r1, r2) in relpairs:
		gloss1 = getRelationGloss(synset1, r1)
		gloss2 = getRelationGloss(synset2, r2)

		# print gloss1
		# print ""
		# print gloss2
		# print glossOverlap(gloss1, gloss2)
		# print "-"*50

		ret += glossOverlap(gloss1, gloss2)
	return ret

def testRelatedness():
	synset1 = wn.synset('car.n.01')
	synset2 = wn.synset('motorcycle.n.01')

	relpairs = [(GLOSS, GLOSS), (HYPE, HYPE), (HYPO, HYPO), (HYPE, GLOSS), (GLOSS, HYPE)]

	assert relatedness(synset1, synset2, relpairs) == 115

	assert(relatedness(synset1, synset2, relpairs) == relatedness(synset2, synset1, relpairs))









		
		