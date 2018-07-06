# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''金鹏·缘故'''
	intro = '''询问明珠需要灵药的原因'''
	detail = '''明珠的样子很着急，询问她为何需要灵药。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1013,E(1013,1045)'''
#导表结束