# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''句芒·塔中'''
	intro = '''进入锁妖塔找到句芒'''
	detail = '''进入锁妖塔，找到句芒，却发现句芒失去意识，打算攻击你。看来只能先制服她了。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1021,E(1021,1062)'''
#导表结束