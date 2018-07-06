#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import backEnd_center_pb2
import endPoint
import misc

class cService(backEnd_center_pb2.backEnd2center):

	@endPoint.result
	def rpcTest1(self,ep,who,reqMsg):return rpcTest1(self,ep,who,reqMsg)
	@endPoint.result
	def rpcGetName(self,ep,who,reqMsg):return rpcGetName(self,ep,who,reqMsg)
	@endPoint.result
	def rpcConfirmName(self,ep,who,reqMsg):return rpcConfirmName(self,ep,who,reqMsg)
	@endPoint.result
	def rpcHotUpdate2center(self,ep,who,reqMsg):return rpcHotUpdate2center(self,ep,who,reqMsg)

	@endPoint.result
	def rpcUpdateName(self, ep, who, reqMsg):return rpcUpdateName(self,ep,who,reqMsg)

	@endPoint.result
	def rpcBackEndReport(self, ep, who, reqMsg):return rpcBackEndReport(self,ep,who,reqMsg)
	
	@endPoint.result
	def rpcUpdateResume(self, ep, who, reqMsg):return rpcUpdateResume(self,ep,who,reqMsg)

	@endPoint.result
	def rpcResumeListReq(self, ep, who, reqMsg):return rpcResumeListReq(self,ep,who,reqMsg)

	@endPoint.result
	def rpcResumeReq(self, ep, who, reqMsg):return rpcResumeReq(self,ep,who,reqMsg)

	@endPoint.result
	def rpcChatSend(self, ep, who, reqMsg):return rpcChatSend(self,ep,who,reqMsg)

	@endPoint.result
	def rpcNearbyReq(self, ep, who, reqMsg):return rpcNearbyReq(self,ep,who,reqMsg)

	@endPoint.result
	def rpcDelAudio(self, ep, who, reqMsg):return rpcDelAudio(self,ep,who,reqMsg)

def rpcBackEndReport(self,ep,ctrlr,reqMsg):#
	iZoneNo=reqMsg.iZoneNo
	iBackEndType=reqMsg.iBackEndType
	sZoneName=reqMsg.sZoneName
	iPageNo=reqMsg.iPageNo
	if iBackEndType not in (1,2,4,8,16,32,64):
		raise Exception,'backEnd的类型只能是1,2,4,8,16,32,64'
	sBackEndName=backEnd.gdServiceName[iBackEndType]
	
	sText='区号"{}"后端"{}"向中心服报到'.format(iZoneNo, sBackEndName)
	print sText
	log.log('info',sText)

	ep.setAssociative(iZoneNo, iBackEndType, sZoneName, iPageNo)
	return True

def rpcTest1(self,ep,who,reqMsg):
	print 'backEnd send msg to centerService'

def rpcGetName(self,ep,who,reqMsg):
	iGender = reqMsg.iGender
	iRoleId = reqMsg.iRoleId
	sName = randNameData.getName(ep.iPageNo,iRoleId,iGender)
	dNameById[iRoleId] = sName
	return sName

def rpcConfirmName(self,ep,who,reqMsg):
	iRoleId = reqMsg.iRoleId
	sName = dNameById.pop(iRoleId)
	if not sName:
		return
	db4center.gConnectionPool.query(sql4center.ROLE_NAME_INSERT,iRoleId,ep.iPageNo,sName)

def rpcHotUpdate2center(self,ep,who,reqMsg):
	sFileName = reqMsg.sValue
	hotUpdate.update(sFileName)

def rpcUpdateName(self,ep,who,reqMsg):
	iRoleId = reqMsg.iRoleId
	sName = reqMsg.sName
	sOld = reqMsg.sOld
	iPageNo = ep.iPageNo
	if sName in randNameData.gdRoleName.get(iPageNo,set()):
		return False
	db4center.gConnectionPool.query(sql4center.ROLE_NAME_UPDATE, sName, iRoleId, iPageNo)
	randNameData.delName(iPageNo,sOld)
	randNameData.addName(iPageNo,sName)
	return True

def rpcUpdateResume(self, ep, who, reqMsg):
	iRoleId = reqMsg.roleId
	attrList = {}
	for attrObj, attrVal in reqMsg.ListFields():
		attrName = attrObj.name
		attrList[attrName] = attrVal

	resumeObj = centerService.resume.getResumeFirst(iRoleId)
	resumeObj.update(ep,**attrList)

def rpcResumeListReq(self,ep,who,reqMsg):
	lst = []
	for resumeMsg in reqMsg:
		roleId = resumeMsg.roleId
		resumeObj = centerService.resume.getResume(iRoleId)
		if not resumeObj:
			continue
		lst.append(resumeObj.getMsg())

	if lst:
		ep.rpcResumeListSend(resumeList=lst,iRoleId=reqMsg.iRoleId)

def rpcResumeReq(self,ep,who,reqMsg):
	roleId = reqMsg.roleId
	resumeObj = centerService.resume.getResume(roleId)
	if not resumeObj:
		msgObj = backEnd_center_pb2.resumeInfo()
		msgObj.roleId = 0
	else:
		msgObj = resumeObj.getMsg()

	return msgObj

def rpcChatSend(self,ep,who,reqMsg):
	iTargetId = reqMsg.iRoleId

	iZoneNo = u.getNoByguId(iTargetId)
	oCenterEp = centerService.getCenterEp(iZoneNo)
	if not oCenterEp:
		ep.rpcTipsCenter(reqMsg.iSenderId,"对方服务器没有开启")
		return
	oCenterEp.rpcChatGet(reqMsg)

def rpcNearbyReq(self,ep,who,reqMsg):
	iRoleId = reqMsg.iRoleId
	roleInfo = collect.gRoleInfoMngObj.dRoleInfoObj.get(iRoleId)
	if not roleInfo:
		ep.rpcTipsCenter(iRoleId,"请先打开定位")
		return
	fPosX, fPosY = roleInfo.fPosX,roleInfo.fPosY
	lst = []
	for iFriendId,friendInfo in collect.gRoleInfoMngObj.dRoleInfoObj.iteritems():
		if collect.getLineDistance(fPosX,fPosY,friendInfo.fPosX,roleInfo.fPosY) > 2000:
			continue
		resumeObj = centerService.resume.getResume(iFriendId)
		lst.append(resumeObj.getMsg())

	msg = {}
	msg["iRoleId"] = iRoleId
	msg["resumeList"] = lst
	ep.rpcNearbySend(**msg)

def rpcDelAudio(self,ep,who,reqMsg):
	'''删除语音
	'''
	iAudioIdx = reqMsg.iValue
	centerService.audio.gAudioKeeper.removeObj(iAudioIdx)

dNameById = {}

import backEnd
import randNameData
import db4center
import hotUpdate
import sql4center
import centerService.resume
import u
import log
import centerService
import collect
import centerService.audio