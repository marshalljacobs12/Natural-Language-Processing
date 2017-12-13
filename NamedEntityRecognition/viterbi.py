import numpy as np

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is a size N array of integers representing the best sequence.
    """
    L = start_scores.shape[0]
    assert end_scores.shape[0] == L
    assert trans_scores.shape[0] == L
    assert trans_scores.shape[1] == L
    assert emission_scores.shape[1] == L
    N = emission_scores.shape[0]

    #print 'N: ' + str(N)
    #print 'L: ' + str(L)

    viterbi = np.empty((N, L))
    #viterbi.fill(-np.inf)
    backtrack = np.empty((N, L))

    # initialization step
    # add start transition score and emission score from 0 --> i
    # for each label in labels 
    for i in xrange(L):
        viterbi[0, i] = start_scores[i] + emission_scores[0, i]
        #backtrack[0, i] = -1

    # recursion step
    # for every sequence length up to number of tokens
    for i in xrange(1, N):
        # for each label in the set of labels
        for j in xrange(0, L):
            # need to find max viterbi[i-1, k] + trans_scores[k, j] where
            # k is a label in L
            argmax = -np.inf
            argmaxVal = -np.inf
            for k in xrange(0, L):
                x = viterbi[i-1, k] + trans_scores[k, j]
                if x > argmaxVal:
                    argmax = k
                    argmaxVal = x

            score = viterbi[i-1, argmax] + trans_scores[argmax, j] + emission_scores[i, j]

            # necesssary? --> No because for loop finding argmax guarantees each entry only
            # updated once
            #if score > viterbi[i, j]:
            viterbi[i, j] = score
            backtrack[i, j] = argmax

    # add end transition score to total score for each entry
    for i in xrange(L):
        viterbi[N-1, i] = viterbi[N-1, i] + end_scores[i]

    # the index in the last row of the 2d array viterbi can also be interpreted as the
    # tag for the final element
    maxScoreIndex = np.argmax(viterbi[N-1])

    # backtrace best sequence
    sequence = []
    sequence.append(np.argmax(viterbi[N-1]))
    
    index = N-1
    prev = int(backtrack[index, np.argmax(viterbi[index])])

    while index > 0:
        sequence.append(prev)
        index -= 1
        prev = int(backtrack[index, prev])

    # best tags added back to front, so reverse for proper sequence
    sequence.reverse()

    # best score is the element stored in the last row of 2d array viterbi in maxStoreIndex
    return (viterbi[N-1, maxScoreIndex], sequence)

