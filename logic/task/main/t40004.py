# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·离尘'''
	intro = '''与$target说话'''
	detail = '''跟$target回报'''
	rewardDesc = '''200001,221101'''
	goAheadScript = ''''''
	initScript = '''N1001,E(1001,1004)'''
#导表结束