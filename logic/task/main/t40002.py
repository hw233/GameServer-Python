# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 0
	title = '''第一章·仙贡'''
	intro = '''寻找$props，将其奉献给$target'''
	detail = '''寻找$props，将其奉献给$target'''
	rewardDesc = '''200001,221401'''
	goAheadScript = ''''''
	initScript = '''N1001,L(221102,1),E(1001,1002)'''
#导表结束
