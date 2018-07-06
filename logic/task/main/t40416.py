# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·情报'''
	intro = '''$target匆匆赶来，莫非他们已经找到#C02温玉#n的下落？'''
	detail = '''$target匆匆赶来，莫非他们已经找到#C02温玉#n的下落？'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2030,E(2030,2039)'''
#导表结束