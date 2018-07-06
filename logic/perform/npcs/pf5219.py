# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5119 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5219
	name = "高级吸血"
	configInfo = {
		"生命":30,
	}
#导表结束