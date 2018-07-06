#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

import u
import keeper
import sceneMng
import launchMng
import entityManager
import door
import misc
import gevent

BOSS_DELAY=2
INFINITY=60*60*24
#怪物管理器
class cMonsterMng(entityManager.cEttMngWithConfig):
	def __init__(self,oHolder):
		entityManager.cEttMngWithConfig.__init__(self,oHolder)
		self.dAliveMonster={}       	#当前存活的怪物分布集合{1:(怪物ID1,怪物ID2,怪物ID3),2:(ID1,ID2),...}
		self.sWaitSpawnMst=set()		#等待刷新的怪物分布集合
		self.sWreckSpawnMst=set()		#可破坏物触发刷怪
		self.sHasSpawnedMst=set()		#已经刷新的怪物分布集合
		self.sHasDiedMst=set()			#已经刷完的怪物分布集合
		self.dCycCount={}  				#记录循环刷新的已经刷次数  {批号:已刷次数}
		self.sBossId=set() 				#Boss的Id(可能有多个Boss)
		self.dAllMonster={} 			#该场景的所有怪物(包含已经刷的和还没刷的)
		self.sWaitSpawnDlg=set() 	#等待生成的怪物对话
		self.sHasSpawnedDlg=set()	#已经生成的怪物对话
		self.bStopSpawn=False		#怪物管理器是否停止刷怪
		self.sDelaySpawnMonster=set()	#记录延时刷新出来的怪物集合set((怪物批次,怪物编号,怪物在批次中的顺序,批次当前循环次数))

	def _createEttByNo(self,iNo,*tArgs,**dArgs):#override 生成怪物实例
		iSceneId,x,y=tArgs
		return monster.new(iNo,iSceneId,x,y)

	def getCurrScene(self):
		return self.getHolder().getCurrScene()

	def getDelaySeconds(self,iMonsterDisNo):
		# iPreType=monsterdisData.getConfig(iMonsterDisNo,'preType')
		# iPreNo=monsterdisData.getConfig(iMonsterDisNo,'preNo')
		# return iPreNo if iPreNo!=0 and iPreType==SPAWN_UNCONDITION else 0
		return monsterdisData.getConfig(iMonsterDisNo,'delay')

	def getCycleTimes(self,iMonsterDisNo):
		return monsterdisData.getConfig(iMonsterDisNo,'cyc')

	def isCycleEnd(self,iMonsterDisNo):
		return self.dCycCount.get(iMonsterDisNo,0)>=monsterdisData.getConfig(iMonsterDisNo,'cyc')

	def isSpawnAfterSpawn(self,iMonsterDisNo):
		return monsterdisData.getConfig(iMonsterDisNo,'cyc')!=0 and monsterdisData.getConfig(iMonsterDisNo,'flush')==SPAWN_AFTER_SPAWN

	def isSpawnAfterDie(self,iMonsterDisNo):
		return monsterdisData.getConfig(iMonsterDisNo,'cyc')!=0 and monsterdisData.getConfig(iMonsterDisNo,'flush')==SPAWN_AFTER_DIE

	def getSquadInterval(self,iMonsterDisNo):
		return monsterdisData.getConfig(iMonsterDisNo,'squadInterval')

	def getMstdisByOrder(self,iSceneNo,iOrder):
		return monsterdisData.gdOrderToMstDis.get(iSceneNo,{}).get(iOrder,0)

	def isCurrSceneSpawnOver(self):#该场景是否刷新完毕
		return self.sHasDiedMst==set(monsterdisData.gdSceneNoToMstDis.get(self.getCurrScene().no(), []))

	def getPreOrder(self,iMonsterDisNo):
		iPreType=monsterdisData.getConfig(iMonsterDisNo,'preType')
		if iPreType!=SPAWN_DIS and iPreType!=SPAWN_SPAWN:
			raise Exception,'只有前置条件为其他怪物分布编号的才可以调用该函数,当前怪物分布编号为{},前置条件为{}'.format(iMonsterDisNo,iPreType)
		return monsterdisData.getConfig(iMonsterDisNo,'preNo',[])

	def getPreTriggerNo(self,iMonsterDisNo):
		iPreType=monsterdisData.getConfig(iMonsterDisNo,'preType')
		if iPreType not in (SPAWN_MINE,SPAWN_MONSTER_STATUS,SPAWN_SUMMON_SKILL,SPAWN_WRECK):
			raise Exception,'只有前置条件为触发刷新的才可以调用该函数,当前怪物分布编号为{},前置条件为{}'.format(iMonsterDisNo,iPreType)
		return monsterdisData.getConfig(iMonsterDisNo,'preNo',0)

	def getPreDlgByOrder(self,iOrder):
		oScene=self.getCurrScene()
		return monsterDialogData.gdOrderToDialog.get(oScene.id,{}).get(iOrder,0)

	def getPosType(self,iMonsterDisNo):
		return monsterdisData.getConfig(iMonsterDisNo,'posType')

	def getSpawnPos(self,iPosType,tCenter):
		oBarrier=self.getHolder()
		if not oBarrier:
			raise Exception,'当前副本已销毁,请检查'
		if not oBarrier.lJoinRole and iPosType!=1:
			raise Exception,'第一波怪物必须是绝对位置刷新'
		if iPosType==1:
			return tCenter
		else:
			iRoleX,iRoleY=self.getRoleXY()
			return iRoleX+tCenter[0],iRoleY+tCenter[1]

	def getRoleXY(self):  #拿到屏幕左上角的坐标,用于相对位置刷怪
		oHolder=self.getHolder()
		if not oHolder:
			raise Exception,'当前副本已销毁,请检查'
		oTeam=oHolder.teamObj()
		if oTeam:                   
			oRole=oTeam.leaderObj()#组队情况下拿队长的坐标
		else:
			for iRoleId in oHolder.getJoinedRoleId(): #单人情况下只有一个ID
				oRole=role.gKeeper.getObj(iRoleId)
		oScene=self.getCurrScene()
		if not oRole or iRoleId not in oScene.dEttById:
			raise Exception,'没有在副本内找到目标对象'
		return oRole.x,oRole.y

	#添加援护助战者实体
	def generateFightHelper(self,oScene,iHelperId,x,y):
		oResume=factoryConcrete.resumeFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE,iHelperId)
		if not oResume:
			raise Exception,'角色id为{}的简要信息在数据库中不存在'.format(iHelperId)

		sName=oResume.name
		iShape=0
		oHelper=helpFight.cMonster(iHelperId,oResume,oResume.fightAbility())	###	生成'援护助战者'实例
		oHelper.name = sName
		oHelper.shape = iShape
		oHelper.sceneId = oScene.id
		return oHelper

	#生成可破坏物
	def generateWreck(self):
		oCurrScene=self.getCurrScene()
		iSceneId=oCurrScene.id
		iSceneNo=oCurrScene.no()
		if iSceneNo not in wreckDisData.gdData:
			return
		tWreckNo=wreckDisData.getConfig(iSceneNo,'wreckNo')
		tX=wreckDisData.getConfig(iSceneNo,'x')
		tY=wreckDisData.getConfig(iSceneNo,'y')
		for iIdx,iWreckNo in enumerate(tWreckNo):
			x=tX[iIdx]
			y=tY[iIdx]
			oWreck=self.makeEttByNo(iWreckNo,iSceneId,x,y)

	#初始化当前房间需要刷新的怪物分布列表
	def initWaitSpawnMst(self):
		oCurrScene=self.getCurrScene()
		sTemp=set()
		for iMonsterDisNo in monsterdisData.gdSceneNoToMstDis.get(oCurrScene.no(),[]):
			sTemp.add(iMonsterDisNo)
		return sTemp

	#可破坏物触发刷新	
	def initWreckSpawnMst(self):
		oCurrScene = self.getCurrScene()
		return monsterdisData.gdWreck.get(oCurrScene.no(), set())

	#初始化当前房间需要生成的怪物对话
	def initWaitSpawnDlg(self):
		oCurrScene=self.getCurrScene()
		sTemp=set()
		for iMstDialogNo in monsterDialogData.gdSceneNoToDialog.get(oCurrScene.no(),[]):
			sTemp.add(iMstDialogNo)
		return sTemp

	#进入场景生成第一批怪物
	def generateMonster(self):
		oCurrScene=self.getCurrScene()
		if oCurrScene.hasPass():#如果已经通过该房间,则不再刷新怪物
		    return
		self.dAliveMonster.clear()  #清空上一个房间的怪物存活表
		self.dCycCount.clear()  #清空上一个房间的怪物循环表
		self.sWaitSpawnMst=self.initWaitSpawnMst()
		self.sWreckSpawnMst=self.initWreckSpawnMst()	
		self.sHasDiedMst.clear()
		self.sHasSpawnedMst.clear()
		self.dAllMonster.clear()
		self.sWaitSpawnDlg=self.initWaitSpawnDlg()
		self.sHasSpawnedDlg.clear()
		self.sDelaySpawnMonster.clear()
		if not monsterdisData.gdSceneNoToMstDis.get(oCurrScene.no(), []):#当前场景无任何怪物
			oCurrScene.setHasPass()
			return 
		lFirstSpawn=monsterdisData.gdUnconditional.get(oCurrScene.no(),[])#gdUncoditional为无条件刷新的波次
		if not lFirstSpawn:
			return
		for iMonsterDisNo in lFirstSpawn:
			self.spawnMonsterSquad(iMonsterDisNo)

	#启动刷新一组怪
	def spawnMonsterSquad(self,iMonsterDisNo):
		self.sHasSpawnedMst.add(iMonsterDisNo)

		iDelay=self.getDelaySeconds(iMonsterDisNo)
		if iDelay:
			func=u.cFunctor(self.realSpawnMonsterSquad,iMonsterDisNo)	
			self.getHolder().startTimer(func,iDelay)
		else:
			self.realSpawnMonsterSquad(iMonsterDisNo)

	#真正开始刷新一组怪
	def realSpawnMonsterSquad(self,iMonsterDisNo):
		if iMonsterDisNo not in self.sWaitSpawnMst or self.getCurrScene().hasPass():#该波次已经刷新完毕或者已通关
			return
		iCycle=self.getCycleTimes(iMonsterDisNo)
		if iCycle:
			self.dCycCount[iMonsterDisNo]=self.dCycCount.get(iMonsterDisNo,0)+1
			if self.dCycCount.get(iMonsterDisNo,0)>iCycle:
				return
		lMonsterNo=monsterdisData.getConfig(iMonsterDisNo,'monsterno')
		iApperType=self.getPosType(iMonsterDisNo)
		if iApperType==1 or iApperType==2:
			lCenter=monsterdisData.getConfig(iMonsterDisNo,'pos')
			tCenter=self.getSpawnPos(self.getPosType(iMonsterDisNo),lCenter) #通过刷新方式获得最后的中心坐标
			lZone=monsterdisData.getConfig(iMonsterDisNo,'zone')
			tPos=self.calMonsterPos(tCenter,lZone)  #怪物分布坐标
		elif iApperType==3:
			bRequestFail=False 	#用来标记请求屏幕坐标是否失败
			iMonsterAmount=len(lMonsterNo)
			iInitX,iInitY=monsterdisData.getConfig(iMonsterDisNo,'initPos')
			lMembers=self.getHolder().getJoinedRoleId()
			ep=mainService.getEndPointByRoleId(lMembers[0]) if lMembers else None 	#
			if ep:
				msg=scene_pb2.requireXY()
	
				bFail,uResponse=ep.rpcRequireSceneXY(msg)
				oHolder=self.getHolder()
				if not oHolder:
					log.log('instanceDestroyed','向客户端请求当前屏幕左上角坐标后,副本已销毁')
					return
				if bFail:
					bRequestFail=True
					log.log('requestPosFail','【超时未返回】向客户端请求角色当前屏幕左上角坐标超时未返回,以服务端角色当前坐标(x-450,280)代替')
				else:
					iAbsoluteX=uResponse.iValue1
					iAbsoluteY=uResponse.iValue2
			else:
				bRequestFail=True
				log.log('requestPosFail','【连接断开】向客户端请求角色当前屏幕左上角坐标时连接断掉了,以服务端角色当前坐标(x-450,280)代替')
			if bRequestFail:	
				iAbsoluteX,iAbsoluteY=self.getSpawnPos(1,(0,0))[0]-450,280#补救,以人物x-450,y固定280
			iInitX+=iAbsoluteX
			iInitY+=iAbsoluteY
			iOffsetX,iOffsetY=monsterdisData.getConfig(iMonsterDisNo,'offset')
			tPos=[]
			for i in xrange(iMonsterAmount):
				tPos.append((iInitX,iInitY))
				iInitX+=iOffsetX
				iInitY+=iOffsetY
		else:
			raise Exception, '怪物分布坐标不能填{}类型'.format(iApperType)

		iIndividualInterval=monsterdisData.getConfig(iMonsterDisNo,'individualInterval')#同组每个怪物间的刷新间隔
		iSequence=0
		if iIndividualInterval:
			iSequence+=iIndividualInterval
		iSceneId=self.getCurrScene().id
		for iIndex,iMonsterNo in enumerate(lMonsterNo):
			x,y=tPos[iIndex][0],tPos[iIndex][1]
			iDelayTime=iSequence
			if self.isBoss(iMonsterNo):
				iDelayTime=iSequence+BOSS_DELAY
				self.dAliveMonster.setdefault(iMonsterDisNo,set()).add('Boss{}'.format(iMonsterNo))
				for iRoleId in self.getHolder().getJoinedRoleId():
					ep=mainService.getEndPointByRoleId(iRoleId)
					if not ep:
						continue
					ep.rpcBossCome()
			if iDelayTime:
				func=u.cFunctor(self.spawnMonster,iMonsterDisNo,iMonsterNo,iSceneId,x,y,iIndex,iCycle)
				self.getHolder().startTimer(func,iDelayTime)
				iSequence+=iIndividualInterval
				self.sDelaySpawnMonster.add((iMonsterDisNo, iMonsterNo, iIndex, iCycle))
			else:
				self.spawnMonster(iMonsterDisNo,iMonsterNo,iSceneId,x,y,iIndex,iCycle)

		if self.isSpawnAfterSpawn(iMonsterDisNo):#同时刷新(从上一波怪刷出来开始计时,时间到刷新下一组)
			iSquadInterval=self.getSquadInterval(iMonsterDisNo)
			func=u.cFunctor(self.realSpawnMonsterSquad,iMonsterDisNo)
			self.getHolder().startTimer(func,iSquadInterval)

		#刷新下一波怪物,刷新条件为前一波刷出
		iSceneNo=self.getCurrScene().no()
		for iMonsterDisNo in monsterdisData.gdAfterSpawn.get(iSceneNo,[]):
			if iMonsterDisNo not in self.sWaitSpawnMst or iMonsterDisNo in self.sHasSpawnedMst:
				continue
			if iMonsterDisNo in self.dAliveMonster or iMonsterDisNo in self.sHasDiedMst:#已经刷出来了,或已经刷完了则跳过(否则若前置条件是第1波,则1,2波刷完都会走到这里,若1先刷完,则2刷完时仍然满足条件,会再次触发刷新)
				continue
			bMeet=True
			for iPreMstOrder in self.getPreOrder(iMonsterDisNo):
				if self.getMstdisByOrder(iSceneNo,iPreMstOrder) not in self.sHasSpawnedMst:
					bMeet=False
					break
			if bMeet:
				self.spawnMonsterSquad(iMonsterDisNo)

	def isBoss(self,iMonsterNo):
		return monsterData.getConfig(iMonsterNo,'kind')==10

	#生成一只怪物对白
	def generateDialog(self,iMonsterDisNo):
		iOrder=monsterdisData.getConfig(iMonsterDisNo,'order')
		lMonsterIds=self.dAllMonster.get(iMonsterDisNo)
		iMstIdx=len(lMonsterIds) if lMonsterIds else None
		if iMstIdx is None:
			return
		for iDialogNo in monsterDialogData.gdMstOrderToDialog.get(self.getCurrScene().no(),{}).get(iOrder,[]):
			iDiaMstIdx=monsterDialogData.getConfig(iDialogNo,'mstIdx')
			if iMstIdx!=iDiaMstIdx:
				continue
			if monsterDialogData.getConfig(iDialogNo,'preType'):
				continue
			self.constructDialog(iDialogNo,iMonsterDisNo)
			self.sHasSpawnedDlg.add(iDialogNo)
			self.sWaitSpawnDlg.discard(iDialogNo)

	#构造对话消息
	def constructDialog(self,iDialogNo,iMonsterDisNo,iPreDuration=0):
		try:
			iMstIdx=monsterDialogData.getConfig(iDialogNo,'mstIdx')
			iMstOrder=monsterDialogData.getConfig(iDialogNo,'mstOrder')
			lMonsterIds=self.dAllMonster.get(iMonsterDisNo)
			if not lMonsterIds:
				return
			iMonsterNo=monsterdisData.getConfig(iMonsterDisNo,'monsterno')[iMstIdx-1]
			bIsBoss=self.isBoss(iMonsterNo)
			dlgInfo=scene_pb2.mstDialog()
			if not bIsBoss:
				if iMstIdx>len(lMonsterIds):#若索引越界,说明目标怪物已经死亡
					return
				iMonsterNo=0
				dlgInfo.iMonsterId=lMonsterIds[iMstIdx-1]
			else:
				dlgInfo.iMonsterId=0
				iPreDuration+=BOSS_DELAY #Boss延时刷,需要加入延迟时间
			dlgInfo.sDialog=monsterDialogData.getConfig(iDialogNo,'dialog')
			dlgInfo.iDuration=monsterDialogData.getConfig(iDialogNo,'duration')
			iInterval=monsterDialogData.getConfig(iDialogNo,'interval')+iPreDuration
			if iInterval:
				func=u.cFunctor(self._rpcDialog,dlgInfo,iMonsterDisNo,iMonsterNo)
				self.getHolder().startTimer(func,iInterval)
			else:
				self._rpcDialog(dlgInfo,iMonsterDisNo)
			self.sHasSpawnedDlg.add(iDialogNo)
			self.sWaitSpawnDlg.discard(iDialogNo)
		except IndexError:
			log.log('mstDialog','对白编号{}，怪物索引{}，怪物组内编号{}，怪物分布{}，已刷出怪物{}'.format(iDialogNo,iMstIdx,iMstOrder,iMonsterDisNo,lMonsterIds))

	#发送对话数据,并生成同一波次的其余对白
	def _rpcDialog(self,dlgMsg,iMonsterDisNo,iMonsterNo=0):
		if iMonsterNo:#如果有怪物编号,说明是Boss,因为Boss延时刷,那时没有id,所以传编号进来,再重新拿id
			for iMonsterId in self.sBossId:
				if self.getCurrScene().dEttById.get(iMonsterId).no()==iMonsterNo:
					dlgMsg.iMonsterId=iMonsterId
					break
		for iRoleId in self.getHolder().getJoinedRoleId():
			ep=mainService.getEndPointByRoleId(iRoleId)
			if not ep:
				continue
			ep.rpcMstDialog(dlgMsg)

		for iDialogNo in monsterDialogData.gdSceneNoToDialog.get(self.getCurrScene().no(),{}):
			iPreType=monsterDialogData.getConfig(iDialogNo,'preType')
			if not iPreType:
				continue
			iPreOrder=monsterDialogData.getConfig(iDialogNo,'preNo')
			iPreNo=self.getPreDlgByOrder(iPreOrder)
			if iPreType==1 and iDialogNo in self.sWaitSpawnDlg and iPreNo in self.sHasSpawnedDlg:
				self.constructDialog(iDialogNo,iMonsterDisNo)
			elif iPreType==2 and iDialogNo in self.sWaitSpawnDlg and iPreNo in self.sHasSpawnedDlg:
				iPreDuration=monsterDialogData.getConfig(iPreNo,'duration')
				self.constructDialog(iDialogNo,iMonsterDisNo,iPreDuration)
			else:
				continue

	def stopSpawnMonster(self):#设置停止刷怪标志
		#因为有可能出现关卡通关
		#但还有些延时刷出的小怪没刷出,但已经进了定时器调度(启动了定时器进行刷新)
		#因此在spawnMonster时需检查self.bStopSpawn
		self.bStopSpawn=True	

	def makeEttByNo(self,iNo,iSceneId=0,x=0,y=0,*tArgs,**dArgs):#override
		oMonster=self._createEttByNo(iNo,iSceneId,x,y,*tArgs,**dArgs)
		oMonster.setkillTarget(self.oHolder().isSpawnTargetMonster(iNo))#设置是否是目标怪物
		self._setupEtt(oMonster,oMonster.sceneId,x,y,*tArgs,**dArgs)
		return oMonster	

	#刷新一只怪
	def spawnMonster(self,iMonsterDisNo,iMonsterNo,iSceneId,x,y,iIndex,iCycle):
		if self.bStopSpawn:
			return
		self.sDelaySpawnMonster.discard((iMonsterDisNo, iMonsterNo,iIndex,iCycle))
		oMonster=self.makeEttByNo(iMonsterNo,iSceneId,x,y)
		self.dAliveMonster.setdefault(iMonsterDisNo,set()).add(oMonster.id)
		self.dAllMonster.setdefault(iMonsterDisNo,[]).append(oMonster.id)
		if oMonster.isBoss():
			self.sBossId.add(oMonster.id)
			self.dAliveMonster.get(iMonsterDisNo,set()).discard('Boss{}'.format(iMonsterNo))
		self.generateDialog(iMonsterDisNo)

	#触发刷怪
	def triggerSpawn(self,iType,iNo):
		iSceneNo=self.getCurrScene().no()
		if iType==SPAWN_MINE:	#地雷触发刷新
			lTriggerMstDisNo=monsterdisData.gdMine.get(iSceneNo,[])
		elif iType==SPAWN_MONSTER_STATUS:	#怪物状态触发刷新
			lTriggerMstDisNo=monsterdisData.gdMonsterStatus.get(iSceneNo,[])
		elif iType==SPAWN_WRECK:
			lTriggerMstDisNo=monsterdisData.gdWreck.get(iSceneNo,{}).get(iNo,[])
		else:
			lTriggerMstDisNo=[]
		for iMonsterDisNo in lTriggerMstDisNo: 
			if iMonsterDisNo not in self.sWaitSpawnMst:
				continue
			if iNo!=self.getPreTriggerNo(iMonsterDisNo):
				continue
			self.sWaitSpawnMst.add(iMonsterDisNo)
			self.spawnMonsterSquad(iMonsterDisNo)

	#从存活列表中移除已经死亡的怪物ID,并触发满足条件(前置波次怪物已刷完)的下一波怪物刷新
	def removeFromAliveList(self,iMonsterId):
		self.sBossId.discard(iMonsterId)
		oCurrScene=self.getCurrScene()
		iSceneNo=oCurrScene.no()
		for iMonsterDisNo,sMonsterIds in self.dAliveMonster.items():
			if iMonsterId not in sMonsterIds:
				continue
			sMonsterIds.discard(iMonsterId)
			if not sMonsterIds:
				if self.isCycleEnd(iMonsterDisNo):
					self.dAliveMonster.pop(iMonsterDisNo,None)
					self.sWaitSpawnMst.discard(iMonsterDisNo)	#该刷新波次已结束,将其从待刷新集合移除
					self.sHasDiedMst.add(iMonsterDisNo)		#将其加入已刷新完毕集合
					self.oHolder().incrMoneterBrew(iMonsterDisNo)	#关卡更新击杀波数
					# if iMonsterDisNo in newbieGuideData.gdMonterDied: #是否需要触发新手引导
					if iMonsterDisNo==812:
						oHolder=self.getHolder()
						for iRoleId in oHolder.getJoinedRoleId():
							oRole=role.gKeeper.getObj(iRoleId)
							if oRole:
								newbieGuide.monsterDieEvent(oRole,iMonsterDisNo)
					for iMonsterDisNo in monsterdisData.gdDistribution.get(iSceneNo,[]): #刷新前置波次已刷完的怪物组
						if iMonsterDisNo not in self.sWaitSpawnMst or iMonsterDisNo in self.sHasSpawnedMst:
							continue
						if iMonsterDisNo in self.dAliveMonster or iMonsterDisNo in self.sHasDiedMst:#已经刷出来了,或已经刷完了则跳过(否则若前置条件是第1波,则1,2波刷完都会走到这里,若1先刷完,则2刷完时仍然满足条件,会再次触发刷新)
							continue
						bMeet=True
						for iPreMstOrder in self.getPreOrder(iMonsterDisNo):
							if self.getMstdisByOrder(iSceneNo,iPreMstOrder) not in self.sHasDiedMst:
								bMeet=False
								break
						if bMeet:
							self.spawnMonsterSquad(iMonsterDisNo)
				elif self.isSpawnAfterDie(iMonsterDisNo):
					iSquadInterval=self.getSquadInterval(iMonsterDisNo)
					func=u.cFunctor(self.realSpawnMonsterSquad,iMonsterDisNo)
					self.getHolder().startTimer(func,iSquadInterval)	
		if not self.sWaitSpawnMst and not self.dAliveMonster and not oCurrScene.bTimeOut and not self.sDelaySpawnMonster:
			#当前房间已经清空,设置标记
			oCurrScene.setHasPass()

	#杀死所有已经刷出来的怪物
	def killAllAliveMonster(self):
		oCurrScene=self.getCurrScene()
		if not oCurrScene:
			return
		lRemove=[]
		for lMonsterIds in self.dAliveMonster.values():
			for iMonsterId in lMonsterIds:
				lRemove.append(iMonsterId)
		for iMonsterId in lRemove:
			oMonster=entity.gEntityProxy.getProxy(iMonsterId)
			if oMonster:
				oCurrScene.removeEntity(oMonster)

	#根据矩形中心点和矩形大小计算坐标,9个坐标位
	def calMonsterPos(self,tCenter,tZone):
		#x轴平均单位坐标
		iUnitX=(int)(tZone[0]/3)
		#x轴平均单位坐标
		iUnitY=(int)(tZone[1]/3)
		#索引0-8之间的坐标位置排列对应键盘上小键盘的数字排列
		#s7 s8 s9
		#s4 s5 s6
		#s1 s2 s3
		iS4,iS5,iS6=(tCenter[0]-iUnitX+random.randint(-iUnitX,iUnitX),tCenter[1]+random.randint(-iUnitY,iUnitY)),tCenter,(tCenter[0]+iUnitX+random.randint(-iUnitX,iUnitX),tCenter[1]+random.randint(-iUnitY,iUnitY))
		iS1,iS2,iS3=(iS4[0]+random.randint(-iUnitX,iUnitX),iS4[1]-iUnitY+random.randint(-iUnitY,iUnitY)),(iS5[0]+random.randint(-iUnitX,iUnitX),iS5[1]-iUnitY+random.randint(-iUnitY,iUnitY)),(iS6[0]+random.randint(-iUnitX,iUnitX),iS6[1]-iUnitY+random.randint(-iUnitY,iUnitY)),
		iS7,iS8,iS9=(iS4[0]+random.randint(-iUnitX,iUnitX),iS4[1]+iUnitY+random.randint(-iUnitY,iUnitY)),(iS5[0]+random.randint(-iUnitX,iUnitX),iS5[1]+iUnitY+random.randint(-iUnitY,iUnitY)),(iS6[0]+random.randint(-iUnitX,iUnitX),iS6[1]+iUnitY+random.randint(-iUnitY,iUnitY)),
		tPos=iS1,iS2,iS3,iS4,iS5,iS6,iS7,iS8,iS9
		return random.sample(tPos,9)

	def _ettRemoveEventHandler(self,oEtt,oAttacker):#override
		if oEtt.ettType()!=scene_pb2.INFO_ROLE:
			return entityManager.cEttMngWithConfig._ettRemoveEventHandler(self,oEtt,oAttacker)

