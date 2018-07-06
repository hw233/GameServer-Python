#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import backEnd_center_pb2
import endPoint

class cService(backEnd_center_pb2.center2backEnd):
	@endPoint.result
	def rpcTest2(self,ep,who,reqMsg):return rpcTest2(self,ep,who,reqMsg)

	@endPoint.result
	def rpcResumeListSend(self,ep,who,reqMsg):return rpcResumeListSend(self,ep,who,reqMsg)

	@endPoint.result
	def rpcChatGet(self,ep,who,reqMsg):return rpcChatGet(self,ep,who,reqMsg)

	@endPoint.result
	def rpcTipsCenter(self,ep,who,reqMsg):return rpcTipsCenter(self,ep,who,reqMsg)

	@endPoint.result
	def rpcNearbySend(self,ep,who,reqMsg):return rpcNearbySend(self,ep,who,reqMsg)

def rpcTest2(self,ep,who,reqMsg):
	print 'centerService send msg to backEnd'

def rpcResumeListSend(self,ep,who,reqMsg):
	iRoleId = reqMsg.iRoleId
	who = getRole(iRoleId)
	if not who:
		return
	for resuemMsg in reqMsg.resumeList:
		attrList = {}
		for attrObj, attrVal in resuemMsg.ListFields():
			attrName = attrObj.name
			attrList[attrName] = attrVal

		oFriend = who.friendCtn.getFriend(resuemMsg.roleId)
		oFriend.update(**attrList)

def rpcChatGet(self,ep,who,reqMsg):
	iTragetId = reqMsg.iRoleId
	iSendTime = reqMsg.iSendTime
	sContent  = reqMsg.sContent
	iAudio    = reqMsg.iAudio
	iAudioLen = reqMsg.iAudioLen
	iAudioIdx = reqMsg.iAudioIdx
	iSenderId = reqMsg.iSenderId

	msg = {}
	msg["iRoleId"] = iTragetId
	msg["iSendTime"] = iSendTime
	msg["sContent"] = sContent
	msg["iAudio"] = iAudio
	msg["iAudioLen"] = iAudioLen
	msg["iAudioIdx"] = iAudioIdx
	msg["iSenderId"] = iSenderId

	friendCtn = block.blockFriend.getFriendCtn(iTragetId)
	if not friendCtn or iSenderId in friendCtn.lBlack:
		return
	addLinkManAboard(friendCtn,iSenderId)
		
	who = getRole(iTragetId)
	if who and who.endPoint:
		who.friendCtn.addLinkMan(iSenderId)
		who.endPoint.rpcFriendChatGet(**msg)
	else:
		resumeObj = resume.getResume(iTragetId)
		if resumeObj:
			resumeObj.addOfflineChat(msg)

def rpcTipsCenter(self,ep,who,reqMsg):
	iRoleId = reqMsg.iRoleId
	sContent = reqMsg.sContent

	message.tips(iRoleId,sContent)

def addLinkManAboard(friendCtn, iFriendId):
	if friendCtn.getItem(iFriendId):
		return
	oCenterEP = client4center.getCenterEndPoint()
	bFail,oRes = oCenterEP.rpcResumeReq(iFriendId)
	if bFail:
		return

	oFriend = friend.new(friend.defines.TYPE_LINKMAN_ABROAD,iFriendId)
	attrList = {}
	for attrObj, attrVal in oRes.ListFields():
		attrName = attrObj.name
		attrList[attrName] = attrVal
	oFriend.update(True,**attrList)
	friendCtn.addItem(oFriend)

def rpcNearbySend(self,ep,who,reqMsg):
	iRoleId = reqMsg.iRoleId
	who = getRole(iRoleId)
	if not who:
		return
	lst = []
	for resuemInfo in reqMsg.resumeList:
		lst.append(resuemInfo)

	who.nearbyFriendList = lst
	who.nearbyFriendNo = 0
	friend.service.rpcSendNearbyFriend(who)

from common import *
import message
import resume
import friend
import friend.defines
import client4center
import block.blockFriend
import friend.service