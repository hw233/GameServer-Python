# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6402
	name = "法术减伤"
	buffId = 507
	applyList = {
		"被法术伤害结果加成":-50,
	}
#导表结束