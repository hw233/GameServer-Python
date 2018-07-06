# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5204
	name = "高级天机"
	performList = (5204,)
	score = 120
	applyList = {
		"magDam":lambda LV:LV,
	}
#导表结束
