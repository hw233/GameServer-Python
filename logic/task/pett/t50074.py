# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''金鹏·谜语'''
	intro = '''解开谜独行的谜语'''
	detail = '''用激将法引得谜独行上当，破解谜独行的谜语。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1012,E(1012,1043)'''
#导表结束