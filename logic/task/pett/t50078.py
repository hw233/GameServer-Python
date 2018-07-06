# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''金鹏·发怒'''
	intro = '''打败发怒的谜独行'''
	detail = '''怪妖谜独行勃然大怒，打败谜独行。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1014,E(1014,1047)'''
#导表结束