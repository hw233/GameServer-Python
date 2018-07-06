# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''阎王蝎·归顺'''
	intro = '''回去告诉仙子，根源已解决'''
	detail = '''回去告诉仙子，云顶村的怪事已经平息。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1074)'''
#导表结束