from itertools import count

from ._classBase_.parse import *


class NU1L_L_Parse(parse):
	# 分隔符
	token = [';', ':', ',', '*']

	def __init__(self):
		super().__init__()

	def parse_token(self, data) -> list:
		buffer = ""
		return_buffer = []
		for i in range(0, len(data)):
			char = data[i]
			if char in self.token:
				return_buffer.append(buffer)
				return_buffer.append(char)
				buffer = ""
			else:
				buffer += char
		if buffer:
			return_buffer.append(buffer)
		return return_buffer

	def build_object(self, token_list: list) -> dict:
		return_object = {}
		current_process = return_object
		build_stack = []
		context = ""
		for token in token_list:
			if token == ';':
				if context:
					current_process[context] = context
				if len(build_stack) > 0:
					current_process = build_stack.pop()
				else:
					raise Exception('stack overflow')
				context = ""
				continue
			if token == ':':
				current_process_tmp = {}
				build_stack.append(current_process)
				current_process[context] = current_process_tmp
				current_process = current_process_tmp
				context = ""
				continue
			if token == ',':
				current_process[context] = context
				context = ""
				continue
			if token == '*':
				current_process[context] = context
				context = ""
				continue
			context = token
		if context:
			current_process[context] = context
		return return_object

	def parse(self, data) -> dict:
		token_list = self.parse_token(data)
		return_object = self.build_object(token_list)
		return return_object


if __name__ == '__main__':
	parse = NU1L_L_Parse()
	print(parse.parse('a:dddd;b:dddd,ff:ff,f,ffr'))
