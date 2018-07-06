# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5207
	name = "高级蹈风"
	performList = (5207,)
	score = 120
	applyList = {
		"spe":lambda LV:LV,
	}
#导表结束
