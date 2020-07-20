class ruleError(Exception):
    pass

class rule:
    def __init__(self,lhs,rhs,support,confidence):
        self.lhs = sorted(lhs)
        self.rhs = sorted(rhs)
        self.support = support
        self.confidence = confidence
    
    def __repr__(self):
        return f"rule({self.lhs},{self.rhs},{self.support},{self.confidence})"
    
    def __str__(self):
        return f"{self.lhs} ==> {self.rhs}"
    
    def isMatched(self,lhs):
        if sorted(lhs) == self.lhs:
            return True
        else:
            return False
    
    def matchedRule(self,lhs):
        if self.isMatched(lhs):
            return self
        else:
            raise ruleError("Rule cannot be matched since lhs doesn't match")
        
    
    def apply(self,lhs):
        if self.isMatched(lhs):
            return self.rhs
        else:
            raise ruleError("Rule cannot be applied since lhs doesn't match")
        