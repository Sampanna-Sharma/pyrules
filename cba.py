from rule import rule
import numpy as np

class CBA():
    def __init__(self,itemsets,min_confidence,min_lhs = 1,restrict_rhs = None):
        self.itemsets = itemsets
        self.min_confidence = min_confidence
        self.min_lhs = min_lhs
        self.freq_dict ={itemset.item : itemset.support for itemset in self.itemsets}
        self.restrict_rhs = restrict_rhs
    
    def run(self):
        result = []
        _itemsets = filter(lambda x: len(x) > self.min_lhs, self.itemsets)
        if self.restrict_rhs:
            _itemsets = filter(lambda x: x.contains(self.restrict_rhs), _itemsets)
        for item in _itemsets:
            for lhs,rhs in item.combination():
                if self.restrict_rhs:
                    if any(np.isin(rhs,self.restrict_rhs)) == False:
                           continue
                support = self.freq_dict[lhs]
                confidence = self.freq_dict[tuple(sorted(lhs+rhs))]/ support
                if confidence > self.min_confidence:
                    result.append(rule(lhs,rhs,support,confidence))

        return result