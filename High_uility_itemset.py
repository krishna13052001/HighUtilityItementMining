import sys
from collections import namedtuple
import flwr as fl
import numpy as np
from numpy import dtype
import unitprice as up
import transcationData as td
Transaction = namedtuple('Transaction',['tid','items'])
UtilListItem = namedtuple('UtilListItem',['tid','iutil','rutil'])
class FindHighUtilityItement:
    def __init__(self,transactions,unit_profit,minutil,high_uility_list,minutil_pc=True):
        self._create_transcation(transactions)
        self.unit_profit = unit_profit
        self.total_db_util = self._total_utility()
        self.minutil_pc = minutil_pc
        if minutil_pc:
            self.minutil = minutil*self.total_db_util
        else:
            self.minutil = minutil
        self.hui_list = high_uility_list
        self.util_lists = {}
        self._get_profitable_utility_set()

    def _create_transcation(self,transactions):
        self.transactions = []
        for i in transactions:
            self.transactions.append(Transaction(i[0],i[1]))
    
    def _total_utility(self):
        total = 0
        for i in self.transactions:
            for j in i.items:
                total += self.unit_profit[j[0]] * j[1]
        return total

    def _get_profitable_utility_set(self):
        self.profitable_utility_list = []
        for i in self.unit_profit.keys():
            self.profitable_utility_list.append((i,self._findItemUtility([i])))
        self.profitable_utility_list = sorted(self.profitable_utility_list,key=lambda x: x[1])
        self.order = {}
        for i,j in enumerate(self.profitable_utility_list):
            self.order[j[0]] = i

    def _findTransactionUtility(self,transcation):
        return sum(sorted([self.unit_profit[x[0]]*x[1] for x in transcation.items],reverse=True))

    def _findItemUtility(self,x):        
        t_subset = list(filter(lambda t: set(x).issubset([j[0] for j in t.items]),self.transactions))
        return sum([self._findTransactionUtility(x) for x in t_subset])


    def _utilListItem(self,t,x):
        iutil = sum([self.unit_profit[j[0]]*j[1] for j in filter(lambda i: i[0] in x,t.items)])
        rutil_list = [x[0] for x in self.profitable_utility_list]
        ix = max([rutil_list.index(j) for j in x])
        rutil_list = rutil_list[ix:]
        rutil = sum([self.unit_profit[j[0]]*j[1] for j in filter(lambda i: (i[0] not in x) and (i[0] in rutil_list),t.items)])
        return UtilListItem(t.tid,iutil,rutil)

    def _createUtilList(self,x):
        return {t.tid:self._utilListItem(t,x) for t in filter(lambda i: set(x).issubset([j[0] for j in i.items]),self.transactions)}


    def _find_high_utility_itement_constuct(self,P,list1,list2):
        combine_util_list = {}
        for i in self.util_lists[frozenset(list1)].values():
            try:
                j = self.util_lists[frozenset([list2])][i.tid]
            except:
                j = None
            if j:
                if P:
                    e = self.util_lists[frozenset(P)][i.tid]
                    exy = UtilListItem(i.tid,i.iutil+j.iutil-e.iutil,j.rutil)
                else:
                    exy = UtilListItem(i.tid,i.iutil+j.iutil,j.rutil)
                combine_util_list[exy.tid] = exy

        return combine_util_list


    def _find_high_utility_search(self,P,extensionsOfP,utility_cooccurance):
        for i in extensionsOfP:
            utility_list = self.util_lists[frozenset(i)]
            iutils_list = [i.iutil for i in utility_list.values()]
            rutils_list = [i.rutil for i in utility_list.values()]
            if(sum(iutils_list) >= self.minutil):
                if self.minutil_pc:
                    self.hui_list.append([i,sum(iutils_list)/self.total_db_util])
                else:
                    self.hui_list.append([i,sum(iutils_list)])

            if(sum(iutils_list) + sum(rutils_list) >= self.minutil):
                Py_list = [x[-1] for x in extensionsOfP]
                Py_list = sorted(Py_list,key=lambda x: self.order[x])
                Py_list.remove(i[-1])
                extensionsOfPx = []
                for Py in Py_list[self.order[i[-1]]:]:
                    if utility_cooccurance[i[-1]][Py] >= self.minutil:
                        Pxy = i + [Py]
                        self.util_lists[frozenset(Pxy)] = self._find_high_utility_itement_constuct(P,i,Py)
                        extensionsOfPx.append(list(Pxy))

                self._find_high_utility_search(i,extensionsOfPx,utility_cooccurance)


    def run_find_high_utility_itement(self):
        for x in self.profitable_utility_list:
            self.util_lists[frozenset([x[0]])] = self._createUtilList([x[0]])
        utility_cooccurance = {k:{j:self._findItemUtility([k,j]) for j in self.unit_profit.keys() if j != k} for k in self.unit_profit.keys()}
        self._find_high_utility_search([],[[x[0]]for x in self.profitable_utility_list],utility_cooccurance)
        return self.hui_list

transactions = [(1,[('a',3),('b',2)]),(2,[('a',1)]),(3,[('c',1),('b',10)]),(4,[('a',7),('b',1),('c',2)])]
unit_profit = {'a': 4,'b': 2,'c': 7}
# transactions = td.get_transactional_data()
# unit_profit = up.get_unit_price()
highUtilityItemset = []
obj = FindHighUtilityItement(transactions,unit_profit,0.3,highUtilityItemset,minutil_pc=False)
highUtilityItemset = obj.run_find_high_utility_itement()
print(highUtilityItemset)
