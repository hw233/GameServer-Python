# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "水之庇佑"
	type = BUFF_TYPE_SPECIAL
	applyList = {
		"被法术伤害结果加成":-50,
	}
#导表结束