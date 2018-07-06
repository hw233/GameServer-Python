# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "花毒致死"
	type = BUFF_TYPE_DEBUFF
	applyList = {
		"被治疗结果加成":-50,
	}
#导表结束