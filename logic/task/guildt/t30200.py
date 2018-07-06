# -*- coding: utf-8 -*-
from task.defines import *
from task.guildt.t30201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''仙盟任务指引'''
	intro = '''仙盟总管正在找你'''
	detail = '''听闻仙盟总管正在找你，赶快前去。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = ''''''
#导表结束