# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6401
	name = "物理减伤"
	buffId = 506
	applyList = {
		"被物理伤害结果加成":-50,
	}
#导表结束