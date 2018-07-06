# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5104
	name = "天机"
	performList = (5104,)
	score = 60
	applyList = {
		"magDam":lambda LV:LV*0.6,
	}
#导表结束
