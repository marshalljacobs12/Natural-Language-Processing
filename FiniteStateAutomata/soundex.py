from fst import FST
import string, sys
from fsmutils import composechars, trace

def letters_to_numbers():
	"""
	Returns an FST that converts letters to numbers as specified by
	the soundex algorithm
	"""
	remove = ['a', 'e', 'h', 'i', 'o', 'u', 'w', 'y']
	group1 = ['b', 'f', 'p', 'v']
	group2 = ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z']
	group3 = ['d', 't']
	group4 = ['l']
	group5 = ['m', 'n']
	group6 = ['r']

	# Let's define our first FST
	f1 = FST('soundex-generate')

	# Indicate that 'start' is the initial state
	f1.add_state('start')
	f1.add_state('1')
	f1.add_state('2')
	f1.add_state('3')
	f1.add_state('4')
	f1.add_state('5')
	f1.add_state('6')
	f1.add_state('7')
	f1.add_state('8')
	f1.add_state('9')
	f1.add_state('10')
	f1.add_state('11')
	f1.add_state('12')
	f1.add_state('13')
	f1.add_state('14')
	f1.add_state('15')
	f1.add_state('16')
	f1.add_state('17')
	f1.add_state('18')
	f1.add_state('19')
	f1.add_state('20')

	f1.initial_state = 'start'

	# Set all the final states
	f1.set_final('16')
	f1.set_final('17')
	f1.set_final('18')
	f1.set_final('19')
	f1.set_final('20')

	for letter in string.ascii_letters:
		f1.add_arc('start', '1', (letter), (letter))
		if letter in remove:
			f1.add_arc('1', '1', (letter), ())
			f1.add_arc('2', '8', (letter), ())
			f1.add_arc('3', '8', (letter), ())
			f1.add_arc('4', '8', (letter), ())
			f1.add_arc('5', '8', (letter), ())
			f1.add_arc('6', '8', (letter), ())
			f1.add_arc('7', '8', (letter), ())
			f1.add_arc('8', '8', (letter), ())
			f1.add_arc('9', '15', (letter), ())
			f1.add_arc('10', '15', (letter), ())
			f1.add_arc('11', '15', (letter), ())
			f1.add_arc('12', '15', (letter), ())
			f1.add_arc('13', '15', (letter), ())
			f1.add_arc('14', '15', (letter), ())
			f1.add_arc('15', '15', (letter), ())
			f1.add_arc('16', '16', (letter), ())

		elif letter in group1:
			f1.add_arc('1', '2', (letter), ('1'))
			f1.add_arc('2', '2', (letter), ())
			f1.add_arc('3', '9', (letter), ('1'))
			f1.add_arc('4', '9', (letter), ('1'))
			f1.add_arc('5', '9', (letter), ('1'))
			f1.add_arc('6', '9', (letter), ('1'))
			f1.add_arc('7', '9', (letter), ('1'))
			f1.add_arc('8', '9', (letter), ('1'))
			f1.add_arc('9', '9', (letter), ())
			f1.add_arc('10', '16', (letter), ('1'))
			f1.add_arc('11', '16', (letter), ('1'))
			f1.add_arc('12', '16', (letter), ('1'))
			f1.add_arc('13', '16', (letter), ('1'))
			f1.add_arc('14', '16', (letter), ('1'))
			f1.add_arc('15', '16', (letter), ('1'))
			f1.add_arc('16', '16', (letter), ('1'))

		elif letter in group2:
			f1.add_arc('1', '3', (letter), ('2'))
			f1.add_arc('3', '3', (letter), ())
			f1.add_arc('2', '10', (letter), ('2'))
			f1.add_arc('4', '10', (letter), ('2'))
			f1.add_arc('5', '10', (letter), ('2'))
			f1.add_arc('6', '10', (letter), ('2'))
			f1.add_arc('7', '10', (letter), ('2'))
			f1.add_arc('8', '10', (letter), ('2'))
			f1.add_arc('10', '10', (letter), ())
			f1.add_arc('9', '16', (letter), ('2'))
			f1.add_arc('11', '16', (letter), ('2'))
			f1.add_arc('12', '16', (letter), ('2'))
			f1.add_arc('13', '16', (letter), ('2'))
			f1.add_arc('14', '16', (letter), ('2'))
			f1.add_arc('15', '16', (letter), ('2'))
			f1.add_arc('16', '16', (letter), ('2'))

		elif letter in group3:
			f1.add_arc('1', '4', (letter), ('3'))
			f1.add_arc('4', '4', (letter), ())
			f1.add_arc('2', '11', (letter), ('3'))
			f1.add_arc('3', '11', (letter), ('3'))
			f1.add_arc('5', '11', (letter), ('3'))
			f1.add_arc('6', '11', (letter), ('3'))
			f1.add_arc('7', '11', (letter), ('3'))
			f1.add_arc('8', '11', (letter), ('3'))
			f1.add_arc('11', '11', (letter), ())
			f1.add_arc('9', '16', (letter), ('3'))
			f1.add_arc('10', '16', (letter), ('3'))
			f1.add_arc('12', '16', (letter), ('3'))
			f1.add_arc('13', '16', (letter), ('3'))
			f1.add_arc('14', '16', (letter), ('3'))
			f1.add_arc('15', '16', (letter), ('3'))
			f1.add_arc('16', '16', (letter), ('3'))

		elif letter in group4:
			f1.add_arc('1', '5', (letter), ('4'))
			f1.add_arc('5', '5', (letter), ())
			f1.add_arc('2', '12', (letter), ('4'))
			f1.add_arc('3', '12', (letter), ('4'))
			f1.add_arc('4', '12', (letter), ('4'))
			f1.add_arc('6', '12', (letter), ('4'))
			f1.add_arc('7', '12', (letter), ('4'))
			f1.add_arc('8', '12', (letter), ('4'))
			f1.add_arc('12', '12', (letter), ())
			f1.add_arc('9', '16', (letter), ('4'))
			f1.add_arc('10', '16', (letter), ('4'))
			f1.add_arc('11', '16', (letter), ('4'))
			f1.add_arc('13', '16', (letter), ('4'))
			f1.add_arc('14', '16', (letter), ('4'))
			f1.add_arc('15', '16', (letter), ('4'))
			f1.add_arc('16', '16', (letter), ('4'))

		elif letter in group5:
			f1.add_arc('1', '6', (letter), ('5'))
			f1.add_arc('6', '6', (letter), ())
			f1.add_arc('2', '13', (letter), ('5'))
			f1.add_arc('3', '13', (letter), ('5'))
			f1.add_arc('4', '13', (letter), ('5'))
			f1.add_arc('5', '13', (letter), ('5'))
			f1.add_arc('7', '13', (letter), ('5'))
			f1.add_arc('8', '13', (letter), ('5'))
			f1.add_arc('13', '13', (letter), ())
			f1.add_arc('9', '16', (letter), ('5'))
			f1.add_arc('10', '16', (letter), ('5'))
			f1.add_arc('11', '16', (letter), ('5'))
			f1.add_arc('12', '16', (letter), ('5'))
			f1.add_arc('14', '16', (letter), ('5'))
			f1.add_arc('15', '16', (letter), ('5'))
			f1.add_arc('16', '16', (letter), ('5'))

		elif letter in group6:
			f1.add_arc('1', '7', (letter), ('6'))
			f1.add_arc('7', '7', (letter), ())
			f1.add_arc('2', '14', (letter), ('6'))
			f1.add_arc('3', '14', (letter), ('6'))
			f1.add_arc('4', '14', (letter), ('6'))
			f1.add_arc('5', '14', (letter), ('6'))
			f1.add_arc('6', '14', (letter), ('6'))
			f1.add_arc('8', '14', (letter), ('6'))
			f1.add_arc('14', '14', (letter), ())
			f1.add_arc('9', '16', (letter), ('6'))
			f1.add_arc('10', '16', (letter), ('6'))
			f1.add_arc('11', '16', (letter), ('6'))
			f1.add_arc('12', '16', (letter), ('6'))
			f1.add_arc('13', '16', (letter), ('6'))
			f1.add_arc('15', '16', (letter), ('6'))
			f1.add_arc('16', '16', (letter), ('6'))
		
		else:
			f1.add_arc('1', '17', (), ())
			f1.add_arc('2', '18', (), ())
			f1.add_arc('3', '18', (), ())
			f1.add_arc('4', '18', (), ())
			f1.add_arc('5', '18', (), ())
			f1.add_arc('6', '18', (), ())
			f1.add_arc('7', '18', (), ())
			f1.add_arc('8', '18', (), ())
			f1.add_arc('9', '19', (), ())
			f1.add_arc('10', '19', (), ())
			f1.add_arc('11', '19', (), ())
			f1.add_arc('12', '19', (), ())
			f1.add_arc('13', '19', (), ())
			f1.add_arc('14', '19', (), ())
			f1.add_arc('15', '19', (), ())
			f1.add_arc('16', '20', (), ())
	
	return f1

	# The stub code above converts all letters except the first into '0'.
	# How can you change it to do the right conversion?

