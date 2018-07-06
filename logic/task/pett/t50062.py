# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''傀儡熊·路人'''
	intro = '''沿路寻找，询问被吓坏的路人'''
	detail = '''沿着仙子所指方向前行，看到被吓坏的书生，问问他看到了什么。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1009,E(1009,1034)'''
#导表结束