# -*- coding: utf-8 -*-
from task.defines import *
from task.guildt.t30201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''仙盟-惩治恶人'''
	intro = '''前往惩治作恶的$target'''
	detail = '''$target又在作恶，我等不能坐视不管。你去惩治$target吧。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''NE(9003,1006)'''
#导表结束