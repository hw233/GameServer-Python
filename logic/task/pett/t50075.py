# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''金鹏·圣女'''
	intro = '''准备离开时，被明珠拦住'''
	detail = '''准备离开锁妖塔，被血神教圣女明珠拦住，让你交出身上灵药。击败拦路的明珠。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1013,E(1013,1044)'''
#导表结束