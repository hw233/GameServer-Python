# -*- coding: utf-8 -*-
from task.defines import *
from task.guildt.t30201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''仙盟-回复总管'''
	intro = '''回复仙盟总管'''
	detail = '''回复仙盟总管。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = ''''''
#导表结束
