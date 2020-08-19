import unittest
import csv
from apriori import Apriori,ItemSet

class TestApriori(unittest.TestCase):
    def setUp(self):
        filename="./test/data_tests/retail.csv"
        self.tidList=[]
        with open(filename,'r') as data:
            for line in csv.reader(data):
                self.tidList.append(line)

        filename="./test/data_tests/itemSet.csv"
        self.targetSet=[]
        with open(filename,'r') as data:
            next(data)
            for line in csv.reader(data):
                itemset = ItemSet(item= tuple(line[0][1:-1].split(',')),
                                                support= int(line[2]))
                self.targetSet.append(itemset)
    
    def test_run(self):
        ap = Apriori(self.tidList,63)
        result = ap.run()
        sort_f = lambda x: (x.support,x.item)
        result.sort(key = sort_f)
        self.targetSet.sort(key = sort_f)
        self.assertListEqual(result, self.targetSet)

        restrict_items = ["Bagel","Cheese","Milk"]
        ap_restrict = Apriori(self.tidList,63,
                                restrict_items=restrict_items)
        result_restrict = ap_restrict.run()
        result_restrict.sort(key = sort_f)
        target_restrict = list(filter(lambda x: x.contains(restrict_items),self.targetSet))
        self.assertListEqual(result_restrict, target_restrict)

if __name__ == "__main__":
    unittest.main()