import unittest
import os
import sys
import data
 
parpath = os.path.join(os.path.dirname(sys.argv[0]), os.pardir)
sys.path.insert(0, os.path.abspath(parpath))

from EngineRoom import ParseText, AST, breakDownStringToTokens
#from lex import LexToken

class EngineRoomTC(unittest.TestCase):
	"""Tests for EngineRoom"""

	# def check(node, rule):
	# 	for r in rule:
	# 		if r in self.nodes:
	# 			if r in self.grammar:
	# 				#then it should be non leaf aka NODE
	# 				#and be type of nodes[r] points to

	# 				pass

	def setUp(self):
		print "setting up mock grammar and parser"
		testName = self.shortDescription()
		self.tokenListOne = breakDownStringToTokens("5 + 5 and 5 + 5", module = data)
		self.tokenListTwo = breakDownStringToTokens("5 + 5", module = data )
		start_node =  data.BaseExprNode()
		self.parser =  ParseText(data.grammar, "baseexpr")

		if testName == "parse test":
			
			self.tokenListThree = breakDownStringToTokens("5 + 5 someword", module = data)
			self.tokenListFour = breakDownStringToTokens("word 5 + 5", module = data)
			#FIX THIS! Or Should i?!
			#self.tokenListFive = breakDownStringToTokens(" ", module = data)
		elif testName == "execute code":	
			self.ast =  AST(self.tokenListOne, start_node,data.grammar, data.nodes)
			self.parser.parse(self.tokenListOne)
			trace = self.parser.where_was_i
			self.ast.create_tree("baseexpr",trace)
			# print self.ast.tree_nodes[0].dooperation() 
		elif testName == "build AST test":
			self.ast =  AST(self.tokenListTwo, start_node,data.grammar, data.nodes)
			self.parser.parse(self.tokenListTwo)
			trace = self.parser.where_was_i
			self.ast.create_tree("baseexpr",trace)

	def tearDown(self):
		print "i m done"

	def test_parse_function(self):
		"parse test"
		#parse func is expecting list of tokens, not strings
		self.assertTrue(self.parser.parse(self.tokenListOne))
		self.assertTrue(self.parser.parse(self.tokenListTwo))
		self.assertFalse(self.parser.parse(self.tokenListThree))
		self.assertFalse(self.parser.parse(self.tokenListFour))
		#self.assertFalse(self.parser.parse(self.tokenListFive))

	# TODO find out if generic check function is more suitable
	# then handwritten one
	def test_build_ast(self):
		"build AST test"
		self.assertIsInstance(self.ast.tree_nodes[0], data.BaseExprNode)
		
		parent_node =  self.ast.tree_nodes[0]
		self.assertIsInstance(parent_node.childrens[0], data.AndMathOpNode)
		
		child_node = parent_node.childrens[0]
		self.assertIsInstance(child_node.childrens[0], data.MathOpNode)

		gchild = child_node.childrens[0]
		self.assertIsInstance(gchild.childrens[0], data.NumberNode)
		self.assertIsInstance(gchild.childrens[1], data.OperatorNode)
		self.assertIsInstance(gchild.childrens[2], data.MathOpNode)
		
		ggchild_1 =  gchild.childrens[1]
		self.assertIsInstance(ggchild_1.childrens[0], data.PlusNode)

		ggchild_2 =  gchild.childrens[2]
		self.assertIsInstance(ggchild_2.childrens[0], data.NumberNode)

	
	# def test_execute_code(self):
	# 	"execute code"
	# 	self.assertEqual(self.ast.tree_nodes[0].dooperation(), 20)

if __name__ == '__main__':
	unittest.main()