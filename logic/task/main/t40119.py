# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第二章·援手'''
	intro = '''$target提起剑就要下手了'''
	detail = '''$target提起剑就要下手了'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2013,NI2014,E(2013,2029),E(2014,2030)'''
#导表结束