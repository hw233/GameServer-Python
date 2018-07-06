#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

def create(iType):
	mod = friend.object.modByType[iType]
	return mod(iType)

def new(iType, iRoleId):
	obj = create(iType)
	obj.set("bd",getDayNo())
	obj.set("friendId",iRoleId)
	return obj

def createAndLoad(iType, data):
	obj = create(iType)
	obj.load(data)
	return obj

def add(who, iFriendId, sMarkName="", iTeamNo=0):
	'''增加好友
	'''
	friend.service.addFriend(who,iFriendId,sMarkName,iTeamNo)

def sendMsg(who, iFriendId, sContent, iAudio=0, iAudioLen=0, iAudioIdx=0):
	'''发送信息给好友
	'''
	friend.service.sendFriendMsg(who, iFriendId, sContent, iAudio, iAudioLen, iAudioIdx)
	
def sendSysMsg(iRoleId, sContent):
	'''发送系统信息
	'''
	msg = {}
	msg["iRoleId"] = iRoleId
	msg["iSendTime"] = getSecond()
	msg["sContent"] = sContent
	msg["iSenderId"] = SYS_ID #系统

	if friend.service.isSameService(iRoleId):
		who = getRole(iRoleId)
		if who and who.endPoint:
			who.endPoint.rpcFriendChatGet(**msg)
		else:
			resumeObj = resume.getResume(iRoleId)
			resumeObj.addOfflineChat(msg)
	else:
		client4center.getCenterEndPoint().rpcChatSend(**msg)

def addFriendPoint(who):
	teamObj = who.getTeamObj()
	if not teamObj:
		return
	for iRoleId in teamObj.memberList:
		if who.id == iRoleId:
			continue
		oRole = getRole(iRoleId)
		if who.friendCtn.isBothFriend(oRole):
			who.friendCtn.addFriendPoint(oRole.id,1)

def addTeamMate(teamObj, who):
	for iRoleId in teamObj.memberList:
		if who.id == iRoleId:
			continue
		oRole = getRole(iRoleId)
		oRole.friendCtn.addTeamMate(who.id)
		who.friendCtn.addTeamMate(oRole.id)

def onLogin(who,bReLogin):
	resumeObj = resume.getResume(who.id)
	if not resumeObj:
		return
	for iInterestMeId in resumeObj.interestList:
		roleObj = getRole(iInterestMeId)
		if not roleObj:
			continue
		oFriend = roleObj.friendCtn.getItem(who.id)
		if oFriend and oFriend.isFriend():
			roleObj.endPoint.rpcFriendOnline(oFriend.getMsg())
			if not bReLogin:
				sContent = "你的好友#C01%s#n已经上线" % who.name
				message.tips(roleObj, sContent)
				message.message(roleObj, sContent)

def onOffline(who):
	resumeObj = resume.getResume(who.id)
	if not resumeObj:
		return
	for iInterestMeId in resumeObj.interestList:
		roleObj = getRole(iInterestMeId)
		if not roleObj:
			continue
		oFriend = roleObj.friendCtn.getItem(who.id)
		if oFriend and oFriend.isFriend():
			roleObj.endPoint.rpcFriendOffline(iRoleId=oFriend.friendRoleId,iOfflineTime=oFriend.offlineTime)

def init():
	import role
	role.geOffLine += onOffline

from common import *
from friend.defines import *
import message
import friend.object
import resume
import friend.service
import client4center

