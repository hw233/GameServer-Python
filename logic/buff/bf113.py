# -*- coding: utf-8 -*-
from buff.defines import *
from buff.object import Buff as CustomBuff

#导表开始
class Buff(CustomBuff):
	name = "金蚕宝甲"
	type = BUFF_TYPE_BUFF
	applyList = {
		"被群体法术伤害结果加成":-20,
	}
#导表结束