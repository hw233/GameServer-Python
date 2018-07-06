# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5102
	name = "灵犀"
	performList = (5102,)
	score = 90
	applyList = {
		"magCrit":10,
	}
#导表结束