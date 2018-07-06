# -*- coding: utf-8 -*-
from skill.object import EquipSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 3302
	name = "白刃"
	performList = (3302,)
	score = 30
	applyList = {
		"phyCrit":1,
	}
#导表结束
