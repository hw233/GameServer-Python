# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·顽石'''
	intro = '''玉匣中空无一物，回报$target'''
	detail = '''玉匣中空无一物，回报$target'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1552,NI1551,E(1552,1573),E(1551,1569)'''
#导表结束