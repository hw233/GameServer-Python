# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第二章·态度'''
	intro = '''$target在路上，难道他已经成了敌人？'''
	detail = '''$target在路上，难道他已经成了敌人？'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2010,E(2010,2013)'''
#导表结束