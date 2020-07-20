import unittest
from rule import rule, ruleError

class TestRule(unittest.TestCase):
    def setUp(self):
        self.r1 = rule(['a'],['b'],0.2,0.8)
        self.r2 = rule(['a','b'],['c'],0.2,0.8)
        self.r3 = rule(['a'],['b','c'],0.2,0.8)
       
    def test_isMatched(self):
        self.assertEqual(self.r1.isMatched(['a']),True)
        self.assertEqual(self.r1.isMatched(['b']),False)
        self.assertEqual(self.r1.isMatched(['d','c']), False)

        self.assertEqual(self.r2.isMatched(['a','b']),True)
        self.assertEqual(self.r2.isMatched(['b','a']),True)
        self.assertEqual(self.r2.isMatched(['b']),False)
        self.assertEqual(self.r2.isMatched(['a','b','c']),False)
    
    
    def test_matchedRule(self):
        self.assertEqual(self.r1.matchedRule(['a']),self.r1)
        self.assertRaises(ruleError, self.r1.matchedRule,['d','c'])
        
        self.assertEqual(self.r2.matchedRule(['a','b']),self.r2)
        self.assertRaises(ruleError, self.r1.matchedRule,['b'])
        self.assertEqual(self.r2.matchedRule(['b','a']),self.r2)
    

    def test_apply(self):
        self.assertEqual(self.r1.apply(['a']),['b'])
        self.assertRaises(ruleError, self.r1.apply,['b'])
        self.assertRaises(ruleError, self.r1.apply,['d','c'])

        self.assertEqual(self.r2.apply(['a','b']),['c'])
        self.assertEqual(self.r2.apply(['b','a']),['c'])
        self.assertRaises(ruleError, self.r1.apply,['b'])
        self.assertRaises(ruleError, self.r1.apply,['b','c'])

        self.assertEqual(self.r3.apply(['a']),['b','c'])
        self.assertRaises(ruleError, self.r3.apply,['a','b'])
    

if __name__ == "__main__":
    unittest.main()
