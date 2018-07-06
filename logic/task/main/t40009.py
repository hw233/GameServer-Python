# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·迷路'''
	intro = '''找不到回师门房间的路，问问$target吧'''
	detail = '''找不到回师门房间的路，四处问问人？'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N1005,E(1005,1009)'''
#导表结束