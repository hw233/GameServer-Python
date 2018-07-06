# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''句芒·失却'''
	intro = '''返回与句芒对话'''
	detail = '''击败红花姥姥后，发现修罗宫的人都已离开，只能返回寻找句芒。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1024,E(1024,1066)'''
#导表结束