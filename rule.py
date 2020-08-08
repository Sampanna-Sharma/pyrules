class ruleError(Exception):
    pass

class rule:
    """
    Class for representing rule.
    """
    def __init__(self,lhs,rhs,support,confidence):
        """
        Args:
            lhs (list): left hand side of rule
            rhs (list): right hand side of rule
            support (float): support value of rule
            confidence (float): confidence of rule
        """
        self.lhs = set(lhs)
        self.rhs = set(rhs)
        self.support = support
        self.confidence = confidence
    
    def __repr__(self):
        return f"rule({self.lhs},{self.rhs},{self.support},{self.confidence})"
    
    def __str__(self):
        return f"{self.lhs} ==> {self.rhs}"
    
    def isMatched(self,li):
        """Checks if provided list triggers the rule

        Args:
            li (list): list of items

        Returns:
            bool: wheter the list triggers the rule or not
        """
        if self.lhs.issubset(set(li)):
            return True
        else:
            return False
    
    def matchedRule(self,li):
        """Returns the rule if provided list triggers the rule

        Args:
            li (list): list of items

        Raises:
            ruleError: the list doesn't trigger the rule

        Returns:
            rule : self rule object
        """
        if self.isMatched(li):
            return self
        else:
            raise ruleError("Rule cannot be matched since lhs doesn't match")
        
    
    def apply(self,li):
        """Returns rhs of the rule if provided list triggers the rule

        Args:
            li (list): list of items

        Raises:
            ruleError: the list doesn't trigger the rule

        Returns:
            list: rhs of the rule
        """
        if self.isMatched(li):
            return self.rhs
        else:
            raise ruleError("Rule cannot be applied since lhs doesn't match")
        