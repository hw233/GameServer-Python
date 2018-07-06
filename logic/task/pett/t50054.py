# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 2
	title = '''云狐·寻药'''
	intro = '''看到云狐有伤，给它找来药物'''
	detail = '''云狐完全听不进任何劝告，只能先给它找来治伤的药物。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1008,L(221101,1),E(1008,1030)'''
#导表结束