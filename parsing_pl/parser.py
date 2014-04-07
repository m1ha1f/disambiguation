import time
from pyparsing import Empty, ParseException, QuotedString, Regex, Word, alphas, nums
from synset import Synset, SynsetCollection
from gloss import Gloss, GlossCollection
from hypernym import Hypernym, HypernymCollection
from meronym import Meronym, MeronymCollection


def parse_s():
	#s(synset_id,w_num,'word',ss_type,sense_number,tag_count)
	#watchout when parsing 'bull''s eye'
	s = "s(" + Word(nums) + "," + \
		Word(nums) + "," + \
		Regex("\'.*\'") + "," + \
		Word(alphas, max=1 ) + \
		(("," + Word(nums) + "," + Word(nums)) | Empty()) + ")."

	list = []

	with open("prolog/wn_s.pl") as f:
		for line in f:
			try:
				parsed_s = s.parseString(line)
				id = int(parsed_s[1])
			except ParseException:
				print "Error parsing ", line
		
			ss_type = parsed_s[7].strip("'")
			text = parsed_s[5].strip("'")

			list.append(Synset(id, text, ss_type))
			# print id, word, ss_type 

	return SynsetCollection(list)

def parse_g():
	#g(synset_id,'gloss')
	g = "g(" + Word(nums) + "," + \
		Regex("\'.*\'") + ")."
		
	list = []

	with open("prolog/wn_g.pl") as f:
		for line in f:
			try:
				parsed_g = g.parseString(line)
				id = int(parsed_g[1])
			except ParseException:
				print "Error parsing ", line
			
			gloss = parsed_g[3].strip("'")
			list.append(Gloss(id, gloss))

	return GlossCollection(list)

def parse_hyp():
	#hyp(synset_id,synset_id). the second synset is a hypernym of the first synset.
	hyp = "hyp(" + Word(nums) + "," + Word(nums) + ")."
		
	list = []

	with open("prolog/wn_hyp.pl") as f:
		for line in f:
			try:
				parsed_hyp = hyp.parseString(line)
				child = int(parsed_hyp[1])
				parent = int(parsed_hyp[3])
			except ParseException:
				print "Error parsing ", line
			
			list.append(Hypernym(parent, child))

	return HypernymCollection(list)

def parse_m(): 
	# mm(synset_id,synset_id).
	# The mm operator specifies that the second synset is a member meronym of the first synset. This relation only holds for nouns. The reflexive operator, member holonym, can be implied.
	# ms(synset_id,synset_id).
	# The ms operator specifies that the second synset is a substance meronym of the first synset. This relation only holds for nouns. The reflexive operator, substance holonym, can be implied.
	# mp(synset_id,synset_id).
	# The mp operator specifies that the second synset is a part meronym of the first synset. This relation only holds for nouns. The reflexive operator, part holonym, can be implied.

	list = []

	def parse_mx(x, type):
		m =  x + "(" + Word(nums) + "," + Word(nums) + ")."
		with open("prolog/wn_" + x + ".pl") as f:
			for line in f:
				try:
					parsed_m = m.parseString(line)
					whole = int(parsed_m[1])
					part = int(parsed_m[3])
				except ParseException:
					print "Error parsing ", line
				
				list.append(Meronym(part, whole, type))

	parse_mx("mm", Meronym.MEMBER)
	parse_mx("ms", Meronym.SUBSTANCE)
	parse_mx("mp", Meronym.PART)

	return MeronymCollection(list)



			