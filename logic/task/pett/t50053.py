# -*- coding: utf-8 -*-
from task.defines import *
from task.pett.t50001 import Task as customTask

#导表开始
class Task(customTask):
	parentId = 50001
	targetType = TASK_TARGET_TYPE_NPC
	icon = 2
	title = '''云狐·劝慰'''
	intro = '''打败云狐后，再试着与它对话'''
	detail = '''从云狐的话里得知它父母被人类杀害了，试着与云狐对话，安慰一下它。'''
	rewardDesc = ''''''
	goAheadScript = ''''''
	initScript = '''N1008,E(1008,1029)'''
#导表结束