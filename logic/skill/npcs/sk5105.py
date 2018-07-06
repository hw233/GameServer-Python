# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5105
	name = "重甲"
	performList = (5105,)
	score = 60
	applyList = {
		"phyDef":lambda LV:LV*0.8,
	}
#导表结束
