# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第二章·三师姐'''
	intro = '''$target刚才重伤昏迷，但此刻又站了起来！'''
	detail = '''$target刚才重伤昏迷，但此刻又站了起来！'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2012,NI2017,E(2012,2023),E(2017,2024)'''
#导表结束