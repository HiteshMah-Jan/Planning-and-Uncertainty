import queue
import copy
# 定义一个问题类，把需要的针对这个问题的变量都放到这里来，代码更优雅，结构更清晰
# 更改类变量要用类名＋.
class Problem:
    # 保存所有的当前状态，最开始是初始状态
    nowState = []
    # 保存目标状态,这个list也不会改变
    goalState = []
    # 记录所有的变量,变量类型作为key，对应的变量作为value,这个变量永远不要修改
    variables = {}
    # 记录解的动作
    solves = []
    # 保存所有的动作
    action_list = []

    # initial里是不会出现动作的
    class Action:
        # 在这里定义的变量是属于整个类的变量，全局变量的优雅使用
        def __init__(self,na = None, yespre = [],notpre:list = [],add = [],dele = [],inst:dict = [],parameter:dict = {}):
            self.name = na
            # 保存所有的前提条件
            self.yesPre = yespre
            self.notPre = notpre
            # 保存这个动作要添加的状态
            self.addlist = add
            # 保存这个动作要减少的状态
            self.deletelist = dele
            # 保存动作的实例
            self.instance = inst
            # 保存动作的变量参数
            self.parameter = parameter

        def canBeDo(self):
            # 用所有的可能地变量组合去实例化这个动作
            # 判断这个动作是不是可以被做
        def renewState(self):
            # 更新当前状态，将该增加的增加进来，该删除的删除出去
            # Problem.nowState
        def pullBack(self):
            #这个动作不行，回溯，把删掉的加回来，加上的删去
        def do(self):
            # 说明这个动作已经实例化了
            if self.instance:
                self.renewState(self.addlist,self.deletelist)

        # 返回bool，判断这个状态是不是包含goal
        def isContainGoal(self, state: list) -> bool:
            for i in Problem.goalState:
                if i not in state:
                    return False
            return True
        # 假装做这个动作
        def fakeDo(self)->list:
            self.do()
            state = Problem.nowState[:]
            self.pullBack()
            return state

        def instanceTheAction(self,clause,instance):
            ret = []
            ret.append(clause[0])
            for j in range(1,len(clause)):
                ret.append(instance[clause[j]])
            return ret

        # 从当前状态出发，只添加不删除找到包含目标状态的那一层
        # 返回两个list,一个是状态层，一个是动作层，下标一一对应
        def getLayeredStruct(self, initstate, problem):
            # 这是一个list，包含所有可以做的动作
            stateret = []
            actionsret = []
            stateret.append(initstate)
            while not self.isContainGoal(initstate):
                # 找到所有可以做的动作，这个里面都是实例化好的动作
                tempactions = problem.findActionsCanBedo(initstate)
                if len(actionsret)>0:
                    # 做差集
                    subset = [i for i in tempactions if i not in actionsret[-1]]
                    actionsret.append(subset)
                else:
                    # 把这个list添加到动作层
                    actionsret.append(tempactions)
                # 添加所有的addlist到当前状态层
                for add in self.addlist:
                    tempadd = self.instanceTheAction(add,self.instance)
                    initstate.append(tempadd)
                stateret.append(initstate)
            return stateret,actionsret

        # S就是状态层,第k层状态层，对应第k-1层动作层
        def countActions(self,G,S,k,A):
            if k==0: return 0
            Gp = list(set(G).intersection(set(S[k-1])))
            Gn = [i for i in G if i not in Gp]
            theA = []
            for a in A[k-1]:
                instant_add = []
                for t in a.addlist:
                    tempac = a.instanceTheAction(t,a.instance)
                    instant_add.append(tempac)
                    if tempac in Gn and a not in theA:
                        theA.append(a)
                if theA[-1] == a:
                    for i in a.yesPre:
                        tempypr = a.instanceTheAction(i,a.instance)
                        Gp.append(tempypr)
                    for i in a.notPre:
                        tempnpr = a.instanceTheAction(i,a.instance)
                        Gp.append(tempnpr)
                    for i in instant_add:
                        if i in Gn:
                            Gn.remove(i)
                if len(Gn)==0:
                    break
            return self.countActions(Gp,S,k-1,A) + len(theA)

        def getHeuristic(self, problem)->int:
            initstate = self.fakeDo()
            statelayer,actionlayer = self.getLayeredStruct(initstate,problem)
            return self.countActions(Problem.goalState,statelayer,len(statelayer)-1,actionlayer)




    def __init__(self,s:list = None,v = None,g:list = None):
        Problem.nowState = s
        Problem.variables = v
        Problem.goalState = g

    def findActionsCanBedo(self, state: list) -> list:
    # 这个还是找所有可以做的动作，但是返回一个list,传入的参数是对于这个状态所有可以做的list
    #     在solve函数里调用的时候传入nowstate就可以了
    #     因为在计算启发式函数的值的时候也要用到这个函数，如果不拆开直接用原来的就相互调用了
    def changeActionstoQueue(self) -> queue.PriorityQueue:
        #     这个函数将上面的结果list转化成queue，大概就像下面那样
        ret = queue.PriorityQueue()
        acts = self.findActionsCanBedo()
        for i in acts:
            ret.put((i.getHeuristic(), i))
        return ret
    # 这个实际上就是搜索函数
    def solve(self,actions):
        # 获取第一个动作
        theAction = actions.get()[1]
        # 做这个动作
        theAction.do()
        Problem.solves.append(theAction)
        if Problem.nowState==Problem.goalState:
            return True
        actionsb = self.findActionsCanBedo()
        if actionsb:
            return self.solve(actionsb)
        # 如果运行到这了就说明这个动作会导致问题无解，回溯
        theAction.pullBack()





