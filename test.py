# %%
import csv
from cba import CBA
from apriori import Apriori
from efficient_apriori import apriori

# %%
filename="retail.csv"
tidList=[]
with open(filename,'r') as data:
    for line in csv.reader(data):
        tidList.append(line)

# %%
ap = Apriori(tidList,63)
itemsets = ap.run()
cb = CBA(itemsets= itemsets, min_confidence=0.8)
rules = cb.run()

# %%
itemsets2, rules2 = apriori(transactions= tidList, min_support= 0.2, min_confidence=0.8)
