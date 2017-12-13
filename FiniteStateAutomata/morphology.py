import re

def iterateRules():
    # the first rule looks for STUFF followed by "e+e" or "e+i"
    # followed by STUFF and removes the initial e (and the '+').
    # e.g. "ice+ing" -> "icing"
    #      "pace+ed" -> "paced"
    yield ("(.*)e\+([ei].*)", "\\1\\2")

    # the next rule removes a '+' if it's between an e and something
    # that is neither an e nor an i
    # e.g. "pace+r" -> "pacer"
    #      "race+s" -> "races"
    yield ("(.+)e\+([^ei].*)", "\\1e\\2")

    # your task is to write the next rule, which should map "_c+ed"
    # and "_c+ing" to a version with "ck" instead, so long as "_" is a
    # vowel.
    #
    # e.g. "traffic+ing" -> "trafficking" (here '_' is an i)
    #      "lilac+ing" -> "lilacking" (here '_' is an a)
    # if you need help with python regular expressions, see:
    #   http://docs.python.org/library/re.html
    #
    # Explanation:
    #
    # Divide the regular expression passed as the first paramaeter into three
    # groups (which are enclosed in parentheses). The first group consists of
    # one or more characters of STUFF, followed by exactly 1 vowel (+ 
    # qualifier creates this pattern). The second group just consists of one
    # character, a 'c'. The '+' character is then excluded from all groups. 
    # The last group uses the | operator to match either the pattern 'ed' or
    # 'ing'. The rule asks us to map _c+ed and _c+ing to a version _cked or
    # _cking given _ is a vowel. The regular expression on the right hand side
    # recalls groups from the regular expression on the left hand side to 
    # implement this rule. \\1 refers to group 1 (.+[aeiou]) which ensures 
    # that the characters in a string before the c are preceded by a vowel (the
    # vowel can be preceded by anything). The second group (c) ensures that
    # what follows the vowel is a c and is referenced by the right hand side 
    # regular expression with \\2. \\2k matches the contents from group (c) 
    # then appends a k, giving the desired behavior of mapping to the "ck" 
    # version if the group 1/3's patterns also match. Finally \\3 references the
    # group (ed|ing), thus mapping _c+ed or _c+ing to _cked or _cking. Because
    # the '+' is omitted from groups 1, 2, and 3, it is deleted during the
    # mapping. 
    yield ("(.+[aeiou])(c)\+(ed|ing)", "\\1\\2k\\3")

def generate(analysis):
    word = analysis
    # apply all rules in sequence
    for (ruleLHS, ruleRHS) in iterateRules():
        word = re.sub("^" + ruleLHS + "$", ruleRHS, word)

    # remove any remaining boundaires.  you may wish to comment this
    # out for debugging purposes
    word = re.sub("\+","", word)
    return word

if __name__ == '__main__':
    user_input = raw_input()
    if user_input:
        print user_input, '-->',
        print generate(user_input)
