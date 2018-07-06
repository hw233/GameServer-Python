# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import BuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5717
	name = "强攻"
	targetType = PERFORM_TARGET_FRIEND
	targetCount = 99
	bout = 2
	readyBout = 2
	frozenBout = 4
	buffId = 905
#导表结束