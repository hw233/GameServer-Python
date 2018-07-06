# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5821 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5861
	name = "高级抗封"
	configInfo = {
		"抵抗封印":5,
	}
#导表结束