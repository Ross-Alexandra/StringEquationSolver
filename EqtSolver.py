from math import pow
import argparse

def SolveEqt(eqt:str, verbose: bool=False) -> float:
	eqt = equationify(eqt)
	outcome = bedmasify(eqt, verbose)
	return outcome

def find_operation(eqt: str):
	for character in eqt:
		if not character.isdigit() or character == ',':
			return character
	return None

def bedmasify(eqt: list, verbose:bool) -> list:
	while '(' in eqt:
		if verbose:
			print_eqt(eqt)
		open_par = eqt.index('(')
		close_par = eqt.index(')')
		if verbose:
			print("\nWithin Brackets-------------------------------------------------")
		eqt[open_par: close_par + 1] = [bedmasify(eqt[open_par + 1: close_par], verbose)]
		if verbose:
			print("Exiting Brackets------------------------------------------------\n")

	while '^' in eqt:
		if verbose:
			print_eqt(eqt)
		hat = eqt.index('^')
		base_pos = hat - 1
		exp_pos = hat + 1
		base = float(eqt[base_pos])
		exponent = float(eqt[exp_pos])
		eval = pow(int(base), int(exponent))

		eqt[base_pos: exp_pos + 1] = [eval]

	while '*' in eqt or '/' in eqt:
		if verbose:
			print_eqt(eqt)
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

		first = float(eqt[first_pos])
		second = float(eqt[second_pos])

		if multiply:
			eval = first * second
		else:
			eval = first / second

		eqt[first_pos:second_pos + 1] = [eval]

	while '+' in eqt or '-' in eqt:
		if verbose:
			print_eqt(eqt)
		try:
			add = eqt.index('+')
		except ValueError:
			add = len(eqt) + 1

		try:
			sub = eqt.index('-')
		except ValueError:
			sub = len(eqt) + 1

		add = False
		if add < sub:
			add = True

		sym_position = min([add, sub])
		first_pos = sym_position - 1
		second_pos = sym_position + 1

		first = float(eqt[first_pos])
		second = float(eqt[second_pos])

		if add:
			eval = first + second
		else:
			eval = first - second

		eqt[first_pos:second_pos + 1] = [eval]
	return eqt[0]

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
				if character != ')':
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
	if builder != "":
		eqt.append(builder)
	return eqt

def print_eqt(eqt: list):
	for item in eqt:
		print(item, end=' ')
	print()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Command line equation solver")
	parser.add_argument("Equation", type=str, help="The equation that should be solved.")
	parser.add_argument('-v', "--verbose", action="store_true", help="Output each step of the equation solver.")

	args = parser.parse_args()
	print(SolveEqt(args.Equation, args.verbose))
