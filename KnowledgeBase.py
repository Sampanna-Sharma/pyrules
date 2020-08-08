from rule import rule

class KnowledgeBase:
    """Class for representing knowledge through a collections of rules
    """
    def __init__(self, rules):
        """
        Args:
            rules (list): list of rules object
        """
        self.rules = rules
        self.total = len(self.rules)
    
    def apply(self,li):
        """Returns rhs of all rules triggered by the provided list

        Args:
            li (list): list of items

        Yields:
            list: rhs of matched rule
        """
        for rule in self.rules:
            if rule.isMatched(li):
                yield rule.apply(li)
            else:
                continue

    def matchedRules(self,li):
        """Return all rules triggered by the provided list

        Args:
            li (list): list of items

        Yields:
            rule: matched rule
        """
        for rule in self.rules:
            if rule.isMatched(li):
                yield rule.matchedRule(li)
            else:
                continue

                