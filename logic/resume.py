# -*- coding: utf-8 -*-
import block
import pst
import jitKeeper
import factoryConcrete
import factory
#角色摘要信息,可以离线获取,主要用于好友栏的显示,
#对于有些好友并不在线,但又需要知道一些好友的信息
#好友关系是多对多的,角色简要要信息会被多个玩家引用

# 需要更新的简历属性列表
updateAttrList = (
	"name", "shape", "school", "level",
	"guildName", "guildId", "shapeParts", "colors",
	"signature","offlineTime",

)

class cResume(block.cBlock,pst.cEasyPersist):
	def __init__(self, roleId):#override
		block.cBlock.__init__(self,'角色简要数据',roleId)
		pst.cEasyPersist.__init__(self,self.__dirtyEventHandler)
		
		self.setIsStm(sql.RESUME_INSERT)
		self.setDlStm(sql.RESUME_DELETE)
		self.setUdStm(sql.RESUME_UPDATE)
		self.setSlStm(sql.RESUME_SELECT)
		
		self.id = roleId
		self.offLineChatList = {}
		self.interestList = set()   #关注我的人,例如加了我好友，我在他的最近联系人等。不存盘

	def __dirtyEventHandler(self):#数据发生变化了,加入到存盘调度队列
		factoryConcrete.resumeFtr.schedule2tail4save(self.id)
		
	def load(self, data):
		pst.cEasyPersist.load(self, data["data"])
		self.offLineChatList = data.pop("offlineChat",{})
	
	def save(self):
		data = {}
		data["data"] = pst.cEasyPersist.save(self)
		data["offlineChat"] = self.offLineChatList
		return data
	
	def onBorn(self):
		who = getRole(self.id)
		if who:
			self.update(who)

	def addInterest(self, iTragetId):
		'''添加关注我的人
		'''
		self.interestList.add(iTragetId)

	def removeInterest(self, iTragetId):
		'''取消关注我的人
		'''
		if iTragetId in self.interestList:
			self.interestList.remove(iTragetId)

	def addOfflineChat(self, msg):
		'''增加离线聊天信息
		'''
		roleId = msg["iSenderId"]
		countMax = 20 if roleId == 51 else 30
		lst = self.offLineChatList.setdefault(roleId,[])
		lst.append(msg)
		if len(lst) > countMax:
			lst.pop(0)
		self.markDirty()

	def getOfflineChat(self,):
		'''获得离线聊天信息
		'''
		for lst in self.offLineChatList.itervalues():
			for msg in lst:
				yield msg

	def clearOfflineChat(self):
		'''清空离线聊天信息
		'''
		self.offLineChatList = {}
		self.markDirty()

	def update(self, who):
		'''更新
		'''
		self.markDirty()
		changeList = {}
		for attrName in updateAttrList:
			attrValue = who.getValByName(attrName)
			if getattr(self,attrName) != attrValue or attrName == "offlineTime":
				self.set(attrName, attrValue)
				changeList[attrName] = attrValue

		if changeList:
			changeList["roleId"] = who.id
			centerService.attrChange(changeList)

	def __getattr__(self, name):
		if name in updateAttrList:
			return self.fetch(name)
		return object.__getattribute__(self, name)

class cResumeKeeper(jitKeeper.cJITproductKeeper):
	pass
# 	def stayAnyway(self,ownerId):#override
# 		who = role.gKeeper.getObj(ownerId)
# 		if who:#主人在线,就不从keeper卸载
# 			return True
# 		return productKeeper.cJITproductKeeper.stayAnyway(self)

if 'gKeeper' not in globals():
	gKeeper=cResumeKeeper(factoryConcrete.resumeFtr)
	
# def anyEventHandler(who):
# 	iRoleId=who.id
# 	oResume=gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iRoleId)
# 	oResume.recover()

def init():
	import role
	role.geOffLine += onOffline

def getResume(roleId):
	resumeObj = gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, roleId)
	return resumeObj

def updateResume(who):
	resumeObj = getResume(who.id)
	if resumeObj:
		resumeObj.update(who)

def addLinkMan(who):
	resumeObj = getResume(who.id)
	if not resumeObj:
		return
	for msg in resumeObj.getOfflineChat():
		who.friendCtn.addLinkMan(msg["iSenderId"],True)

def onLogin(who):
	resumeObj = getResume(who.id)
	if not resumeObj:
		return
	if resumeObj.offLineChatList:
		resumeObj.clearOfflineChat()

	updateResume(who)

def onOffline(who):
	updateResume(who)
	
from common import *
import sql
import centerService

