#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import pst

#迷你游戏,允许多人参与
#不仅是关卡结束后玩,任意时候都可调出来玩,使用一个道具,点击npc都可以玩小游戏.
#要不要存盘呢???通关后不存盘,但是使用道具后玩小游戏要不要存盘呢.
class cMiniGame(pst.cEasyPersist):
	def __init__(self,iNo):
		pst.cEasyPersist.__init__(self)		
		self.iNo=iNo				
		self.eGameOver=u.cEvent()
		self.lRoleId=[]#游戏参与者的id
		self.iBeginStamp=0 #开始时间戳
		self.iTimeout=0 #持续秒数
		self.bHasStart=False #是否已经开始
		self.dJob={}

	def no(self):#迷你游戏的编号,即是类型
		return self.iNo

	def roleIds(self):#参与者的角色id
		return self.lRoleId[:]

	def addRole(self,who):#增加参与者
		if self.bHasStart:
			raise Exception,'迷你游戏已经开始,不允许再增加玩家.'
		self.lRoleId.append(who.id)
		who.oMiniGame=self

	def play(self,iTimeout=0,*tArgs,**dArgs):#对外接口,阻塞的,小游戏结束才返回.
		self.bHasStart=True
		self.iTimeout=iTimeout
		self.iBeginStamp=timeU.getStamp()
		
		for iRoleId in self.lRoleId:
			#who=role.gKeeper.getObj(iRoleId)
			#if not who:
			#	continue
			self.dJob[iRoleId]=gevent.spawn(u.cFunctor(self._openUIjob),iRoleId,iTimeout,*tArgs,**dArgs)

		gevent.joinall(self.dJob.values(),iTimeout)#等待全部玩家结束迷你游戏

		#做一些自动发奖,发一个关闭ui网络包之类的
		lNoReplyRoleIds=[iRoleId for iRoleId,job in self.dJob.iteritems() if not job.dead]
		self._onTimeoutNoReply(lNoReplyRoleIds)

		#杀掉超时的协程,做不做都可以的
		lTimeoutJob=[job for job in self.dJob.itervalues() if not job.dead]
		gevent.killall(lTimeoutJob)

		for iRoleId in self.lRoleId:#删除每一个玩家身上的游戏对象.
			who=role.gKeeper.getObj(iRoleId)
			if not who or not hasattr(who,'oMiniGame'):
				continue
			del who.oMiniGame
		self.eGameOver(self)#触发结束事件

	def _openUIjob(self,iRoleId,iTimeout,*tArgs,**dArgs):#发送网络包给某个玩家,子类可以override这个方法
		try:
			bRet,uResponse=self._sendBlockUI(iRoleId,iTimeout,*tArgs,**dArgs)#不理返回值
		finally:
			self.dJob.pop(iRoleId,None)		

	def _sendBlockUI(self,iRoleId,iTimeout,*tArgs,**dArgs):#发送一个阻塞服务端的,客户端结束会回复包的ui
		raise NotImplementedError,'请在子类override,实现发包给客户端,让客户端打开ui.'


	def _onTimeoutNoReply(self,lNoReplyRoleIds):#超时没回复
		pass

	def killJobByRoleId(self,iRoleId):
		job=self.dJob.pop(iRoleId,None)
		if job is not None:
			job.kill()


def roleLoginEventHandler(who):#角色上线,重发迷你游戏的窗口
	oGame=getattr(who,'oMiniGame',None)
	if oGame:
		pass

def roleLoginEventHandler(who):#角色下线,杀掉协程,减少其他玩家等待时间
	oGame=getattr(who,'oMiniGame',None)
	if oGame:
		oGame.killJobByRoleId(who.id)

#迷你游戏结束的方法
#1.客户端强行关闭ui结束
#2.玩家抽完奖/翻完卡牌结束
#3.玩家不操作,超时结束



def create(iNo):
	if iNo not in gdGameModule:
		raise Exception,'没有类型为{}的迷你游戏.'.format(iNo)
	return gdGameModule[iNo].cMiniGame(iNo)

def new(iNo,who,*tArgs,**dArgs):
	obj=create(iNo)
	obj.onBorn(who,*tArgs,**dArgs)	
	return obj

def createAndLoad(iNo,dData):
	obj=create(iNo)
	obj.load(dData)
	return obj

#import wheel
#import turnCard


gdGameModule={
#	1:turnCard,

}

import terminal_main_pb2
import endPoint

class cService(terminal_main_pb2.terminal2main):
	@endPoint.result
	def rpcMiniGameOver(self,ep,who,reqMsg):return rpcMiniGameOver(self,ep,who,reqMsg)


def rpcMiniGameOver(self,ep,who,reqMsg):#小游戏结束
	oMiniGame=getattr(who,'oMiniGame',None)
	if not oMiniGame:
		return
	#二次提示一下他吧,关闭是有损失的.


import types
import gevent
import u
import timeU
import role
import misc
import log

