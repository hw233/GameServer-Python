# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "金光乍现"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"物理伤害结果加成":lambda HPR:100+(100-HPR)/5*10,
		"法术伤害结果加成":lambda HPR:100+(100-HPR)/5*10,
	}
#导表结束