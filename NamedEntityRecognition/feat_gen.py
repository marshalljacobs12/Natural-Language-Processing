#!/bin/python
import os
import re
import string
import nltk

lexiconDict = {}
clusterDict = {}
featureClusterDict = {}

# CITE: https://gist.github.com/kissgyorgy/5734469
regex = re.compile('[%s\s]+' % re.escape(string.punctuation))

def load_lexicons(path):
    for d in os.listdir(path):
        lexiconDict[d] = set()
        for line in open(path + '/' + d):
            word = line.rstrip('\n')
            word = word.strip(' ').lower()
            # replace sequences of one or more punctuation marks/white spaces with a single white space
            word = regex.sub(' ', word)
            if word and word not in lexiconDict[d]:
                lexiconDict[d].add(word)

def load_brown_clusters(path):
    with open(path,"r") as f_in:
        for line in f_in:
            (clusterId, word, count) = line.strip().split()
            word = str(word).upper()
            clusterDict[word] = clusterId

def preprocess_corpus(train_sents):
    """Use the sentences to do whatever preprocessing you think is suitable,
    such as counts, keeping track of rare features/words to remove, matches to lexicons,
    loading files, and so on. Avoid doing any of this in token2features, since
    that will be called on every token of every sentence.

    Of course, this is an optional function.

    Note that you can also call token2features here to aggregate feature counts, etc.
    """
    load_brown_clusters('./data/brown_clusters800.txt')

    load_lexicons('./data/lexicon')

