# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import DeBuffPerform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5709
	name = "魅惑"
	targetType = PERFORM_TARGET_ENEMY
	targetCount = 2
	bout = 1
	readyBout = 2
	frozenBout = 4
	buffId = 903
#导表结束