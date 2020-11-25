import queue
import copy
import itertools
import operator


# 数据结构部分
class Problem:
    # 保存所有的当前状态，最开始是初始状态
    nowState = []
    # 保存目标状态,这个list也不会改变
    goalState = []
    # 记录所有的变量,变量类型作为key，对应的变量作为value,这个变量永远不要修改
    variables = {}
    # 记录解的动作
    solves = []
    # 动作列表，存放Action类对象
    action_list = []

    # 构造函数
    def __init__(self, s: list = [], v={}, g: list = []):
        Problem.nowState = s
        Problem.variables = v
        Problem.goalState = g

    # 子类 Action
    class Action:
        # 构造函数
        def __init__(self,na = None, yespre = [],notpre:list = [],add = [],delete = [],instance:dict = [],
                     parameter:dict = {}, paraorder = []):
            self.name = na
            self.yesPre = yespre  # 二维列表，存放需要在状态列表中的literal
            self.notPre = notpre
            self.add = add
            self.delete = delete
            self.instance = instance
            self.parameter = parameter
            self.paraorder = paraorder

        # 判断一个动作能否被做，以及可以做的实例赋值，返回为bool和二位列表
        def canBeDo(self) -> (bool, list):
            # 用所有的可能地变量组合去实例化这个动作
            # 判断这个动作是不是可以被做,可以的话，返回满足的赋值字典的列表
            # 遍历所有变量的组合，类型一样的判断组成的前提能否全部在now_state被满足，
            # 如果可以就在这里实例化出一个列表，里面是赋值字典
            # var_len = len(Problem.variables)
            parameter_num = len(self.parameter)
            ok_permutation_list = []  # 二维列表

            ret = False
            # 进行排列
            permutation_var_list = list(itertools.permutations(list(Problem.variables.keys()), parameter_num))
            for permutation in permutation_var_list:
                flag = True
                # 1.对应类型要一样
                for i in range(len(permutation)):

                    if Problem.variables[permutation[i]] != self.parameter[self.paraorder[i]]:
                        flag = False
                        break

                if flag == False:
                    continue
                # 2.yes前提要在状态中
                para_list = self.parameter.keys()
                temp_instances = dict(zip(para_list, permutation))
                for pre in self.yesPre:
                    # 逐个item进行替换
                    temp_yes_pre = self.instanceTheAction(pre, temp_instances)
                    print("替换后temp yes pre = ", temp_yes_pre)

                    # 在状态查找是否有这个，没有的话break
                    can_find = False
                    for state in Problem.nowState:
                        if operator.eq(temp_yes_pre, state):  # 找到了，不用继续，直接判断下一个前提
                            can_find = True
                            break
                    if can_find == False:  # 找不到,这个赋值不可以
                        flag = False
                        break
                # 2.no前提要不在状态中
                for pre in self.notPre:
                    temp_not_pre = self.instanceTheAction(pre, temp_instances)
                    print("替换后temp not pre = ", temp_not_pre)

                    # 在状态查找是否有这个，有的话break
                    for state in Problem.nowState:
                        if operator.eq(temp_not_pre, state):  # 找到了，这个赋值不可以
                            flag = False
                            break
                    if flag == False:  # 这个赋值有不满足前提直接break
                        break
                if flag == False:  # 这个赋值不可，找下一个排列
                    continue
                else:  # 这个赋值可以，构造新的action对象加入list
                    ret = True
                    ok_permutation_list.append(dict(zip(self.parameter.keys(), permutation)))
            # 根据可行的permutation进行实例化构造可行的动作对象赋值列表如True,[[npc,town,field]]
            return ret, ok_permutation_list

        def renewState(self):
            # 更新当前状态，将该增加的增加进来，该删除的删除出去
            # Problem.nowState
            # 首先进行替换后的add，del分别作用，替换已经在构造的时候就已经实现了
            # 加入add
            for add_state in self.add:
                if add_state not in Problem.nowState:
                    Problem.nowState.append(add_state)
                    print("加入state:" , add_state)
            # 删去del
            for del_state in self.delete:
                if del_state in Problem.nowState:
                    Problem.nowState.remove(del_state)
                    print("删除state:" , del_state)

        def pullBack(self):
            # 这个动作不行，回溯，把删掉的加回来，加上的删去
            # 删除add
            for add_state in self.add:
                if add_state not in Problem.nowState:
                    Problem.nowState.remove(add_state)
                    print("pullback删除state:" , add_state)
            # 加入del
            for del_state in self.delete:
                if del_state in Problem.nowState:
                    Problem.nowState.append(del_state)
                    print("pullback加入state:" , del_state)

        def do(self):
            # 说明这个动作已经实例化了
            if self.instance:
                self.renewState()

        # 返回bool，判断这个状态是不是包含goal
        def isContainGoal(self, state: list) -> bool:
            for i in Problem.goalState:
                if i not in state:
                    return False
            return True

        # 假装做这个动作
        def fakeDo(self) -> list:
            self.do()
            state = Problem.nowState[:]
            self.pullBack()
            return state

        def instanceTheAction(self, clause, instance):
            ret = []
            ret.append(clause[0])
            for j in range(1, len(clause)):
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
                if len(actionsret) > 0:
                    # 做差集
                    subset = [i for i in tempactions if i not in actionsret[-1]]
                    actionsret.append(subset)
                else:
                    # 把这个list添加到动作层
                    actionsret.append(tempactions)
                # 添加所有的addlist到当前状态层
                for add in self.add:
                    tempadd = Problem.instanceTheAction(add, self.instance)
                    initstate.append(tempadd)
                stateret.append(initstate)
            return stateret, actionsret

        # S就是状态层,第k层状态层，对应第k-1层动作层
        def countActions(self, G, S, k, A):
            if k == 0: return 0
            Gp = list(set(G).intersection(set(S[k - 1])))
            Gn = [i for i in G if i not in Gp]
            theA = []
            for a in A[k - 1]:
                instant_add = []
                for t in a.addlist:
                    tempac = a.instanceTheAction(t, a.instance)
                    instant_add.append(tempac)
                    if tempac in Gn and a not in theA:
                        theA.append(a)
                if theA[-1] == a:
                    for i in a.yesPre:
                        tempypr = a.instanceTheAction(i, a.instance)
                        Gp.append(tempypr)
                    for i in a.notPre:
                        tempnpr = a.instanceTheAction(i, a.instance)
                        Gp.append(tempnpr)
                    for i in instant_add:
                        if i in Gn:
                            Gn.remove(i)
                if len(Gn) == 0:
                    break
            return self.countActions(Gp, S, k - 1, A) + len(theA)

        def getHeuristic(self, problem) -> int:
            initstate = self.fakeDo()
            statelayer, actionlayer = self.getLayeredStruct(initstate, problem)
            return self.countActions(Problem.goalState, statelayer, len(statelayer) - 1, actionlayer)

    # 根据赋值字典，返回动作实例
    def getActionInstance(self, original_action, assign) -> Action:
        new_action = self.Action()
        # name
        new_action.name = original_action.name
        # instance
        new_action.instance = assign
        # 把yesPre替换
        new_action.yesPre = []
        for i in original_action.yesPre:
            new_action.yesPre.append(new_action.instanceTheAction(i, assign))
        # 把notPre替换
        new_action.notPre = []
        for i in original_action.notPre:
            new_action.notPre.append(new_action.instanceTheAction(i, assign))
        # 把add替换
        new_action.add = []
        for i in original_action.add:
            new_action.add.append(new_action.instanceTheAction(i, assign))
        # 把add替换
        new_action.delete = []
        for i in original_action.delete:
            new_action.delete.append(new_action.instanceTheAction(i, assign))
        # parameter
        new_action.parameter = original_action.parameter

        return new_action

    def findActionsCanBedo(self) -> list:
        #     这个还是找所有可以做的动作，但是返回一个list,传入的参数是对于这个状态所有可以做的list
        #     在solve函数里调用的时候传入nowstate就可以了
        #     因为在计算启发式函数的值的时候也要用到这个函数，如果不拆开直接用原来的就相互调用了
        action_list = []
        for action in self.action_list:

            can_do, assign_list = action.canBeDo()
            # 如果可以做,对其中每一个可行的排列进行实例化
            if can_do == True:
                # 遍历每一个赋值字典
                for assign in assign_list:
                    new_action = self.getActionInstance(action, assign)
                    action_list.append(new_action)
        return action_list

    def changeActionstoQueue(self) -> queue.PriorityQueue:
        #     这个函数将上面的结果list转化成queue，大概就像下面那样
        ret = queue.PriorityQueue()
        acts = self.findActionsCanBedo()
        for i in acts:
            ret.put((i.getHeuristic(self), i))
        return ret



    # 这个实际上就是搜索函数
    def solve(self, actions):
        # 获取第一个动作
        theAction = actions.get()[1]
        # 做这个动作
        theAction.do()
        Problem.solves.append(theAction)
        if Problem.nowState == Problem.goalState:
            return True

        actionsb = self.changeActionstoQueue()
        if actionsb:
            return self.solve(actionsb)
        # 如果运行到这了就说明这个动作会导致问题无解，回溯
        theAction.pullBack()
        Problem.solves.remove(theAction)

    def printActions(self):
        print("-------Actions-------")
        for i in range(len(self.solves)):
            print("action ", i, " ", self.solves[i])
        print("--------Done--------")


