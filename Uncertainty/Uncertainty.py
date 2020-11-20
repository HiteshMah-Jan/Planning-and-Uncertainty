import copy
class VariableElimination:
    @staticmethod
    def inference(factorList, queryVariables,
    orderedListOfHiddenVariables, evidenceList, valueMap):
        for ev in evidenceList:
            #Your code here
            for i in range(0,len(factorList)):
                if ev in factorList[i].varList:
                   factorList[i] = factorList[i].restrict(ev,evidenceList[ev],valueMap)

        for var in orderedListOfHiddenVariables:
            #Your code here
            eliminataList = []
            for i in range(0,len(factorList)):
                if var in factorList[i].varList:
                    eliminataList.append(i)
            newfactor = factorList[eliminataList[0]]
            for i in range(1,len(eliminataList)):
                newfactor = newfactor.multiply(factorList[eliminataList[i]])
            newfactor = newfactor.sumout(var)

            # Here must be traversed backwards to delete
            for i in range(len(eliminataList)-1,-1,-1):
                del factorList[eliminataList[i]]
            factorList.append(newfactor)

        print("RESULT:")
        res = factorList[0]
        for factor in factorList[1:]:
            res = res.multiply(factor)
        total = sum(res.cpt.values())
        res.cpt = {k: v/total for k, v in res.cpt.items()}
        res.printInf()

    @staticmethod
    def printFactors(factorList):
        for factor in factorList:
            factor.printInf()
class Util:
    @staticmethod
    def to_binary(num, len):
        return format(num, '0' + str(len) + 'b')
class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.varList = var_list
        self.cpt = {}
        self.valuemap = {}
    def setValuemap(self,valuemap):
        self.valuemap = valuemap
    def setCpt(self, cpt):
        self.cpt = cpt
    def printInf(self):
        print("Name = " + self.name)
        print(" vars " + str(self.varList))
        for key in self.cpt:
            print("   key: " + key + " val : " + str(self.cpt[key]))
        print("")
    def multiply(self, factor):
        # The incoming factors are all Node type
        """function that multiplies with another factor"""
        #Your code here
        newList = []
        for i in self.varList:
            newList.append(i)
        for i in factor.varList:
            if i not in newList:
                newList.append(i)
        new_cpt = {}
        commonList = sorted(set(self.varList) & set(factor.varList),key = self.varList.index)

        commonindex1 = []
        commonindex2 = []
        for term in commonList:
            # Save the subscript of the common term in the first factor
            commonindex1.append(self.varList.index(term))
            # Save the subscript of the common term in the second factor
            commonindex2.append(factor.varList.index(term))
        for iter1 in self.cpt:
            for iter2 in factor.cpt:
                flag = True
                for (i,j) in zip(commonindex1,commonindex2):
                    if iter1[i] != iter2[j]:
                        flag = False
                        break
                # It means these two items can be multiplied
                tempstr = len(newList)*[0]
                if flag:
                    # For each variable in the first factor
                    for i in range(0,len(self.varList)):
                        # Find the subscript of this variable in the new list
                        tempindex = newList.index(self.varList[i])
                        tempstr[tempindex] = iter1[i]
                    for i in range(0,len(factor.varList)):
                        tempindex = newList.index(factor.varList[i])
                        tempstr[tempindex] = iter2[i]
                    temp = ""
                    for s in tempstr:
                        temp = temp + s
                    new_cpt[temp] = self.cpt[iter1] * factor.cpt[iter2]
        new_node = Node("f" + str(newList), newList)
        new_node.setCpt(new_cpt)
        return new_node
    def sumout(self, variable):
        """function that sums out a variable given a factor"""
        #Your code here
        index = self.varList.index(variable)
        new_var_list = copy.deepcopy(self.varList)
        del new_var_list[index]
        new_cpt = {}
        for c in self.cpt:
            tempstr = ""
            # Here is to delete the value that is combined to get a new valued string
            for i in range(0,len(c)):
                if i != index:
                    tempstr = tempstr + c[i]
            if tempstr in new_cpt:
                new_cpt[tempstr] = new_cpt[tempstr] + self.cpt[c]
            else:
                new_cpt[tempstr] = self.cpt[c]


        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node
    def restrict(self, variable, value,factorlist):
        """function that restricts a variable to some value
        in a given factor"""
        #Your code here
        # Variables are not deleted when adding restrictions, so you can use this function when replacing evi
        index = self.varList.index(variable)
        new_var_list = copy.deepcopy(self.varList)

        # del new_var_list[index]
        # Rename, change the corresponding limit value to the corresponding symbol
        # if value==1:
        #     new_var_list[index] = new_var_list[index].lower()
        # else:
        #     new_var_list[index] = "~" + new_var_list[index].lower()

        new_var_list[index] = valueMap[variable][value]


        new_cpt = {}
        # c is a string
        for c in self.cpt:
            # Requirements for dictionary items that meet the value requirements
            if int(c[index])==value:
                # If it is already in the dictionary, add this value
                if c in new_cpt:
                    new_cpt[c] = new_cpt[c] + self.cpt[c]
                else:
                    # Otherwise, insert a new pair (in fact, in this case, the new insert should not be added again)
                    new_cpt[c] = self.cpt[c]

        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node

