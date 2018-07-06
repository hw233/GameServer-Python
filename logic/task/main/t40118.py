# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·不屈'''
	intro = '''$target十分气愤，破口大骂'''
	detail = '''$target十分气愤，破口大骂'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2014,NI2013,NI2017,E(2014,2028),E(2013,2027),E(2017,2026)'''
#导表结束