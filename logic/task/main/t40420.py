# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·质问'''
	intro = '''$target满腔怒火质问事情真相，该如何回答？'''
	detail = '''$target满腔怒火质问事情真相，该如何回答？'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2041,NI2035,NI2036,NI2037,NI2038,NI2039,NI2040,E(2041,2048),E(2035,2049),E(2036,2050),E(2037,2051),E(2040,2052),E(2038,2047),E(2039,2047)'''
#导表结束