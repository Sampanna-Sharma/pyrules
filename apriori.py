import numpy as np
from itertools import combinations,chain
from sklearn.feature_extraction.text import CountVectorizer
from dataclasses import dataclass, field
from collections import defaultdict, deque
from typing import List, Tuple
from scipy.sparse import triu

@dataclass
class ItemSet:
    """
    Class to represent itemset and its methods
    """    
    item : Tuple
    support : float
    
    def __len__(self):
        return len(self.item)
    
    def __eq__(self,other):
        return (sorted(self.item) == sorted(other.item)) and (self.support == other.support)
    
    def combination(self):
        """
        Returns combinations of items in the itemset to form the rule.
        for eg,
        ItemSet(("a","b","c"),1).combination() yields:
        (("a","b"),("c'))
        (("a","c"),("b'))
        (("b","c"),("a'))
        (("a"),("b","c'))
        (("b"),("a","c'))
        (("c"),("a","b'))

        Yields:
            tuple: tuple containing the combinations
        """        
        for comb in chain((combinations(self.item,r) for r in range(1,len(self.item)))):
            for lhs in comb:
                rhs = tuple(x for x in self.item if x not in lhs)
                yield lhs,rhs
    
    def contains(self,li):
        """
        Checks if any of the items in list is contained in the itemset or not.

        Args:
            li (List): Provided list to check against

        Returns:
            bool: True if itemsets contains any of the list items else False
        """        
        for i in li:
            if i in self.item:
                return True
        return False

class Vtid:
    """
    Class to represent vertical transaction list. It converts basket transaction list
    into vertical transsactions. 
    """    
    def __init__(self,tidList,minsupp=1):
        self.vectorizer = CountVectorizer(lowercase=False,tokenizer = lambda x: x,min_df=minsupp)
        self.vtid = self.vectorizer.fit_transform(tidList).tocsc()
        self.vocab = self.vectorizer.get_feature_names()
    
       
    def __getitem__(self, key):
        #index = np.isin(self.vocab,key)
        #return np.multiply.reduce(self.vtid[index,:])
        #index = np.where(self.vocab == key)[0].item()
        index = self.vocab.index(key)
        return self.vtid[:,index]

    def __str__(self):
        return str(self.vtid)

@dataclass
class Graph:
    vocab : List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.vocab = np.array(self.vocab)
        n = len(self.vocab)
        self.tree = triu(np.ones((n,n)).astype(np.bool), k = 1, format='lil')
        
    def __getitem__(self,key):
        index = np.where(self.vocab == key)[0].item()
        vocab_index = np.squeeze(self.tree[index].toarray())
        return self.vocab[vocab_index]
    
    def __setitem__(self,key,value):
        key1, key2 = key
        index1 = np.where(self.vocab == key1)[0].item()
        index2 = np.where(self.vocab == key2)[0].item()
        self.tree[index1,index2] = value

class Apriori:
    def __init__(self,tidList,minsup,restrict_items = None):
        self.minsup = minsup
        self.vtid = Vtid(tidList,minsup)
        self.vocab = self.vtid.vocab
        self.restrict_items = restrict_items
        if self.restrict_items:
            self.restrict_items.sort()
    
    def _concat(self,tuple_,list_,D):
        return ((tuple_[0] + (x,),tuple_[1].multiply(D[x])) for x in list_)
    
    def run(self):
        if self.restrict_items:
            v = sorted(self.vocab,key = lambda x:(0 if x in self.restrict_items else 1,x))
            queue = deque(((x,),self.vtid[x]) for x in self.restrict_items)
        else:
            v = self.vocab
            queue = deque(((x,),self.vtid[x]) for x in v)
            
        S = Graph(v)
        soln= []
        while queue:
            popped = queue.popleft()
            supp = popped[1].sum()
            if supp >= self.minsup:
                queue.extend(self._concat(popped,S[popped[0][-1]],self.vtid))
                #queue.extend(((popped[0] + (x,),popped[1].multiply(vtid[x])) for x in S[popped[0][-1]]))
                soln.append(ItemSet(popped[0],supp))
            else:
                S[popped[0][-2],popped[0][-1]] = False
        return soln

if __name__ == "__main__":
    import csv
    filename="retail_dataset.csv"
    tidList=[]
    with open(filename,'r') as data:
        next(data)
        for line in csv.reader(data):
            tidList.append(list(filter(None,line)))
    ap = Apriori(tidList,63)
    results = ap.run()
    print(results)