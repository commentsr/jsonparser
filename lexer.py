import re

from tokens import *

class LexError(Exception):
    pass

def lex(string):
	index = 0
	tokens = []
	while index < len(string):
		for pattern, tag, ignore in [(*x, *[False]*(3-len(x))) for x in TOKENS]:
			match = re.compile(pattern).match(string, index)
			if match:
				if not ignore:
					tokens.append((match.group(), tag))
				index += match.span()[1] - match.span()[0]
				break
		else:
			raise LexError(f"Invalid character '{string[index]}'")

	return tokens