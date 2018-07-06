# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第三章·决战妖尸'''
	intro = '''火云洞中，$target正在中央端坐#C04（建议组队）#n'''
	detail = '''火云洞中，$target正在中央端坐#C04（建议组队）#n'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2058,NI2038,NI2039,E(2058,2077),E(2038,2076),E(2039,2076)'''
#导表结束