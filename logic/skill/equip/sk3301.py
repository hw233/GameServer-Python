# -*- coding: utf-8 -*-
from skill.object import EquipSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 3301
	name = "舍身"
	performList = (3301,)
	score = 30
	applyList = {
		"phyDamRatio":3,
		"magDamRatio":3,
		"phyDefRatio":-2,
		"magDefRatio":-2,
	}
#导表结束
