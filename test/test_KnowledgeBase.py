import unittest
from KnowledgeBase import KnowledgeBase
from rule import rule

class TestKnowledgeBase(unittest.TestCase):
    def setUp(self):
        self.ab = rule(['a'],['b'],0.2,0.8)
        self.ac = rule(['a'],['c'],0.2,0.8)
        self.bc = rule(['b'],['c'],0.2,0.8)
        self.kb = KnowledgeBase([self.ab,self.ac,self.bc])
    
    def test_apply(self):
        self.assertEqual(list(self.kb.apply(['a'])),[['b'],['c']])
        self.assertEqual(list(self.kb.apply(['b'])),[['c']])
        self.assertEqual(list(self.kb.apply(['c'])),[])
    
    def test_matchedRules(self):
        self.assertEqual(list(self.kb.matchedRules(['a'])),[self.ab,self.ac])
        self.assertEqual(list(self.kb.matchedRules(['b'])),[self.bc])
        self.assertEqual(list(self.kb.matchedRules(['c'])),[])


if __name__ == "__main__":
    unittest.main()