def truncate_to_three_digits():
	"""
	Create an FST that will truncate a soundex string to three digits
	"""

	# Ok so now let's do the second FST, the one that will truncate
	# the number of digits to 3
	f2 = FST('soundex-truncate')

	# Indicate initial and final states
	f2.add_state('1')
	f2.add_state('2')
	f2.add_state('3')
	f2.add_state('4')
	f2.initial_state = '1'
	# Need to account for truncation scenarious where soundex string is less
	# than four characters
	f2.set_final('2')
	f2.set_final('3')
	f2.set_final('4')

	# Add the arcs
	for letter in string.letters:
		f2.add_arc('1', '1', (letter), (letter))

	for n in range(10):
		f2.add_arc('1', '2', (str(n)), (str(n)))
		
	for n in range(10):
		f2.add_arc('2', '3', (str(n)), (str(n)))

	for n in range(10):
		f2.add_arc('3', '4', (str(n)), (str(n)))

	for n in range(10):
		f2.add_arc('4', '4', (str(n)), ())

	return f2

def add_zero_padding():
	# Now, the third fst - the zero-padding fst
	f3 = FST('soundex-padzero')

	f3.add_state('1')
	f3.add_state('1a')
	f3.add_state('1b')
	f3.add_state('2')

	f3.initial_state = '1'

	# The soundex string will either need no padding in which case its final 
	# state is 1, or it will need 1 to 3 zeros and have final state 2
	f3.set_final('1')
	f3.set_final('2')

	f3.add_arc('1', '2', (), ('000'))
	f3.add_arc('1a', '2', (), ('00'))
	f3.add_arc('1b', '2', (), ('0'))

	for letter in string.letters:
		f3.add_arc('1', '1', (letter), (letter))
	for number in xrange(10):
		f3.add_arc('1', '1a', (str(number)), (str(number)))
	for number in xrange(10):
		f3.add_arc('1a', '1b', (str(number)), (str(number)))
	for number in xrange(10):
		f3.add_arc('1b', '2', (str(number)), (str(number)))

	return f3

if __name__ == '__main__':
	user_input = raw_input().strip()
	f1 = letters_to_numbers()
	f2 = truncate_to_three_digits()
	f3 = add_zero_padding()

	if user_input:
		print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))
