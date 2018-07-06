# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·抉择'''
	intro = '''闯进去救人，就可能导致妖蛇逃跑，怎么办好？'''
	detail = '''闯进去救人，就可能导致妖蛇逃跑，怎么办好？'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1025,E(1025,1068)'''
#导表结束