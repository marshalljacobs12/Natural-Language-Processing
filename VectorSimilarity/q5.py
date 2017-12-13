#!/usr/bin/env python
import distsim
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
###Provide your answer below

###Answer examples
#distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['jack'],set(['jack']),distsim.cossim_dense)
# people
rihanna = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['rihanna'],set(['rihanna']),distsim.cossim_dense)
obama = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['obama'],set(['obama']),distsim.cossim_dense)
# companies
nba = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['nba'],set(['nba']),distsim.cossim_dense)
netflix = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['netflix'],set(['netflix']),distsim.cossim_dense)
# country
iran = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['iran'],set(['iran']),distsim.cossim_dense)
# common nouns
terrorism = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['terrorism'],set(['terrorism']),distsim.cossim_dense)
economy = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['economy'],set(['economy']),distsim.cossim_dense)
data = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['data'],set(['data']),distsim.cossim_dense)
sex = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['sex'],set(['sex']),distsim.cossim_dense)
texting = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['texting'],set(['texting']),distsim.cossim_dense)
# time periods
year2007 = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['2007'],set(['2007']),distsim.cossim_dense)
year2015 = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['2015'],set(['2015']),distsim.cossim_dense)
# adjectives
medical = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['medical'],set(['medical']),distsim.cossim_dense)
israeli = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['israeli'],set(['israeli']),distsim.cossim_dense)
congressional = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['congressional'],set(['congressional']),distsim.cossim_dense)
# verbs
leaked = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['leaked'],set(['leaked']),distsim.cossim_dense)
failed = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['failed'],set(['failed']),distsim.cossim_dense)
voted = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['voted'],set(['voted']),distsim.cossim_dense)
# adverbs
suddenly = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['suddenly'],set(['suddenly']),distsim.cossim_dense)
finallyAdv = distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['finally'],set(['finally']),distsim.cossim_dense)


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