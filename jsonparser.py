from parser import Parser
from lexer import lex

def parse_json(string):
	tokens = lex(string)
	parser = Parser(tokens)
	return parser.parse()