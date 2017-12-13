#!/usr/bin/env python
import distsim
import sys

def loadAnalogies():
	analogies = {}
	currentIndex = ''

	with open("word-test.v3.txt","r") as f_in:
		for line in f_in:
			if line.startswith('//'):
				#print 'line: ' + str(line)
				#print 'starts with //'
				continue
			elif line.startswith(':'):
				#print 'starts with : ' + str(line)
				tokens = line.split()
				category = tokens[1]
				#print 'category: ' + category
				analogies[category] = []
				currentIndex = category
			else:
				#print line
				tokens = line.split()
				#print tokens
				analogies[currentIndex].append(tokens)

	"""
	for k, v in analogies.iteritems():
		print 'k: ' + str(k)
		for i in v:
			print 'i: ' + str(i)
	"""
	return analogies

def calculateAccuracies(solutions):
	word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
	accuracies = {}
	errors = {}

	for k, v in solutions.iteritems():
		#print 'group: ' + str(k)
		accuracies[k] = (float(0.0), float(0.0), float(0.0))
		errors[k] = ''
		size = len(v)
		hasShownError = False
		for i in v:
			w1 = word_to_vec_dict[i[0]]
			w2 = word_to_vec_dict[i[1]]
			w4 = word_to_vec_dict[i[3]]
			ret = distsim.show_nearest(word_to_vec_dict,
               	           				w1-w2+w4,
                   	       				set([str(i[0]), str(i[1]), str(i[3])]),
                       	   				distsim.cossim_dense)
			isInTenBest = False
			for n in range(len(ret)):
				(p, q) = ret[n]
				if p == i[2]:
					isInTenBest = True
					if n == 0:
						(x, y, z) = accuracies[k]
						x += 1.0
						y += 1.0
						z += 1.0
						accuracies[k] = (x, y, z)
					elif n < 5:
						(x, y, z) = accuracies[k]
						y += 1.0
						z += 1.0
						accuracies[k] = (x, y, z)
					else:
						(x, y, z) = accuracies[k]
						z += 1.0
						accuracies[k] = (x, y, z)

			if not isInTenBest and not hasShownError:
				errors[k] = (i[0], i[1], i[2], i[3], ret[0][0])
				hasShownError = True

		(a, b, c) = accuracies[k]
		a /= size
		b /= size
		c /= size
		accuracies[k] = (a, b, c)
		#print accuracies[k]

	#print errors
	return (accuracies, errors)

def displayResults(results, errors):
	
	print 'Analogy Accuracies\n-------------------------------'

	for k, v in results.iteritems():
		print 'Relation group: ' + str(k)
		(x, y, z) = v
		print '1-best accuracy: ' + str(x)
		print '5-best accuracy: ' + str(y)
		print '10-best accuracy: ' + str(z)
		print '-------------------------------'

	print '\nIncorrect Predictions\n-------------------------------'

	for k, v in errors.iteritems():
		print 'Relation group: ' + str(k)
		(u, w, x, y, z) = v
		print 'My prediction: ' + str(u) + ' : ' + str(w) + ' :: ' + str(z) + ' : ' + str(y)
		print 'Correct prediction: ' + str(u) + ' : ' + str(w) + ' :: ' + str(x) + ' : ' + str(y)
		print '-------------------------------'

def main():
	analogies = loadAnalogies()
	(accuracies, errors) = calculateAccuracies(analogies)
	displayResults(accuracies, errors)

if __name__ == '__main__':
  main()