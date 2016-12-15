import random
import argparse
import os.path
import pygame
from pygame.locals import *

events = []

class Module(object):
	def __init__(self, name, modid):
		self.functions = []
		self.name = name
		self.modid = modid
	
	def add_function(self, name, action):
		fn = Function(name, action)
		self.functions.append(fn)
		return len(self.functions)-1
	
	def __str__(self):
		return self.name

class Function(object):
	def __init__(self, name, action):
			self.name = name
			self.action = action
	def __str__(self):
		return self.name


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
		tape = []
		instruction = 0
		cjumps = dict((x,y) for y,x in self.braces.items())
		
		for _ in range(5):
			tape.append(0)

		while instruction < len(self.code):
			c = self.code[instruction]
			#print(pointer, tape[pointer], instruction, tape)
			if c == '>':
				pointer += 1
				if pointer >= len(tape):
					tape.append(0)
			elif c == '<':
				if pointer > 0:
					pointer -= 1
			elif c == '+':
				if tape[pointer]+1<=2**64:
					tape[pointer]+=1
				else:
					tape[pointer]=0
			elif c == '-':
				if tape[pointer]-1 >= 0:
					tape[pointer]-=1
				else:
					tape[pointer]=2**64
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
					print(tape[:5])
					raise Exception("No such module")
			elif c == ',':
				if len(events) != 0:
					tape[pointer] = events.pop()
				else:
					tape[pointer] = 0
			elif c == '~':
				print(pointer, tape[pointer], tape)
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
		super().__init__("IO", modid)
		self.add_function("print", self.fn_print)
	
	def fn_print(self, pointer, tape, args):
		print("".join([chr(x) for x in args]))
		return 0

class ModuleRandom(Module):
	def __init__(self, modid):
		super().__init__("Random", modid)
		self.add_function("randbool", self.fn_bool)
		self.add_function("randrange", self.fn_range)
		self.add_function("randchoice", self.fn_choice)
	
	def fn_bool(self, pointer, tape, args):
		return random.getrandbits(1)
	
	def fn_range(self, pointer, tape, args):
		return random.range(args[0], args[1])
	
	def fn_choice(self, pointer, tape, args):
		return random.choice(args)

	def fn_setseed(self, pointer, tape, args):
		random.seed(args[0])

class ModuleGame(Module): # Oh god no ;_;
	def __init__(self, modid):
		super().__init__("Game", modid)
		self.vars = []
		if not pygame.font: print('Warning: fonts disabled')
		if not pygame.mixer: print('Warning: sound disabled')
		self.add_function("init", self.fn_init)
		self.add_function("newdisplay", self.fn_newdisplay)
		self.add_function("setcaption", self.fn_setcaption)
		self.add_function("update", self.fn_update)

		
	def fn_init(self, pointer, tape, args):
		pygame.init()
		print("pygame initialized!")
		return 0
	
	def fn_newdisplay(self, pointer, tape, args):
		self.vars.append(pygame.display.set_mode(args[0:2]))
		ptr = len(self.vars)-1
		print("display created!")
		return ptr
	
	def fn_setcaption(self, pointer, tape, args):
		title = "".join([chr(x) for x in tape[args[0]:args[1]+1]])
		pygame.display.set_caption(title)
		return 0
	
	def fn_update(self, pointer, tape, args):
		for event in pygame.event.get():
			print("EVENT: %d" % event.type)
			events.append(event.type)
		pygame.display.flip()
	

argparser = argparse.ArgumentParser(description="A brainfuck game framework. Yes, seriously.")
argparser.add_argument("file", help="The file to run")
args = argparser.parse_args()

if os.path.isfile(args.file):
	with open(args.file) as f:
		interpreter = Interpreter(f.read())
		interpreter.add_module(ModuleIO)
		interpreter.add_module(ModuleRandom)
		interpreter.add_module(ModuleGame)
		interpreter.run()
else:
	print("bfgame: %s: no such file" % args.file)

