# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "沾衣欲湿"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"法术伤害结果加成":-10,
		"治疗结果加成":-10,
	}
	replacable = False
#导表结束