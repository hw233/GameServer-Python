# -*-coding:utf-8-*-
# 作者:马昭@曹县闫店楼镇
import productKeeper

# 角色管理器,持有角色对象

class cRoleKeeper(productKeeper.cProductkeeper):	
	def removeObj(self, iRoleId):  # override,应timingWheel的要求,返回真值才表示踢成功.不然过段时间还会再踢一次
		with primitive.cLockByKey(lock4key.dLock4role, iRoleId):#self.getObj(iRoleId)也在要锁范围内,避免who对象失效
			who = self.getObj(iRoleId)
			if not who:
				return True
			if not self.canRemove(who):
				return False
			if task.offlineTask.tryOfflineTask(who):
				return False
			
			who.set("offlineTime",getSecond())
			role.geOffLine(who)  # 全局事件
			who.eRemove(who)  # 触发删除事件.
			role.login.onOffline(who)
			role.removeFromLevelList(who)
			self.removeFromScene(who,iRoleId)#从场景上删除自已
			self.removeTeam(who)
			self.removeAccount(who,iRoleId)
			role.register.unRegisterRole(who)
			productKeeper.cProductkeeper.removeObj(self, iRoleId)  # 最后才做真正的移除
			return True

	def removeTeam(self,who):#
		# 策划要求下线时退出队伍
		teamObj = who.getTeamObj()
		if teamObj:
			teamObj.remove(who.id)
# 				who.set("teamId", teamObj.id)
# 				teamObj.setOffline(who)

	def removeAccount(self,who,iRoleId):#
		oAccount = who.accountObj
		if not oAccount:
			return
		# logReport.gLogReporter.logRoleLogout(who)	#记录角色下线报表日志		
		if oAccount.playingRoleId() == iRoleId:  # 当前账号对象的活跃角色是自己,顺便把账号对象移除掉.							
			oAccount.setPlayingRoleId(0)  # 当前角色对象被移除,重置帐号指向的当前活跃角色
			ep = mainService.getEndPointByUserSourceAccount(*oAccount.userSourceAccount())
			if not ep:
				account.gKeeper.removeObj(*oAccount.userSourceAccount())
				# ep.rpcModalDialog('超时未检测到操作,请重新登录','连接超时')

	def removeFromScene(self,who,iRoleId):#
		oScene = scene.gSceneProxy.getProxy(who.sceneId)
		if not oScene:
			return
		oScene.removeEntity(who)
		if oScene.isTempScene():  # 临时场景(不合理情况,哪个副本没有把玩家传出来)
			pass
# 			iSceneId = scene.getScene(c.NEW_ROLE_BORN_NO).id
# 			who.sceneId = iSceneId
# 			log.log('error', '角色{}从keeper移除了,但是身上的场景id还指着一个临时场景id'.format(iRoleId))
		else:  # 永久场景(合理情况)#临时加了保存最后下线位置
			who.active.setLastRealPos(who.sceneId, who.x, who.y, False)
		backEnd.gSceneEp4ms.rpcDeleteEntity(who.id)		

	def canRemove(self,who):#是否可以从内存中踢掉玩家
		if who.inWar():
			return False
		if task.offlineTask.inOfflineTask(who): # 离线任务中
			return False
		return True

from common import *
import lock4key
import primitive
import role
import account
import mainService
import scene
import log
import role.register
import task.offlineTask
import backEnd
import role.login
