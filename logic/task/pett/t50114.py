# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''阎王蝎·突发'''
	intro = '''打败想吃人的阎王蝎'''
	detail = '''找到阎王蝎后，阎王蝎却要吃掉你。打败阎王蝎。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1025,E(1025,1071)'''
#导表结束