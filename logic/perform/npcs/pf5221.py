# -*- coding: utf-8 -*-
from perform.defines import *
from perform.npcs.pf5121 import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 5221
	name = "高级无畏"
	applyList = {
		"免疫反弹":True,
	}
	configInfo = {
		"物理伤害结果加成":10,
	}
#导表结束