#场景管理器
class cTempSceneMng(sceneMng.cTempSceneMng):
	def _createScene(self,iNo):#override
		return cTempScene(iNo,self.getHolder())

	def makeScene(self,iNo):#override
		oScene=sceneMng.cTempSceneMng.makeScene(self,iNo)
		self.oCurrScene=oScene
		
		return oScene

#临时场景
class cTempScene(sceneMng.cTempScene):
	def __init__(self,iNo,oHolder):
		sceneMng.cTempScene.__init__(self,iNo)
		self.iBeginStamp=0
		self.bHasPass=False #是否通过了某个房间
		self.bTimeOut=False #是否超时
		self.oHolder=weakref.ref(oHolder)
		self.lMstTrigger=[] #保存触发刷新点(非地雷)

		self.dKillMonster={} #当前场景击杀怪物数量{编号:数量}

	def getHolder(self):
		return self.oHolder()

	def addMine(self):
		lMineNo=mstTriggerData.gdGroupByScNo.get(self.no(),{}).get('mine',[])
		for iNo in lMineNo:
			oMine=mstTrigger.newMine(iNo,self)
			self.addEntity(oMine,oMine.x,oMine.y)

	def setMstTrigger(self):
		lMstTriggerNo=mstTriggerData.gdGroupByScNo.get(self.no(),{}).get('monster',[])
		for iNo in lMstTriggerNo:
			oMstTrigger=mstTrigger.newMstTrigger(iNo,self)
			oMstTrigger.setup(self.getHolder().getJoinedRoleId())
			self.lMstTrigger.append(oMstTrigger)

	def addTrick(self):#添加机关
		lTrick=trickData.getTrickList(self.no())
		for iTrickNo in lTrick:
			oTrick=trick.new(iTrickNo, self.no())
			self.addEntity(oTrick, oTrick.x, oTrick.y)

	def onBeforeEnter(self,who,oOldScene,iOldX,iOldY,oNewScene,iNewX,iNewY):#override
		sceneMng.cTempScene.onBeforeEnter(self,who,oOldScene,iOldX,iOldY,oNewScene,iNewX,iNewY)		
		#todo:从临时场景切换到永久场景,更新队伍所在场景
		
		oInstance=who.getInstanceObj()	#取消关卡的限时定时器
		if oInstance:
			oInstance.cancleCountDownTimer()

	def _initScene(self, who):
		oInstance=who.getInstanceObj()
		if oInstance:
			oInstance.tryPushPassProgressInfo(who.id)
			oInstance.iBeginStamp=timeU.getStamp() if oInstance.iBeginStamp==0 else oInstance.iBeginStamp #设置关卡开始时间戳
			oInstance.tryPushCountDown(who)	#若当前副本有时间限制,则下发时间给客服端

		#初始化场景中各种实体
		if self.iBeginStamp:
			return False
		self.iBeginStamp=timeU.getStamp()
		self.addMine()	#添加刷怪地雷
		self.addDoor()	#添加传送门
		self.setMstTrigger()	#添加刷怪触发器
		self.addTrick()
		if self.passReq():
			self.dNeed=self.passReq()
		if self.timeLimit():
			self.dTimerId={}
			self.timerMng=timer.cTimerMng()
			self.dTimerId['time']=self.timerMng.run(self.timeOut,self.timeLimit())
		return True

	def onAfterEnter(self,who,oOldScene,iOldX,iOldY,oNewScene,iNewX,iNewY):#override
		sceneMng.cTempScene.onAfterEnter(self,who,oOldScene,iOldX,iOldY,oNewScene,iNewX,iNewY)
		#!#
		return
		bInit=self._initScene(who)
		if bInit:
			self.getHolder().monsterMng.generateWreck()
			self.getHolder().monsterMng.generateMonster()#生成场景怪物

	def hasPass(self):
		return self.bHasPass

	def setHasPass(self):
		if self.bHasPass:
			return
		self.bHasPass=True
		if not self.getHolder().isPassed():
			self.getHolder().sendBornBarrierProg(self.no())
			self.openDoor() #通关则不显示箭头
		self.removeTrigger()#移除各种刷怪触发器
		#触发通过场景对话
		# for iRoleId in self.getEntityIdsByType(scene_pb2.INFO_ROLE):
		# 	oRole=self.getEntityById(iRoleId)
		# 	if not oRole:
		# 		continue
		# 	oRole.taskCtn.triggerTaskDialog(block.blockTask.TASK_DIALOG_PASS_SCENE,scene=self.no())

	def removeTrigger(self):
		self.removeEntityByType(scene_pb2.INFO_MST_TRIGGER)
		self.lMstTrigger=[]

	def timeLimit(self):
		return self.getConfig('timeLimit',0)

	def passReq(self):
		return self.getConfig('passReq',{})

	def checkPassReq(self):#检查是否满足击杀怪物条件
		if getattr(self,'dNeed',{}):
			bMeet=True
			for iNo,iAmount in self.dNeed.iteritems():
				if self.allKilledMonster(iNo)<iAmount:
					bMeet=False
					return False
			if bMeet and not self.bTimeOut:
				self.setHasPass()
				return True
		return False

	def timeOut(self):#超时处理
		self.timerMng.cancel(self.dTimerId.get('time'))
		self.bTimeOut=True
		if not self.bHasPass:
			for iRoleId in self.getEntityIdsByType(scene_pb2.INFO_ROLE):
				ep=mainService.getEndPointByRoleId(iRoleId)
				if ep:
					ep.rpcTips('闯关失败,大侠请重新来过')

	def addKillMinor(self,iNo):#记录玩家杀小怪数量
		self.dKillMonster[iNo]=self.dKillMonster.get(iNo,0)+1

	def allKilledMonster(self,iNo):#所击杀的某种小怪全部数量
		return self.dKillMonster.get(iNo,0)

	def openDoor(self):
		#通知开启下一个房间的传送门(所有人)
		for iDoorId in self.getEntityIdsByType(scene_pb2.INFO_GATE):
			oDoor=self.getEntityById(iDoorId)
			if oDoor:
				oDoor.setState(1)
				oDoor.open()

	def isFightScene(self):#是否是战斗区
		return True

import math
import types
import random

import weakref
import copy
import role
# import monster
import timeU


import miniGame
import consumeParser
import scene

import c
import timer
import mainService
import block
import entity
import scene_pb2
import log

import factory
import factoryConcrete
import sysConfigData
import rand

import sceneMng

#刷新方式
SPAWN_AFTER_DIE=1   #消灭刷新(从上一波怪全部死亡开始计时,时间到刷新下一组)
SPAWN_AFTER_SPAWN=2 #同时刷新(从上一波怪刷出来开始计时,时间到刷新下一组)

#刷新条件
SPAWN_UNCONDITION=0			#无触发条件刷新(含延迟刷,延迟不算触发条件,延迟意味着已经开始计时,即已经触发了)
SPAWN_DIS=1
SPAWN_MINE=2
SPAWN_MONSTER_STATUS=3
SPAWN_SUMMON_SKILL=4
SPAWN_SPAWN=5
SPAWN_WRECK=6				#可破坏物触发

#随机波动范围,90%~105%
NUM_MIN=90 	
NUM_MAX=105 
