from parsec import *


spaces = regex(r'\s*', re.MULTILINE)
lexeme = lambda p: p << spaces
lbrace = lexeme(string('{'))
rbrace = lexeme(string('}'))
lbrack = lexeme(string('['))
rbrack = lexeme(string(']'))
lparen = lexeme(string('('))
rparen = lexeme(string(')'))
at = lexeme(string('@'))

@generate
def parse_temporalinst():
	value = yield spaces >> regex(r'[^@]+') << spaces
	yield string('@')
	time = yield spaces >> regex(r'[^,}\]\)]+')
	return [value, time]

@generate
def parse_temporali():
	yield spaces >> lbrace << spaces
	instants = yield sepEndBy1(parse_temporalinst, string(','))
	yield spaces >> rbrace << spaces
	return instants

@generate
def parse_temporalseq():
	ip = yield spaces >> (string('Interp=Stepwise;') | string('')) << spaces
	if ip == '':
		interp = None
	else:
		interp = 'Stepwise'
	lb = yield spaces >> (lbrack | lparen) << spaces
	lower = True if lb == '[' else False
	instants = yield sepEndBy1(parse_temporalinst, string(','))
	ub = yield spaces >> (rbrack | rparen) << spaces
	upper = True if ub == ']' else False
	return (instants, lower, upper, interp)

@generate
def parse_temporals():
	ip = yield spaces >> string('Interp=Stepwise;') | string('') << spaces
	if ip == '':
		interp = None
	else:
		interp = 'Stepwise'
	yield spaces >> lbrace << spaces
	sequences = yield sepEndBy1(parse_temporalseq, string(','))
	yield spaces >> rbrace << spaces
	return (sequences, interp)

