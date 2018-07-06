# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第一章·修炼'''
	intro = '''入门咯，与$target战斗'''
	detail = '''入门咯，与$target战斗'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N1003,NI1004,E(1003,1005),E(1004,1006)'''
#导表结束