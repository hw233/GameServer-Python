# -*- coding: utf-8 -*-
from task.defines import *
from task.school.t30001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 30001
	targetType = TASK_TARGET_TYPE_ITEM
	icon = 0
	title = '''师门-寻找物品'''
	intro = '''去帮师父找个$props来(拥有$process)'''
	detail = '''师父准备闭关炼药，急需$props作为药引，才能修炼丹药，请尽快找回来。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''B(1001,lv),E(master,1004)'''
#导表结束