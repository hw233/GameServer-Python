# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''毕方·听闻'''
	intro = '''与唐百草闲聊，探问羽衣来由'''
	detail = '''毕方不肯说出缘故，但仙子发现唐百草处出售毕方羽毛制成的羽衣，与她闲聊探听来历。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10204,1053)'''
#导表结束