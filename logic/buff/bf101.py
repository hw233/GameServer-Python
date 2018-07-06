# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "纯阳心法"
	type = BUFF_TYPE_BUFF
	applyList = {
		"物理伤害加成":10,
	}
#导表结束