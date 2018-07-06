# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·六大门派'''
	intro = '''$target决定正式向慈云寺出发'''
	detail = '''$target决定正式向慈云寺出发'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1509,NI1507,NI1508,E(1509,1544),E(1507,1545),E(1508,1546)'''
#导表结束