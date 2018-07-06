# -*- coding: utf-8 -*-
from task.defines import *
from task.guildt.t30201 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30201
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 0
	title = '''仙盟-采购物资'''
	intro = '''找个$props来(拥有$process)'''
	detail = '''近日仙盟物资不足，你去采购一些$props回来。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''B(1001,lv),E(101,1002)'''
#导表结束
