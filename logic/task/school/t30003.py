# -*- coding: utf-8 -*-
from task.defines import *
from task.school.t30001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30001
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 0
	title = '''师门-寻找物品'''
	intro = '''去帮师父找个$props来(拥有$process)，上交高于$quality品质，可以获得额外经验奖励'''
	detail = '''师父准备斩妖除魔，急需$props（高于$quality品质），带上战场，快去准备！'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''B(1002,lv),E(master,1003),QU30'''
#导表结束
