STRING = "STRING"
NUMBER = "NUMBER"
KEYWORD = "KEYWORD"

DELIMITER = "DELIMITER"
ASSIGNMENT = "ASSIGNMENT"

OPEN_BRACE = "OPEN_BRACE"       # {
CLOSE_BRACE = "CLOSE_BRACE"     # }
OPEN_BRACKET = "OPEN_BRACKET"   # [
CLOSE_BRACKET = "CLOSE_BRACKET" # ]

WHITESPACE = "WHITESPACE"

TOKENS = [
	(r'"([^"]|\\.)*"', STRING),
	(r"-?([1-9]|0)\d*(\.\d+)?([eE][+-]?[1-9]\d*)?", NUMBER),
	(r"true|false|null", KEYWORD),
	(r",", DELIMITER),
	(r":", ASSIGNMENT),
	(r"{", OPEN_BRACE),
	(r"}", CLOSE_BRACE),
	(r"\[", OPEN_BRACKET),
	(r"\]", CLOSE_BRACKET),
	(r"[ \n\r\t]", WHITESPACE, True)
]

TOKEN = 1
VALUE = 0