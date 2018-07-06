# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''灵猴·回归'''
	intro = '''恶徒已除，回去向仙子汇报'''
	detail = '''除掉了盘踞城西的恶徒，与灵猴一道回去向异兽仙子禀报吧。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1020)'''
#导表结束