'''
def init():
	pass#role.geUpLevel+=anyEventHandler

# def roleLoginHandler(who):
# 	iRoleId=who.id
# 	gAllFriendIds=who.friendCtn.getAllKeys()
# 	#遍历全部在线的玩家,如果我是他的好友,通知他们我上线了
# 	for iOtherId,oOtherRole in role.roleHelper.dOnlineRoleKeeper.iteritems():
# 		if iOtherId==iRoleId:#跳过自已
# 			continue
# 		if iRoleId in oOtherRole.friendCtn.getAllKeys():
# 			oOtherRole.ep.rpcTips('你的好友{}上线了'.format(who.name))

# def roleOfflineHandler(who):
# 	iRoleId=who.id
# 	gAllFriendIds=who.friendCtn.getAllKeys()
# 	#遍历全部在线的玩家,如果我是他的好友,通知他们我上线了
# 	for iOtherId,oOtherRole in role.roleHelper.dOnlineRoleKeeper.iteritems():
# 		if iOtherId==iRoleId:#跳过自已
# 			continue
# 		if iRoleId in oOtherRole.friendCtn.getAllKeys():
# 			oOtherRole.ep.rpcTips('你的好友{}下线了'.format(who.name))

class cImMsg(pst.cPersist):#即时通信的消息	
	def __init__(self,*tArgs,**dArgs):
		pst.cPersist.__init__(self,*tArgs,**dArgs)
		self.iSendStamp=0 #发送时间戳
		self.iSenderId=0 #发送者id
		self.sContent='' #内容
		self.sSenderName='' #发送者名字


	def onBorn(self,iSenderId,sSenderName,sContent):		
		self.iSendStamp=timeU.getStamp()
		self.iSenderId=iSenderId
		self.sContent=sContent
		self.sSenderName=sSenderName
		self.markDirty()	

	def save(self):
		d={}
		d['st']=self.iSendStamp
		d['id']=self.iSenderId
		d['ct']=self.sContent
		d['name']=self.sSenderName
		return d

	def load(self,dData):
		self.iSendStamp=dData.pop('st', 0)
		self.iSenderId=dData.pop('id', 0)
		self.sContent=dData.pop('ct', '')
		self.sSenderName=dData.pop('name', '')

	def sendStamp(self):
		return self.iSendStamp

	def senderId(self):
		return self.iSenderId

	def content(self):
		return self.sContent

	def senderName(self):
		return self.sSenderName

	def notify(self,iRoleId,sSenderName):#通知有好友聊天消息到达
		ep=mainService.getEndPointByRoleId(iRoleId)
		if ep:
			ep.rpcImMsgArrival(self.iSenderId,self.sSenderName)
		
	def send(self,who):#发好友聊天消息
		ep=mainService.getEndPointByRoleId(who.id)
		if ep:
			ep.rpcSendImMsg(self.iSenderId,self.sContent,self.iSendStamp)
		who.friendCtn.addRecentContact(self.iSenderId)#将其加入最近联系人
		who.friendCtn.rpcRecentContact(ep)#更新最近联系人列表

class cSysMsg(pst.cPersist):#系统消息
	def __init__(self,*tArgs,**dArgs):
		pst.cPersist.__init__(self,*tArgs,**dArgs)
		self.bSave=True
		self.iSendStamp=0 #发送时间戳		
		self.sContent='' #内容

		#self.iSenderId=0 #发送者id
		#self.sSenderName='' #发送者名字		

	def onBorn(self,sContent,bSave):		
		# self.iSenderId=iSenderId
		# self.sSenderName=sSenderName
		self.sContent=sContent #聊天内容
		self.iSendStamp=timeU.getStamp() #发送时间
		self.bSave=bSave
		if bSave:
			self.markDirty()

	def save(self):
		if self.bSave:
			d={}
			d['st']=self.iSendStamp			
			d['ct']=self.sContent
			#d['id']=self.iSenderId
			#d['name']=self.sSenderName
			return d
		else:
			return None

	def content(self):
		return self.sContent

	def sendStamp(self):
		return self.iSendStamp

	def load(self,dData):
		self.iSendStamp=d['st']		
		self.sContent=d['ct']
		#self.iSenderId=d['id']
		#self.sSenderName=d['name']			

	def notify(self,iRoleId):#通知有系统消息到达
		ep=mainService.getEndPointByRoleId(iRoleId)
		if ep:
			ep.rpcSysMsgArrival()

	def send(self,iRoleId):#发关系统消息
		ep=mainService.getEndPointByRoleId(iRoleId)
		if ep:
			ep.rpcSendSysMsg(self.sContent,self.iSendStamp)


########################登录执行函数映射#####################

DELETEGUILDID=1  #删除关联的公会ID
DEALROLEAPPLY=2  #加入公会
GUILDMEMBERSETTING=3 #发送系统通知
SENDADDFRIENDMSG=4	#发送请求好友通知
CHECKADDFRIENDREPLAY=5	#好友请求对方回应通知
DELFRIEND=6	#删除好友通知

import guild
# import guild.svcGuild
if 'gdFunc' not in globals():
	#针对一些不在线的角色进行操作,等到角色上线了在执行
	gdFunc={
		DELETEGUILDID:guild.deleteRoleGuildId,
		DEALROLEAPPLY:guild.dealRoleApply,
		# JOININGUILDID:guild.joinGuildOnline,
		# GUILDMEMBERSETTING:guild.svcGuild.sendSysNotice,
		SENDADDFRIENDMSG:friend.svcFriend.sendAddFriendMsg,
		CHECKADDFRIENDREPLAY:friend.svcFriend.checkAddFriendReplay,
		DELFRIEND:friend.svcFriend.delFriend,
	}


############################登录执行函数映射#####################

from common import *
import sql
import weakref
import cycleData
import u

import log
import c
import factory
import role
import timeU
import role_pb2

import mainService
import guild
import role.roleHelper
import block.blockPackage
import roleAttrData


class cCycDayInResume(cycleData.cCycDay):
	pass #只是为了起个别名

class cCycWeekInResume(cycleData.cCycWeek):
	pass
'''