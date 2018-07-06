# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·盗玉'''
	intro = '''$target突然从后洞转出，似乎有话要说'''
	detail = '''$target突然从后洞转出，似乎有话要说'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2059,NI2038,NI2039,E(2059,2080),E(2038,2076),E(2039,2076)'''
#导表结束