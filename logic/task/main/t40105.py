# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第二章·岩石怪'''
	intro = '''听说远方有一只巨怪，看来必须战胜$target，才有可能再上蜀山'''
	detail = '''听说远方有一只巨怪，看来必须战胜$target，才有可能再上蜀山'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''E(20901,2006)'''
#导表结束