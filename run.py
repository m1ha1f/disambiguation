from parsing_pl.wordnet import WordNet
from parsing_pl.parser import *


t0 = time.time()

print "Loading WordNet..."

print "Parsing synsets..."
synsets = parse_s()

print "Parsing glosses..."
glosses = parse_g()

print "Parsing hypernyms..."
hypernyms = parse_hyp()

print "Parsing meronyms..."
meronyms = parse_m()

wordnet = WordNet(synsets, glosses, hypernyms, meronyms)

print "Wordnet database loaded in %s seconds" % (time.time() - t0)