# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·下山'''
	intro = '''转眼间已过三月，今天师父有事寻你'''
	detail = '''转眼间已过三月，今天师父有事寻你'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''B(1005,school)'''
#导表结束