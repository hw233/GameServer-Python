# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''句芒·回禀'''
	intro = '''带句芒去见仙子'''
	detail = '''失却法器的句芒只能长驻人间，带句芒去见仙子，看仙子如何安排句芒吧。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1067)'''
#导表结束