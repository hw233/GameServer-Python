# -*- coding: utf-8 -*-
# 好友服务
import endPoint
import friend_pb2

class cService(friend_pb2.terminal2main):

	@endPoint.result
	def rpcFriendAddReq(self, ep, who, reqMsg): return rpcFriendAddReq(who,reqMsg)

	@endPoint.result
	def rpcFriendDelReq(self, ep, who, reqMsg): return rpcFriendDelReq(who,reqMsg)

	@endPoint.result
	def rpcFriendInfoReq(self, ep, who, reqMsg): return rpcFriendInfoReq(who,reqMsg)

	@endPoint.result
	def rpcFriendAddBlackReq(self, ep, who, reqMsg): return rpcFriendAddBlackReq(who,reqMsg)

	@endPoint.result
	def rpcFriendDelBlackReq(self, ep, who, reqMsg): return rpcFriendDelBlackReq(who,reqMsg)

	@endPoint.result
	def rpcFriendAddTeamReq(self, ep, who, reqMsg): return rpcFriendAddTeamReq(who,reqMsg)

	@endPoint.result
	def rpcFriendSetTeamSet(self, ep, who, reqMsg): return rpcFriendSetTeamSet(who,reqMsg)

	@endPoint.result
	def rpcFriendDelTeamReq(self, ep, who, reqMsg): return rpcFriendDelTeamReq(who,reqMsg)

	@endPoint.result
	def rpcFriendModReq(self, ep, who, reqMsg): return rpcFriendModReq(who,reqMsg)

	@endPoint.result
	def rpcFriendChatSend(self, ep, who, reqMsg): return rpcFriendChatSend(who,reqMsg)

	@endPoint.result
	def rpcFriendRecommendReq(self, ep, who, reqMsg): return rpcFriendRecommendReq(who,reqMsg)

	@endPoint.result
	def rpcFriendSearch(self, ep, who, reqMsg): return rpcFriendSearch(who,reqMsg)

	@endPoint.result
	def rpcFriendAddRecLinkManReq(self, ep, who, reqMsg): return rpcFriendAddRecLinkManReq(who,reqMsg)

def rpcFriendAddReq(who,reqMsg):
	'''添加好友
	'''
	iFriendId = reqMsg.iRoleId
	sMarkName = reqMsg.sMarkName
	iTeamNo = reqMsg.iTeamNo
	addFriend(who,iFriendId,sMarkName,iTeamNo)

def rpcFriendDelReq(who,reqMsg):
	'''删除好友
	'''
	iFriendId = reqMsg.iRoleId
	oFriend = who.friendCtn.getItem(iFriendId)
	if not oFriend:
		message.tips(who,"对方并不是你的好友")
		return
	who.friendCtn.removeItem(oFriend)
	message.tips(who,"删除成功，#C01{}#n不再是你的好友".format(oFriend.name))

def rpcFriendInfoReq(who,reqMsg):
	'''查看好友信息
	'''
	iFriendId = reqMsg.iRoleId
	oFriend = who.friendCtn.getFriend(iFriendId)  #有可能是查看最近联系人或者队友的
	if not oFriend:
		return
	who.endPoint.rpcFriendInfoSend(oFriend.getMsg(False))

def rpcFriendAddBlackReq(who,reqMsg):
	'''添加黑名单
	'''
	iBlackId = reqMsg.iRoleId
	bSameService = isSameService(iBlackId)
	if not checkBlackAdd(who, iBlackId):
		return
	if not bSameService:  #跨服的
		gevent.spawn(aboardBlackAdd,who.id, iBlackId)
		return

	resumeObj = resume.getResume(iBlackId) 
	if not resumeObj:  #不存在的角色
		return
	oBlack = friend.new(TYPE_BLACK,iBlackId)
	who.friendCtn.addItem(oBlack)
	mainService.getChatEP().rpcUpdateBlack(who.id,iBlackId,1)

def rpcFriendDelBlackReq(who,reqMsg):
	'''删除黑名单
	'''
	iBlackId = reqMsg.iRoleId
	oBlack = who.friendCtn.getItem(iBlackId)
	if not oBlack or not oBlack.isBlack():
		message.tips(who,"对方不在你的黑名单中")
		return
	who.friendCtn.removeItem(oBlack)
	mainService.getChatEP().rpcUpdateBlack(who.id,iBlackId,0)

