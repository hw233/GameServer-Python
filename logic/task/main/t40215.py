# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 0
	title = '''第一章·闯祸'''
	intro = '''找到$props，交给$target救助小人'''
	detail = '''找到$props，交给$target救助小人'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1014,NI1015,L(221103,1),E(1014,1054),E(1015,1053)'''
#导表结束