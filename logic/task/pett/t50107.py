# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''句芒·魔女'''
	intro = '''明修罗离去，击败拦阻的红花姥姥'''
	detail = '''打败明修罗后，你正想追上去，却被红花姥姥拦住。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1023,E(1023,1065)'''
#导表结束