def rpcFriendAddTeamReq(who,reqMsg):
	sName = reqMsg.sName
	if who.friendCtn.isFullTeam():
		return
	if not checkName(sName):
		return
	lFriendId = []
	for iFriendId in reqMsg.roleIdList:
		lFriendId.append(iFriendId)
	if len(lFriendId) > 100:
		message.tips(who, "自定义分组人数已达上限，操作失败")
		return
	if who.friendCtn.hasTeamName(sName):
		message.tips(who, "已有同名分组，不能添加分组")
		return
	who.friendCtn.addTeam(sName,lFriendId)
	message.tips(who,"创建分组成功")

def rpcFriendSetTeamSet(who,reqMsg):
	'''编辑分组
	'''
	iTeamNo = reqMsg.iTeamNo
	sName = reqMsg.sName
	if not checkName(sName):
		return
	if iTeamNo not in who.friendCtn.dTeamName:
		return
	lFriendId = []
	for iFriendId in reqMsg.roleIdList:
		lFriendId.append(iFriendId)
	if len(lFriendId) > 100:
		message.tips(who, "自定义分组人数已达上限，操作失败")
		return

	who.friendCtn.setTeam(iTeamNo,sName,lFriendId)
	message.tips(who,"编辑分组成功")

def rpcFriendDelTeamReq(who,reqMsg):
	'''删除分组
	'''
	iTeamNo = reqMsg.iTeamNo
	if iTeamNo not in who.friendCtn.dTeamName:
		return
	who.friendCtn.removeTeam(iTeamNo)

def rpcFriendModReq(who,reqMsg):
	'''设置好友分组
	'''
	iFriendId = reqMsg.iRoleId
	oFriend = who.friendCtn.getItem(iFriendId)
	if not oFriend or not oFriend.isFriend():
		return
	for attrObj, attrVal in reqMsg.ListFields():
		attrName = attrObj.name
		if attrName == "iTeamNo":
			if attrVal >= 100 and who.friendCtn.isFull(attrVal):
				message.tips(who, "自定义分组人数已达上限，操作失败")
				continue

			who.friendCtn.setTeamNo(attrVal,oFriend)
		elif attrName == "sMarkName":
			if not checkName(attrVal):
				continue
			if oFriend.markName != attrVal:
				oFriend.setMarkName(attrVal)
				oFriend.attrChange("markName")

	message.tips(who,"修改成功")

def rpcFriendChatSend(who,reqMsg):
	'''发送聊天信息
	'''
	iFriendId = reqMsg.iRoleId
	sContent  = reqMsg.sContent
	iAudio    = reqMsg.iAudio
	iAudioLen = reqMsg.iAudioLen
	iAudioIdx = reqMsg.iAudioIdx
	sendFriendMsg(who, iFriendId, sContent, iAudio, iAudioLen, iAudioIdx)

def rpcFriendRecommendReq(who,reqMsg):
	'''推荐请求
	'''
	iType = reqMsg.iType
	bRefresh = reqMsg.bRefresh
	if iType == 1:
		sendRecommendFriend(who,bRefresh)
	elif iType == 2:
		sendNearbyFriend(who,bRefresh)
	else:
		message.tips(who,"该功能暂未开启")

def rpcFriendSearch(who,reqMsg):
	'''搜索好友
	'''
	nowSec = getSecond()
	if hasattr(who,"searchFriendSec") and nowSec - who.searchFriendSec < 3:
		message.tips(who,"操作太频繁，请稍后尝试")
		return
	who.searchFriendSec = nowSec

	iType = reqMsg.iType
	sContent = reqMsg.sContent
	if iType == 2: #跨服
		gevent.spawn(searchAboard,who.id,sContent)
	else:
		search(who,sContent)

def rpcFriendAddRecLinkManReq(who,reqMsg):
	'''最近联系人添加请求
	'''
	minLevel = baseConfigData.getConfig("好友等级")
	if who.level < minLevel:
		message.tips(who, "%d开启好友系统" % minLevel)
		return

	iFriendId = reqMsg.iRoleId
	if iFriendId == who.id:
		return
	resumeObj = resume.getResume(iFriendId)
	if not resumeObj:  #不存在的角色
		return
	if resumeObj.level < minLevel:
		message.tips(who,"目标等级小于#C04%d级#n，不能与对方进行聊天" % minLevel)
		return

	who.friendCtn.addLinkMan(iFriendId)

