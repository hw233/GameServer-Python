# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''句芒·陷阱'''
	intro = '''与出现的明修罗交手'''
	detail = '''与句芒交谈后得知是修罗宫的陷阱，此时明修罗出现，与之交手。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1022,E(1022,1064)'''
#导表结束