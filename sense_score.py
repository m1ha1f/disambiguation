from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.porter import PorterStemmer
from relatedness import relatedness, HYPE, HYPO, GLOSS, MERONYMY

STOPWORDS = stopwords.words("english")
SYMBOLS = ['$', "''", '(', ')', ',', '--', '.', ':', 'SYM', "``"]
#stemmer = PorterStemmer() #do we need this?

def getPos(posString):
	if posString in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
		return wn.VERB
	if posString in ['NN', 'NNP', 'NNPS', 'NNS']:
		return wn.NOUN
	if posString in ['JJ', 'JJR', 'JJS']:
		return wn.ADJ
	if posString in ['RB', 'RBR', 'RBS']:
		return wn.ADV

	# raise Exception('Not yet implemented')
	return None

def getImportance(synset):
	#to do: check if this is right (maybe http://stackoverflow.com/questions/15551195/how-to-get-the-wordnet-sense-frequency-of-a-synset-in-nltk)
	return int(synset.name.split(".")[-1])

def senseScore(text, target, window, relpairs):
	words = word_tokenize(text)
	posTags = pos_tag(words)

	targetPos = [x[1] for x in posTags if x[0] == target]
	if len(targetPos) == 0:
		raise Exception("Target word not in text")
	targetPos = targetPos[0] #assume target occurs only once in text
	targetSynsets = wn.synsets(target, pos=getPos(targetPos))

	# words = [stemmer.stem_word(x.lower()) for x in words if x not in STOPWORDS]
	# target = stemmer.stem_word(target.lower())

	#filter symbols
	words = [x.lower() for x in words if x not in SYMBOLS]
	posTags = [x for x in posTags if x[0] not in SYMBOLS]

	#filter stopwords
	words = [x for x in words if x not in STOPWORDS]
	posTags = [x for x in posTags if x[0] not in STOPWORDS]

	#to do: check if we have to filter out other things like numerals etc

	p = words.index(target)
	bag = []
	for i in range(max(p-window, 0), p):
		bag.append(posTags[i])
	for i in range(p+1, min(p+window+1, len(words))):
		bag.append(posTags[i])

	ss = [0]*len(targetSynsets)

	for (i, targetSynset) in enumerate(targetSynsets):
		for (word, wordPos) in bag:
			for wordSynset in wn.synsets(word, pos=getPos(wordPos)):
				ss[i] += relatedness(targetSynset, wordSynset, relpairs)


	targetSynset = targetSynsets[0]
	pmax = 0
	for i in range(1, len(targetSynsets)):
		if ss[pmax] < ss[i] or (ss[pmax] == ss[i] \
			and getImportance(targetSynset) > getImportance(targetSynsets[i])):
				targetSynset = targetSynsets[i]
				pmax = i

	return targetSynset

def testSenseScore():
	text = "The driver got off the car in the middle of the drive-way"
	target = "car"
	relpairs = [(GLOSS, GLOSS), (HYPE, HYPE), (HYPO, HYPO), (HYPE, GLOSS), (GLOSS, HYPE)]

	assert senseScore(text, target, 3, relpairs).definition == 'a motor vehicle with four wheels; usually propelled by an internal combustion engine'


	text = "Everyone waited in line for the bank to open"
	target = "line"
	relpairs = [(GLOSS, GLOSS), (HYPE, HYPE), (MERONYMY, MERONYMY), (HYPE, GLOSS), (GLOSS, HYPE)]

	assert senseScore(text, target, 3, relpairs).definition == 'a formation of people or things one beside another'

	# text = "This line of products was discontinued"
	# target = "line"
	# relpairs = [(GLOSS, GLOSS), (HYPE, HYPE), (MERONYMY, MERONYMY), (HYPE, GLOSS), (GLOSS, HYPE)]

	# print senseScore(text, target, 3, relpairs).definition
	# assert senseScore(text, target, 3, relpairs).definition == 'a particular kind of product or merchandise'
	



