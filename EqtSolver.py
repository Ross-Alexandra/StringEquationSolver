import argparse

def SolveEqt(eqt:str, verbose: bool=False) -> float:
	""" The main controller, it takes the eqation string
	    and returns the outcome.

	Args:
		eqt(str): The equation string. It is a string
			  containing an equation (ex:
			  1 + 2 / (2 * 4) )
		verbose(bool): Whether or not an output should be
				generated.
	Returns:
		The outcome of the passed equation
	"""

	eqt = equationify(eqt)  #: Get back a list of each valid element for the equation
	outcome = bedmasify(eqt, verbose)  #: Get the outcome of the equation
	return outcome  #: Return the outcome.

def bedmasify(eqt: list, verbose:bool, nested_level: int=0) -> list:
	""" Evaluates the equation based on bedmas/pedmas rules.

	Args:
		eqt(list): A list containing all of the operations and numbers of
			   the equation. (ex ['1', '+', '1', '*', '2'])
		vebose(bool): Whether or not an output should be generated.
	Returns:
		The outcome of the passed equation list.
	"""

	#: Evaluate all equations within curly braces as if they are their
	#: own seperate equations.
	while '{' in eqt:
		if verbose:
			for i in range(nested_level):
				print("\t", end='')
			print_eqt(eqt)

		#: Get the indices of the first opening and closing curl braces.
		open_cur = eqt.index('{')
		close_cur = eqt.index('}')
		if verbose:
			print()
			for i in range(nested_level):
				print("\t", end='')
			print('{')

		#: If nested parenthesis exist, find the outermost closing curly brace..
		i = 0
		while '(' in eqt[open_par + 1: close_par] and ')' not in eqt[open_par + 1: close_par]:
			i += 1
			close_par = eqt.index(')', i)

		#: Black magic of recursion.
		#: Replace the chunk of the list containing the bracketed section
		#: With the outcome of the chunk within brackets by recursively
		#: Evaluating the inside of the brackets.
		#: Example:
		#:	['1', '+', '{', '3', '*', '2', '}']
		#: 	the inside of the brackets (3 * 2) are evaluated recursively
		#:	 so the list becomes:
		#:		['3', '*', '2']
		#:	which is evaluated to [6] by upcoming devices, and then the
		#:	original list becomes:
		#:	['1', '+', '6']
		#: 	which is finally resolved to [7]
		eqt[open_cur: close_cur + 1] = [bedmasify(eqt[open_cur + 1: close_cur], verbose, nested_level + 1)]

		if verbose:
			for i in range(nested_level):
				print("\t", end='')
			print('}\n')

	#: Evalulate all equations within square braces as if they are their own
	#: Seperate equations.
	while '[' in eqt:
		if verbose:
			for i in range(nested_level):
				print("\t", end='')
			print_eqt(eqt)

		#: Get the indices of the first appearing set of opening and
		#: Square Braces.
		open_sq = eqt.index('[')
		close_sq = eqt.index(']')

		if verbose:
			print()
			for i in range(nested_level):
				print("\t", end='')
			print('[')

		#: If nested square brackets exist, find the outermost closing square bracket.
		i = 0
		while '[' in eqt[open_sq + 1: close_sq] and ']' not in eqt[open_sq + 1: close_sq]:
			i += 1
			close_sq = eqt.index(']', i)

		#: Black magic of recursion. PLEASE NOTE, THIS USES THE SAME
		#: FUNCTIONALTY AS THE CURLY BRACES SECTION
		#: Replace the chunk of the list containing the bracketed section
		#: With the outcome of the chunk within brackets by recursively
		#: Evaluating the inside of the brackets.
		#: Example:
		#:	['1', '+', '[', '3', '*', '2', ']']
		#: 	the inside of the brackets (3 * 2) are evaluated recursively
		#:	 so the list becomes:
		#:		['3', '*', '2']
		#:	which is evaluated to [6] by upcoming devices, and then the
		#:	original list becomes:
		#:	['1', '+', '6']
		#: 	which is finally resolved to [7]
		eqt[open_sq: close_sq + 1] = [bedmasify(eqt[open_sq + 1: close_sq], verbose, nested_level + 1)]
		if verbose:
			for i in range(nested_level):
				print("\t", end='')
			print(']\n')

	#: Evaluate all equations within paranthesis as if they are their
	#: own seperate equations.
	while '(' in eqt:
		if verbose:
			for i in range(nested_level):
				print("\t", end='')
			print_eqt(eqt)

		#: Find the first appearance of an opening and closing parenthesis.
		open_par = eqt.index('(')
		close_par = eqt.index(')')

		if verbose:
			print()
			for i in range(nested_level):
				print("\t", end='')
			print('(')

		#: If nested parenthesis exist, find the outermost closing parenthesis.
		i = 0
		while '(' in eqt[open_par + 1: close_par] and ')' not in eqt[open_par + 1: close_par]:
			i += 1
			close_par = eqt.index(')', i)

		#: Black magic of recursion. PLEASE NOTE, THIS USES THE SAME
		#: FUNCTIONALTY AS THE CURLY BRACES SECTION
		#: Replace the chunk of the list containing the bracketed section
		#: With the outcome of the chunk within brackets by recursively
		#: Evaluating the inside of the brackets.
		#: Example:
		#:	['1', '+', '[', '3', '*', '2', ']']
		#: 	the inside of the brackets (3 * 2) are evaluated recursively
		#:	 so the list becomes:
		#:		['3', '*', '2']
		#:	which is evaluated to [6] by upcoming devices, and then the
		#:	original list becomes:
		#:	['1', '+', '6']
		#: 	which is finally resolved to [7]
		eqt[open_par: close_par + 1] = [bedmasify(eqt[open_par + 1: close_par], verbose, nested_level + 1)]
		if verbose:
			for i in range(nested_level):
				print("\t", end='')
			print(")\n")

	#: Evaluate all powers as this comes after brackets/parenthesis in bedmas/pedmas.
	while '^' in eqt:
		if verbose:
			for i in range(nested_level):
				print("\t", end='')
			print_eqt(eqt)

		#: Find the index of the first appearance of the power symbol.
		hat = eqt.index('^')

		base_pos = hat - 1  #: Get the index for the base of the found symbol.
		exp_pos = hat + 1  #: Get the index for the exponent of the found symbol.
		base = float(eqt[base_pos])  #: Gets the value of the base.
		exponent = float(eqt[exp_pos])  #: Gets the value of the exponent.
		eval = float(base) ** float(exponent)  #: Evaluates the exponential expression.

		#: Replace the 'X', '^', 'Y' portion of the list with the
		#: outcome of the exponential expression.
		eqt[base_pos: exp_pos + 1] = [eval]

	#: Evaluate all multiplication and division expressions from left to right
	#: as this comes after exponentials in bedmas/pedmas.
	while '*' in eqt or '/' in eqt:
		if verbose:
			for i in range(nested_level):
				print("\t", end='')
			print_eqt(eqt)
		#: Try to find an index for the multiplication symbol. If it isnt found
		#: Set its position to 1 + the length of the list so that it will be ignored.
		#: PLEASE NOTE:
		#: 	this block of code will never be reached unless either the division
		#: 	or multiplication symbols exist, so setting one of the symbols to
		#:	1 + the length of the list is NOT an issue
		try:
			mul = eqt.index('*')
		except ValueError:
			mul = len(eqt) + 1

		#: Try to find an index  for the division symbol. If it isnt found
		#: set its position to 1 + the length of the list so that it will be ignored.
		#: PLEASE NOTE:
		#: 	this block of code will never be reached unless either the division
		#: 	or multiplication symbols exist, so setting one of the symbols to
		#:	1 + the length of the list is NOT an issue
		try:
			div = eqt.index('/')
		except ValueError:
			div = len(eqt) + 1

		#: Multiply the two values if a multiplication symbol is found before a
		#: Division symbol, otherwise divide.
		multiply = False  #: Default
		if mul < div:  #: If the multiply index is lower than the division index,
			multiply = True  #: Set multiply to true.

		#: Find the index of the first type of appearing symbol.
		sym_position = min([mul, div])

		first_pos = sym_position - 1  #: Get the operator's index
		second_pos = sym_position + 1  #: Get the operand's index

		first = float(eqt[first_pos])  #: Get the value for the operator
		second = float(eqt[second_pos])  #: Get the value for the operand

		#: If multply is true, then set eval equal to the operator times the operand.
		#: Otherwise, set eval to the operator divided by the operand.
		if multiply:
			eval = first * second
		else:
			eval = first / second

		#: Replace the 'X', '*', 'Y' or 'X', '/', 'Y'  portion of the list with the
		#: outcome of the multiplication/division expression.
		eqt[first_pos:second_pos + 1] = [eval]

	#: Evaluate all addition and subtractions expressions from left to right
	#: as this comes after division and multiplication in bedmas/pedmas.
	while '+' in eqt or '-' in eqt:
		if verbose:
			for i in range(nested_level):
				print("\t", end='')
			print_eqt(eqt)

		#: Try to find an index for the addition symbol. If it isnt found
		#: Set its position to 1 + the length of the list so that it will be ignored.
		#: PLEASE NOTE:
		#: 	this block of code will never be reached unless either the subtraction
		#: 	or addtion symbols exist, so setting one of the symbols to
		#:	1 + the length of the list is NOT an issue
		try:
			add = eqt.index('+')
		except ValueError:
			add = len(eqt) + 1

		#: Try to find an index for the subtraction symbol. If it isnt found
		#: Set its position to 1 + the length of the list so that it will be ignored.
		#: PLEASE NOTE:
		#: 	this block of code will never be reached unless either the subtraction
		#: 	or addtion symbols exist, so setting one of the symbols to
		#:	1 + the length of the list is NOT an issue
		try:
			sub = eqt.index('-')
		except ValueError:
			sub = len(eqt) + 1

		#: add the two values if an addition symbol is found before a
		#: subtraction symbol, otherwise subtract.
		add = False
		if add < sub:
			add = True

		#: Find the index of the first type of appearing symbol.
		sym_position = min([add, sub])
		first_pos = sym_position - 1  #: The index of the operatior.
		second_pos = sym_position + 1  #: The index of the operand.

		first = float(eqt[first_pos])  #: Get the value of the operator
		second = float(eqt[second_pos])  #: Get the value of the operand.

		#: If addition is true, then set eval equal to the operator plus the operand.
		#: Otherwise, set eval to the operator subtract by the operand.
		if add:
			eval = first + second
		else:
			eval = first - second
		#: Replace the 'X', '+', 'Y' or 'X', '-', 'Y'  portion of the list with the
		#: outcome of the addition/subtraction expression.
		eqt[first_pos:second_pos + 1] = [eval]

	if verbose:
		for i in range(nested_level):
			print('\t', end='')
		print(eqt[0])
	return eqt[0]  #: Return the outcome of the equation.

