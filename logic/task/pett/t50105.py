# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''句芒·清醒'''
	intro = '''与清醒的句芒交谈'''
	detail = '''句芒终于清醒了过来，问问句芒发生了什么事。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1021,E(1021,1063)'''
#导表结束