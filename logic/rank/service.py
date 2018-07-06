# -*- coding: utf-8 -*-
import endPoint
import rank_pb2

class cService(rank_pb2.terminal2main):

	@endPoint.result
	def rpcRankRequest(self, ep, who, reqMsg): return rpcRankRequest(who, reqMsg)
	
	@endPoint.result
	def rpcRankQuit(self, ep, who, reqMsg): return rpcRankQuit(who, reqMsg)

	@endPoint.result
	def rpcRankLookInfo(self, ep, who, reqMsg): return rpcRankLookInfo(who, reqMsg)
	

def packetRankInfo(who, rankObj, iUid):
	msg = rank_pb2.rankInfo()
	msg.iRank = rankObj.getRank(iUid)
	msg.sTitle2 = str(rankObj.title2(iUid))
	msg.sTitle3 = str(rankObj.title3(iUid))
	msg.sTitle4 = str(rankObj.title4(iUid))
	msg.iUid = iUid
	return msg

def packetMyInfo(who, iRankNo, tMyInfo):
	msg = rank_pb2.rankInfo()

	dRankQuit = who.fetch("rankQuit", {})
	if dRankQuit.get(iRankNo, 0) == 0:	#上榜
		msg.iRank = tMyInfo[0]
	else:	#离榜
		msg.iRank = -1
	msg.sTitle2 = str(tMyInfo[1])
	msg.sTitle3 = str(tMyInfo[2])
	msg.sTitle4 = str(tMyInfo[3])
	msg.iUid = 0
	return msg

def rpcRankRequest(who, reqMsg):
	'''查看排行榜
	'''
	if who.level < 20:
		message.tips(who, "#C04{}级#n开启本系统".format(20))
		return

	iRankNo = reqMsg.iRankNo
	rankObj = rank.getRankObjBySubNo(iRankNo)
	iPage = reqMsg.iPage
	iStart = (iPage-1)*20
	iEnd = min(100, iPage*20)
	lRank = rankObj.ranking()[iStart:iEnd]
	dRankQuit = who.fetch("rankQuit", {})

	msg = rank_pb2.rankList()
	msg.iRankNo = iRankNo
	msg.iPage = iPage
	msg.iQuitFlag = dRankQuit.get(iRankNo, 0)
	msg.lRank.extend([packetRankInfo(who, rankObj, iUid) for iUid in lRank])
	
	tMyInfo = rankObj.getMyRankInfo(who)
	if tMyInfo:
		msg.iShowMyRank = 1
		msg.myRankInfo.CopyFrom(packetMyInfo(who, iRankNo, tMyInfo))
	else:#榜外
		msg.iShowMyRank = 0

	who.endPoint.rpcRankInfo(msg)

def rpcRankQuit(who, reqMsg):
	'''退榜
	'''
	iRankNo = reqMsg.iRankNo
	iQuitFlag = reqMsg.iQuitFlag 
	rankObj = rank.getRankObjBySubNo(iRankNo)
	if not rankObj.canQuit():#不能加退榜
		message.tips(who, "本排行榜不能退榜")
		return

	dRankQuit = who.fetch("rankQuit", {})
	dRankQuit[iRankNo] = iQuitFlag
	who.set("rankQuit", dRankQuit)

	if iQuitFlag == 0:	#加入榜
		rankObj.addRank(who)
	else:	#退榜
		rankObj.quitRank(who)

	#回复
	msg = rank_pb2.quitRank()
	msg.iRankNo = iRankNo
	msg.iQuitFlag = dRankQuit.get(iRankNo, 0)
	who.endPoint.rpcRankQuitResponse(msg)

def rpcRankLookInfo(who, reqMsg):
	iRankNo = reqMsg.iRankNo
	rankObj = rank.getRankObjBySubNo(iRankNo)
	iUid = reqMsg.iUid
	iRoldId = rankObj.getRoleId(iUid)
	other = getRole(iRoldId)
	if not other:
		message.tips(who, "玩家不在线无法查看")
		return
	rankObj.lookInfo(who, other, iUid)


def rpcLookOtherRoleScore(who, other):
	'''查看其它玩家评分
	'''
	msg = rank_pb2.roleScoreInfo()
	msg.iRoleId = other.id
	msg.sRoleName = other.name
	msg.iSchool = other.school

	iRoleScore = other.fetch("highestScore", other.fightPower)
	msg.iRoleScore = iRoleScore	#历史最高分
	iPetScore = rank.rankPetHighestScore(other)
	msg.iPetScore = iPetScore	#历史最高分
	msg.iTotalScore = iRoleScore+iPetScore
	
	msg.iShape = other.shape
	msg.shapeParts.extend(other.shapeParts)
	msg.colors.extend(other.getColors())
	who.endPoint.rpcRankLookRoleInfo(msg)


import c
from common import *
import message
import rank