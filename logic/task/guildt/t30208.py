# -*- coding: utf-8 -*-
from task.defines import *
from task.guildt.t30201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30201
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 0
	title = '''仙盟-采购物资'''
	intro = '''找个$props来(拥有$process)，上交高于$quality品质，可以获得额外经验奖励'''
	detail = '''近日仙盟物资缺乏，急需$props为用（高于$quality品质则可获得额外奖励），请速去寻找！'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''B(1002,lv),E(101,1008),QU30'''
#导表结束