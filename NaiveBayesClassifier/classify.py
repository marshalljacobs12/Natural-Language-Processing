#!/usr/bin/env python
from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
import codecs
import sys
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk import bigrams
from nltk.util import ngrams

import re

from string import punctuation

from nltk.tokenize import TreebankWordTokenizer

from decimal import Decimal

kTOKENIZER = TreebankWordTokenizer()
stop_words = nltk.corpus.stopwords.words('english')

def morphy_stem(word):
	"""
	Simple stemmer
	"""
	stem = wn.morphy(word)
	if stem:
		return stem.lower()
	else:
		return word.lower()

class FeatureExtractor:

	def __init__(self, trainData):
	
		self._pronunciations = nltk.corpus.cmudict.dict()
		self._rhymeWords = []

		for ii in trainData:
			if ii['cat'] == 's':
				line = ii['text']
				lastWord = line.rsplit(None, 1)[-1]
				if lastWord[-1] in punctuation:
					self._rhymeWords.append(lastWord[0:-1])
				else:
					self._rhymeWords.append(lastWord)
			else:
				continue
		
	def features(self, text):
		d = defaultdict(int)
	
		tokens = kTOKENIZER.tokenize(text)

		d['numTokens'] += len(tokens)

		#starts with token Y
		startsWithY = 'startsWith' + tokens[0].lower()
		d[startsWithY] += 1
		
		numPunctuationTokens = 0

		for ii in tokens:
			d['totalTokenLength'] += len(ii)

			if ii in punctuation:
				numPunctuationTokens += 1
				continue

			d[morphy_stem(ii)] += 1
			#avoid double counting if stem is same as token
			if morphy_stem(ii) != ii.lower():
				d[ii.lower()] += 1

			d['numSyllables'] += self.guess_syllables(ii)
			d['numSyllablesSquared'] = d['numSyllables'] ** 2

			if self.guess_syllables(ii) >= 4:
				xSyllablesInWord = str(self.guess_syllables(ii)) + '-syllable-word'
				d[xSyllablesInWord] += 1

		d['numWords'] = len(tokens) - numPunctuationTokens

		lastIndex = 0

		if tokens[-1] in punctuation:
			d['ends-with-punctuation'] += 1
			d['endNumSyllables'] = self.guess_syllables(tokens[-2])
			lastIndex = -2
		else:
			d['end-word'] += 1
			d['endNumSyllables'] = self.guess_syllables(tokens[-1])
			lastIndex = -1
		
		bgs = list(bigrams(tokens))
		for j in bgs:
			bigram = (j[0], j[1])
			if bigram[0] is not None and bigram[1] is not None and bigram[0] not in punctuation and bigram[1] not in punctuation:
				d[bigram] += 1
		
		trigrams = ngrams(tokens, 3)
		for k in trigrams:
			trigram = (k[0], k[1], k[2])
			if trigram[0] is not None and trigram[1] is not None and trigram[2] is not None and trigram[0] not in punctuation and trigram[1] not in punctuation and trigram[2] not in punctuation and trigram[0] not in stop_words and trigram[1] not in stop_words and trigram[2] not in stop_words:
				d[trigram] += 1

		if tokens[lastIndex] in self._rhymeWords:
			d['inRhymeWords'] += 1
			listIndex = self._rhymeWords.index(tokens[lastIndex])
			prevWord = self._rhymeWords[listIndex+1]
			twoBack = self._rhymeWords[listIndex+2]
			nextWord = self._rhymeWords[listIndex-1]
			twoForward = self._rhymeWords[listIndex-2]
			if self.rhymes(tokens[lastIndex], prevWord) or self.rhymes(tokens[lastIndex], nextWord) or self.rhymes(tokens[lastIndex], twoBack) or self.rhymes(tokens[lastIndex], twoForward):
				d['doesRhyme'] += 1

		return d

	def guess_syllables(self, word):
		"""
		From my HW1 submission
		"""
		vowels = ['a', 'e', 'i', 'o', 'u']
		consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p',
						'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
		diphthongs = ['ai', 'au', 'ea', 'ee', 'ei', 'eu', 'ie', 'oa', 'oe', 'oi',
						'oo', 'ou', 'ue', 'ui']
		triphthongs = ['iou'] # Don't count eau because it is two diphthongs


		word = word.lower()

		numSyllables = 0

		# Count vowels in word
		for c in word:
			if c in vowels:
				numSyllables += 1

		# Subtract diphthongs because they were double counted
		for i in range(len(word) - 1):
			j = word[i]
			k = word[i + 1]
			if j + k in diphthongs:
				 numSyllables -= 1

		# Subtract 1 for triphthong iou 
		for i in range(len(word) - 2):
			j = word[i]
			k = word[i + 1]
			l = word[i + 2]
			if j + k + l in triphthongs:
				numSyllables -= 1

		# Add a syllable for words that end in y that are preceded by a consonant
		# but not those preceded by a vowel
		if word[-1] == 'y' and word[-2] in consonants:
			numSyllables += 1

		# Subtract a syllable for words that end with a silent that are preceded 
		# by a consonant but not those preceded by a vowel because those have been 
		# accounted for in diphthongs
		if word[-1] == 'e' and word[-2] in consonants:
			numSyllables -= 1

		# Subtract a syllable for words that end with a s that are preceded by an
		# a consonant followed by an e (plurals nouns or third person singular
		# versions of the words accounted for in the previous if statement)
		if word[-1] == 's' and word[-2] == 'e' and word[-3] in consonants:
			numSyllables -= 1

		# If the word ends with le, add one if the letter before l is a consonant
		if word[-1] == 'e' and word[-2] == 'l' and word[-3] in consonants:
			numSyllables += 1

		# If the word ends with les, add one if the letter before l is a consonant
		if word[-1] == 's' and word[-2] == 'e' and word[-3] == 'l' and word[-4] in consonants:
			numSyllables += 1

		return numSyllables

	def rhymes(self, a, b):
		"""
		Returns True if two words (represented as lower-case strings) rhyme,
		False otherwise.
		"""
		# a and b should be lower case, but I convert just in case to ensure 
		# proper lookup in CMU Pronouncing Dictionary 
		a = a.lower()
		b = b.lower()

		# Looking a word up may throw a KeyError if it is not in dictionary
		try:
			aEntry = self._pronunciations[a]
			bEntry = self._pronunciations[b]
			doesRhyme = False
			for aOption in aEntry:
				for bOption in bEntry:
					flag = self.rhymes_helper(aOption, bOption)
					if flag: 
						doesRhyme = True
					continue
		# Default behavior if a or b is not in CMY Pronouncing Dictionary is to
		# return false
		except KeyError:
			return False

		# doesRhyme returns true if any combination of possible pronounciations
		# of a and b satisfy the rhyming criteria
		return doesRhyme

	# relaxed the rhyming requirements from HW1 to better suit this use case
	def rhymes_helper(self, x, y):
	  # The phenomes in the CMU Pronouncing Dictionary that correspond to 
	  # consonant sounds
	  consonantPhenomes = ['B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L',
						   'M', 'N', 'NG', 'P', 'R', 'S', 'SH', 'T', 'TH', 'V', 
						   'W', 'X', 'Y', 'Z', 'ZH']

	  # The phenomes in the CMU Pronouncing Dictionary that correspond to 
	  # vowel sounds
	  vowelPhenomes = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 
					   'IH', 'IY', 'OW', 'OY', 'UH', 'UW']

	  # xTrimmed and yTrimmed store the normalizations of x and y
	  xTrimmed = []
	  yTrimmed = []

	  foundLastVowelSound = False
	  for phenome in reversed(x):
	  	if phenome in vowelPhenomes and not foundLastVowelSound:
	  		foundLastVowelSound = True
	  	elif phenome[0:2] in consonantPhenomes and not foundLastVowelSound:
	  		continue
	  	elif phenome[0:1] in consonantPhenomes and not foundLastVowelSound:
	  		continue
	  	else:
	  		xTrimmed.insert(0, phenome)

	  foundLastVowelSound = False
	  for phenome in reversed(y):
	  	if phenome in vowelPhenomes and not foundLastVowelSound:
	  		foundLastVowelSound = True
	  	elif phenome[0:2] in consonantPhenomes and not foundLastVowelSound:
	  		continue
	  	elif phenome[0:1] in consonantPhenomes and not foundLastVowelSound:
	  		continue
	  	else:
	  		yTrimmed.insert(0, phenome)

	  # Account for different normalization lengths
	  if len(xTrimmed) > len(yTrimmed):
		while len(xTrimmed) - len(yTrimmed) != 0:
		  del xTrimmed[0]
	  elif len(yTrimmed) > len(xTrimmed):
		while len(yTrimmed) - len(xTrimmed) != 0:
		  del yTrimmed[0]

	  # Check if xTrimmed and yTrimmed are equal. Return False if they are not
	  for phenomeX, phenomeY in zip(xTrimmed, yTrimmed):
		if phenomeX != phenomeY:
		  return False

	  # xTrimmed and yTrimmed are equal so return True
	  return True

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')


