# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·际遇'''
	intro = '''远远看见$target，在旁偷听一下吧'''
	detail = '''远远看见$target，在旁偷听一下吧'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2018,E(2018,2031)'''
#导表结束