# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·禁地'''
	intro = '''这里是……那边有个人，去问问他吧'''
	detail = '''这里是……那边有个人，去问问他吧'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N1009,E(1009,1013)'''
#导表结束