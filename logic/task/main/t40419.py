# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·入火云洞'''
	intro = '''由二矮带路，火云洞就在前方，$target果然回死未醒'''
	detail = '''由二矮带路，火云洞就在前方，$target果然回死未醒'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2035,NI2036,NI2037,NI2038,NI2039,E(2035,2044),E(2036,2045),E(2037,2046),E(2038,2047),E(2039,2047)'''
#导表结束