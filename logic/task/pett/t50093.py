# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''毕方·守口'''
	intro = '''回去告诉$target，毕方不肯透露'''
	detail = '''毕方不愿说出原因，只能回去告诉仙子。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1052)'''
#导表结束