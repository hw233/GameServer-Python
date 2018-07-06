# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·抉择'''
	intro = '''旁门者们在求饶，但$target似乎并不想放过他们'''
	detail = '''旁门者们在求饶，但$target似乎并不想放过他们'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2029,NI2028,NI2027,E(2029,2035),E(2028,2036),E(2027,2037)'''
#导表结束