# create nodes for Bayes Net
# B = Node("B", ["B"])
# E = Node("E", ["E"])
# A = Node("A", ["A", "B","E"])
# J = Node("J", ["J", "A"])
# M = Node("M", ["M", "A"])
PatientAge = Node("PatientAge",["PatientAge"])
CTScanResult = Node("CTScanResult",["CTScanResult"])
MRIScanResult = Node("MRIScanResult",["MRIScanResult"])
Anticoagulants = Node("Anticoagulants",["Anticoagulants"])
StrokeType = Node("StrokeType",["StrokeType","CTScanResult","MRIScanResult"])
Disability = Node("Disability",["Disability","PatientAge","StrokeType"])
Mortality = Node("Mortality",["Mortality","StrokeType","Anticoagulants"])

PatientAge.setValuemap({0:'0-30',1:'31-65',2:'65+'})
CTScanResult.setValuemap({0:'Ischemic Stroke',1:'Hemmorraghic Stroke'})
MRIScanResult.setValuemap({0:'Ischemic Stroke',1:'Hemmorraghic Stroke'})
Anticoagulants.setValuemap({0:'Not used',1:'Used'})
StrokeType.setValuemap({0:'Ischemic Stroke',1:'Hemmorraghic Stroke',2:'Stroke Mimic'})
Disability.setValuemap({0:'Negligible',1:'Moderate',2:'Severe'})
Mortality.setValuemap({0:'False',1:'True'})

valueMap = {'PatientAge':{0:'0-30',1:'31-65',2:'65+'},
            'CTScanResult':{0:'Ischemic Stroke',1:'Hemmorraghic Stroke'},
            'MRIScanResult':{0:'Ischemic Stroke',1:'Hemmorraghic Stroke'},
            'Anticoagulants':{0:'Not used',1:'Used'},
            'StrokeType':{0:'Ischemic Stroke',1:'Hemmorraghic Stroke',2:'Stroke Mimic'},
            'Disability':{0:'Negligible',1:'Moderate',2:'Severe'},
            'Mortality':{0:'False',1:'True'}
            }


PatientAge.setCpt({'0':0.1,'1':0.3,'2':0.6})
CTScanResult.setCpt({'0':0.7,'1':0.3})
MRIScanResult.setCpt({'0':0.7,'1':0.3})
Anticoagulants.setCpt({'0':0.5,'1':0.5})
StrokeType.setCpt({'000':0.8,'001':0.5,'010':0.5,'011':0,
                   '100':0  ,'101':0.4,'110':0.4,'111':0.9,
                   '200':0.2,'201':0.1,'210':0.1,'211':0.1})
Mortality.setCpt({'001':0.28,'011':0.99,'021':0.1,'000':0.56,'010':0.58,'002':0.05,
                  '101':0.72,'111':0.01,'121':0.9,'100':0.44,'110':0.42,'102':0.95})
Disability.setCpt({'000':0.8,'010':0.7,'002':0.9,'001':0.6,'011':0.5,'012':0.4,'020':0.3,'021':0.2,'022':0.1,
                   '100':0.8,'110':0.7,'102':0.9,'101':0.6,'111':0.5,'112':0.4,'120':0.3,'021':0.2,'022':0.1,
                   '200':0.8,'210':0.7,'202':0.9,'201':0.6,'211':0.5,'212':0.4,'220':0.3,'021':0.2,'022':0.1,})


# Generate cpt for each node
# B.setCpt({'0': 0.999, '1': 0.001})
# E.setCpt({'0': 0.998, '1': 0.002})
# A.setCpt({'111': 0.95, '011': 0.05, '110':0.94,'010':0.06,
# '101':0.29,'001':0.71,'100':0.001,'000':0.999})
# J.setCpt({'11': 0.9, '01': 0.1, '10': 0.05, '00': 0.95})
# M.setCpt({'11': 0.7, '01': 0.3, '10': 0.01, '00': 0.99})

# print("P(A) **********************")
# VariableElimination.inference([B,E,A,J,M], ['A'], ['B', 'E', 'J','M'], {})
#
# print("P(B | J~M) **********************")
# VariableElimination.inference([B,E,A,J,M], ['B'], ['E','A'], {'J':1,'M':0})

VariableElimination.inference([PatientAge,CTScanResult,MRIScanResult,Anticoagulants,StrokeType,Disability,Mortality],
                              ['Mortality','CTScanResult'],['Disability','MRIScanResult','StrokeType','Anticoagulants'],{'PatientAge':1},valueMap)
VariableElimination.inference([PatientAge,CTScanResult,MRIScanResult,Anticoagulants,StrokeType,Disability,Mortality],
                              ['Disability','CTScanResult'],['Anticoagulants','StrokeType','Mortality'],{'PatientAge':2,'MRIScanResult':1},valueMap)