def token2features(sent, i, add_neighs = True):
    """Compute the features of a token.

    All the features are boolean, i.e. they appear or they do not. For the token,
    you have to return a set of strings that represent the features that *fire*
    for the token. See the code below.

    The token is at position i, and the rest of the sentence is provided as well.
    Try to make this efficient, since it is called on every token.

    One thing to note is that it is only called once per token, i.e. we do not call
    this function in the inner loops of training. So if your training is slow, it's
    not because of how long it's taking to run this code. That said, if your number
    of features is quite large, that will cause slowdowns for sure.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """
    ftrs = []
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")

    # the word itself
    word = unicode(sent[i])
    ftrs.append("WORD=" + word)
    ftrs.append("LCASE=" + word.lower())
    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric():
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")
    if word and word[0].isupper():
        ftrs.append('IS_CAPITALIZED')

    # LEXICON RELATED FEATURES
    # CHECK TO SEE IF A LEXICON ELEMENT APPEARS IN THIS TOKENS WINDOW WHILE
    # INCREASING SIZE OF WINDOW. FEATURES REVEAL WHETHER IT IS A PARTIAL WINDOW
    # (I.E. JUST FORWARDS OR BACKWARDS FROM THE TOKEN) AS WELL AS THE SIZE OF THE
    # WINDOW. 

    # first check the word with a window of size 0 (meaning just the token itself)
    # to see if it matches any elements in the lexicons
    token = word.rstrip('\n')
    token = token.strip(' ').lower()
    token = regex.sub(' ', token)
    for k, v in lexiconDict.iteritems():
        if token in v:
            ftrs.append('LEXICON_' + k + '_SINGLE_TOKEN')

    # Now check to see if any lexicon elements appear in windows ranging from size
    # 1 to size 3. 
    windowSize = 3
    for j in xrange(1, windowSize+1):
        # Check a half-window (just RHS) that include this token + the next j tokens
        start = i #index of current token in sentence
        end = i + j + 1
        if start > -1 and end < len(sent)+1:
            token = ' '.join(sent[start:end]).lower().strip(string.punctuation)
            token = regex.sub(' ', token)
            for k, v in lexiconDict.iteritems():
                if token in v:
                    ftrs.append('LEXICON_' + k + '_FWD' + str(j))
                    continue

        # Check a half-window (just LHS) that include the previous j tokens + this token
        start = i-j
        end = i+1
        if start > -1 and end < len(sent)+1:
            token = ' '.join(sent[start:end]).lower().strip(string.punctuation)
            token = regex.sub(' ', token)
            for k, v in lexiconDict.iteritems():
                if token in v:
                    ftrs.append('LEXICON_' + k + '_BWD' + str(j))
                    continue

        # Check the full window which includes the previous j tokens, this token, and the
        # next j tokens that follow
        start = i-j
        end = i+j+1
        if start > -1 and end < len(sent)+1:
            token = ' '.join(sent[start:end]).lower().strip(string.punctuation)
            token = regex.sub(' ', token)
            for k, v in lexiconDict.iteritems():
                if token in v:
                    ftrs.append('LEXICON_' + k + '_WINDOW' + str(j))
                    continue

    # prefixes and suffixes
    prefix1 = word[0]
    ftrs.append('PREFIX1=' + prefix1.upper())
    prefix2 = word[:2]
    ftrs.append('PREFIX2=' + prefix2.upper())
    prefix3 = word[:3]
    ftrs.append('PREFIX3=' + prefix3.upper())
    prefix4 = word[:4]
    ftrs.append('PREFIX4=' + prefix4.upper())
    suffix1 = word[-1]
    ftrs.append('SUFFIX1=' + suffix1.upper())
    suffix2 = word[-2:]
    ftrs.append('SUFFIX2=' + suffix2.upper())
    suffix3 = word[-3:]
    ftrs.append('SUFFIX3=' + suffix3.upper())
    suffix4 = word[-4:]
    ftrs.append('SUFFIX4=' + suffix4.upper())

    # word shape
    shape = ''
    for c in word:
        if c in string.ascii_uppercase:
            shape = shape + 'X'
        elif c in string.ascii_lowercase:
            shape = shape + 'x'
        elif c in string.digits:
            shape = shape + 'd'
        elif c in string.punctuation:
            shape += c

    # appending word shape and adding short word shape
    if len(shape) != 0:
        ftrs.append('SHAPE=' + shape)
        shortShape = ''
        currentLetter = shape[0]
        shortShape = shortShape + currentLetter
        for c in shape:
            if c != currentLetter:
                currentLetter = c
                shortShape = shortShape + currentLetter
        ftrs.append('SHORT_SHAPE=' + shortShape)

    # POS tag
    t = nltk.pos_tag([word])
    (token, tag) = t[0]
    if tag == 'CC':
        ftrs.append("CC")
    elif tag == 'CD':
        ftrs.append("CD")
    elif tag == 'DT':
        ftrs.append('DT')
    elif tag == 'FW':
        ftrs.append('FW')
    elif tag == 'IN':
        ftrs.append('IN')
    elif tag == 'JJ':
        ftrs.append('JJ')
    elif tag == 'JJR':
        ftrs.append('JJR')
    elif tag == 'JJS':
        ftrs.append('JJS')
    elif tag == 'LS':
        ftrs.append('LS')
    elif tag == 'NN':
        ftrs.append('NN')
    elif tag == 'NNS':
        ftrs.append('NNS')
    elif tag == 'NNP':
        ftrs.append('NNP')
    elif tag == 'NNPS':
        ftrs.append('NNPS')
    elif tag == 'PDT':
        ftrs.append('PDT')
    elif tag == 'POS':
        ftrs.append('POS')
    elif tag == 'PRP':
        ftrs.append('PRP')
    elif tag == 'PRP$':
        ftrs.append('PRP$')
    elif tag == 'RB':
        ftrs.append('RB')
    elif tag == 'RBR':
        ftrs.append('RBR')
    elif tag == 'RBS':
        ftrs.append('RBS')
    elif tag == 'SYM':
        ftrs.append('SYM')
    elif tag == 'TO':
        ftrs.append('TO')
    elif tag == 'UH':
        ftrs.append('UH')
    elif tag == 'VB':
        ftrs.append('VB')
    elif tag == 'VBD':
        ftrs.append('VBD')
    elif tag == 'VBG':
        ftrs.append('VBG')
    elif tag == 'VBN':
        ftrs.append('VBN')
    elif tag == 'VBP':
        ftrs.append('VBP')
    elif tag == 'VBZ':
        ftrs.append('VBZ')
    elif tag == 'WDT':
        ftrs.append('WDT')
    elif tag == 'WP':
        ftrs.append('WP')
    elif tag == 'WP$':
        ftrs.append('WP$')
    elif tag == 'WRB':
        ftrs.append('WRB')
        

    # Cluster ID   
    if word in clusterDict:
        ftrs.append('CLUSTERID=' + clusterDict[word])

    # previous/next word feats
    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i-1, add_neighs = False):
                ftrs.append("PREV_" + pf)
        if i < len(sent)-1:
            for pf in token2features(sent, i+1, add_neighs = False):
                ftrs.append("NEXT_" + pf)

    # return it!
    return ftrs

if __name__ == "__main__":
    sents = [
    [ "I", "love", "food" ]
    ]
    preprocess_corpus(sents)
    for sent in sents:
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i)
