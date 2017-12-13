#!/usr/bin/env python
import distsim

# you may have to replace this line if it is too slow 
word_to_ccdict = distsim.load_contexts("nytcounts.4k")


### provide your answer below

###Answer examples
#distsim.show_nearest(word_to_ccdict, word_to_ccdict['jack'],set(['jack']),distsim.cossim_sparse)
# people
rihanna = distsim.show_nearest(word_to_ccdict, word_to_ccdict['rihanna'],set(['rihanna']),distsim.cossim_sparse)
obama = distsim.show_nearest(word_to_ccdict, word_to_ccdict['obama'],set(['obama']),distsim.cossim_sparse)
# companies
nba = distsim.show_nearest(word_to_ccdict, word_to_ccdict['nba'],set(['nba']),distsim.cossim_sparse)
netflix = distsim.show_nearest(word_to_ccdict, word_to_ccdict['netflix'],set(['netflix']),distsim.cossim_sparse)
# country
iran = distsim.show_nearest(word_to_ccdict, word_to_ccdict['iran'],set(['iran']),distsim.cossim_sparse)
# common nouns
terrorism = distsim.show_nearest(word_to_ccdict, word_to_ccdict['terrorism'],set(['terrorism']),distsim.cossim_sparse)
economy = distsim.show_nearest(word_to_ccdict, word_to_ccdict['economy'],set(['economy']),distsim.cossim_sparse)
data = distsim.show_nearest(word_to_ccdict, word_to_ccdict['data'],set(['data']),distsim.cossim_sparse)
sex = distsim.show_nearest(word_to_ccdict, word_to_ccdict['sex'],set(['sex']),distsim.cossim_sparse)
texting = distsim.show_nearest(word_to_ccdict, word_to_ccdict['texting'],set(['texting']),distsim.cossim_sparse)
# time periods
year2007 = distsim.show_nearest(word_to_ccdict, word_to_ccdict['2007'],set(['2007']),distsim.cossim_sparse)
year2015 = distsim.show_nearest(word_to_ccdict, word_to_ccdict['2015'],set(['2015']),distsim.cossim_sparse)
# adjectives
medical = distsim.show_nearest(word_to_ccdict, word_to_ccdict['medical'],set(['medical']),distsim.cossim_sparse)
israeli = distsim.show_nearest(word_to_ccdict, word_to_ccdict['israeli'],set(['israeli']),distsim.cossim_sparse)
congressional = distsim.show_nearest(word_to_ccdict, word_to_ccdict['congressional'],set(['congressional']),distsim.cossim_sparse)
# verbs
leaked = distsim.show_nearest(word_to_ccdict, word_to_ccdict['leaked'],set(['leaked']),distsim.cossim_sparse)
failed = distsim.show_nearest(word_to_ccdict, word_to_ccdict['failed'],set(['failed']),distsim.cossim_sparse)
voted = distsim.show_nearest(word_to_ccdict, word_to_ccdict['voted'],set(['voted']),distsim.cossim_sparse)
# adverbs
suddenly = distsim.show_nearest(word_to_ccdict, word_to_ccdict['suddenly'],set(['suddenly']),distsim.cossim_sparse)
finallyAdv = distsim.show_nearest(word_to_ccdict, word_to_ccdict['finally'],set(['finally']),distsim.cossim_sparse)


print 'Rihanna'
for (x, y) in rihanna:
	print str(x) + ': ' + str(y)

print '\nObama'
for (x, y) in obama:
	print str(x) + ': ' + str(y)

print '\nNBA'
for (x, y) in nba:
	print str(x) + ': ' + str(y)

print '\nNetflix'
for (x, y) in netflix:
	print str(x) + ': ' + str(y)

print '\nIran'
for (x, y) in iran:
	print str(x) + ': ' + str(y)

print '\nTerrorism'
for (x, y) in terrorism:
	print str(x) + ': ' + str(y)

print '\nEconomy'
for (x, y) in economy:
	print str(x) + ': ' + str(y)

print '\nData'
for (x, y) in data:
	print str(x) + ': ' + str(y)

print '\nSex'
for (x, y) in sex:
	print str(x) + ': ' + str(y)

print '\nTexting'
for (x, y) in texting:
	print str(x) + ': ' + str(y)

print '\n2007'
for (x, y) in year2007:
	print str(x) + ': ' + str(y)

print '\n2015'
for (x, y) in year2015:
	print str(x) + ': ' + str(y)

print '\nMedical'
for (x, y) in medical:
	print str(x) + ': ' + str(y)

print '\nIsraeli'
for (x, y) in israeli:
	print str(x) + ': ' + str(y)

print '\nCongressional'
for (x, y) in congressional:
	print str(x) + ': ' + str(y)

print '\nLeaked'
for (x, y) in leaked:
	print str(x) + ': ' + str(y)

print '\nFailed'
for (x, y) in failed:
	print str(x) + ': ' + str(y)

print '\nVoted'
for (x, y) in voted:
	print str(x) + ': ' + str(y)

print '\nSuddenly'
for (x, y) in suddenly:
	print str(x) + ': ' + str(y)

print '\nFinally'
for (x, y) in finallyAdv:
	print str(x) + ': ' + str(y)