# -*- coding: utf-8 -*-
from skill.object import EquipSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 3603
	name = "绕指柔"
	performList = (3603,)
	score = 30
	applyList = {
		"phyReCrit":1,
		"magReCrit":1,
	}
#导表结束
