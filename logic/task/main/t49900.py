# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NONE
	icon = 0
	title = '''角色升级'''
	intro = '''达到$level级开启新剧情'''
	detail = '''达到$level级开启新剧情'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = ''''''
#导表结束