# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·布阵'''
	intro = '''看一下$target布阵布得如何'''
	detail = '''看一下$target布阵布得如何'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1022,NI1023,E(1022,1064),E(1023,1065)'''
#导表结束