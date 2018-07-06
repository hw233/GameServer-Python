# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''金鹏·怪妖'''
	intro = '''进入塔中，找到怪妖谜独行'''
	detail = '''进入锁妖塔，找到喜欢出谜语的怪妖谜独行，试图从他身上取得灵药。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1012,E(1012,1042)'''
#导表结束