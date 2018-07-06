# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5707
	name = "无敌"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 99
	bout = 1
	readyBout = 2
	frozenBout = 4
	buffId = 901
#导表结束