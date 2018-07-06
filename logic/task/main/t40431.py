# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·回天'''
	intro = '''快把温玉放在$target胸口'''
	detail = '''快把温玉放在$target胸口'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2060,E(2060,2081)'''
#导表结束