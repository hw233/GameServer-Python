# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·求饶'''
	intro = '''$target哭哭啼啼的，想向樗散子求饶'''
	detail = '''$target哭哭啼啼的，想向樗散子求饶'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2013,NI2017,E(2013,2025),E(2017,2026)'''
#导表结束