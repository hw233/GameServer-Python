# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "花醉迷香"
	type = BUFF_TYPE_DEBUFF
	applyList = {
		"物理伤害结果加成":-15,
		"法术伤害结果加成":-15,
	}
#导表结束