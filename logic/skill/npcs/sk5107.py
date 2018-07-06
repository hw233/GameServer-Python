# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5107
	name = "蹈风"
	performList = (5107,)
	score = 60
	applyList = {
		"spe":lambda LV:LV*0.6,
	}
#导表结束