'''
import pst

class cFriend(pst.cEasyPersist):
	def __init__(self,iFriendRoleId):
		pst.cEasyPersist.__init__(self)
		self.iFriendRoleId=iFriendRoleId
		self.iOwnerId=0
		self.oResume=factoryConcrete.resumeFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE,iFriendRoleId)
		if not self.oResume:
			raise Exception,'找不到角色id为{}相应的简要信息.'.format(iFriendRoleId)
		#这里持有了resume的强引用,而不是每次要用到resume时从keeper中拿出来.
		#目的是阻止resume被踢出内存.减少resume频繁地进出内存

		self.sMemo=''#备注名字
		self.iBirthday=0

	def load(self,dData):#override
		pst.cEasyPersist.load(self,dData)
		self.sMemo=dData.pop('memo','')
		self.iBirthday=dData.pop('bd',0)

	def save(self):#override
		dData=pst.cEasyPersist.save(self)
		if self.sMemo:
			dData['memo']=self.sMemo
		if self.iBirthday:
			dData['bd']=self.iBirthday
		return dData

	def onBorn(self,*tArgs,**dArgs):#override
		# pass
		self.iBirthday=timeU.getDayNo()#生产日期

	def setup(self,who):#新加好友的时候才会调用
		who.triggerEvent(event.FRIEND)

	def friendId(self):#好友的id
		return self.iFriendRoleId

	@property
	def ownerId(self):
		return self.iOwnerId
	
	@ownerId.setter
	def ownerId(self, ownerId):
		self.iOwnerId = ownerId

	@property
	def key(self):#被放入容器时的唯一标识
		return self.iFriendRoleId

	def memo(self):#备注名字
		return self.sMemo

	def setMemo(self,sMemo):
		self.sMemo=sMemo
		self.markDirty()

	def birthday(self):
		return self.iBirthday

	def isNewFriend(self):#是否新的好友
		return timeU.getDayNo()==self.birthday()

	@property
	def name(self):
		return self.oResume.name

	def onAdd2container(self):#当增加到容器时
		self.oResume.addInterestMe(self.ownerId)		

	def onRemoveFromContainer(self):#当从容器里删除时
		self.oResume.removeInterestMe(self.ownerId)

	def tacit(self):#默契值
		return self.fetch('tacit',0)

	def tacitMax(self):#默契值最大值
		dStar=sysConfigData.getConfig('rTacitStar')
		return dStar[max(dStar)]

	def nextTacit(self):#还差默契值多少升星	
		iMyTacit=self.tacit()
		if iMyTacit>=self.tacitMax():
			return 0
		dStar=sysConfigData.getConfig('rTacitStar')
		lKeys=dStar.keys()
		lKeys.sort()#从小到大
		for iTacit in lKeys:
			if iMyTacit<iTacit:
				return iTacit-iMyTacit

	def addTacit(self,iAdd):#增加默契值
		if iAdd==0 or self.tacit()>=self.tacitMax():
			return 0
		if self.tacit()+iAdd<0:
			raise Exception,'不能把默契值扣成负数,否则{}+({})={}.'.format(self.tacit(),iAdd,self.tacit()+iAdd)
		if self.tacit()+iAdd>=self.tacitMax():
			iAdd=self.tacitMax()-self.tacit()
		self.add('tacit',iAdd)
		ep=mainService.getEndPointByRoleId(self.ownerId)
		if not ep:
			return iAdd
		self.tacitMsgSend(ep)
		return iAdd

	def tacitStar(self):#默契值星星数
		dStar=sysConfigData.getConfig('rTacitStar')
		return findSort.getRightValue(self.tacit(),dStar)

	def getTacitAdd(self,sKey,uDefault=0):
		if not self.tacitStar():
			return 0
		return tacitData.getConfig(self.tacitStar(),sKey,uDefault)

	def fightAdd(self):#组队战力加成
		iFight=self.getTacitAdd('force')
		ownerResume=resume.gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,self.ownerId)
		iFightAdd=iFight/ownerResume.fightAbility()
		return iFightAdd

	def attrAdd(self):#默契值增加的属性
		dAttr={}
		for sKey,iValue in c.ATTR_MAP4.iteritems():
			if self.getTacitAdd(sKey):
				dAttr[iValue]=self.getTacitAdd(sKey)
		return dAttr

	def tacitMsgSend(self,ep):#默契值改变时下发给客户端
		friendList=im_pb2.roleList()
		friendList.iType=3
		friend=friendList.roles.add()
		friend.iRoleId=self.friendId()
		friend.iTacit=self.tacit()
		friend.iTacitStar=self.tacitStar()
		friend.iNextTacit=self.nextTacit()
		friend.iFightAdd=self.fightAdd()
		ep.rpcFriendChange(friendList)

def new(iFriendRoleId,*tArgs,**dArgs):
	obj=cFriend(iFriendRoleId)
	obj.onBorn(*tArgs,**dArgs)
	return obj

def cretaeAndLoad(iFriendRoleId,dData):
	obj=cFriend(iFriendRoleId)
	obj.load(dData)
	return obj

def initEvent():
	role.geLogin+=Player_Login
	role.geOffLine+=Player_OffLine
	role.geUpLevel+=G2CVouchFriend


import role
import resume
import weakref
import u
import c
import log
import misc
import factory
import factoryConcrete
import role
import role_pb2
import timeU

import sysConfigData
import findSort
import svcFriend
import im_pb2
import mainService
import event
'''