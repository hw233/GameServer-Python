# -*- coding: utf-8 -*-
from task.defines import *
from task.main.t40001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 40001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 1
	title = '''第二章·富贵剑'''
	intro = '''$target受了伤也不肯后退，不得已，击倒他！'''
	detail = '''$target受了伤也不肯后退，不得已，击倒他！'''
	rewardDesc = '''200001'''
	goAheadScript = ''''''
	initScript = '''N2009,E(2009,2012)'''
#导表结束