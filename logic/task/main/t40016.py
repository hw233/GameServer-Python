# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·回报'''
	intro = '''向$target汇报醉汉的事'''
	detail = '''向$target汇报醉汉的事'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N1013,E(1013,1019)'''
#导表结束