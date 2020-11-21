"""
    File:STRIPS_palnner
    TASK:读取两个文件：domain和problem，进行PDDL规划，
        输出应做的动作
    思路：用A*搜索算法解决，
        状态：当前时刻谓词的合取
        动作：有前提，add和del三个list
        设计启发式函数h来评估每个状态，使用最小f值来进行搜索
        每轮遍历对动作列表里的并比对当前状态能否全部有
        如果可以：则计算f=g+h值并放入边界队列中，每次选择最小的f进行探索
"""
import queue
import copy
import itertools

#数据结构部分
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

    #构造函数
    def __init__(self, s: list = None, v=None, g: list = None):
        Problem.nowState = s
        Problem.variables = v
        Problem.goalState = g

    #子类 Action
    class Action:
        #构造函数
        def __init__(self, na = None,yespre=None,notpre=None, add=None, delete=None, instance: dict = None, parameter:dict = None):
            self.name = na
            self.yesPre = yespre  # 二维列表，存放需要在状态列表中的literal
            self.notPre = notpre
            self.add = add
            self.delete = delete
            self.instance = instance
            self.parameter = parameter

        def canBeDo(self):
            # 用所有的可能地变量组合去实例化这个动作
            # 判断这个动作是不是可以被做,可以的话，返回满足的赋值列表
            # 遍历所有变量的组合，类型一样的判断组成的前提能否全部在now_state被满足
            #var_len = len(Problem.variables)
            parameter_num = len(self.parameter)
            ok_permutation_list = []

            ret = False
            #进行排列
            permutation_var_list = list(itertools.permutations(list(Problem.variables.keys()),parameter_num))
            for permutation in permutation_var_list:
                flag = True
                for i in permutation.range():
                    #1.类型要一样
                    if Problem.variables[permutation[i]] != self.parameter[i]:
                        flag = False
                        break
                    #2.前提要在状态中
                    new_yesPre = []
                    #遍历元素寻找替换
                    TODO
                if flag == True:
                    ret = True
                    ok_permutation_list.append(permutation)
            #根据可行的permutation进行实例化构造可行的动作列表
            return ret,ok_permutation_list

        def renewState(self):
            # 更新当前状态，将该增加的增加进来，该删除的删除出去
            # Problem.nowState
            #首先进行替换后的add，del分别作用


        def pullBack(self):
            #这个动作不行，回溯，把删掉的加回来，加上的删去

        # findAction调用的函数，计算h值
        def getHeuristic(self):

        def do(self):
            # 做这个动作
            if self.instance:
                self.renewState(self.addlist, self.deletelist)

    #读txt文件，建立世界
    def buildWorld(self):

    def findActionsCanBedo(self)->queue.PriorityQueue:
        # 根据nowState的值寻找当前所有可以做的动作
        # 保存到actions中
        # 这个动作和动作的启发式函数值作为一个tuple存在这里，启发式函数值就是做了这个动作之后的状态的countAction
    # 这个实际上就是搜索函数
        front = queue.PriorityQueue()# 存放可以进行的动作
        #遍历动作列表，寻找所有动作实例
        for action in self.action_list:
            can_do,permutation_list = action.canBeDo()
            if can_do:


    def solve(self,actions):

        if actions.empty():
            return False
        # 获取第一个动作
        theAction = actions.get()[1]
        # 做这个动作
        theAction.do()
        Problem.solves.append(theAction)
        if Problem.nowState==Problem.goalState:
            return True
        actionscopy = copy.deepcopy(actions)
        actions = self.findActionsCanBedo()
        if actions:
            return self.solves(actions)
        # 如果运行到这了就说明这个动作会导致问题无解，回溯
        actions = actionscopy
        theAction.pullBack()

if __name__ == '__main__':

"""
#test case 0
#world初始化参数
nowState = [['borber','town','field'],['borber','field','castle'],['at','npc','town']]
goalState = [['at','npc','castle']]
action_list = [move] #move是一个动作类对象
variables = {'npc':'player','town':'location','field':'location','castle':'location'}

#action的初始化参数
parameter={‘p’:'player','l1':'location','l2':'location'}
yesPre = [['at','p','l1'],['border', 'l1' ,'l2']]
noPre = [['guarded', 'l2']]
add = [['at', 'p' ,'l2']]
delete = [['at','p','l1']]

"""




