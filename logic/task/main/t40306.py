# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·金蝉'''
	intro = '''回碧筠庵回报时，途遇$target'''
	detail = '''回碧筠庵回报时，途遇$target'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1511,NI1512,E(1511,1519),E(1512,1520)'''
#导表结束