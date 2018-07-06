# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf6203 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6204
	name = "护卫何在"
	targetType = PERFORM_TARGET_FRIEND
	configInfo = {
		"战斗编号":2002,
	}
#导表结束
