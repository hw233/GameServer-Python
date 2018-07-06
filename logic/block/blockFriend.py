#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import ctn
import block
import pst
import factory

#好友容器
class cFriendContainer(ctn.cContainerBase,block.cCtnBlock):
	def __init__(self,iOwnerId):#override
		block.cCtnBlock.__init__(self,'好友容器',iOwnerId)
		ctn.cContainerBase.__init__(self,iOwnerId)
		self.setIsStm(sql.FRIEND_INSERT)
		self.setDlStm(sql.FRIEND_DELETE)
		self.setUdStm(sql.FRIEND_UPDATE)
		self.setSlStm(sql.FRIEND_SELECT)

		self.lRecLinkMan = []  #最近联系人  存盘
		self.lRecTeamMate = [] #最近队友    存盘
		self.lFriend = []  #好友    不存盘 登录时构建
		self.lBlack = []  #黑名单    不存盘 登录时构建
		self.dTeamName = {}  #自定义名字分组，存盘
		self.dTeamRoleId = {}  #自定义分组玩家，存盘
		self.lDummyFriend = {}  #虚拟的好友。非好友的最近联系人和最近队友.不存盘
		self.dChatTime = {}  #聊天时间 不存盘
		
	def _dirtyEventHandler(self):#override
		factoryConcrete.friendCtnFtr.schedule2tail4save(self.ownerId)

	def _initItem4container(self,obj,uData=None):#override
		if obj.isFriend():
			self.lFriend.append(obj.key)
		elif obj.isBlack():
			self.lBlack.append(obj.key)

		return ctn.cContainerBase._initItem4container(self,obj,uData)

	def _saveItem(self,iIndex,obj):#生成子项的保存数据
		dData=obj.save()
		if dData is None:
			return None
		if dData:
			return (obj.iType,dData)
		else:
			return obj.iType

	def _createAndLoadItem(self,iIndex,uData):#override
		if isinstance(uData,tuple):
			iType,dData=uData		
		else:
			iType,dData=uData,{}			
		obj=friend.createAndLoad(iType,dData)
		return obj

	def removeItem(self,obj):#移除子项
		if obj.isFriend():
			self.lFriend.remove(obj.key)
		elif obj.isBlack():
			self.lBlack.remove(obj.key)
		return ctn.cContainerBase.removeItem(self,obj)

	def addFriendPoint(self, iFriendId, iValue):
		'''增加亲密度
		'''
		oFriend = self.getItem(iFriendId)
		if oFriend:
			oFriend.addFriendPoint(iValue)
			oFriend.attrChange("friendPoint")

	def isBothFriend(self, oFriend):
		'''是否双方都是好友
		'''
		if self.ownerId not in oFriend.friendCtn.lFriend:
			return False
		if oFriend.id not in self.lFriend:
			return False
		return True

	def isFullTeam(self,):
		'''自定义分组数量是否满了
		'''
		return len(self.dTeamName) >= 10

	def isFull(self, iTeamNo=0):
		'''是否满人
		'''
		if not iTeamNo:
			return len(self.lFriend) >= 200
		elif iTeamNo in self.dTeamRoleId:
			return len(self.dTeamRoleId) >= 100
		return True

	def isFullBlack(self):
		'''黑名单是否满人
		'''
		return len(self.lBlack) >= 100

	def addTeamMate(self, iFriendId):
		'''添加最近队友
		'''
		if self.lRecTeamMate and iFriendId == self.lRecTeamMate[len(self.lRecTeamMate)-1]:
			return
		if iFriendId in self.lRecTeamMate:
			self.lRecTeamMate.remove(iFriendId)

		self.markDirty()
		self.lRecTeamMate.append(iFriendId)
		if len(self.lRecTeamMate) > 20:
			popLinkManId = self.lRecTeamMate.pop(0)

		self.endPoint.rpcFriendAddRecTeamMate(self.getFriend(iFriendId).getMsg())

	def addLinkMan(self, iFriendId, bLogin=False):
		'''添加最近联系人
		'''
		if iFriendId == SYS_ID or iFriendId == SPIRIT_ID:
			return
		if self.lRecLinkMan and iFriendId == self.lRecLinkMan[len(self.lRecLinkMan)-1]:
			#本来就是最后一个联系人就直接return
			return
		if iFriendId in self.lRecLinkMan:
			self.lRecLinkMan.remove(iFriendId)

		self.markDirty()
		self.lRecLinkMan.append(iFriendId)
		if len(self.lRecLinkMan) > 20:
			popLinkManId = self.lRecLinkMan.pop(0)
		if not bLogin:
			self.endPoint.rpcFriendAddRecLinkMan(self.getFriend(iFriendId).getMsg())

	def nextTeamNo(self):
		'''下一个组号
		'''
		if not self.dTeamName:
			return 100

		return max(self.dTeamName.keys()) + 1

	def getTeamNo(self, iFriendId):
		'''获得组号
		'''
		for iTeamNo,lFriend in self.dTeamRoleId.iteritems():
			if iFriendId in lFriend:
				return iTeamNo

		return 0

	def setTeamNo(self, iTeamNo, oFriend):
		'''设置组号
		'''
		iOldTeamNo = self.getTeamNo(oFriend.friendRoleId)
		if iOldTeamNo:
			self.dTeamRoleId[iOldTeamNo].remove(oFriend.friendRoleId)
			friend.service.rpcModTeam(self.endPoint,iOldTeamNo,self.dTeamName[iOldTeamNo],self.dTeamRoleId[iOldTeamNo])
		
		if iTeamNo not in self.dTeamRoleId:
			return

		self.dTeamRoleId[iTeamNo].append(oFriend.friendRoleId)
		friend.service.rpcModTeam(self.endPoint,iTeamNo,self.dTeamName[iTeamNo],self.dTeamRoleId[iTeamNo])
		self.markDirty()

	def addTeam(self, sName, lFriendId):
		'''添加分组
		'''
		self.markDirty()
		iTeamNo = self.nextTeamNo()
		self.dTeamName[iTeamNo] = sName
		self.dTeamRoleId[iTeamNo] = lFriendId
		friend.service.rpcAddTeam(self.endPoint,iTeamNo,sName,lFriendId)
		return iTeamNo

	def removeTeam(self, iTeamNo):
		'''删除分组
		'''
		self.markDirty()
		self.dTeamName.pop(iTeamNo)
		self.dTeamRoleId.pop(iTeamNo)
		self.endPoint.rpcFriendDelTeam(iTeamNo)

	def setTeam(self, iTeamNo, sName, lFriendId):
		'''编辑分组
		'''
		self.markDirty()
		self.dTeamName[iTeamNo] = sName
		self.dTeamRoleId[iTeamNo] = lFriendId
		friend.service.rpcModTeam(self.endPoint,iOldTeamNo,sName,lFriendId)

	def hasTeamName(self, sName):
		'''是否有改组名
		'''
		return sName in self.dTeamName.values()

	def getTeamMsg(self):
		lst = []
		for iTeamNo,sName in self.dTeamName.iteritems():
			oMsg = friend_pb2.teamInfo()
			oMsg.iTeamNo = iTeamNo
			oMsg.sName = sName
			oMsg.roleIdList.extend(self.dTeamRoleId[iTeamNo])
			lst.append(oMsg)
		return lst

	def getOfflineChatMsg(self):
		'''获取离线消息
		'''
		lst = []
		offlineChat = resume.getResume(self.ownerId).getOfflineChat()
		for msg in offlineChat:
			if msg["iSenderId"] in self.lBlack:
				continue
			oMsg = friend_pb2.chatInfo()
			oMsg.iRoleId = msg["iRoleId"]
			oMsg.iSendTime = msg["iSendTime"]
			oMsg.sContent = msg["sContent"]
			oMsg.iAudio = msg.get("iAudio",0)
			oMsg.iAudioLen = msg.get("iAudioLen",0)
			oMsg.iAudioIdx = msg.get("iAudioIdx",0)
			oMsg.iSenderId = msg["iSenderId"]

			lst.append(oMsg)
		
		return lst

	def getFriend(self, iFriendId):
		oFriend = self.getItem(iFriendId)
		if not oFriend:
			if iFriendId not in self.lDummyFriend:
				self.lDummyFriend[iFriendId] = friend.object.cFriendDummy(iFriendId,self.ownerId)

			oFriend = self.lDummyFriend[iFriendId]

		return oFriend

	def _rpcRefresh(self):
		msg = {}
		msg["friendList"] = [self.getItem(iFriendId).getMsg() for iFriendId in self.lFriend]
		msg["recLinkManList"] = [self.getFriend(iFriendId).getMsg() for iFriendId in self.lRecLinkMan]
		msg["recTeamMateList"] = [self.getFriend(iFriendId).getMsg() for iFriendId in self.lRecTeamMate]
		msg["blackList"] = [self.getItem(iFriendId).getMsg() for iFriendId in self.lBlack]
		msg["teamList"] = self.getTeamMsg()
		msg["chatList"] = self.getOfflineChatMsg()

		self.endPoint.rpcFriendListSend(**msg)
	
	def onBorn(self):#override
		pass

	def load(self,dData):
		ctn.cContainerBase.load(self,dData)
		self.lRecLinkMan = dData.pop("recLinkMan",[])
		self.lRecTeamMate = dData.pop("recTeamMate",[])
		self.dTeamName = dData.pop("teamName",{})
		self.dTeamRoleId = dData.pop("teamRole",{})

	def save(self):
		dData=ctn.cContainerBase.save(self)
		if self.lRecLinkMan:
			dData["recLinkMan"] = self.lRecLinkMan
		if self.lRecTeamMate:
			dData["recTeamMate"] = self.lRecTeamMate
		if self.dTeamName:
			dData["teamName"] = self.dTeamName
		if self.dTeamRoleId:
			dData["teamRole"] = self.dTeamRoleId
		return dData
	
	@property
	def endPoint(self):
		import mainService
		return mainService.getEndPointByRoleId(self.ownerId)

	def _rpcAddItem(self,obj):#override
		if obj.isFriend():
			self.endPoint.rpcFriendAdd(obj.getMsg())
		elif obj.isBlack():
			self.endPoint.rpcFriendAddBlack(obj.getMsg())

	def _rpcRemoveItem(self,obj):#override
		if obj.isFriend():
			self.endPoint.rpcFriendDel(obj.friendRoleId)
		elif obj.isBlack():
			self.endPoint.rpcFriendDelBlack(obj.friendRoleId)

def getFriendCtn(iRoleId):
	return gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, iRoleId)

from friend.defines import *
import sql
import role
import friend
import productKeeper
import factoryConcrete
import jitKeeper
import config
import friend_pb2
import friend.object
import resume
import friend.service

#用于查看离线玩家的包裹/装备信息.一段时间后不访问,自动从容器上移除
if 'gKeeper' not in globals():
	KEEP_SECOND=30 if config.IS_INNER_SERVER else 60*5
	# gKeeper=productKeeper.cJITproductKeeper(factoryConcrete.friendCtnFtr,KEEP_SECOND)	临时屏蔽,测试jitKeeper
	gKeeper=jitKeeper.cJITproductKeeper(factoryConcrete.friendCtnFtr)