# 先读problem，把变量和对应的类型先读出来
def readproblem( filename):
    file = open(filename)
    lines = file.readlines()
    i = 0
    while (i < len(lines)):
        line = lines[i]
        line = line.strip()
        one = line.split(' ')
        if one[0] == '(:objects':
            for j in range(i + 1, len(lines)):
                temp = lines[j]
                temp = temp.strip()
                templist = temp.split(' ')
                if templist[0] != ')':
                    for v in templist[0:-2]:
                        Problem.variables[v] = templist[-1]
                else:
                    i = j
                    break
        if one[0] == '(:init':
            for j in range(i + 1, len(lines)):
                temp = lines[j]
                temp = temp.strip()
                temp = temp.strip('(')
                temp = temp.strip(')')
                templist = temp.split(' ')
                if templist[0] != '':
                    Problem.nowState.append(templist)
                else:
                    i = j
                    break
        if one[0] == '(:goal':
            for j in range(i + 1, len(lines)):
                temp = lines[j]
                temp = temp.strip()
                temp = temp.strip('(')
                temp = temp.strip(')')
                templist = temp.split(' ')
                if templist[0] != '':
                    Problem.goalState.append(templist)
                else:
                    i = j
                    break

        i = i + 1
def readdomain(filename):
    file = open(filename)
    lines = file.readlines()
    a = []
    for i in range(0, 10):
        a.append(Problem.Action())
    cnt = 0
    i = 0
    while (i < len(lines)):
        line = lines[i]
        line = line.strip()
        one = line.split(' ')
        if one[0] == '(:action':
            # a[cnt] = Problem.Action()
            a[cnt].name = lines[i + 1].strip()
            j = i + 2
            while (j < len(lines)):
                temp1 = lines[j]
                temp1 = temp1.strip()
                temp1list = temp1.split(' ')
                if temp1list[0] == ':parameters':
                    tempcnt = 0
                    a[cnt].parameter = {}
                    for k in range(j + 1, len(lines)):
                        temp2 = lines[k]
                        temp2 = temp2.strip()
                        temp2 = temp2.strip('?')
                        temp2list = temp2.split(' ')
                        if temp2list[0] == ')':
                            j = k
                            break

                        for v in temp2list[0:-2]:
                            a[cnt].paraorder.append(v)
                            a[cnt].parameter[v] = temp2list[-1]
                if temp1list[0] == ':precondition' or temp1list[0] == ':effect':
                    if temp1list[0] == ':precondition':
                        a[cnt].notPre = []
                        a[cnt].yesPre = []
                    else:
                        a[cnt].add = []
                        a[cnt].delete = []
                    for k in range(j + 1, len(lines)):
                        temp2 = lines[k]
                        temp2 = temp2.strip()
                        temp2 = temp2.strip('(')
                        temp2 = temp2.strip(')')
                        temp2list = temp2.split(' ')
                        if temp2list[0] == '':
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
                        if temp1list[0] == ':precondition':
                            if temp2list[0] == 'not':
                                a[cnt].notPre.append(temp3)
                            else:
                                a[cnt].yesPre.append(temp3)
                        elif temp1list[0] == ':effect':
                            if temp2list[0] == 'not':
                                a[cnt].delete.append(temp3)
                            else:
                                a[cnt].add.append(temp3)
                if temp1list[0] == ')':
                    i = j
                    break
                j = j + 1
            Problem.action_list.append(a[cnt])
            cnt += 1
        i = i + 1


if __name__ == '__main__':
    # problem = Problem()
    # 读文件
    readproblem('pddl\\test0\\test0_problem.txt')
    readdomain('pddl\\test0\\test0_domain.txt')
    problem = Problem(Problem.nowState,Problem.variables,Problem.goalState)
    print(Problem.variables)

    initial_actions = problem.changeActionstoQueue()
    Problem.solve(initial_actions)