# 先读problem，把变量和对应的类型先读出来
def readproblem(filename):
    file = open(filename)
    lines = file.readlines()
    i = 0
    while(i<len(lines)):
        line = lines[i]
        line = line.strip()
        one = line.split(' ')
        if one[0] == '(:objects':
            for j in range(i+1,len(lines)):
                temp = lines[j]
                temp = temp.strip()
                templist = temp.split(' ')
                if templist[0]!=')':
                    for v in templist[0:-2]:
                        Problem.variables[v] = templist[-1]
                else:
                    i = j
                    break
        if one[0] == '(:init':
            for j in range(i+1,len(lines)):
                temp = lines[j]
                temp = temp.strip()
                temp = temp.strip('(')
                temp = temp.strip(')')
                templist = temp.split(' ')
                if templist[0]!='':
                    Problem.nowState.append(templist)
                else:
                    i = j
                    break
        if one[0] == '(:goal':
            for j in range(i+1,len(lines)):
                temp = lines[j]
                temp = temp.strip()
                temp = temp.strip('(')
                temp = temp.strip(')')
                templist = temp.split(' ')
                if templist[0]!='':
                    Problem.goalState.append(templist)
                else:
                    i = j
                    break
        i = i + 1
def readdomain(filename):
    file = open(filename)
    lines = file.readlines()
    i = 0
    while(i<len(lines)):
        line = lines[i]
        line = line.strip()
        one = line.split(' ')
        if one[0]=='(:action':
            a = Problem.Action()
            a.name = lines[i+1].strip()
            j = i+2
            while(j<len(lines)):
                temp1 = lines[j]
                temp1 = temp1.strip()
                temp1list = temp1.split(' ')
                if temp1list[0]==':parameters':
                    for k in range(j+1,len(lines)):
                        temp2 = lines[k]
                        temp2 = temp2.strip()
                        temp2 = temp2.strip('?')
                        temp2list = temp2.split(' ')
                        if temp2list[0]==')':
                            j = k
                            break
                        for v in temp2list[0:-2]:
                            a.parameter[v] = temp2list[-1]
                if temp1list[0]==':precondition' or temp1list[0]==':effect':
                    for k in range(j+1,len(lines)):
                        temp2 = lines[k]
                        temp2 = temp2.strip()
                        temp2 = temp2.strip('(')
                        temp2 = temp2.strip(')')
                        temp2list = temp2.split(' ')
                        if temp2list[0]=='':
                            j = k
                            break
                        temp3 = []
                        if temp2list[0] != 'not':
                            temp3.append(temp2list[0])
                        for cl in range(1, len(temp2list)):
                            tempstr = temp2list[cl].strip('(')
                            tempstr = tempstr.strip(')')
                            tempstr = tempstr.strip('?')
                            temp3.append(tempstr)
                        if temp1list[0]==':precondition':
                            if temp2list[0] == 'not':
                                a.notPre.append(temp3)
                            else:
                                a.yesPre.append(temp3)
                        elif temp1list[0]==':effect':
                            if temp2list[0] == 'not':
                                a.deletelist.append(temp3)
                            else:
                                a.addlist.append(temp3)
                j = j + 1
            Problem.action_list.append(a)
        i = i+1

readproblem('pddl\\test0\\test0_problem.txt')
print(Problem.variables)
