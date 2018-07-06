# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·不动'''
	intro = '''$target似乎不愿意出手'''
	detail = '''$target似乎不愿意出手'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2011,E(2011,2018)'''
#导表结束