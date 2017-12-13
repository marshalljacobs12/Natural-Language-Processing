#!/usr/bin/env python
import argparse
import sys
import codecs
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

scriptdir = os.path.dirname(os.path.abspath(__file__))


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

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)

class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()

    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """

        """
        syllable: a unit of pronunciation having one vowel sound, with or 
        without surrounding consonants, forming the whole or a part of a word.
        """
        word = word.lower()

        # The phenomes in the CMU Pronouncing Dictionary that correspond to 
        # vowels
        vowelPhenomes = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY',
                         'IH', 'IY', 'OW', 'OY', 'UH', 'UW']

        # Looking a word up may throw a KeyError if it is not in dictionary
        try:
          entry = self._pronunciations[word]
          numSyllables = []
          for option in entry:
            numSyllables.append(0)
            for phoneme in option:
              if phoneme[0:2] in vowelPhenomes:
                numSyllables[-1] += 1
          # If multiple pronounciations exist, choose the pronounciation with 
          # the fewest syllables
          minValue = min(numSyllables)
          return minValue
        # word is not in CMU Pronouncing Dictionary
        except KeyError:
          return 1

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

      foundFirstConsonantSound = False

      # Normalization of x
      for phenome in x:
        if phenome in consonantPhenomes and not foundFirstConsonantSound:
          foundFirstConsonantSound = True
        elif phenome[0:2] in vowelPhenomes and not foundFirstConsonantSound:
          continue
        else:
          xTrimmed.append(phenome)

      foundFirstConsonantSound = False

      # Normalization of y
      for phenome in y:
        if phenome in consonantPhenomes and not foundFirstConsonantSound:
          foundFirstConsonantSound = True
        elif phenome[0:2] in vowelPhenomes and not foundFirstConsonantSound:
          continue
        else:
          yTrimmed.append(phenome)

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

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)


        """  
        # NOTE: NEED TO IMPLEMENT APOSTROPHE TOKENIZE SO THAT I JOIN THE TWO 
        # PARTS OF THE CONTRACTION INTO ONE WORD. RIGHT NOW IT IS TWO SEPARATE
        # WORDS

        # Initially, I assume text is not a limerick. If text satisfies all
        # the limerick criteria, isLimerick is then set to True
        isLimerick = False

        lines = text.splitlines()

        # Get rid of lines that are just white space or special whitespace-
        # related characters (like newlines or tabs)
        # CITE: https://stackoverflow.com/questions/3711856/how-to-remove-empty-lines-with-or-without-whitespace-in-python
        lines = filter(lambda x:  not re.match(r'^\s*$', x), lines)

        # Limericks must be 5 lines
        if len(lines) != 5:
          return isLimerick

        syllableCount = []
        rhymeWords = []
        filteredLines = []

        # Sanitizes the tokens in each line, counts the number of syllables in
        # a line, and stores the last word of a line to assess rhyme scheme
        for line in lines:
          words = word_tokenize(line)
          totalSyllables = 0
          filteredLine = []
          for word in words:
            # Remove word from line if it is simply a punctuation mark or 
            # several punctuation marks with no non-punctuation characters
            isAllPunctuation = True
            for c in word:
              if c not in punctuation:
                isAllPunctuation = False
            if isAllPunctuation:
              continue
            # Otherwise add the number of syllables in that word to the number
            # of syllables for the entire line
            else:
              totalSyllables += self.num_syllables(word)
              filteredLine.append(word)
          filteredLines.append(filteredLine)
          syllableCount.append(totalSyllables)
          rhymeWords.append(filteredLine[-1])

        # No two A lines should differ in their number of syllables by more than two
        # B lines should differ in their number of syllables by no more than two
        if abs(syllableCount[0] - syllableCount[1]) > 2:
          return isLimerick
        elif abs(syllableCount[0] - syllableCount[4]) > 2:
          return isLimerick
        elif abs(syllableCount[1] - syllableCount[4]) > 2:
          return isLimerick
        elif abs(syllableCount[2] - syllableCount[3]) > 2:
          return isLimerick

        # Each of the B lines should have fewer syllables than each of the A lines.
        if syllableCount[2] > syllableCount[0]:
          return isLimerick
        elif syllableCount[2] > syllableCount[1]:
          return isLimerick
        elif syllableCount[2] > syllableCount[4]:
          return isLimerick
        elif syllableCount[3] > syllableCount[0]:
          return isLimerick
        elif syllableCount[3] > syllableCount[1]:
          return isLimerick
        elif syllableCount[3] > syllableCount[4]:
          return isLimerick

        # No line should have fewer than 4 syllables
        if syllableCount[0] < 4:
          return isLimerick
        elif syllableCount[1] < 4:
          return isLimerick
        elif syllableCount[2] < 4:
          return isLimerick
        elif syllableCount[3] < 4:
          return isLimerick
        elif syllableCount[4] < 4:
          return isLimerick

        # Check rhyme scheme
        # All A lines must rhyme. Both B lines must rhyme. A lines must not 
        # rhyme with B lines. Because rhyming is transitive, it is not 
        # necessary to enumerate all possible cases. If rhyme scheme is 
        # satisfied, text is a valid limerick
        if not self.rhymes(rhymeWords[0], rhymeWords[1]):
          return isLimerick
        elif not self.rhymes(rhymeWords[0], rhymeWords[4]):
          return isLimerick
        elif not self.rhymes(rhymeWords[2], rhymeWords[3]):
          return isLimerick
        elif self.rhymes(rhymeWords[1], rhymeWords[2]):
          return isLimerick
        else:
          isLimerick = True

        # isLimerick is True as all limerick criteria have been satisfied
        return isLimerick

    def apostrophe_tokenize(self, line):
      """
      Finds all tokens that either match an alphanumeric pattern (\w) but the 
      pattern also allows for apostrophes (hence the \w') OR tokens that match
      a punctuation mark. The list of punctuation marks is the list in 
      string.punctuation minus the apostrophe character
      """
      tokens = re.findall(r"[\w']+|[\"#$!%&()*+,-./:;<=>\?@\[\]^_`{|}~]", line)
      return tokens

    def guess_syllables(self, word):
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


# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")

  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

if __name__ == '__main__':
  main()
