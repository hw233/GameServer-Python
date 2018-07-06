# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5129 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5229
	name = "高级逆境"
	configInfo = {
		"伤害加成":5,
		"次数限制":3,
	}
#导表结束