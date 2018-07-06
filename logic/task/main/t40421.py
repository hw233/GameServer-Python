# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第三章·谷辰'''
	intro = '''一声厉啸，$target站了起来#C04（建议组队）#n'''
	detail = '''一声厉啸，$target站了起来#C04（建议组队）#n'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2042,NI2036,NI2037,NI2038,NI2039,NI2040,E(2042,2053),E(2036,2055),E(2037,2056),E(2040,2057),E(2038,2047),E(2039,2047)'''
#导表结束