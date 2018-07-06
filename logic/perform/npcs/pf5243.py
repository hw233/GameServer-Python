# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5143 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5243
	name = "高级怒火"
	configInfo = {
		"愤怒":25,
	}
#导表结束