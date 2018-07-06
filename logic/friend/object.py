#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import pst

resumeAttrList = ["level","shape","school","name","signature","guildName","offlineTime"]

class cFriend(pst.cEasyPersist):
	def __init__(self,iType):
		pst.cEasyPersist.__init__(self)
		self.iType=iType
		self.iOwnerId=0
		self.friendPoint=0
		self.markName=""

	def load(self,dData):#override
		pst.cEasyPersist.load(self,dData)
		self.friendPoint = dData["friendPoint"]
		self.markName = dData["markName"]

	def save(self):#override
		dData=pst.cEasyPersist.save(self)
		dData["friendPoint"] = self.friendPoint
		dData["markName"] = self.markName
		return dData

	def attrChange(self, *attrList):
		who = getRole(self.ownerId)
		if not who:
			return
			
		msg = {}
		msg["iRoleId"] = self.friendRoleId
		for attrName in attrList:
			if attrName == "level":
				msg["iLevel"] = self.level
			elif attrName == "shape":
				msg["shape"] = self.shape
			elif attrName == "school":
				msg["school"] = self.school
			elif attrName == "signature":
				msg["sSignature"] = self.signature
			elif attrName == "online":
				msg["bOnline"] = self.isOnline()
			elif attrName == "friendPoint":
				msg["iFriendPoint"] = self.friendPoint
			elif attrName == "markName":
				msg["sMarkName"] = self.markName
			elif attrName == "offlineTime":
				msg["iOfflineTime"] = self.offlineTime

		who.endPoint.rpcFriendMod(**msg)

	def __getattr__(self, name):
		if name in resumeAttrList:
			return self.resume.fetch(name)

		return object.__getattribute__(self, name)

	@property
	def resume(self):
		#这里持有了resume的强引用,而不是每次要用到resume时从keeper中拿出来.d)
		#目的是阻止resume被踢出内存.减少resume频繁地进出内存
		if not hasattr(self, "oResume"):
			self.oResume = factoryConcrete.resumeFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE,self.friendRoleId)
			if self.isFriend():
				self.oResume.addInterest(self.ownerId)
		return self.oResume

	@property
	def friendRoleId(self):
	    return self.fetch("friendId")

	def addFriendPoint(self, iValue):
		'''添加亲密度
		'''
		self.friendPoint += iValue
		self.markDirty()

	def setMarkName(self, markName):
		'''设置备注名字
		'''
		self.markName = markName
		self.markDirty()

	def isOnline(self):
		'''是否在线
		'''
		oRole = getRole(self.friendRoleId)
		if oRole:
			return True
		return False

	def isSameService(self):
		'''是否同服
		'''
		return True

	def inTeam(self):
		'''是否在队
		'''
		who = getRole(self.friendRoleId)
		if who and who.inTeam():
			return True
		return False

	@property
	def serviceName(self,):
		'''服务器名字
		'''
		return config.ZONE_NAME

	def getMsg(self, isFirst=True):
		oMsg = friend_pb2.frinedInfo()
		oMsg.iRoleId = self.friendRoleId
		oMsg.iLevel = self.level
		oMsg.iShape = self.shape
		oMsg.iSchool = self.school
		oMsg.sName = self.name
		oMsg.sSignature = self.signature
		oMsg.bOnline = self.isOnline()
		oMsg.bSameService = self.isSameService()
		oMsg.iFriendPoint = self.friendPoint
		oMsg.sMarkName = self.markName
		oMsg.sServiceName = self.serviceName
		oMsg.iOfflineTime = self.offlineTime
		if not isFirst:
			oMsg.bInTeam = self.inTeam()
			oMsg.sGuildName = self.guildName
		return oMsg

	def chat(self, msg):
		'''聊天
		'''
		oRole = getRole(self.friendRoleId)
		if oRole and oRole.endPoint:   #需要连接在才发送
			if self.ownerId in oRole.friendCtn.lBlack:
				message.tips(self.ownerId,"你在对方的黑名单中")
				return
			oRole.friendCtn.addLinkMan(self.ownerId)
			oRole.endPoint.rpcFriendChatGet(**msg)
		else:
			friendCtn = block.blockFriend.getFriendCtn(self.friendRoleId)
			if self.ownerId in friendCtn.lBlack:
				message.tips(self.ownerId,"你在对方的黑名单中")
				return
			self.resume.addOfflineChat(msg)

	@property
	def ownerId(self):
		return self.iOwnerId
	
	@ownerId.setter
	def ownerId(self, ownerId):
		self.iOwnerId = ownerId

	@property
	def key(self):#被放入容器时的唯一标识
		return self.friendRoleId

	def isFriend(self):
		return self.iType == TYPE_FRIEND

	def isBlack(self):
		return self.iType == TYPE_BLACK

#虚拟好友，用作最近联系人，组队好友
class cFriendDummy(cFriend):

	def __init__(self,iRoleId,iOwnerId):
		cFriend.__init__(self,TYPE_FRIEND)
		self.iFriendRoleId = iRoleId
		self.iOwnerId = iOwnerId

	@property
	def friendRoleId(self):
	    return self.iFriendRoleId

#跨服好友
class cFriendAbroad(cFriend):

	def isSameService(self):
		'''是否同服
		'''
		return False

	def isOnline(self):
		'''是否在线
		'''
		if self.offlineTime:
			return False

		return True

	@property
	def serviceName(self,):
		'''服务器名字
		'''
		return self.fetch("serviceName","")

	def chat(self, msg):
		'''聊天
		'''
		oCenterEP = client4center.getCenterEndPoint()
		if oCenterEP:
			oCenterEP.rpcChatSend(**msg)

	@property
	def resume(self):  #没有resume，都是存盘数据
		return self

	def isFriend(self):
		return self.iType == TYPE_FRIEND_ABROAD

	def isBlack(self):
		return self.iType == TYPE_BLACK_ABROAD

	def update(self, bFirst=False, **attrList):
		'''更新
		'''
		for attrName,attrValue in attrList.iteritems():
			if attrName == "roleId":
				continue
			if not self.hasKey(attrName) or self.fetch(attrName) != attrValue:
				self.set(attrName,attrValue)

		if not bFirst:
			who = getRole(self.friendRoleId)
			if who:
				who.endPoint.rpcFriendMod(self.getMsg())


from common import *
from friend.defines import *
import role
import resume
import factory
import factoryConcrete
import role
import friend_pb2
import config
import client4center
import block.blockFriend
import message


modByType = {
	TYPE_FRIEND:cFriend,
	TYPE_BLACK:cFriend,
	TYPE_FRIEND_ABROAD:cFriendAbroad,
	TYPE_BLACK_ABROAD:cFriendAbroad,
	TYPE_LINKMAN_ABROAD:cFriendAbroad,
}
