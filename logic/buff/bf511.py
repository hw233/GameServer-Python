# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "苗疆弟子"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"封印命中":10,
	}
#导表结束