def sendNearbyFriend(who, bRefresh):
	'''发送附近好友
	'''
	if bRefresh or not hasattr(who,"nearbyFriendList"):
		oCenterEP = client4center.getCenterEndPoint()
		oCenterEP.rpcNearbyReq(iRoleId=who.id)
	else:
		rpcSendNearbyFriend(who)

def rpcSendNearbyFriend(who):
	'''发送附近好友
	'''	
	iNo = who.nearbyFriendNo

	lst = []
	lFriend = who.friendCtn.lFriend
	minLevel = baseConfigData.getConfig("好友等级")
	for resuemInfo in who.nearbyFriendList[iNo:]:
		iNo += 1
		iRoleId = resuemInfo.roleId
		if iRoleId in lFriend or iRoleId == who.id:
			continue
		if resuemInfo.level < minLevel:
			continue
		oMsg = friend_pb2.frinedInfo()
		oMsg.iRoleId = iRoleId
		oMsg.iLevel = resuemInfo.level
		oMsg.iShape = resuemInfo.shape
		oMsg.iSchool = resuemInfo.school
		oMsg.sName = resuemInfo.name
		oMsg.sSignature = resuemInfo.signature
		oMsg.sServiceName = resuemInfo.serviceName
		oMsg.bSameService = resuemInfo.serviceName == config.ZONE_NAME
		lst.append(oMsg)
		if len(lst) == 8:
			break

	if not lst and who.nearbyFriendNo:
		message.tips(who,"已是最后一页")
		return

	who.nearbyFriendNo = iNo

	msg = {}
	msg["iType"] = 2
	msg["resultList"] = lst

	who.endPoint.rpcFriendRecommendSend(**msg)

def sendRecommendFriend(who, bRefresh):
	'''发送推荐好友
	'''
	if bRefresh or not hasattr(who,"recFriendList"):
		who.recFriendList = createRecommendList(who)
		who.recFriendNo = 0

	iNo = who.recFriendNo
	lst = []
	lFriend = who.friendCtn.lFriend
	for iRoleId in who.recFriendList[iNo:]:
		iNo += 1
		oRole = getRole(iRoleId)
		if not oRole:
			continue
		if iRoleId in lFriend or iRoleId == who.id:
			continue
		oMsg = friend_pb2.frinedInfo()
		packRole(oRole,oMsg)
		lst.append(oMsg)
		if len(lst) == 8:
			break

	if not lst and who.recFriendNo:
		message.tips(who,"已是最后一页")
		return

	who.recFriendNo = iNo

	msg = {}
	msg["iType"] = 1
	msg["resultList"] = lst

	who.endPoint.rpcFriendRecommendSend(**msg)

def createRecommendList(who):
	'''生成推荐列表
	'''
	minLevel = baseConfigData.getConfig("好友等级")
	iLevel = who.level
	lRoleId = []
	iMin = max(minLevel,who.level-10)
	iMax = min(100,who.level+10)
	for i in xrange(iMin,iMax+1):
		lst = role.gdRoleIdByLevel.get(i,[])
		lRoleId.extend(lst)

	shuffleList(lRoleId)
	return lRoleId

def checkFriendAdd(who, iFriendId, sMarkName, iTeamNo):
	'''检查添加好友
	'''
	minLevel = baseConfigData.getConfig("好友等级")
	if who.level < minLevel:
		message.tips(who, "%d开启好友系统" % minLevel)
		return False

	oFriend = who.friendCtn.getItem(iFriendId)
	if oFriend:
		if oFriend.isBlack():
			who.friendCtn.removeItem(oFriend)
		else:
			message.tips(who,"对方已在你的好友名单中")
			return False
	if who.friendCtn.isFull():
		message.tips(who,"你的好友已满，不能添加好友")
		return False
	if iTeamNo >= 100 and who.friendCtn.isFull(iTeamNo):
		return False
	if iFriendId == who.id:
		message.tips(who,"不能添加自己为好友")
		return
	if not checkName(sMarkName):
		return
	if not (0<iFriendId<=c.MAX_ROLE_ID):
		return False

	if isSameService(iFriendId):
		resumeObj = resume.getResume(iFriendId)
		if not resumeObj:  #不存在的角色
			return False

		if resumeObj.level < minLevel:
			message.tips(who, "目标等级小于#C04%d#n，不能加为好友" % minLevel)
			return False

	return True

