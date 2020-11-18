# -*- coding: utf-8 -*-
# @Time    : 2018/6/12 20:20
# @Author  : Alex
# @File    : data_structure.py
# @Software: PyCharm
from common.myException.exceptions import CaculateException
from common.myException.exceptions import QueueEmptyException

class Stack():
    def __init__(self):
        self.stack = []
        self.top = -1
    def push(self, x):
        self.stack.append(x)
        self.top = self.top + 1
    def pop(self):
        ''''''
        if self.is_empty():
            raise Exception("stack is empty")
        else:
            self.top = self.top - 1
            self.stack.pop()
    def is_empty(self):
        return self.top == -1
    def peek(self):
        '''
        :return:栈顶元素
        '''
        if self.stack is not []:
            return self.stack[self.top]
        else:
            return None


class Queue(object):
    def __init__(self):
        self.queue = []
    def put(self, i):
        self.queue.append(i)
        # print self.queue

    def get(self):
        try:
            i = self.queue[0]
            self.queue.pop(0)
            return i
        except:
            raise QueueEmptyException()
    def empty(self):
        if self.queue == []:
            return True
        else:
            return False


if __name__ == "__main__":
    # q = testqueue()
    # for i in q.queue:
    #     print i,
    # print ""
    # print testcalc(q.queue)
    # from Queue import Queue
    l_value = [i for i in "asdfgh"]
    l_oper = [i for i in "+-*/"]
    q1 = Queue()
    q2 = Queue()
    # print q1.queue
    print([q1.put(i) for i in l_value])
    print([q2.put(i) for i in l_oper])


    # q = Queue()
    # q.put(1)
    # print q.get()
    # sourcestr = "5+3-1*2-6/2"
    # # sourcestr = "5*(3-1)"
    # # print("orig:%s" % sourcestr)
    # # re1 = parse(sourcestr)
    # # print("niBolan:%s" % " ".join(re1))
    # result = caculate(sourcestr)
    # print('result:%s' % result)
