# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第三章·灾祸'''
	intro = '''赶到武林盟营地时，满地尸骸，$target坐在中央'''
	detail = '''赶到武林盟营地时，满地尸骸，$target坐在中央'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N2051,NI2052,NI2053,NI2054,NI2055,E(2051,2067),E(2052,2068),E(2053,2069),E(2054,2069),E(2055,2069)'''
#导表结束