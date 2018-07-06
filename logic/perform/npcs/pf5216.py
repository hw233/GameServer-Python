# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5116 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5216
	name = "高级杀戮"
	configInfo = {
		"伤害":80,
	}
#导表结束