from sys import argv

def SolveEqt(eqt:str):
	eqt = equationify(eqt)
	print(eqt)


def find_operation(eqt: str):
	for character in eqt:
		if not character.isdigit() or character == ',':
			return character
	return None

def equationify(eqt: str):
	proper = ""
	symbol = False
	eqt = "".join(eqt.split())
	operations = ['+', '-', '*', 'x', 'X', '/', '^', '(', ')']
	for index, character in enumerate(eqt):
		if character.isdigit() or character in operations:
			proper += character.lower()
	return proper

if argv[1] != "n":
	SolveEqt(argv[1])
else:
	pass
