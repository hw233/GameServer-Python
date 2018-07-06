# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40201
	targetType = TASK_TARGET_TYPE_NPC
	icon = 0
	title = '''第一章·拜师'''
	intro = '''醉道人的话提醒了你，回去找$target学艺'''
	detail = '''醉道人的话提醒了你，回去找$target学艺'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''STORY40008,B(1004,school)'''
#导表结束