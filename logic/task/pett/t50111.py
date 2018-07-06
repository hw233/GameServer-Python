# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''阎王蝎·怪事'''
	intro = '''从仙子那了解云顶村的怪事'''
	detail = '''仙子说最近云顶村发生不少怪事，请你去看看到底是什么原因。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1068)'''
#导表结束