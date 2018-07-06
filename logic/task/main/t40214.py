# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·生变'''
	intro = '''齐金蝉在前面呆呆站着，发生什么事？'''
	detail = '''齐金蝉在前面呆呆站着，发生什么事？'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1014,NI1015,E(1014,1052),E(1015,1053)'''
#导表结束