def equationify(eqt: str):
	""" Takes in a string (preferably without garbage characters, though it
	    does handle those) and converts it into a list of operators, operands and
	    operations.

	    PLEASE NOTE:
			All comments marked with (GR) are used to remove garbage from the
			equation string.

	Args:
		eqt(str): The equation string to convert.
	Returns:
		A list with the operators operands, and operations
		of the passed strings.
	"""

	proper = ''  #: Initialize the "proper" string.
	symbol = True  #: Used to determine whether the last encountered item was a symbol (GR)
	eqt = "".join(eqt.split())  #: Removes all whitespace from the string (GR)
	brackets = ['(', ')', '[', ']', '{', '}']  #: A list of the types of brackes that may be used.
	operations = ['+', '-', '*', 'x', 'X', '/', '^']  #: A list of valid operators.

	#: Append each bracket type to the operators list.
	for type in brackets:
		operations.append(type)

	#: Sanatize the string so that it only contains valid operands and operators.
	#: This will remove any doubled up operators (excluding a symbol followed by a -
	#: for negative numbers, and a symbol following a brackets or a bracket following
	#: a symbol.
	#: Example sanitized string:
	#:		"1asjdfie+dlfdk2*kkkkkkkkkkkk3"
	#:		becomes: "1+2*3"
	#: 		---- OR ----
	#:		"1 ++* 2 /@R #3"
	#:		becomes: "1+2/3"
	#:
	for index, character in enumerate(eqt):

		if character.isdigit() or character == '.':  #: If this character is a digit or a decimal point for a number.
			if symbol:  #: then, if the previous character was a symbol
				symbol = False #: then set symbol to false.
			proper += character  #: And finally append the character to proper.

		elif character in operations:  #: Otherwise, if the character is an operation (GR)
			if not symbol:  #: If the previous character wasn't a symbol

				#: Then if the character is not a closing bracket, set
				#: symbol to true, and...
				if character != ')' and character != ']' and character != '}':
					symbol = True

				#: If the character is an x or X, append a multiplication symbol.
				if 'x' == character.lower():
					proper += "*"

				#: Otherwise, append the operation's character to the proper string.
				else:
					proper += character

			#: If the last character WAS a symbol
			#: Then check the special cases, and append
			#: characters if this is a special case.

			elif character == '-':  #: Special case: Number is negative
				proper += ':' #: ':' is being used to signify a negative value.

			elif character in brackets:  #: Special case: This is a bracket
				proper += character  #: Append the characer.

	eqt = []  #: Initialize a list to hold the equation.
	builder = ""  #: Initialize a string to build numbers with.

	#: For each chatacter in the string that has been sanitized,
	#: Add each character to the builder string until an operator
	#: is reached, then append the builder string (which will be a number)
	#: then append the symbol.
	for character in proper:
		if  character in operations:  #: If the character is in operations,
			if builder != "":  #: If the builder string is not empty
				eqt.append(builder)  #: Append the string
			eqt.append(character)  #: Then append the operator.
			builder = ""  #: And finally reset the builder string for a new number.

		#: If the character is a colon, then this is leftovers from sanitation, and
		#: the colon means that this number is negative.
		elif character == ':':
			builder += '-'

		#: After all special cases are accounted for, append the character to the builder
		#: string as the character is guarenteed to be a number.
		else:
			builder += character

	#: Catch the last number.
	if builder != "":  #: If the builder string is not empty
		eqt.append(builder)  #: Append that string to the equation list.

	return eqt #: Return the equation list.

def print_eqt(eqt: list):
	""" Used to print out the equation lists without
	    the square brackets, commas, or quotes that come
	    with printing a list.
	    For example, printing the list ['5', '5'] you would get:
		"['5', '5']"
	    When using this function, you would get:
	    "5 5"

	Args:
		eqt(list): The equation to be printed

	"""

	#: Print each item of the list seperately followed by a space.
	for item in eqt:
		print(item, end=' ')

	print()  #: Print a newline after for readablity.


if __name__ == "__main__":  #: Allow this code to be used outside of just the command line.

	#: Create an arugment parser to be used when this is called from the command line.
	parser = argparse.ArgumentParser(description="Command line equation solver")

	#: Create the equation argument.
	parser.add_argument("Equation", type=str, help="The equation that should be solved. Type = str")

	#: Create the verbose argument.
	parser.add_argument('-v', "--verbose", action="store_true",
			    help="Output each step of the equation solver.")

	#: Parse the arguments.
	args = parser.parse_args()

	#: Print the result of the passed equation. If the verbose argument was given,
	#: output each step of the computing process.
	if args.verbose:
		SolveEqt(args.Equation, args.verbose)
	else:
		print(SolveEqt(args.Equation))
