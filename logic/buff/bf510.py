# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "武林盟弟子"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"物理伤害结果加成":10,
	}
#导表结束