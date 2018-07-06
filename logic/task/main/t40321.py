# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第二章·血神之战'''
	intro = '''碧筠庵处，恰逢$target出来，与他决斗吧！#C04（建议组队）#n'''
	detail = '''碧筠庵处，恰逢$target出来，与他决斗吧！#C04（建议组队）#n'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1550,NI1551,NI1552,E(1550,1568),E(1551,1569),E(1552,1570)'''
#导表结束