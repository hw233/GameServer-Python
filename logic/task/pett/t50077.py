# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''金鹏·返回'''
	intro = '''回去找谜独行，试图再取灵药'''
	detail = '''为了明珠回去再找谜独行，看看能否从他那再取得一份灵药。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1014,E(1014,1046)'''
#导表结束