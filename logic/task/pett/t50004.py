# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''玄武龟·结伴'''
	intro = '''向异兽仙子回禀情况'''
	detail = '''除去了意图擒抓玄武龟的魔道，向异兽仙子回禀情况。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1005)'''
#导表结束