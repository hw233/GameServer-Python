# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·逃脱'''
	intro = '''回到碧筠庵时，$target等正怒气冲冲地等着我们'''
	detail = '''回到碧筠庵时，$target等正怒气冲冲地等着我们'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1508,NI1507,NI1509,E(1508,1544),E(1507,1545),E(1509,1546)'''
#导表结束