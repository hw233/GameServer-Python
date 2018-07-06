# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''金鹏·受伤'''
	intro = '''$target请你前去蜀山'''
	detail = '''异兽金鹏受伤多时还不见好转，仙子请你寻找蜀山掌门齐漱溟，求取医治之法。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''E(10208,1040)'''
#导表结束