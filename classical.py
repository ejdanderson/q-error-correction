"""
10.2.1 (a). Consider the restricted bit-flip error model where at most 1 bit flip
can occur within each codeword. For the three-bit code, show that the
condition for classical error correction holds; and so it is possible
to uambiguously correct single bit flips using this code.
"""

"""
error_1 : first bit flipped
000 => 001 (1)
001 => 000 (0)
010 => 011 (3)
011 => 010 (2)
100 => 101 (5)
101 => 100 (4)
110 => 111 (7)
111 => 110 (6)

error_2 : second bit flipped
000 => 010 (2)
001 => 011 (3)
010 => 000 (0)
011 => 001 (1)
100 => 110 (6)
101 => 111 (7)
110 => 100 (4)
111 => 101 (5)

error_3 : third bit flipped
000 => 100 (4)
001 => 101 (5)
010 => 110 (6)
011 => 111 (7)
100 => 000 (0)
101 => 001 (1)
110 => 010 (2)
111 => 011 (3)
"""

import itertools
import numpy as np

no_flip = np.matrix(np.identity(8))

flip_first = np.matrix([ \
	[0,1,0,0,0,0,0,0], \
	[1,0,0,0,0,0,0,0], \
	[0,0,0,1,0,0,0,0], \
	[0,0,1,0,0,0,0,0], \
	[0,0,0,0,0,1,0,0], \
	[0,0,0,0,1,0,0,0], \
	[0,0,0,0,0,0,0,1], \
	[0,0,0,0,0,0,1,0]  \
])
flip_second = np.matrix([ \
	[0,0,1,0,0,0,0,0], \
	[0,0,0,1,0,0,0,0], \
	[1,0,0,0,0,0,0,0], \
	[0,1,0,0,0,0,0,0], \
	[0,0,0,0,0,0,1,0], \
	[0,0,0,0,0,0,0,1], \
	[0,0,0,0,1,0,0,0], \
	[0,0,0,0,0,1,0,0]  \
])
flip_third = np.matrix([ \
	[0,0,0,0,1,0,0,0], \
	[0,0,0,0,0,1,0,0], \
	[0,0,0,0,0,0,1,0], \
	[0,0,0,0,0,0,0,1], \
	[1,0,0,0,0,0,0,0], \
	[0,1,0,0,0,0,0,0], \
	[0,0,1,0,0,0,0,0], \
	[0,0,0,1,0,0,0,0]  \
])

def bit_to_vector(bit_string) :
	bit_dict = { \
		'000' : np.matrix([1,0,0,0,0,0,0,0]).T, \
		'001' : np.matrix([0,1,0,0,0,0,0,0]).T, \
		'010' : np.matrix([0,0,1,0,0,0,0,0]).T, \
		'011' : np.matrix([0,0,0,1,0,0,0,0]).T, \
		'100' : np.matrix([0,0,0,0,1,0,0,0]).T, \
		'101' : np.matrix([0,0,0,0,0,1,0,0]).T, \
		'110' : np.matrix([0,0,0,0,0,0,1,0]).T, \
		'111' : np.matrix([0,0,0,0,0,0,0,1]).T
	}
	return bit_dict[bit_string]


def classical_a(error_prob):
	case_0 = bit_to_vector('000')
	case_1 = bit_to_vector('111')

	error_ops = [flip_first, flip_second, flip_third]
	set_0 = set()
	set_1 = set()

	noflip_prob = 1 - error_prob




	# Case with no bit flips
	set_0.add((np.binary_repr(np.argmax(case_0), 3), error_prob**3))
	set_1.add((np.binary_repr(np.argmax(case_1), 3), error_prob**3))
	for error_op in error_ops :
		result_0 = np.matmul(error_op, case_0)
		result_1 = np.matmul(error_op, case_1)

		set_0.add(( \
			np.binary_repr(np.argmax(result_0), 3), \
			np.power(error_prob,1) * np.power(noflip_prob,2) \
		))

		set_1.add(( \
			np.binary_repr(np.argmax(result_1), 3), \
			np.power(error_prob,1) * np.power(noflip_prob,2) \
		))

	sym_dif = set_0.symmetric_difference(set_1)
	if 0 == len(sym_dif) :
		print('non-unique')
		print(set_0)
		print(set_1)
	else :
		print('unique')
		print('Case 000: ', set_0)
		print('Case 111: ', set_1)

"""
The Most probable case of generating non-unique sets which break the condition
for classical error correction is allowing p = (1-p) or 0.5
"""
print('======= 10.2.1(a) =======')
classical_a(0.5)
print('=========================\n')


# --------------------------------------------------------------------------- #

"""
10.2.1 (b). Show that under an error model in which 2 or more bit flips can ocur within
each codeword, the condition for classical error correction does not hold, and
so the three-bit code cannot correct these errors
"""

def classical_b(error_prob):
	case_0 = bit_to_vector('000')
	case_1 = bit_to_vector('111')

	error_ops = [flip_first, flip_second, flip_third]
	set_0 = set()
	set_1 = set()

	noflip_prob = 1 - error_prob

	# Case with no bit flips
	set_0.add((np.binary_repr(np.argmax(case_0), 3), error_prob**3))
	set_1.add((np.binary_repr(np.argmax(case_1), 3), error_prob**3))

	for L in range(1, len(error_ops)+1):
		# Generate all possible cases
		for error_chain in itertools.combinations(error_ops, L):
			result_0 = case_0
			result_1 = case_1
			for error_op in error_chain :
				result_0 = np.matmul(error_op, result_0)
				result_1 = np.matmul(error_op, result_1)

			set_0.add(( \
				np.binary_repr(np.argmax(result_0), 3), \
				np.power(error_prob,L) * np.power(noflip_prob,3-L) \
				))

			set_1.add(( \
				np.binary_repr(np.argmax(result_1), 3), \
				np.power(error_prob,L) * np.power(noflip_prob,3-L) \
				))

	sym_dif = set_0.symmetric_difference(set_1)
	if 0 == len(sym_dif) :
		print('non-unique')
		print('Set: ', set_0)
	else :
		print('unique')
		print('Case 000: ', set_0)
		print('Case 111: ', set_1)

"""
The Most probable case of generating non-unique sets which break the condition
for classical error correction is allowing p = (1-p) or 0.5
"""
print('======= 10.2.1(b) =======')
classical_b(0.5)
print('=========================\n')
