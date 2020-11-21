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

    # initial里是不会出现动作的
    class Action:
        # 在这里定义的变量是属于整个类的变量，全局变量的优雅使用
        def __init__(self,na = None, pre = None,add = None,dele = None,inst:dict = None):
            self.name = na
            # 保存所有的前提条件
            self.precondition = pre
            # 保存这个动作要添加的状态
            self.addlist = add
            # 保存这个动作要减少的状态
            self.deletelist = dele
            # 保存动作的实例
            self.instance = inst

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



    def __init__(self,s:list = None,v = None,g:list = None):
        Problem.nowState = s
        Problem.variables = v
        Problem.goalState = g


    def findActionsCanBedo(self)->queue.PriorityQueue:
        # 根据nowState的值寻找当前所有可以做的动作
        # 保存到actions中
        # 这个动作和动作的启发式函数值作为一个tuple存在这里，启发式函数值就是做了这个动作之后的状态的countAction
    # 这个实际上就是搜索函数
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


