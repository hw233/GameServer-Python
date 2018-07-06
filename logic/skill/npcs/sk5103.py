# -*- coding: utf-8 -*-
from skill.object import NpcSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 5103
	name = "悍勇"
	performList = (5103,)
	score = 60
	applyList = {
		"phyDam":lambda LV:LV*0.6,
	}
#导表结束
