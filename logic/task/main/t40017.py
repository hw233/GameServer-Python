# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·蒙冤'''
	intro = '''向$target解释事情起末'''
	detail = '''向$target解释事情起末'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N1013,E(1013,1020)'''
#导表结束