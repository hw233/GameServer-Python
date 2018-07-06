# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''阎王蝎·原因'''
	intro = '''与阎王蝎交谈，问出原因'''
	detail = '''和阎王蝎交谈，问出阎王蝎要吃人的原因。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1025,E(1025,1072)'''
#导表结束