def checkBlackAdd(who, iBlackId):
	'''检查添加黑名单
	'''
	oBlack = who.friendCtn.getItem(iBlackId)
	if oBlack:
		if oBlack.isFriend():
			who.friendCtn.removeItem(oBlack)
		else:
			message.tips(who,"对方已在你的黑名单中")
			return False
	if who.friendCtn.isFullBlack():
		return False
	if not (0<iBlackId<=c.MAX_ROLE_ID):
		return False

	return True

def addFriend(who, iFriendId, sMarkName="", iTeamNo=0):
	bSameService = isSameService(iFriendId)
	if not checkFriendAdd(who, iFriendId, sMarkName, iTeamNo):
		return

	if not bSameService: #跨服的
		if who.level < 30:
			message.tips(who,"30级以上才可跨服添加好友")
		else:
			gevent.spawn(aboardFriendAdd,who.id,iFriendId,sMarkName,iTeamNo)
		return

	oFriend = friend.new(TYPE_FRIEND,iFriendId)
	if sMarkName:
		oFriend.setMarkName(sMarkName)
	who.friendCtn.addItem(oFriend)
	if iTeamNo:
		who.friendCtn.setTeamNo(iTeamNo,oFriend)
	message.tips(who,"你添加了#C01{}#n为好友".format(oFriend.name))
	targetFriendCtn = block.blockFriend.getFriendCtn(iFriendId)
	if who.id in targetFriendCtn.lBlack:
		return
	sContent = "#C06{}#n把你加为好友，以后常联系~#L1<57,{},{},{},{},{}>*[点击添加好友]*02#n".format(who.name,who.id,who.level,who.name,who.school,who.shape)
	friend.sendSysMsg(iFriendId,sContent)

def aboardFriendAdd(roleId, iFriendId, sMarkName, iTeamNo):
	'''添加跨服好友
	'''
	oCenterEP = client4center.getCenterEndPoint()
	bFail,oRes = oCenterEP.rpcResumeReq(iFriendId)
	if bFail or not oRes.roleId:
		return
	who = getRole(roleId)
	if not who:
		return
	if oRes.level < 30:
		message.tips(who, "对方等级小于30，无法跨服加为好友")
		return
	if not checkFriendAdd(who, iFriendId, sMarkName, iTeamNo):
		return

	oFriend = friend.new(friend.defines.TYPE_FRIEND_ABROAD,iFriendId)
	attrList = {}
	for attrObj, attrVal in oRes.ListFields():
		attrName = attrObj.name
		attrList[attrName] = attrVal
	oFriend.update(True,**attrList)
	if sMarkName:
		oFriend.setMarkName(sMarkName)
	who.friendCtn.addItem(oFriend)
	if iTeamNo:
		who.friendCtn.setTeamNo(iTeamNo,oFriend)

def aboardBlackAdd(roleId, iBlackId):
	'''添加跨服黑名单
	'''
	oCenterEP = client4center.getCenterEndPoint()
	bFail,oRes = oCenterEP.rpcResumeReq(iBlackId)
	if bFail or not oRes.roleId:
		return
	who = getRole(roleId)
	if not who:
		return
	if not checkBlackAdd(who, iBlackId):
		return

	oBlack = friend.new(friend.defines.TYPE_BLACK_ABROAD,iBlackId)
	attrList = {}
	for attrObj, attrVal in oRes.ListFields():
		attrName = attrObj.name
		attrList[attrName] = attrVal
	oBlack.update(True,**attrList)
	who.friendCtn.addItem(oBlack)

