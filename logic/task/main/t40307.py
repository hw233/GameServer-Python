# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第二章·路遇'''
	intro = '''跟着金蝉四处游乐时，巧遇$target'''
	detail = '''跟着金蝉四处游乐时，巧遇$target'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1513,E(1513,1521)'''
#导表结束