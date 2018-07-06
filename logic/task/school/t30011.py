# -*- coding: utf-8 -*-
from task.defines import *
from task.school.t30001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''师门-清除叛徒'''
	intro = '''背叛师门的$target被发现行踪，前往消灭他'''
	detail = '''$target曾作出欺师灭祖的事情来，这些年一直在躲藏，如今有人发现他的踪迹，速去清理门户。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''B(1008,school)'''
#导表结束