def sendFriendMsg(who, iFriendId, sContent, iAudio=0, iAudioLen=0, iAudioIdx=0):
	'''发送聊天信息
	'''
	if who.id == iFriendId:
		return
		
	if calLenForWord(sContent) > 60:
		message.tips(who,"输入内容超过最大字数，请分开发送")
		return

	if not (0<iFriendId<=c.MAX_ROLE_ID):
		return

	oFriend = who.friendCtn.getItem(iFriendId)
	if not oFriend:
		resumeObj = resume.getResume(iFriendId)  #非法id
		minLevel = baseConfigData.getConfig("好友等级")
		if not resumeObj or resumeObj.level < minLevel:
			message.tips(who,"目标等级小于#C04%d级#n，不能与对方进行聊天" % minLevel)
			return

	perSec = 1 if iFriendId in who.friendCtn.lFriend else 3
	nowSec = getSecond()
	if nowSec - who.friendCtn.dChatTime.get(iFriendId,0) < perSec:
		message.tips(who,"说话太快啦，缓一缓吧！")
		return

	who.friendCtn.dChatTime[iFriendId] = nowSec
	msg = {}
	msg["iRoleId"] = iFriendId
	msg["iSendTime"] = nowSec
	msg["sContent"] = sContent
	msg["iAudio"] = iAudio
	msg["iAudioLen"] = iAudioLen
	msg["iAudioIdx"] = iAudioIdx
	msg["iSenderId"] = who.id

	who.friendCtn.addLinkMan(iFriendId)
	who.endPoint.rpcFriendChatGet(**msg)
	oFriend = who.friendCtn.getFriend(iFriendId)
	oFriend.chat(msg)

def search(who, sContent):
	'''搜索本服好友
	'''
	msgObj = friend_pb2.searchInfo()
	msgObj.iType = 1
	msgObj.sContent = sContent

	if sContent.isdigit():
		iSearchId = int(sContent)
		oRole = getRole(iSearchId)
		if oRole:
			roleMsg = msgObj.resultList.add()
			packRole(oRole,roleMsg)
	else:
		i = 0
		for iRoleId,oRole in role.gKeeper.getIterItems():
			if sContent in oRole.name:
				roleMsg = msgObj.resultList.add()
				packRole(oRole, roleMsg)
				i = i + 1
			if i >= 8:
				break

	who.endPoint.rpcFriendSearchResule(msgObj)

def packRole(who, roleMsg):
	'''打包人物摘要属性
	'''
	roleMsg.iRoleId = who.id
	roleMsg.iLevel = who.level
	roleMsg.iShape = who.shape
	roleMsg.iSchool = who.school
	roleMsg.sName = who.name
	roleMsg.sSignature = who.getSignature()
	roleMsg.bSameService = True

def searchAboard(roleId, sContent):
	'''搜索跨服好友
	'''
	if not sContent.isdigit():
		return
	iSearchId = int(sContent)
	oCenterEP = client4center.getCenterEndPoint()
	bFail,oRes = oCenterEP.rpcResumeReq(iSearchId)
	if bFail or not oRes.roleId:
		return
	who = getRole(roleId)
	if not who:
		return

	msgObj = friend_pb2.searchInfo()
	msgObj.iType = 2
	msgObj.sContent = sContent
	if oRes.roleId and not oRes.offlineTime: #在线的
		roleMsg = msgObj.resultList.add()
		roleMsg.iRoleId = oRes.roleId
		roleMsg.iLevel = oRes.level
		roleMsg.iShape = oRes.shape
		roleMsg.iSchool = oRes.school
		roleMsg.sName = oRes.name
		roleMsg.sSignature = oRes.signature
		roleMsg.bSameService = oRes.serviceName == config.ZONE_NAME
		roleMsg.sServiceName = oRes.serviceName
	else:
		message.tips(who,"你搜索的玩家不存在或不在线")
		pass
		
	who.endPoint.rpcFriendSearchResule(msgObj)

def checkName(sName):
	'''检查备注
	'''
	if calLenForWord(sName) > 6:
		return False
	if sName != trie.fliter(sName):
		return False
	return True

def rpcAddTeam(endPoint, iTeamNo, sName, roleIdList):
	'''增加组
	'''
	msg = {}
	msg["iTeamNo"] = iTeamNo
	msg["sName"] = sName
	msg["roleIdList"] = roleIdList
	endPoint.rpcFriendAddTeam(**msg)

def rpcModTeam(endPoint, iTeamNo, sName, roleIdList):
	'''改变组
	'''
	msg = {}
	msg["iTeamNo"] = iTeamNo
	msg["sName"] = sName
	msg["roleIdList"] = roleIdList
	endPoint.rpcFriendModTeam(**msg)

def isSameService(iRoleId):
	'''是否本服
	'''
	zoneNo = u.getNoByguId(iRoleId)
	return zoneNo == config.ZONE_NO

from common import  *
from friend.defines import *
import message
import friend
import resume
import c
import client4center
import gevent
import role
import config
import mainService
import u
import block.blockFriend
import trie
import baseConfigData