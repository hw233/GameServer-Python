# -*- coding: utf-8 -*-
from perform.defines import *
from perform.object import Perform as CustomPerform

#导表开始
class Perform(CustomPerform):
	id = 6105
	name = "宠物攻法"
	applyList = {
		"物理伤害结果加成":lambda SLV:(2*SLV),
		"法术伤害结果加成":lambda SLV:(2*SLV),
		"治疗结果加成":lambda SLV:(2*SLV),
		"封印命中":lambda SLV:2*SLV,
	}
#导表结束