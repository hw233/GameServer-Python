# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''金鹏·取药'''
	intro = '''与取得灵药的明珠对话'''
	detail = '''打败谜独行后，与取得灵药的明珠对话。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1015,E(1015,1048)'''
#导表结束