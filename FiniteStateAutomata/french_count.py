import sys
from fst import FST
from fsmutils import composewords

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    f.add_state('start')
    f.initial_state = 'start'

    f.add_state('200-999')    
    f.add_state('100-199')
    f.add_state('<100')
    f.add_state('*00')
    f.add_state('1-9')
    f.add_state('10-16')
    f.add_state('17-19')
    f.add_state('et-1') #for 21, 31, etc...
    f.add_state('20-69')
    f.add_state('et-2') #for 71
    f.add_state('70-79')
    f.add_state('80-89')
    f.add_state('90-99')

    f.add_state('final-state')

    f.set_final('*00')
    f.set_final('1-9')
    f.set_final('10-16')
    f.set_final('17-19')
    f.set_final('20-69')
    f.set_final('70-79')
    f.set_final('80-89')
    f.set_final('90-99')

    # No hundreds digit (0 will be leading item in list)
    f.add_arc('start', '<100', '0', ())

    # Translate the 1 in the hundreds digit to "cent"
    f.add_arc('start', '100-199', '1', [kFRENCH_TRANS[100]])

    # For 200 - 999, the hundreds digit needs to have the corresponding ones
    # digit french word prior to "cent" (like "deux cent")
    for i in xrange(2, 10):
        f.add_arc('start', '200-999', str(i), [kFRENCH_TRANS[i]] + [kFRENCH_TRANS[100]])

    # '00' in tens and one digits
    f.add_arc('200-999', '*00', '00', ())
    f.add_arc('100-199', '*00', '00', ())
    f.add_arc('<100', '*00', '00', [kFRENCH_TRANS[0]])

    # '01' - '09' in tens/ones digits
    f.add_arc('200-999', '1-9', '0', ())
    f.add_arc('100-199', '1-9', '0', ())
    f.add_arc('<100', '1-9', '0', ())
    for ii in xrange(1, 10):
        f.add_arc('1-9', '1-9', str(ii), [kFRENCH_TRANS[ii]])
        f.add_arc('1-9', '1-9', str(ii), [kFRENCH_TRANS[ii]])
        f.add_arc('1-9', '1-9', str(ii), [kFRENCH_TRANS[ii]])


    # '10' - '16' in tens and ones digits
    # These values have special names so ignore the 1 in the tens digit and
    # translate based off the ones digit
    f.add_arc('200-999', '10-16', '1', ())
    f.add_arc('100-199', '10-16', '1', ())
    f.add_arc('<100', '10-16', '1', ())
    f.add_arc('10-16', '10-16', '0', [kFRENCH_TRANS[10]])
    f.add_arc('10-16', '10-16', '1', [kFRENCH_TRANS[11]])
    f.add_arc('10-16', '10-16', '2', [kFRENCH_TRANS[12]])
    f.add_arc('10-16', '10-16', '3', [kFRENCH_TRANS[13]])
    f.add_arc('10-16', '10-16', '4', [kFRENCH_TRANS[14]])
    f.add_arc('10-16', '10-16', '5', [kFRENCH_TRANS[15]])
    f.add_arc('10-16', '10-16', '6', [kFRENCH_TRANS[16]])

    # '17' - '19' in tens and ones digits
    f.add_arc('200-999', '17-19', '1', [kFRENCH_TRANS[10]])
    f.add_arc('100-199', '17-19', '1', [kFRENCH_TRANS[10]])
    f.add_arc('<100', '17-19', '1', [kFRENCH_TRANS[10]])
    f.add_arc('17-19', '17-19', '7', [kFRENCH_TRANS[7]])
    f.add_arc('17-19', '17-19', '8', [kFRENCH_TRANS[8]])
    f.add_arc('17-19', '17-19', '9', [kFRENCH_TRANS[9]])

    # '20' - '69' in tens and ones digits

    # Handle 10s digit
    f.add_arc('200-999', '20-69', '2', [kFRENCH_TRANS[20]])
    f.add_arc('100-199', '20-69', '2', [kFRENCH_TRANS[20]])
    f.add_arc('<100', '20-69', '2', [kFRENCH_TRANS[20]])
    f.add_arc('200-999', '20-69', '3', [kFRENCH_TRANS[30]])
    f.add_arc('100-199', '20-69', '3', [kFRENCH_TRANS[30]])
    f.add_arc('<100', '20-69', '3', [kFRENCH_TRANS[30]])
    f.add_arc('200-999', '20-69', '4', [kFRENCH_TRANS[40]])
    f.add_arc('100-199', '20-69', '4', [kFRENCH_TRANS[40]])
    f.add_arc('<100', '20-69', '4', [kFRENCH_TRANS[40]])
    f.add_arc('200-999', '20-69', '5', [kFRENCH_TRANS[50]])
    f.add_arc('100-199', '20-69', '5', [kFRENCH_TRANS[50]])
    f.add_arc('<100', '20-69', '5', [kFRENCH_TRANS[50]])
    f.add_arc('200-999', '20-69', '6', [kFRENCH_TRANS[60]])
    f.add_arc('100-199', '20-69', '6', [kFRENCH_TRANS[60]])
    f.add_arc('<100', '20-69', '6', [kFRENCH_TRANS[60]])

    # Handle 1s digit for normal case (2-9)
    for i in xrange(2, 10):
        f.add_arc('20-69', '20-69', str(i), [kFRENCH_TRANS[i]])

    # Handle '0' in 1s digit
    f.add_arc('20-69', '20-69', '0', ())

    #Handle '1' in 1s digit
    f.add_arc('20-69', 'et-1', '1', [kFRENCH_AND])
    f.add_arc('et-1', '20-69', (), [kFRENCH_TRANS[1]])

    # '70' - '79' in tens and ones digits

    #handle 10s digit
    f.add_arc('200-999', '70-79', '7', [kFRENCH_TRANS[60]])
    f.add_arc('100-199', '70-79', '7', [kFRENCH_TRANS[60]])
    f.add_arc('<100', '70-79', '7', [kFRENCH_TRANS[60]])

    # Handle '1' in 1s digit (71)
    f.add_arc('70-79', 'et-2', '1', [kFRENCH_AND])
    f.add_arc('et-2', '70-79', (), [kFRENCH_TRANS[11]])

    # Handle '0' and '2' through '6' in 1s digit
    f.add_arc('70-79', '70-79', '0', [kFRENCH_TRANS[10]])
    f.add_arc('70-79', '70-79', '2', [kFRENCH_TRANS[12]])
    f.add_arc('70-79', '70-79', '3', [kFRENCH_TRANS[13]])
    f.add_arc('70-79', '70-79', '4', [kFRENCH_TRANS[14]])
    f.add_arc('70-79', '70-79', '5', [kFRENCH_TRANS[15]])
    f.add_arc('70-79', '70-79', '6', [kFRENCH_TRANS[16]])

    # Handle '7' through '9' in 1s digit
    f.add_arc('70-79', '70-79', '7', [kFRENCH_TRANS[10]] + [kFRENCH_TRANS[7]])
    f.add_arc('70-79', '70-79', '8', [kFRENCH_TRANS[10]] + [kFRENCH_TRANS[8]])
    f.add_arc('70-79', '70-79', '9', [kFRENCH_TRANS[10]] + [kFRENCH_TRANS[9]])


    # '80' - '89' in tens and ones digits
    f.add_arc('200-999', '80-89', '8', [kFRENCH_TRANS[4]] + [kFRENCH_TRANS[20]])
    f.add_arc('100-199', '80-89', '8', [kFRENCH_TRANS[4]] + [kFRENCH_TRANS[20]])
    f.add_arc('<100', '80-89', '8', [kFRENCH_TRANS[4]] + [kFRENCH_TRANS[20]])

    # Handle 1s digit for normal case for '81' - '89'
    for i in xrange(1, 10):
        f.add_arc('80-89', '80-89', str(i), [kFRENCH_TRANS[i]])

    # Handle '80'
    f.add_arc('80-89', '80-89', '0', ())

    # Handles 90-99 in 10s and 1s digit

    # Handle 10s digit
    f.add_arc('200-999', '90-99', '9', [kFRENCH_TRANS[4]] + [kFRENCH_TRANS[20]])
    f.add_arc('100-199', '90-99', '9', [kFRENCH_TRANS[4]] + [kFRENCH_TRANS[20]])
    f.add_arc('<100', '90-99', '9', [kFRENCH_TRANS[4]] + [kFRENCH_TRANS[20]])
    
    # Handle '0' through '6' in 1s digit
    f.add_arc('90-99', '90-99', '0', [kFRENCH_TRANS[10]])
    f.add_arc('90-99', '90-99', '1', [kFRENCH_TRANS[11]])
    f.add_arc('90-99', '90-99', '2', [kFRENCH_TRANS[12]])
    f.add_arc('90-99', '90-99', '3', [kFRENCH_TRANS[13]])
    f.add_arc('90-99', '90-99', '4', [kFRENCH_TRANS[14]])
    f.add_arc('90-99', '90-99', '5', [kFRENCH_TRANS[15]])
    f.add_arc('90-99', '90-99', '6', [kFRENCH_TRANS[16]])

    # Handle '7' through '9' in 1s digit
    f.add_arc('90-99', '90-99', '7', [kFRENCH_TRANS[10]] + [kFRENCH_TRANS[7]])
    f.add_arc('90-99', '90-99', '8', [kFRENCH_TRANS[10]] + [kFRENCH_TRANS[8]])
    f.add_arc('90-99', '90-99', '9', [kFRENCH_TRANS[10]] + [kFRENCH_TRANS[9]])
    
    return f

if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))
