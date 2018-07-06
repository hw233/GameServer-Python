# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''灵猴·劝说'''
	intro = '''找到灵猴，劝它回去'''
	detail = '''果然如仙子所说，找到了在城西的灵猴，劝它回去吧。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1004,E(1004,1016)'''
#导表结束