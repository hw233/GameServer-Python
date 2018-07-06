# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·口诀'''
	intro = '''与$target说话'''
	detail = '''师父觉得你在刚才战斗中有许多地方不足，特意传授战斗口诀于你，快去。'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N1013,E(1013,1007)'''
#导表结束