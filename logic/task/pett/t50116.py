# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''阎王蝎·斩妖'''
	intro = '''除去霸占蝎子洞府的毒尸'''
	detail = '''替蝎子们除去霸占洞府的毒尸。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1026,E(1026,1073)'''
#导表结束