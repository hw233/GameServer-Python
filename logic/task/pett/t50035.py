# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''灵猴·除妖'''
	intro = '''前往城西恶徒藏身处，为民除害'''
	detail = '''跟随灵猴前往恶徒藏身之所，灭掉作恶多端的恶徒。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1005,E(1005,1019)'''
#导表结束