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
#数据结构部分
class World:

    now_state = []# 当前状态，二维列表【【谓词1，变量1，变量2】，【谓词2，变量3，变量4】】
    goal_state = []# 目标状态，二维列表
    action_list = []# 动作列表，存放Action类对象
    variable = {}# 变量字典，如p1-location,
    solution_list = []# 动作序列列表

    #构造函数
    def __init__(self,nowSate:list=None,goalState:list=None,actionList=None,variable=None):
        World.now_state = nowSate
        World.goal_state = goalState
        World.action_list = actionList
        World.variable = variable

    #子类 Action
    class Action:
        #构造函数
        def __init__(self, pre=None, add=None, delete=None, instance: dict = None):
            self.pre = pre  # 二维列表，存放
            self.add = add
            self.delete = delete
            self.instance = instance

        #遍历变量列表的可行组合，判断pre列表是否全部在now_state中【【谓词1，变量1，变量2】，【谓词2，变量3，变量4】】
        def cando(self):

        # 用动作（已经实例化）改变now_state
        def changeState(self):

        # 动作回溯
        def pullBack(self):

        # findAction调用的函数，计算h值
        def getHeuristic(self):

    #读txt文件，建立世
    def buildWorld(self):

    #寻找可用且最优动作
    def findAction(self):


    # 对一个进行搜索（递归函数
    def searchOneState(self):






