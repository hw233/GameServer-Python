# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5250
	name = "高级缠身"
	performList = (5250,)
	score = 120
	applyList = {
		"speRatio":-30,
	}
#导表结束
