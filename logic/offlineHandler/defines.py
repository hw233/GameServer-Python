# -*- coding: utf-8 -*-

#===============================================================================
# 离线处理函数
#===============================================================================

def guildAddMember(who, **kwargs):
	guildId = kwargs["guildId"]
	who.setGuildId(guildId)

def guildRemoveMember(who, **kwargs):
	who.setGuildId(0)

def guildTitle(who, **kwargs):
	titleNo = kwargs.get("titleNo")
	if not titleNo:
		return
	isClear = kwargs.get("isClear")
	if isClear:
		title.removeTitle(who, titleNo)
		return
	title.newTitle(who, titleNo)

def addBetFlowerPoint(who, **kwargs):
	point = kwargs.get("point", 0)
	launch.launchBySpecify(who, 200010, point, False, "上线加献花")

def finalExamReward(who, **kwargs):
	answer.finalExam.finalExamOfflineReward(who, **kwargs)

def schoolFightTitle(who, **kwargs):
	titleNo = kwargs["titleNo"]
	title.newTitle(who, titleNo)

def listenerRaceAchv(who, **kwargs):
	rank = kwargs.get("rank", 0)
	if rank:
		import listener
		listener.doListen("竞技场排名", who, rank=rank)

gHandlerList = {
	"guildAddMember": guildAddMember,
	"guildRemoveMember": guildRemoveMember,
	"guildTitle": guildTitle,

	"addBetFlowerPoint": addBetFlowerPoint,#加献花积分
	"finalExamReward": finalExamReward,#殿试奖励

	"schoolFightTile": schoolFightTitle,#门派试炼称谓

	"listenerRaceAchv": listenerRaceAchv,#竞技积分成就
}

import launch
import answer.finalExam
import title
