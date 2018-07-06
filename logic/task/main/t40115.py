# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·神秘人'''
	intro = '''$target已经被释放了？'''
	detail = '''$target已经被释放了？'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2016,NI2015,E(2016,2021),E(2015,2022)'''
#导表结束