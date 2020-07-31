import numpy as np
from collections import defaultdict
from functools import reduce
from itertools import combinations,chain

class ItemSet:
    def __init__(self,comb,vtid):
        self.itemSet = self.to_itemSet(comb,vtid)
    
    def __str__(self):
        return str(self.itemSet)
    
    def to_itemSet(self,comb,vtid):
        itemSet = defaultdict(int)
        for item in comb:
            itemSet[item] = sum(vtid[item])
        return itemSet

class Vtid:
    def __init__(self,tidList):
        self.vocab = np.unique(sum(tidList,[]))
        self.vtid = self.to_vtid(tidList)
    
    def to_vtid(self,tidList):
        vtid = np.array(list(map((lambda x: np.isin(self.vocab,x).astype(int)),tidList))).T
        return vtid
    
    def __getitem__(self, key):
        index = np.isin(self.vocab,key)
        return list(reduce(np.multiply,self.vtid[index,:]))

    def __str__(self):
        return str(self.vtid)

class Apriori:
    def __init__(self,tidList,minsup):
        self.minsup = minsup
        self.vtid = Vtid(tidList)
    
    def run(self):
        arr = self.vtid.vocab
        comb1 = chain(*[combinations(arr,i + 1)for i, a in enumerate(arr)])
        itemset = ItemSet(comb1,self.vtid)
        return itemset

if __name__ == "__main__":
    tidList = [
            ['beer', 'rice', 'apple', 'chicken'],
            ['beer', 'rice', 'apple'],
            ['beer', 'apple'],
            ['mango', 'apple'],
            ['beer', 'rice', 'milk', 'chicken'],
            ['beer', 'rice', 'milk'],
            ['beer', 'milk'],
            ['mango', 'milk']
        ]
    ap = Apriori(tidList,0.1)
    results = ap.run()
    print(results)