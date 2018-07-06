# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·阴素棠'''
	intro = '''剑光一闪，突然散修$target从天而降'''
	detail = '''剑光一闪，突然散修$target从天而降'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2012,NI2013,NI2014,E(2012,2017),E(2013,2018),E(2014,2019)'''
#导表结束