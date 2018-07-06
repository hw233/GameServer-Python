# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''文雀·询问'''
	intro = '''到达青螺竹林后，与文雀对话'''
	detail = '''到达青螺竹林后找到文雀，询问它闷闷不乐的原因。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1006,E(1006,1022)'''
#导表结束