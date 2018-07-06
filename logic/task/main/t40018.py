# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第一章·逃跑'''
	intro = '''说不清了，还是尽快战胜$target逃跑吧'''
	detail = '''说不清了，还是尽快战胜$target逃跑吧'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N1008,E(1008,1021)'''
#导表结束