import time
from pyparsing import Empty, ParseException, QuotedString, Regex, Word, alphas, nums

def parse_s():
	#s(synset_id,w_num,'word',ss_type,sense_number,tag_count)
	s = "s(" + Word(nums) + "," + \
		Word(nums) + "," + \
		Regex("\'.*\'") + "," + \
		Word(alphas, max=1 ) + \
		(("," + Word(nums) + "," + Word(nums)) | Empty()) + ")."

	with open("prolog/wn_s.pl") as f:
		for line in f:
			try:
				parsed_s = s.parseString(line)
			except ParseException:
				print "Error parsing ", line
			id = parsed_s[1]
			ss_type = parsed_s[7]
			word = parsed_s[5]
			print id, word, ss_type 


t0 = time.time()
parse_s()
print time.time() - t0

#'bull''s eye'
			