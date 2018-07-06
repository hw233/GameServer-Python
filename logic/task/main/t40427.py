# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第三章·旧友新敌'''
	intro = '''来到火云洞前，只见$target与司徒雷连诀而来'''
	detail = '''来到火云洞前，只见$target与司徒雷连诀而来'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2056,NI2057,NI2038,NI2039,E(2056,2070),E(2057,2075),E(2038,2076),E(2039,2076)'''
#导表结束