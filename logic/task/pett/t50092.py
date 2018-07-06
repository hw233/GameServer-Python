# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''毕方·探问'''
	intro = '''找到毕方，询问原因'''
	detail = '''找到在凌云大佛下潜修的毕方，询问羽毛和修为损耗的原因。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1016,E(1016,1051)'''
#导表结束