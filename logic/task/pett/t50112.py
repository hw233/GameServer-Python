# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''阎王蝎·打听'''
	intro = '''问问小虎儿最近村里的情况'''
	detail = '''正好看到路边的小虎儿，问问村里最近发生什么怪事。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(20301,1069)'''
#导表结束