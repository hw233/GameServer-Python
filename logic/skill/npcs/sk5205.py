# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5205
	name = "高级重甲"
	performList = (5205,)
	score = 120
	applyList = {
		"phyDef":lambda LV:LV*1.2,
	}
#导表结束
