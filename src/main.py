import random


class Module(object):
	functions=[]
	def __init__(self, name, modid):
		self.name = name
		self.modid = modid
	
	def add_function(self, name, action):
		fn = Function(name, action)
		self.functions.append(fn)
		return len(self.functions)-1


class Function(object):
	def __init__(self, name, action):
			self.name = name
			self.action = action


class Interpreter(object):
	def __init__(self, code):
		self.code = self.minify(code)
		self.tape = []
		self.modules = []
		
		self.braces = self.matchbraces(self.code)
	
	def find(self, s, ch):
		return [i for i, ltr in enumerate(s) if ltr==ch]

	def matchbraces(self, code):
		if "[" in code or "]" in code:
			matches = {}

			cbrackets = self.find(code, ']')[::-1]
			obrackets = self.find(code, '[')

			if len(cbrackets) == len(obrackets):
				stack = []

				for char in code:
					if char == '[' or char == ']':
						if char == ']':
							raise Exception("Unbalanced braces")
							break
						else:
							break

				for i,c in enumerate(code):
					if c == '[':
						stack.append(i)
					elif c == ']':
						matches[stack.pop()] = i
				return matches
			else:
				raise Exception("Unbalanced braces")
		else:
			return {}

	def minify(self, code):
		out = ""
		for c in code:
			if c in '.,+-><[]':
				out += c
		return out
	
	def add_module(self, module):
		mod = module(len(self.modules)+1)
		self.modules.append(mod)
		return len(self.modules)
	
	def run(self):
		pointer = 0
		tape = [0]
		instruction = 0

		cjumps = dict((x,y) for y,x in self.braces.items())

		while instruction < len(self.code):
			c = self.code[instruction]
			if c == '>':
				pointer += 1
				if pointer >= len(tape):
					tape.append(0)
			elif c == '<':
				if pointer > 0:
					pointer -= 1
			elif c == '+':
				tape[pointer]+=1
			elif c == '-':
				tape[pointer]-=1 #TODO: Should it allow values < 0?
			elif c == '.':
				if tape[0] <= len(self.modules) and tape[0] > 0:
					m = self.modules[tape[0]-1]
					if tape[1] <= len(m.functions) and tape[1] > 0:
						fn = m.functions[tape[1]-1]
						args = tape[tape[2]:tape[3]+1]
						r=fn.action(pointer, tape, args)
						if r:
							tape[4] = r
						else:
							tape[4] = 0
				else:
					raise Exception("No such module")
			elif c == ',':
				#TODO: EVENTS
				tape[pointer] = 0
			if c not in '[]':
				instruction += 1
			else:
				if c == '[':
					if tape[pointer] == 0:
						instruction = self.braces[instruction]+1
					else:
						instruction += 1
				else:
					if tape[pointer] != 0:
						instruction = cjumps[instruction]
					else:
						instruction += 1

	
# MODULES!
class ModuleIO(Module):
	def __init__(self, modid):
		self.add_function("print", self.fn_print)
	
	def fn_print(self, pointer, tape, args):
		print("".join([chr(x) for x in args]))
		return 0

interpreter = Interpreter("""
+     Load the IO module
>     Move forward to cell #1
+     Add 1 to its value so it's now 1
>     Move to cell #2
+++++ Add 5 to its value so it points to cell #5 which is where our string will start
>     Move to cell #3
+++++ Add 5 to its value which is where our string will end
>>>   Move to cell #6 our loop counter
++++++ Set the loop counter to 6
[
    <++++++++++ Go back to cell #5 and add 10
    >-          Go back to cell #6 and subtract 1
													
]
<+++++ Go back to cell #5 and add 5 so it's 65
<<<<. Go back to cell #1 and print it to run the function
""")
interpreter.add_module(ModuleIO)
interpreter.run()
