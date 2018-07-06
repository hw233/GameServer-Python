# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·妙一真人'''
	intro = '''远方五色祥云涌现，$target御剑飞行，落在了不远处'''
	detail = '''远方五色祥云涌现，$target御剑飞行，落在了不远处'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1553,NI1552,NI1551,E(1553,1574),E(1552,1575),E(1551,1569)'''
#导表结束