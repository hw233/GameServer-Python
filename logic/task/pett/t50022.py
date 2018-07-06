# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''螺旋草·寻找'''
	intro = '''在附近转转，找寻$target'''
	detail = '''螺旋草不在家，但看迹象并没离开多久，在附近转转，看能不能遇到。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1002,E(1002,1007)'''
#导表结束