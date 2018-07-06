# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5119 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6403
	name = "吸血"
	configInfo = {
		"生命":40,
	}
#导表结束