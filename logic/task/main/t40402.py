# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第三章·僵尸'''
	intro = '''$target咆哮着扑过来，把它们消灭吧'''
	detail = '''$target咆哮着扑过来，把它们消灭吧'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2002,NI2003,NI2004,E(2002,2003),E(2003,2004),E(2004,2005)'''
#导表结束