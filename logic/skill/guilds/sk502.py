# -*- coding: utf-8 -*-
from skill.object import GuildSkill as CustomSkill

#导表开始
class Skill(CustomSkill):
	id = 502
	name = "冥想"
	applyList = {
		"mpMax":lambda SLV:SLV*10,
	}
#导表结束
