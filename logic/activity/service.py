# -*- coding: utf-8 -*-
# 活动服务
import endPoint
import act_guaji_pb2
import act_center_pb2
import act_pk_pb2
import act_race_pb2
import act_escort_pb2
import act_guildFight_pb2
import act_treasure_pb2
import act_instance_pb2
import act_fairyland_pb2
import act_star_pb2
import act_teamRace_pb2

class cServiceGuaji(act_guaji_pb2.terminal2main):

	# @endPoint.result
	# def rpcActGuajiTrans(self, ep, who, reqMsg): return activity.guaji.rpcTrans(who, reqMsg)
	
	# @endPoint.result
	# def rpcActGuajiSetAutoFight(self, ep, who, reqMsg): return activity.guaji.rpcSetAutoFight(who, reqMsg)

	# @endPoint.result
	# def rpcActGuajiGetTask(self, ep, who, reqMsg): return activity.guaji.rpcGetTask(who, reqMsg)

	# @endPoint.result
	# def rpcActGuajiMonsterCnt(self, ep, who, reqMsg): return activity.guaji.rpcMonsterCnt(who, reqMsg)

	@endPoint.result
	def rpcActGuajiGetConfig(self, ep, who, reqMsg): return activity.guaji.rpcGetConfig(who, reqMsg)

	@endPoint.result
	def rpcActGuajiSetConfig(self, ep, who, reqMsg): return activity.guaji.rpcSetConfig(who, reqMsg)


class cServiceCenter(act_center_pb2.terminal2main):

	@endPoint.result
	def rpcActCenterOpen(self, ep, who, reqMsg): return activity.center.rpcOpen(who, reqMsg)

	@endPoint.result
	def rpcActCenterJoin(self, ep, who, reqMsg): return activity.center.rpcJoin(who, reqMsg)

	@endPoint.result
	def rpcActCenterReward(self, ep, who, reqMsg): return activity.center.rpcReward(who, reqMsg)

	@endPoint.result
	def rpcActCenterGetDoublePoint(self, ep, who, reqMsg): return activity.center.rpcGetDoublePoint(who, reqMsg)

	@endPoint.result
	def rpcActCenterGetJumeData(self, ep, who, reqMsg): return activity.center.rpcGetJumeData(who, reqMsg)

class cServicePk(act_pk_pb2.terminal2main):

	@endPoint.result
	def rpcActPk(self, ep, who, reqMsg): return activity.pk.rpcPk(who, reqMsg)


class cServiceRace(act_race_pb2.terminal2main):
	'''竞技场服务
	'''

	@endPoint.result
	def rpcRaceRankGet(self, ep, who, reqMsg): return activity.race.rpcRaceRankGet(who, reqMsg)
	
	@endPoint.result
	def rpcRaceQuit(self, ep, who, reqMsg): return activity.race.rpcRaceQuit(who, reqMsg)
	
	@endPoint.result
	def rpcRaceMatchStart(self, ep, who, reqMsg): return activity.race.rpcRaceMatchStart(who, reqMsg)
	
	@endPoint.result
	def rpcRaceMatchStop(self, ep, who, reqMsg): return activity.race.rpcRaceMatchStop(who, reqMsg)


class cServiceTeamRace(act_teamRace_pb2.terminal2main):
	'''组队竞技场服务
	'''
	@endPoint.result
	def rpcTeamRaceQuit(self, ep, who, reqMsg): return activity.teamRace.rpcTeamRaceQuit(who, reqMsg)

	@endPoint.result
	def rpcTeamRaceRankGet(self, ep, who, reqMsg): return activity.teamRace.rpcTeamRaceRankGet(who, reqMsg)

class cServiceEscort(act_escort_pb2.terminal2main):
	@endPoint.result
	def rpcEscortAbort(self, ep, who, reqMsg): return activity.escort.rpcEscortAbort(who, reqMsg)

	@endPoint.result
	def rpcEscortQuest(self, ep, who, reqMsg): return activity.escort.rpcEscortQuest(who, reqMsg)

	@endPoint.result
	def rpcEscortQuestGoAhead(self, ep, who, reqMsg): return activity.escort.rpcEscortQuestGoAhead(who, reqMsg)


class cServiceGuildFight(act_guildFight_pb2.terminal2main):
	'''仙盟大战服务
	'''

	@endPoint.result
	def rpcActGuildFightTeamRequest(self, ep, who, reqMsg): return activity.guildFight.rpcActGuildFightTeamRequest(who, reqMsg)
	
	@endPoint.result
	def rpcActGuildFightQuitRequest(self, ep, who, reqMsg): return activity.guildFight.rpcActGuildFightQuitRequest(who, reqMsg)
	
	@endPoint.result
	def rpcActGuildFightResultRequest(self, ep, who, reqMsg): return activity.guildFight.rpcActGuildFightResultRequest(who, reqMsg)

	@endPoint.result
	def rpcActGuildFightPK(self, ep, who, reqMsg): return activity.guildFight.rpcActGuildFightPK(who, reqMsg)


class cServiceTreasure(act_treasure_pb2.terminal2main):
	'''探宝服务
	'''
	@endPoint.result
	def rpcTreasureQuit(self, ep, who, reqMsg): return activity.treasure.rpcTreasureQuit(who, reqMsg)

	@endPoint.result
	def rpcTreasureRankGet(self, ep, who, reqMsg): return activity.treasure.rpcTreasureRankGet(who, reqMsg)

	@endPoint.result
	def rpcTreasureCubeThrow(self, ep, who, reqMsg): return activity.treasure.rpcTreasureCubeThrow(who, reqMsg)

	@endPoint.result
	def rpcTreasureEffectDone(self, ep, who, reqMsg): return activity.treasure.rpcTreasureEffectDone(who, reqMsg)


class cServiceInstance(act_instance_pb2.terminal2main):
	@endPoint.result
	def rpcActInstanceEnter(self, ep, who, reqMsg): return activity.instance.rpcActInstanceEnter(who, reqMsg)
	


class cServiceFairylandFight(act_fairyland_pb2.terminal2main):
	'''幻境服务
	'''

	@endPoint.result
	def rpcFairylandEnter(self, ep, who, reqMsg): return activity.fairyland.rpcEnter(who, reqMsg)
	
	@endPoint.result
	def rpcFairylandQuit(self, ep, who, reqMsg): return activity.fairyland.rpcQuit(who, reqMsg)
	
	@endPoint.result
	def rpcFairylandStageGet(self, ep, who, reqMsg): return activity.fairyland.rpcStageGet(who, reqMsg)

	@endPoint.result
	def rpcFairylandStageFight(self, ep, who, reqMsg): return activity.fairyland.rpcStageFight(who, reqMsg)

	@endPoint.result
	def rpcFairylandPass(self, ep, who, reqMsg): return activity.fairyland.rpcPass(who, reqMsg)

	@endPoint.result
	def rpcFairylandTaskQuest(self, ep, who, reqMsg): return activity.fairyland.rpcTaskQuest(who, reqMsg)

	@endPoint.result
	def rpcFairylandBoxChoose(self, ep, who, reqMsg): return activity.fairyland.rpcBoxChoose(who, reqMsg)

class cServiceStar(act_star_pb2.terminal2main):
	'''杀星服务
	'''
	@endPoint.result
	def rpcStarSelectCancle(self, ep, who, reqMsg): return activity.star.rpcSelectCancle(who, reqMsg)

import activity.guaji
import activity.center
import activity.pk
import activity.race
import activity.escort
import activity.guildFight
import activity.treasure
import activity.instance
import activity.guildFight
import activity.fairyland
import activity.star