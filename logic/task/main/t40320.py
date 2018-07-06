# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·陷阱'''
	intro = '''扫荡剩余妖人之时，一直失踪的$target突然出现'''
	detail = '''扫荡剩余妖人之时，一直失踪的$target突然出现'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1549,E(1549,1567)'''
#导表结束