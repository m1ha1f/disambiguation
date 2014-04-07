import re
from nltk.stem.porter import PorterStemmer


def glossOverlap(gloss1, gloss2):
	# stopws = stopwords.words('english')
	stopws = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
	'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 
	'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 
	'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 
	'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 
	'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
	'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
	'in', 'out', 'on', 'off', 'over', 'under', 'then',  
	'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
	'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 
	'too', 'very', 's', 't', 'just', 'don', 'now']

	stemmer = PorterStemmer()

	# print "-"*50
	# for x in stopws:
	# 	if stemmer.stem_word(x) != x:
	# 		print x, stemmer.stem_word(x)

	def longestOverlap(a, b):
		now = [0]*len(b)
		bestOverlap = 0
		aStart = 0
		bStart = 0

		nextNonStopWord = [-1]*(len(a)+1)
		for i in range(len(a)-1, 0, -1):
			if a[i] not in stopws:
				nextNonStopWord[i] = i
			else:
				nextNonStopWord[i] = nextNonStopWord[i+1]

		for i in range(1, len(a)):
			prev = now
			now = [0]*len(b)
			if a[i] == '#':
				continue
			for j in range(1, len(b)):
				if b[j] == '#':
					continue
				if a[i] == b[j]:
					now[j] = max(now[j], prev[j-1] + 1)
					if a[i] in stopws:
						continue

					overlap = now[j]
					start = i - overlap + 1
					start = nextNonStopWord[start]
					overlap = i - start + 1
					if bestOverlap < overlap:
						bestOverlap = overlap
						aStart = i - overlap + 1
						bStart = j - overlap + 1

		return (bestOverlap, aStart, bStart)


	regex = ',|\.|\s|\?|\'|\"|!|;|-'
	#maybe check what happens if we don't stem the glosses
	a1 = ['#'] + [stemmer.stem_word(x.lower()) for x in re.split(regex, gloss1) if x]
	a2 = ['#'] + [stemmer.stem_word(x.lower()) for x in re.split(regex, gloss2) if x]

	score = 0
	(overlap, start1, start2) = longestOverlap(a1, a2)
	while overlap > 0:
		# print overlap
		# print a1[start1:start1+overlap]
		# print a2[start2:start2+overlap]
		a1[start1:start1+overlap] = ['#']
		a2[start2:start2+overlap] = ['#']
		score += overlap**2
		(overlap, start1, start2) = longestOverlap(a1, a2)

	return score


def testGlossOverlap():
	gloss1 = "Ana has green apples and red oranges"
	gloss2 = "Georgiana has orange apples and tomatoes"

	assert(glossOverlap(gloss1, gloss2) == 3)

	gloss1 = "Ana has apples!"
	gloss2 = "Ana has apples?"

	assert(glossOverlap(gloss1, gloss2) == 9)

	gloss1 = "Ana has apples, oranges and pineapple; her fruit is fresh."
	gloss2 = "Type of fresh pineapple with apple flavour"

	assert(glossOverlap(gloss1, gloss2) == 3)

	gloss1 = "fruit with red or yellow or green skin and sweet to tart crisp whitish flesh"
	gloss2 = "sweet juicy gritty-textured fruit available in many varieties"

	assert(glossOverlap(gloss1, gloss2) == 2)

	gloss1 = "a motor vehicle with four wheels; usually propelled by an internal combustion engine"
	gloss2 = "a motor vehicle with two wheels and a strong frame"

	assert(glossOverlap(gloss1, gloss2) == 5)