def prepfile(fh, code):
  if type(fh) is str:
	fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
	if code.startswith('r'):
	  ret = reader(fh)
	elif code.startswith('w'):
	  ret = writer(fh)
	else:
	  sys.stderr.write("I didn't understand code "+code+"\n")
	  sys.exit(1)
  return ret

# Only changes to main are that FeatureExtractor constructor takes a parameter and I had to make a separate args and trainfile to
# pass to the DictReader constructor (the new parameter in my FeatureExtractor constructor)

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument("--trainfile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input train file")
	parser.add_argument("--testfile", "-t", nargs='?', type=argparse.FileType('r'), default=None, help="input test file")
	parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")
	parser.add_argument('--subsample', type=float, default=1.0,
						help='subsample this fraction of total')

	# Added args2 and trainfile2 because DictReader required a separate file to work correctly. 
	args = parser.parse_args()
	args2 = parser.parse_args()
	trainfile = prepfile(args.trainfile, 'r')
	trainfile2 = prepfile(args2.trainfile, 'r')
	if args.testfile is not None:
		testfile = prepfile(args.testfile, 'r')
	else:
		testfile = None
	outfile = prepfile(args.outfile, 'w')


	# Create feature extractor (you may want to modify this)
	fe = FeatureExtractor(DictReader(trainfile2, delimiter='\t'))

	# Read in training data
	train = DictReader(trainfile, delimiter='\t')

	# Split off dev section
	dev_train = []
	dev_test = []
	full_train = []

	for ii in train:
		if args.subsample < 1.0 and int(ii['id']) % 100 > 100 * args.subsample:
			continue
		feat = fe.features(ii['text'])
		if int(ii['id']) % 5 == 0:
			dev_test.append((feat, ii['cat']))
		else:
			dev_train.append((feat, ii['cat']))
		full_train.append((feat, ii['cat']))

	# Train a classifier
	sys.stderr.write("Training classifier ...\n")
	classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)

	# was just using this function for reference
	#classifier.show_most_informative_features(25)

	right = 0
	total = len(dev_test)
	for ii in dev_test:
		prediction = classifier.classify(ii[0])
		if prediction == ii[1]:
			right += 1
	sys.stderr.write("Accuracy on dev: %f\n" % (float(right) / float(total)))

	if testfile is None:
		sys.stderr.write("No test file passed; stopping.\n")
	else:
		# Retrain on all data
		classifier = nltk.classify.NaiveBayesClassifier.train(dev_train + dev_test)

		# Read in test section
		test = {}
		for ii in DictReader(testfile, delimiter='\t'):
			test[ii['id']] = classifier.classify(fe.features(ii['text']))

		# Write predictions
		o = DictWriter(outfile, ['id', 'pred'])
		o.writeheader()
		for ii in sorted(test):
			o.writerow({'id': ii, 'pred': test[ii]})
