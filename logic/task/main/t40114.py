# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·阴谋'''
	intro = '''$target已经走火入魔？'''
	detail = '''$target已经走火入魔？'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2011,NI2015,E(2011,2019),E(2015,2020)'''
#导表结束