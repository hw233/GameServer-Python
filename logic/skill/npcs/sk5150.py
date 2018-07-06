# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5150
	name = "缠身"
	performList = (5150,)
	score = 60
	applyList = {
		"speRatio":-20,
	}
#导表结束
