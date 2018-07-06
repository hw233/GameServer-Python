# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5720
	name = "加速"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 99
	bout = 3
	readyBout = 1
	frozenBout = 4
	buffId = 907
#导表结束
