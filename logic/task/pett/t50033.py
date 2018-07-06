# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''灵猴·比试'''
	intro = '''灵猴不听劝告，反而要和你比试'''
	detail = '''劝告灵猴后，它不愿回去，反而提出要与你比试。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1004,E(1004,1017)'''
#导表结束