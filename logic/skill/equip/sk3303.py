# -*- coding: utf-8 -*-
from skill.object import EquipSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 3303
	name = "霜剑"
	performList = (3303,)
	score = 30
	applyList = {
		"magCrit":1,
	}
#导表结束
