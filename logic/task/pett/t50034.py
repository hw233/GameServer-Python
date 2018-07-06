# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''灵猴·交谈'''
	intro = '''打败灵猴后，询问为何出手'''
	detail = '''打败灵猴后，得知原来是慈云寺恶徒盘踞城西为害，灵猴无法除掉，所以想一试你身手，一同前往除恶。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1004,E(1004,1018)'''
#导表结束