# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·救星'''
	intro = '''实力太悬殊了，与$target陷入了危难之中'''
	detail = '''实力太悬殊了，与$target陷入了危难之中'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1530,E(1530,1543)'''
#导表结束