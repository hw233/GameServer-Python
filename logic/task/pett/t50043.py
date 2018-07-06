# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 2
	title = '''文雀·方法'''
	intro = '''受文雀所托，找来$props'''
	detail = '''文雀听说多吃杜仲能轻身健体，增长道行，请你替它寻来杜仲。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1006,L(221104,1),E(1006,1023)'''
#导表结束