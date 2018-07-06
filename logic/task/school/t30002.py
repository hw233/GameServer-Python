# -*- coding: utf-8 -*-
from task.defines import *
from task.school.t30001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30001
	targetType = TASK_TARGET_TYPE_FIGHT
	icon = 1
	title = '''师门-收集物品'''
	intro = '''去$scene收集$props'''
	detail = '''师门$props消耗过大，去$scene收集一些。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''L(9003,1),ANLEI(1001,1002,9004)'''
#导表结束