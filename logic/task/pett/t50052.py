# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''云狐·袭击'''
	intro = '''在城南遇到逃出的云狐，却被袭击'''
	detail = '''按仙子所说前往城南，果然遇到云狐。但云狐突然对你发起攻击。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1008,E(1008,1028)'''
#导表结束