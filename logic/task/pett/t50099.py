# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''毕方·侥幸'''
	intro = '''战胜鸠盘婆分神后，回报仙子'''
	detail = '''战胜了鸠盘婆的分神，告诉毕方关于唐百草的回复后，赶快回去告知仙子。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1058)'''
#导表结束