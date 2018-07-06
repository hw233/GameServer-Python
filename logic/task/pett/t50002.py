# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''玄武龟·援手'''
	intro = '''与仙子交谈后，前往碧凝崖'''
	detail = '''从仙子那得知玄武龟有难，前往碧凝崖寻找玄武龟，对付魔道。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1003)'''
#导表结束