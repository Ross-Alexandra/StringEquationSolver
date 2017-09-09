from sys import argv
from math import pow

def SolveEqt(eqt:str):
	eqt = equationify(eqt)
	eqt = bedmasify(eqt)
	print(eqt)

def find_operation(eqt: str):
	for character in eqt:
		if not character.isdigit() or character == ',':
			return character
	return None

def bedmasify(eqt: list) -> list:
	while '(' in eqt:
		open_par = eqt.index('(')
		close_par = eqt.index(')')

		eqt[open_par: close_par + 1] = bedmasify(eqt[open_par + 1: close_par])
	print(eqt)
	while '^' in eqt:
		hat = eqt.index('^')
		base_pos = hat - 1
		exp_pos = hat + 1
		base = float(eqt[base_pos])
		exponent = float(eqt[exp_pos])
		eval = pow(int(base), int(exponent))

		print(base_pos, hat, exp_pos, sep=' ')

		eqt[base_pos: exp_pos + 1] = [eval]
	print(eqt)

	while '*' in eqt or '/' in eqt:
		try:
			mul = eqt.index('*')
		except ValueError:
			mul = len(eqt) + 1
		try:
			div = eqt.index('/')
		except ValueError:
			div = len(eqt) + 1

		multiply = False
		if mul < div:
			multiply = True

		sym_position = min([mul, div])
		first_pos = sym_position - 1
		second_pos = sym_position + 1

		print(first_pos, second_pos, sep=' ')

		first = float(eqt[first_pos])
		second = float(eqt[second_pos])

		if multiply:
			eval = first * second
		else:
			eval = first / second

		eqt[first_pos:second_pos + 1] = [eval]
		print(eqt)

def equationify(eqt: str):
	proper = ""
	symbol = True
	eqt = "".join(eqt.split())
	operations = ['+', '-', '*', 'x', 'X', '/', '^', '(', ')']
	for index, character in enumerate(eqt):
		if character.isdigit():
			if symbol:
				symbol = False
			proper += character
		elif character in operations:
			if not symbol:
				symbol = True
				if 'x' == character.lower():
					proper += "*"
				else:
					proper += character
			elif character == '-':
				proper += ':' #: ':' is being used to signify a negative value.
			elif character == '(' or character == ')':
				proper += character

	if '(' in proper and ')' not in proper:
		proper += ')'

	eqt = []
	builder = ""
	for character in proper:
		if  character in operations:
			if builder != "":
				eqt.append(builder)
			eqt.append(character)
			builder = ""
		elif character == ':':
			builder += '-'
		else:
			builder += character
	eqt.append(builder)
	return eqt

if argv[1] != "n":
	SolveEqt(argv[1])
else:
	pass
