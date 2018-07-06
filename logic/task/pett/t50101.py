# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''句芒·反常'''
	intro = '''$target请你前往苗疆'''
	detail = '''天气反常，春天不到，仙子请你前往苗疆找寻苗疆大族长，询问可能的原因。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1059)'''
#导表结束