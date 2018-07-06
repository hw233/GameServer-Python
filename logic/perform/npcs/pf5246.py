# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5146 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5246
	name = "高级丙火"
	configInfo = {
		"概率":30,
	}
#导表结束