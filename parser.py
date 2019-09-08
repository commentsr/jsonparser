from tokens import *


class ParseError(Exception):
    pass


class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.index = 0

	def parse(self):
		return self.try_parse_value()


	# type parsers

	def parse_number(self):
		value = self.consume(VALUE)
		return float(value) if "." in value else int(value)

	def parse_string(self):
		return self.consume(VALUE)[1:-1]

	def parse_keyword(self):
		return {"true": True, "false": False, "null": None}[self.consume(VALUE)]

	def parse_object(self):
		self.expect(TOKEN, OPEN_BRACE)
		pairs = {}
		while True:
			if self.get(TOKEN) != STRING:
				raise ParseError(f"Object key: Expected token '{STRING}' but instead found '{self.get(TOKEN)}'")
			name = self.parse_string()
			self.expect(TOKEN, ASSIGNMENT)
			value = self.try_parse_value()
			pairs.update({name: value}) 

			if self.get(TOKEN) == CLOSE_BRACE:
				break
			else:
				self.expect(TOKEN, DELIMITER)

		self.expect(TOKEN, CLOSE_BRACE)
		return pairs

	def parse_list(self):
		self.expect(TOKEN, OPEN_BRACKET)
		elements = []
		while True:
			value = self.try_parse_value()
			elements.append(value)

			if self.get(TOKEN) == CLOSE_BRACKET:
				break
			else:
				self.expect(TOKEN, DELIMITER)

		self.expect(TOKEN, CLOSE_BRACKET)
		return elements


	# meta parsers

	def try_parse(self, token=None):
		token_parsers = {
			NUMBER: self.parse_number,
			STRING: self.parse_string,
			KEYWORD: self.parse_keyword,
			OPEN_BRACE: self.parse_object,
			OPEN_BRACKET: self.parse_list,
			CLOSE_BRACE: lambda: None,
			CLOSE_BRACKET: lambda: None,
			DELIMITER: lambda: None,
			ASSIGNMENT: lambda: None
		}
		if token:
			if self.get(TOKEN) != token:
				raise ParseError(f"Expected token '{token}' but instead found '{self.get(TOKEN)}'")
			return token_parsers[token]()

		else:
			return token_parsers[self.get(TOKEN)]()

	def try_parse_value(self):
		token = self.get(TOKEN)
		try:
			return {
				NUMBER: self.parse_number,
				STRING: self.parse_string,
				KEYWORD: self.parse_keyword,
				OPEN_BRACE: self.parse_object,
				OPEN_BRACKET: self.parse_list
			}[token]()
		except KeyError:
			raise ParseError(f"Expected value token but instead found '{self.get(TOKEN)}'")


	# token helpers

	def get(self, component):
		return self.tokens[self.index][component]

	def consume(self, component):
		value = self.tokens[self.index][component]
		self.index += 1
		return value

	def peek(self, component):
		return self.tokens[self.index+1][component]

	def expect(self, component, expected):
		value = self.consume(component)
		if value != expected:
			raise ParseError(f"Expected '{expected}' but instead found '{value}'")