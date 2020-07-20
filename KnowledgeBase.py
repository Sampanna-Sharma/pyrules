from rule import rule

class KnowledgeBase:
    def __init__(self, rules):
        self.rules = rules
        self.total = len(self.rules)
    
    def apply(self,lhs):
        for rule in self.rules:
            if rule.isMatched(lhs):
                yield rule.apply(lhs)
            else:
                continue

    def matchedRules(self,lhs):
        for rule in self.rules:
            if rule.isMatched(lhs):
                yield rule.matchedRule(lhs)
            else:
                continue

                