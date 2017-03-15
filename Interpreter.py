from Stack import Stack
import re

'''Replace nilads with single character commands'''
def atomize(snippet):
	for nilad,atom in zip(["()","{}","<>","[]"],"ABCD"):
		snippet = snippet.replace(nilad,atom)
	return snippet

'''Interpreter object'''
class Interpreter(object):
	def __init__(self,source):
		self.pointer = [0]
		self.stacks = (Stack(),Stack())
		self.scope = []
		self.source = [atomize(source)]
		self.functions = [atomize(source)]
	def insert(self,array):
		self.stacks[0].extend(array)
	def perform(self,action):
		if   action == "{":
			#We will parse until the end of the current brace
			stack = ["{"]
			matches = ["{}","()","[]","<>"]
			start = self.pointer[-1]+1
			while stack:
				self.pointer[-1] += 1
				if stack[-1]+self.source[-1][self.pointer[-1]] in matches:
					stack.pop()
				elif self.source[-1][self.pointer[-1]] in "".join(matches):
					stack.append(self.source[-1][self.pointer[-1]])
			self.functions.append(self.source[-1][start:self.pointer[-1]])
			self.pointer[-1]+=1
		elif action in "([<":
			self.scope.append([action,self.pointer[-1],0])
			self.pointer[-1] += 1
		elif action == ")":
			value = self.scope.pop()[-1]
			self.stacks[0].append(value)
			if self.scope:
				self.scope[-1][-1]+=value
			self.pointer[-1] += 1
		elif action == "]":
			value = self.scope.pop()[-1]
			if self.scope:
				self.scope[-1][-1]-=value
			self.pointer[-1] += 1
		elif action == ">":
			value = self.scope.pop()[-1]
			self.pointer[-1] += 1
			self.source.append(self.functions[value])
			self.pointer.append(0)
		elif action == "A":
			if self.scope:
				self.scope[-1][-1]+=1
			self.pointer[-1] += 1
		elif action == "B":
			if self.scope:
				self.scope[-1][-1]+=self.stacks[0].pop()
			self.pointer[-1] += 1
		elif action == "C":
			self.stacks = self.stacks[::-1]
			self.pointer[-1] += 1
		elif action == "D":
			if self.scope:
				self.scope[-1][-1]+=len(self.stacks[0])
			self.pointer[-1] += 1
		#Remove spent fucntions
		while self.source and self.pointer[-1] >= len(self.source[-1]):
			self.source.pop()
			self.pointer.pop()
	
	def run(self):
		while self.source:
			self.perform(self.source[-1][self.pointer[-1]])

