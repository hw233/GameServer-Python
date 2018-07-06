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

if 'gePassBarrier' not in globals():
	gePassBarrier=u.cEvent()

if 'gWeakRefMng' not in globals():
	gWeakRefMng=u.cWeakRefManager()

FRIEND_POINT=10#组队增加的友情点

#通关方式有哪些呢??
#杀死boss通关
#获得某种物品n个则通关.
#不限时间杀够{怪a:3个,怪b:2个....}
#限定时间内杀够{怪a:3个,怪b:2个....}
#保护人质不死
#扛多久时间若不死则通关.

#-------------------------
#刷新怪物的方式有哪些??
#拾取了某种物品
#定时刷新怪物
#某怪被杀之后

#副本基类定义
class cInstance(object):
	def __init__(self,iNo):
		self.iNo=iNo #副本编号
		self.timerMng=timer.cTimerMng()#定时器
		self.sceneMng=self.getSceneMng() #场景管理器
		self.launchMng=self.getLaunchMng() #随机投放管理器
		self.monsterMng=self.getMonsterMng() #怪物管理器
		self.monsterMng.eEttRemove+=self.ettRemoveEventHandler #监听移除事件

		self.iBeginStamp,self.iEndStamp=0,0 #副本开始时间戳,副本结束时间戳
		self.bSuccess=False 	#关卡是否成功通关
		self.iHasOpenSceneCnt=1 #已经打通的场景数量
		self.dKillMonster={} #杀死各种怪物的数量,key是怪物的编号
		self.dPassReq={}	#通关要求的各种怪物(物品),数量,key是编号
		#self.bHostageIsExist=True #人质是否存活

		self.lJoinRole=[] #副本参与者
		self.iTeamId=0	#队伍id
		self.bRealTeam=False #是否真正意义上组队(按照进入副本的人数算,超过1人就算组队)
		self.dPoint={} #每个角色得到的积分,key是角色id
		self.dExp={} #每个角色得到的经验,key是角色id
		self.dGold={} #每个角色得到的元宝,key是角色id		
		self.dBossDamage={} #各角色对boss造成的伤害,key是角色id
		self.dRoleDamage={} #各角色累计受到的伤害,key是角色id
		self.dKillMinor={} #各角色杀小怪数量
		#self.iMode=iMode	#关卡模式，1单人，2多人，3PK	
		gWeakRefMng.addObj(self)
		self.hasAwardList={}  #已经翻拍玩家列表
		self.dTimerId={}	#用来存放各种定时器id
		self.bTimeOut=False #超时标记
		self.dScoreInfo={}  #评分信息,{roleid:{}}
		self.oEscortNpc=None  #护送的NPC
		self.dAwardList={} #获得的物品列表,{玩家ID:{物品No:数量}}  通关结束给予玩家
		self.dHpBottle={}	#关卡血瓶信息
		self.dPassAndCardInfo={}	#玩家的通关信息{roleId:[step, info]}
		self.iAiRoleId=0	#AI同步目标角色ID
		
		self.dPassAwardList={}	#通关投放的物品列表,用于向客户端发送通关信息

		self.lCheckPassFunc=[]	#监听是否达到通关条件

	def isActivity(self):#不是活动本
		return False

	def setVipExtraMsg(self, who, oPassInfo):##由基类提供
		pass

	def setVipExtra(self, who, iNo, iAmount):
		return iAmount

	def addhasAwardRoleId(self,iRoleId,iType,iPos,award):
		self.hasAwardList.setdefault(iType,{})[iRoleId]=self.hasAwardList.setdefault(iType,{}).get(iRoleId,0)+1 #翻牌次数加1
		#记录下本次翻牌信息
		if not self.dPassAndCardInfo[iRoleId] or self.dPassAndCardInfo[iRoleId][0]!=CARD_STEP:	#其实可以去掉
			return	
		cardInfo=self.dPassAndCardInfo[iRoleId][1]
		choosedInfo=cardInfo.hasChoosed.add()
		choosedInfo.iPos=iPos
		choosedInfo.iIcon=award.iIcon
		choosedInfo.iNum=award.iNum
		choosedInfo.sName=award.sName
 		choosedInfo.iType=iType
 		choosedInfo.iColor=award.iColor

 	def addNothasAwardRoleId(self,iRoleId,iType, award):#记录没有翻牌翻中的信息
 		cardInfo=self.dPassAndCardInfo[iRoleId][1]
		notChoosedInfo=cardInfo.notHasChoosed.add()
		notChoosedInfo.iPos=award.iPos
		notChoosedInfo.iIcon=award.iIcon
		notChoosedInfo.iNum=award.iNum
		notChoosedInfo.sName=award.sName
 		notChoosedInfo.iType=iType
 		notChoosedInfo.iColor=award.iColor

	def isHasAward(self,iRoleId,iType,iFrequency):#frequency为翻了多少次
		return self.hasAwardList.get(iType,{}).get(iRoleId,0)==iFrequency

	def getSceneMng(self):#场景管理器,如果你的子类想要一个不同的manager,请在你的子类override这个函数,并返回你想要的manager
		return helperClass.cTempSceneMng(self)

	def getLaunchMng(self):#投放管理器,如果你的子类想要一个不同的manager,请在你的子类override这个函数,并返回你想要的manager
		return helperClass.cLaunchMng('关卡{}'.format(self.iNo),barrierLaunchData.gdData)

	def getMonsterMng(self):#怪物管理器,如果你的子类想要一个不同的manager,请在你的子类override这个函数,并返回你想要的manager
		return helperClass.cMonsterMng(self)

	def getTrapMng(self):#机关管理器,如果你的子类想要一个不同的manager,请在你的子类override这个函数,并返回你想要的manager
		return entityManager.cTrapMngWithConfig(self)

	def getNpcMng(self):#npc管理器,如果你的子类想要一个不同的manager,请在你的子类override这个函数,并返回你想要的manager
		return entityManager.CNpcMngWithConfig(self)

	# def mode(self):#关卡模式，1单人，2多人，3PK
	# 	return self.iMode

	def clearRecordByRoleId(self,iRoleId):#清除某个人的信息记录
		t=(self.dPoint,self.dExp,self.dGold,self.dRoleDamage,self.dKillMinor,self.dBossDamage)
		for d in t:
			d.pop(iRoleId,None)

	def getCurrScene(self):
		return self.sceneMng.oCurrScene

	def setTeamId(self,iTeamId):#设置队伍id
		self.iTeamId=iTeamId

	def teamId(self):#队伍id
		return self.iTeamId

	def teamObj(self):#队伍实例
		return team.gTeamProxy.getProxy(self.iTeamId)

	def bossDamage(self,who):#玩家对boss伤害的百分比
		iDividend=self.dBossDamage.get(who.id,0)
		iDivisor=sum(self.dBossDamage.values())
		if iDivisor<=0:
			return 0
		else:
			return int(100.0*iDividend/iDivisor)

	def no(self):#关卡编号
		return self.iNo

	def kind(self):
		return barrierData.getConfig(self.no(), 'barrierKind')

	def diffName(self):#难度名称
		return {0:'普通',1:'困难',2:'噩梦',3:'王者'}[self.iDiff]

	def getJoinedRoleDict(self):
		return copy.copy(self.lJoinRole)

	def getJoinedRoleId(self):#副本内全部玩家id
		return self.lJoinRole

	def joinedRoleCnt(self):#副本内玩家的个数
		return len(self.lJoinRole)

	def removeEntity(self):#删掉全部实体,打扫战场
		self.monsterMng.removeAllEtt()	#清除怪物
		#self.trapMng.removeAllEtt()	#清除机关
		#self.npcMng.removeAllEtt()		#清除npc
		#self.goodsMng.removeAllEtt()	#清除地上的物品

	#刷新评分信息
	def flushScoreInfo(self,roleId,iType,iValue):
		self.dScoreInfo[roleId][iType]=self.dScoreInfo.setdefault(roleId,{}).setdefault(iType,0)+iValue

	#更新角色被某类型怪物攻击次数	
	def flushAttTime(self,iRoleId,iEntityType):
		self.dScoreInfo[iRoleId][ATT_TIME][iEntityType]=self.dScoreInfo.setdefault(iRoleId,{}).setdefault(ATT_TIME,{}).get(iEntityType,0)+1
		
	def getScoreInfo(self,roleId,iType):
		return self.dScoreInfo.get(roleId,{}).get(iType,0)

	def isTargetDrop(self, iDropNo):#判断是否是目标掉落物
		return getattr(self, 'bCollectProps', False) and iDropNo in self.dNeed

	def isSpawnTargetMonster(self, iMonsterNo):
		return getattr(self, 'bKillAssignMons', False) and iMonsterNo in self.dNeed

	#怪物死亡触发
	def triggerMonsterDie(self,oMonster,oAttacker):
		oHolderScene=oMonster.getHolderScene()
		if oHolderScene:
			oHolderScene.removeEntity(oMonster,oAttacker)

	def _doDrop(self, oMonster, bOverFPAward):#bOverFPAward是否首通覆盖
		oCurrScene=self.getCurrScene()
		if not oCurrScene:
			raise Exception,'没有找到当前场景'
		uLaunchGroup, bIsBoss=oMonster.launch(), oMonster.isBoss()
		if bIsBoss and getattr(self, 'bKillMonstBrew', False):	#指定杀多少波怪物掉落参见 incrMoneterBrew函数
			return
		if isinstance(uLaunchGroup,list):
			lLaunchGroup=uLaunchGroup
		else:
			lLaunchGroup=[]
			lLaunchGroup.append(uLaunchGroup)
		dLaunch, lDropProps={}, []	#缓存本次投放信息
		for iLaunchGroup in lLaunchGroup:
			if not iLaunchGroup:
				continue
			bDropFirstPassAward=False 	#是否掉落首通
			for iRoleId in self.lJoinRole:
				who=role.gKeeper.getObj(iRoleId)
				if not who:
					continue
				lDrop=self.launchMng.launch(who,iLaunchGroup)
				if oMonster.isBoss() and bOverFPAward and who.barrier.isFirstPass(self.no()):
					#将首通奖励添加到boss身上
					iFirstPassAward=barrierData.getConfig(self.no(), 'firstaward')
					if iFirstPassAward:
						lFirstPassAward=self.launchMng.launch(who,iFirstPassAward)
						lDrop=lFirstPassAward  #如果掉落了首通奖励,就不会在掉落boss本身的掉落物品
						bDropFirstPassAward=True	
				for (iPropsNo,iAmount,tPropsArgs,dPropsArgs,bIsBind,sAnnounce) in lDrop:
					spoils=drop.cSpoils(oCurrScene,iPropsNo,iAmount,oMonster.id,iRoleId)  #生成一个战利品对象并加入场景
					spoils.x = who.x+random.randint(0,50)
					spoils.y = who.y+random.randint(0,50) #设置掉落坐标
					spoils.setDropTarget(self.isTargetDrop(iPropsNo))	#设置是否是目标掉落物
					oCurrScene.addEntity(spoils,0,0)  #加入场景,掉落是独立的,不需要广播所有玩家
					if not spoils.isHpDrug() and not spoils.isMpDrug():#不是红蓝
						self.dAwardList.setdefault(iRoleId,{})[iPropsNo]=self.dAwardList.get(iRoleId,{}).get(iPropsNo, 0)+iAmount	#缓存角色获得的物品
						dLaunch.setdefault(iRoleId,{})[iPropsNo]=dLaunch.get(iRoleId, {}).get(iPropsNo, 0)+iAmount
						lDropProps.append(spoils)
			if bDropFirstPassAward:
				break			
		if bIsBoss:
			self.dPassAwardList=dLaunch	#缓存投放奖励,用于向客户端发送奖励信息
			for oDrop in lDropProps:
				oDrop.setPropsShamePick(True)		

	#掉落物品处理
	def DropHandler(self,oMonster):
		self._doDrop(oMonster, True)

	def tacitAdd(self):
		iDegree=barrierData.gdData[self.iNo].get('degree',0)
		return tacitData.getTacitAdd(iDegree)

	def setInstancePass(self,bSendSlowMotion=True):#bSendSlowMotion是否发送慢动作
		if self.iEndStamp:
			return
		self.bSuccess=True 	#成功通关了
		self.iEndStamp=timeU.getStamp()
		oCurrScene=self.getCurrScene()  #拿到当前场景对象,在怪物管理器中缓存有
		if not oCurrScene:
			return
		oCurrScene.setHasPass()	#设置当前场景通过
		self.monsterMng.killAllAliveMonster()
		self.monsterMng.stopSpawnMonster()	#设置停止刷怪标志
		self.sendPassAwardToAllRole()

		if not self.bRealTeam and self.lJoinRole and storyChat(self.lJoinRole[0],oCurrScene.no(),2):
			pass

		for iRoleId in self.lJoinRole:	#下发通关奖励
			ep=mainService.getEndPointByRoleId(iRoleId)
			if not ep:
				continue
			if bSendSlowMotion:
				ep.rpcClientSlowMotion()	#通知客户端播放通关慢动作
			#向客户端请求战斗信息,例如 连击,连击杀伤率等信息,然后下发通关结算
			job=gevent.spawn(ep.rpcClientBarrierRecord)	
			func=u.cFunctor(self.passBarrier,iRoleId)
			job.link(func)

			# oRole=role.gKeeper.getObj(iRoleId)
			# #增加默契值,友情点
			# for iFriendId in self.lJoinRole:
			# 	if iFriendId==iRoleId:
			# 		continue
			# 	if iFriendId in oRole.friendCtn.getAllKeys():
			# 		ep2=mainService.getEndPointByRoleId(iFriendId)#防止掉线后两边默契值不同步
			# 		if not ep2:
			# 			return
			# 		oRole.friendCtn.getItem(iFriendId).addTacit(self.tacitAdd())
			# 		oRole.active.addFriendPoint(FRIEND_POINT,'组队下副本',None)

	def ettRemoveEventHandler(self,oEtt,oAttacker):	#副本内ett移除事件
		iEttType=oEtt.ettType()
		bMonster=(iEttType==scene_pb2.INFO_MONSTER or iEttType==scene_pb2.INFO_WRECK)
		if bMonster:	#怪物
			self.monsterRemoveEventHandler(oEtt, oAttacker)
		self.addPassReq(oEtt, bMonster, oAttacker)
		for func in self.lCheckPassFunc:	#判断是否通关
			if not func(oEtt, oAttacker):
				return

		self.setInstancePass()

	def monsterRemoveEventHandler(self,oMonster,oAttacker):#监听怪物被杀事件
		iMonsterId=oMonster.id  #怪物ID
		oCurrScene=self.getCurrScene()  #拿到当前场景对象,在怪物管理器中缓存有
		if not oCurrScene:
			return
		self.monsterMng.removeFromAliveList(iMonsterId)
		#触发掉落,以杀死该怪物的角色来计算相应掉落,拾取掉落的逻辑是在掉落物品的trigger方法中
		self.DropHandler(oMonster)

		oCurrScene.addKillMinor(oMonster.no()) #场景杀怪数统计

		self.addKillMinor(oMonster,oAttacker) #副本杀怪数统计与任务触发

		#判断是否满足通过场景条件(击杀指定怪物多少只)
		oCurrScene.checkPassReq()

	#判断当前场景是否是最后一个场景
	def isLastBarrierScene(self,*args):
		oCurrScene=self.getCurrScene()
		iNextSceneNo=oCurrScene.no()+1  #假设下一个场景存在
		if iNextSceneNo in sceneData.gdData and sceneData.gdData.get(iNextSceneNo).get('barrier')==self.no():
			return False
		return True

	def isPassed(self):
		return self.iEndStamp!=0#是否已经通关

	def passExp(self):#通关每个玩家将获得的经验
		return self.getConfig('passExp',0)

	#若关卡没有boss掉落,则发放关卡奖励给玩家作为通关奖励	
	def _launchPassAward(self, dLaunchGroup):	
		oCurrScene=self.getCurrScene()
		if not oCurrScene:
			raise Exception, '场景丢失'
		for iRoleId in self.lJoinRole:
			oRole=role.gKeeper.getObj(iRoleId)
			if not oRole:
				continue
			uLaunchGroup=dLaunchGroup.get(iRoleId, [])
			lLaunchGroup = uLaunchGroup if isinstance(uLaunchGroup, list) else [uLaunchGroup]
			for iLaunchGroup in lLaunchGroup:
				lDrop=self.launchMng.launch(oRole,iLaunchGroup)
				for (iPropsNo,iAmount,tPropsArgs,dPropsArgs,bIsBind,sAnnounce) in lDrop:
					spoils=drop.cSpoils(oCurrScene,iPropsNo,iAmount,10000,iRoleId)  #生成一个战利品对象并加入场景
					spoils.x = oRole.x+random.randint(0,50)
					spoils.y = oRole.y+random.randint(0,50) #设置掉落坐标
					spoils.setDropTarget(self.isTargetDrop(iPropsNo))	#设置是否是目标掉落物
					oCurrScene.addEntity(spoils,0,0)  #加入场景,掉落是独立的,不需要广播所有玩家
					if not spoils.isHpDrug() and not spoils.isMpDrug():#不是红蓝
						spoils.setPropsShamePick(True)
						self.dAwardList.setdefault(iRoleId,{})[iPropsNo]=self.dAwardList.get(iRoleId,{}).get(iPropsNo, 0)+iAmount	#缓存角色获得的物品
						self.dPassAwardList.setdefault(iRoleId,{})[iPropsNo]=self.dPassAwardList.get(iRoleId, {}).get(iPropsNo, 0)+iAmount

	#玩家通关后发送通关奖励给玩家
	def sendPassAwardToAllRole(self, dLaunchGroup=None):
		if not self.dPassAwardList:#没有boss掉落(通关奖励)
			if dLaunchGroup==None:
				dLaunchGroup={}
				for iRoleId in self.lJoinRole:
					oRole=role.gKeeper.getObj(iRoleId)
					sAwardKind = 'firstaward' if oRole.barrier.isFirstPass(self.no()) else 'passaward'
					dLaunchGroup[iRoleId]=barrierData.getConfig(self.no(), sAwardKind, [])
			self._launchPassAward(dLaunchGroup)
		for iRoleId in self.lJoinRole:
			oRole=role.gKeeper.getObj(iRoleId)
			if not oRole:
				return
			for iPropsNo, iAmount in self.dPassAwardList.get(iRoleId,{}).iteritems():
				iAmountNew = self.setVipExtra(oRole, iPropsNo, iAmount)
				if iAmountNew != iAmount:
					self.dPassAwardList.get(iRoleId,{})[iPropsNo]=iAmountNew
					iAmount = iAmountNew

				log.log('instance_launch', '角色ID{}:在关卡:{}获得{}*{}'.format(oRole.id, self.no(), misc.getNameByNo(iPropsNo), iAmount))
				log.log('ddic/instanceLaunch','\t{}\t{}\t{}\t{}\t{}\t{}'.format(oRole.id,oRole.name,self.no(),self.name,iPropsNo,iAmount))
				self.launchMng.launchBySpecify(oRole, iPropsNo, iAmount, (), {}, False,'怪物掉落', None)	
				
	#发送客服端翻牌信息
	def _dealCardLogic(self, iRoleId):
		ep=mainService.getEndPointByRoleId(iRoleId)	
		if not ep:
			return
		iShowAccountBtn = getShowAccountBtn(iRoleId, self.no()) 	
		#策划要求屏蔽翻牌界面	
		ep.rpcClientShowAccount(iShowAccountBtn)
		return	

		iStep=self.dPassAndCardInfo[iRoleId][0]
		if iStep==CARD_STEP:
			cardInfo=self.dPassAndCardInfo[iRoleId][1]
			iFreeAwardTime, iPayAwardTime=cardInfo.iFreeAwardTime, cardInfo.iPayAwardTime	#免费翻牌次数,付费翻牌次数
			for chossedInfo in cardInfo.hasChoosed:
				if chossedInfo.iType==c.PASS_AWARD_FREE:	iFreeAwardTime-=1
				elif chossedInfo.iType==c.PASS_AWARD_PAY:	iPayAwardTime-=1
			iFreeAwardTime,iPayAwardTime=max(iFreeAwardTime, 0), max(iPayAwardTime, 0)
			if iFreeAwardTime==0 and iPayAwardTime==0:	#翻完所有的牌
				ep.rpcClientShowAccount(iShowAccountBtn)
				return
			cardInfo.iFreeAwardTime, cardInfo.iPayAwardTime=iFreeAwardTime,iPayAwardTime
		elif iStep==BALANCE_STEP:
			self.dPassAndCardInfo[iRoleId]=[CARD_STEP, self._makeCardInfo(iRoleId)]
		cardInfo=self.dPassAndCardInfo[iRoleId][1]
		ep.rpcClientShowChooseCard(cardInfo)	#下发翻牌信息
		oRole=role.gKeeper.getObj(iRoleId)
		if not oRole:
			return
		newbieGuide.awardEvent(oRole)
	
	def _makeStar(self, who, iMaxHit):#计算星星数量
		iDegree = self.getConfig('degree')
		if iDegree <= 1: ##普通关卡评分
			iRemain = self.dHpBottle[who.id]
			iHpPot = self.getConfig('hpbot', 0)
			iUsed = iHpPot - iRemain
			if iUsed == 0:
				return 3
			elif iUsed == 1:
				return 2
			else:
				return 1
		else:##噩梦以上难度
			iRemain = (who.hp*1.0 / who.hpMax) * 100
			if iRemain >= 70:
				return 3
			elif iRemain >= 40:
				return 2
			else:
				return 1
		return 0
		iScore=0
		iPassSceond=self.passCostSecond()
	 	if iPassSceond<=self.getConfig('singlePreTime' if not who.getTeamObj() else 'teamPreTime', iPassSceond+1):
	 		iScore+=2  #没有加时加2分
	 	if getattr(who, 'iDieTimes', 0)<=0: #没有死亡加2分
	 		iScore+=2
	 	if iMaxHit>=50:
	 		iScore+=1  #连击数有50或以上加1分
	 	iStar=gdStar.get(iScore,0)
	 	who.iPassBarrierStar=iStar
	 	return iStar
	
	def _makePassAward(self, iRoleId, lPassAward):
	 	if not self.dPassAwardList:#没有通关奖励
	 		raise Exception, '关卡{},类型{}无通关奖励信息'.format(self.no(), self.passKind())
	 	dLaunch=self.dPassAwardList.get(iRoleId, {})
	 	for iPropsNo, iAmount in dLaunch.iteritems():
	 		passAward=lPassAward.add()
	 		passAward.iIcon=misc.getIconByNo(iPropsNo)
	 		passAward.iNum=iAmount
	 		passAward.sName=misc.getNameByNo(iPropsNo)
	 		passAward.iColor=misc.getColorByNo(iPropsNo)

	def _makePassExpAndGold(self, iRoleId, oPassInfo):
		oRole=role.gKeeper.getObj(iRoleId)
		iAddExp=0 if not oRole else oRole.level * 5 * self.getConfig('vitality', 1)	#消耗体力增加经验
		oPassInfo.iExp='{}经验'.format(self.dPassAwardList.get(iRoleId, {}).pop(c.EXP, 0) + iAddExp)
		oPassInfo.iGold=self.dPassAwardList.get(iRoleId, {}).pop(c.GOLD, 0)

	#生成通关结算信息
	def _makePassInfo(self,job,iRoleId):
		iMaxHit=job.value[1].iMaxHit  #最大连接
		iHKRate=job.value[1].iHKRate  #连击杀伤率

		passInfo=barrier_pb2.passInfo() #通关信息
		iBarrierNo=self.no()
		self._makePassExpAndGold(iRoleId, passInfo)
		# iExp=barrierData.getConfig(iBarrierNo,'exp')
		# passInfo.iExp='{}经验'.format(iExp)
		passInfo.iTime=self.passCostSecond()
		# passInfo.iGold=barrierData.getConfig(iBarrierNo,'gold')  #通关奖励元宝
		passInfo.iDeadTime=self.getScoreInfo(iRoleId,DEAD_TIME)  #死亡次数
		who=role.gKeeper.getObj(iRoleId)
		if not who.getTeamObj():
			iScore=barrierData.scoreSigal(self.getConfig('fixedScore'),passInfo.iDeadTime,self.getConfig('singlePreTime'),passInfo.iTime,iMaxHit,iHKRate)
		else:
			iTotalHp=0
			for dInfo in self.dScoreInfo.itervalues():
				iTotalHp+=dInfo.get(HURT_TOTAL,0)
			iHurt=0
			if iTotalHp>0:
				iHurt=int((self.getScoreInfo(iRoleId,HURT_TOTAL)/float(iTotalHp))*100)
			iScore=barrierData.scoreTeam(self.getConfig('fixedScore'),passInfo.iDeadTime,self.getConfig('teamPreTime'),passInfo.iTime,iMaxHit,iHKRate,iHurt)
			passInfo.iHurt=iHurt  #伤害比,组队才下发
		passInfo.iStar=self._makeStar(who,iMaxHit)
		self._makePassAward(iRoleId, passInfo.lPassAward)	#通关奖励信息
		# passInfo.iStar=barrierData.star(iScore,who.getTeamObj())  #星星
		passInfo.iBestTime=min(passInfo.iTime, who.barrier.getBestPassTime(iBarrierNo))
		passInfo.iMaxComb=max(iMaxHit, who.barrier.getMaxComb(iBarrierNo))
		passInfo.iLoseTime=min(passInfo.iDeadTime, who.barrier.getLoseDieTime(iBarrierNo))
		who.barrier.updateUseTimeAndHitAndDieTie(iBarrierNo, passInfo.iTime, iMaxHit, passInfo.iDeadTime)	#记录最佳时间,最大连击,最少死亡次数
		log.log('barrierScore','{}({})通关{},保底分数{},死亡次数{},通关时间{},连击数{},杀伤率{},评分{},星星{}'.format(who.name,who.id,self.name,self.getConfig('fixedScore'),passInfo.iDeadTime,passInfo.iTime,iMaxHit,iHKRate,iScore,passInfo.iStar))
		log.log('ddic/barrierScore','\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(who.id,who.name,self.no(),self.name,passInfo.iDeadTime,passInfo.iTime,iMaxHit,iHKRate,iScore,passInfo.iStar))
		who.barrier.updateScoreAndStar(iBarrierNo,iScore,passInfo.iStar)	#记录最高分数和星数
		passInfo.sBarrierName=self.name
		#是否完美首通,首通+6星
		# passInfo.iPerfectFirpassGold=self.getConfig('addGold') if who.barrier.isFirstPass(iBarrierNo) and  passInfo.iStar==6 else 0
		self.setVipExtraMsg(who, passInfo)
		return passInfo

	#生成翻牌信息
	def _makeCardInfo(self, iRoleId):
		chooseCardInfo=barrier_pb2.chooseCardInfo() #通关信息
		iBarrierNo=self.no()
		chooseCardInfo.iFreeAwardTime=barrierData.getConfig(iBarrierNo,'freefrequency')
		chooseCardInfo.iPayAwardTime=barrierData.getConfig(iBarrierNo,'payfrequency')
		chooseCardInfo.iPayAwardVIPTime=0
		chooseCardInfo.iPayType=barrierData.getConfig(iBarrierNo,'paytype')  #付费类型  1元宝  2钻石
		chooseCardInfo.iAwardPrice=barrierData.getConfig(iBarrierNo,'pay')  #付费价格
		who=role.gKeeper.getObj(iRoleId)
		if who.barrier.hasFirstPass(iBarrierNo):
			chooseCardInfo.iPayType=barrierData.getConfig(iBarrierNo,'firstpaytype')  #付费类型  1元宝  2钻石
			chooseCardInfo.iAwardPrice=barrierData.getConfig(iBarrierNo,'firstpay')  #付费价格
			if chooseCardInfo.iAwardPrice>0 and who.lazy.fetch('rpf', 1):#rpc是否出现付费翻牌提示
				chooseCardInfo.iReminder=2
				who.lazy.set('rpf', 0)
			elif chooseCardInfo.iAwardPrice==0 and  who.lazy.fetch('rff', 1):
				chooseCardInfo.iReminder=1
				who.lazy.set('rff', 0)
		chooseCardInfo.iStar=getattr(who,'iPassBarrierStar',0)
		return chooseCardInfo

	def _savePassDataAndSendTaskInfo(self,job,iRoleId):
		who=role.gKeeper.getObj(iRoleId)
		passInfo=self._makePassInfo(job, iRoleId)	#生成通关信息
		iBarrierNo=self.no()
		ep=mainService.getEndPointByRoleId(iRoleId)
		if not ep:
			return
		who.barrier.setPass(iBarrierNo)	#激活关卡
		iTrickAttTime=self.dScoreInfo.get(iRoleId,{}).get(scene_pb2.INFO_TRICK, 0)	#角色被机关攻击次数
		iDegree=self.getConfig('degree', 1)
		who.triggerEvent(event.PASS_FB, self.no(), self.bRealTeam, passInfo.iStar, job.value[1].iMaxHit, self.getScoreInfo(iRoleId,DEAD_TIME),iTrickAttTime,iDegree)

		#完成任务发送TIPS
		# lBackTownSubmit=who.taskCtn.getBackTownSubmit()
		# if lBackTownSubmit:
		# 	tips=task_pb2.operateTips()
		# 	tips.iState=1 #1表示已完成
		# 	for iTaskNo in lBackTownSubmit:
		# 		oTask=who.taskCtn.getItem(iTaskNo)
		# 		if not oTask:
		# 			continue
		# 		tip=tips.taskTips.add()
		# 		tip.iTaskType=oTask.taskType()
		# 		tip.sTaskName=oTask.name
		# 	ep.rpcClientTips(tips)
		return passInfo
	
	def sendBornBarrierProg(self, iSceneNo):#新手关卡通关进度,iSceneNo已通关的场景
		if self.iNo != c.NEW_ROLE_BORN_BARRIER_NO or not self.getCurrScene().hasPass() or self.iEndStamp:
			return
		iIndex=sceneData.dBarrierToSceneList[self.iNo].index(iSceneNo)+1
		if iIndex==len(sceneData.dBarrierToSceneList[self.iNo]):#过滤掉最后一个场景
			return
		for iRoleId in self.lJoinRole:
			ep=mainService.getEndPointByRoleId(iRoleId)
			if ep:ep.rpcClientRecvFreshPass(iIndex)

	#通关处理
	def passBarrier(self,job,iRoleId):
		who=role.gKeeper.getObj(iRoleId)
		iBarrierNo=self.no()
		if not who:
			return
		statistics.addInstancePass(who.level)
		if self.iNo==c.NEW_ROLE_BORN_BARRIER_NO:
			ep=mainService.getEndPointByRoleId(iRoleId)
			ep.rpcClientRecvFreshPass(0)	#表示新手关卡最后一个场景 
			return
		passInfo=self._savePassDataAndSendTaskInfo(job, iRoleId)
		if not self.bRealTeam:#判断首通,单人通关才会触发首通
			who.barrier.addFirstPass(iBarrierNo)	
		self.dPassAndCardInfo[iRoleId]=[BALANCE_STEP, passInfo]
		#通关这一关开放强化按钮,先写死
		if self.no()==ENHANCE:
			who.lazy.set('ce',1)
		#设置新手引导标志,等出了关卡后执行
		if self.no() in newbieGuideData.gdPassFb:
			newbieGuide.passFbEvent(who,self.no())
		#设置通关
		who.bPassStory=True
		#发包通知玩家通关了
		ep=mainService.getEndPointByRoleId(iRoleId)
		if not ep:
			return
		svcFunction.addUnlockAndNoticeFunction(who,ep,2,iBarrierNo)
		bFail,bRes=ep.rpcClientBarrierPass(passInfo)	#返回值代表结算显示完成
		iCostRest=self.getConfig('vitality', 0) ##胜利后扣除体力加经验
		if iCostRest:
			who.addRest(-iCostRest, '胜利关卡消耗', None)
		if not bFail:
			self._dealCardLogic(iRoleId)


	def getConfig(self,sKey,uDefault=None):#查对应关卡策划数据
		return barrierData.getConfig(self.no(),sKey,uDefault)

	def passCostSecond(self):#通关消耗时间
		return abs(self.iEndStamp - self.iBeginStamp)

	def addKillMinor(self,oMonster,oAttacker):#记录玩家杀小怪数量
		iMonsterNo=oMonster.no()
		if oAttacker:
			iAttackerId=oAttacker.id
			self.dScoreInfo[iAttackerId][MONSTER_KILLED][iMonsterNo]=self.dScoreInfo.setdefault(iAttackerId,{}).setdefault(MONSTER_KILLED,{}).get(iMonsterNo,0)+1
		self.dKillMonster[iMonsterNo]=self.dKillMonster.get(iMonsterNo,0)+1

		#触发角色身上监听的杀怪事件(任务等)
		for iRoleId in self.lJoinRole:
			oRole=role.gKeeper.getObj(iRoleId)
			if not oRole:
				continue
			ep=mainService.getEndPointByRoleId(iRoleId)
			if not ep:
				continue
			# oRole.triggerEvent(event.KILL_MONSTER,oMonster.no())  #触发任务
			# #触发杀死怪物场景对话
			# oRole.taskCtn.triggerTaskDialog(block.blockTask.TASK_DIALOG_KILL_MONSTER,monster=iMonsterNo)

	def killMinorCnt(self,iRoleId):#玩家杀小怪总数
		iCounter=0
		dKilled=self.dScoreInfo.get(iRoleId,{}).get(MONSTER_KILLED,{})
		for iNo,iCnt in dKilled.iteritems():
			iCounter+=iCnt
		return iCounter

	def killMinorCntNo(self,iRoleId,iNo):#玩家所杀某种小怪数
		return self.dScoreInfo.get(iRoleId,{}).get(MONSTER_KILLED,{}).get(iNo,0)

	def allKilledMonster(self,iNo):#死亡的某种小怪全部数量(包括非玩家击杀的)
		return self.dKillMonster.get(iNo,0)

	def initFirstScene(self):#初始化副本的第1个场景
		iSceneNo,x,y=self.getInitPos()
		self.sceneMng.makeScene(iSceneNo)

	# def addClock(self,who,iBarrierNo):#增加倒计时小控件
	# 	#需要遍历任务列表决定是否添加clock吗???
	# 	iTimeout=self.getConfig('passTime',0)
	# 	if iTimeout:
	# 		pass
			#who.ep.rpcClock
			
	#启动定时器
	def startTimer(self,func,iInterval):
		return self.timerMng.run(func,iInterval)

	#停止一个定时器
	def stopTimer(self,iTimerID):
		b=self.timerMng.cancel(iTimerID)

	#玩家进入
	def onEnter(self,who,oTeam=None,bBroadcast=True,bTaskTips=True):#队伍进入的时候,需要对队员进行for循环调用此函数	
		#死亡,掉线,移除,重连
		#组队AI同步,怎么处理,怪物血量同步需要显示不?
		iBarrierKind=self.getConfig('barrierKind', 0)
		for iRoleId in self.lJoinRole:
			oRole=role.gKeeper.getObj(iRoleId)
			if not oRole:
				continue
			oRole.propsCtn.clearRecEquip()	#清空上一次新获取装备的缓存	
			#self.addClock(who,self.no()) #给客户端增加倒计时器,由tryPushCountDown实现
			oRole.setInstanceObj(self)#玩家直接持有副本实例(组队则是多个队友共同持有副本实例)
			oRole.setDieHandler(self.roleDieEventHandler) #玩家死亡处理函数
			#who.eBeAttack+=self.Player_BeAttack #关注玩家被攻击事件
			oRole.eRemove+=self.roleRemoveEventHandler #关注玩家remove事件
			oRole.eReLogin+=self.roleReLogin
			oRole.eDisConnected+=self.roleDisconnectHandler	#关注角色掉线事件
			#todo:如果是限时通关副本,要挂定时器
			#event.addObserver(event.LOGIN,self.Role_Login,who)
			#重连复活提示框
			oRole.eReLogin+=self.reLoginAliveCheck
			#监听移动事件
			# oRole.eSceneMove+=self.monsterMng.triggerMonsterFlush
			oRole.triggerEvent(event.ENTER_FB, iBarrierKind)
			#数据字典日志:角色ID  用户来源   用户账号   关卡类型
			log.log('ddic/enterInstance', '\t{}\t{}\t{}\t{}'.format(iRoleId, oRole.accountObj.sUserSource, oRole.accountObj.sUserSource, self.getConfig('degree', 0)))


		oScene=self.getCurrScene()
		if not oScene:
			return
		iSceneNo,x,y=self.getInitPos()
		if not scene.tryTransfer(who,oScene.id,x,y):
			return
		self.tryPushEscortData()	
		self.sendHpBtnInfo()	#发送关卡血瓶信息
		self.sendTeamAndAIInfo()	#发送队伍信息和AI玩家信息]
		self.sendGuide()		#推送新手引导消息
		if bTaskTips:#是否提示任务	
			self.pushTaskStartTips(bBroadcast)


	def sendGuide(self):	#推送新手引导信息
		for iRoleId in self.lJoinRole:
			oRole = role.gKeeper.getObj(iRoleId)
			if oRole:	newbieGuide.sendInBarrierGuide(oRole)

	#下发队伍信息及AI玩家信息	
	#iRoleId指定角色,没有则为所有队员
	#bSendTeamInfo是否发送队伍信息	
	def sendTeamAndAIInfo(self,iRoleId=None,bSendTeamInfo=False):
		if not self.bRealTeam:
			return
		oTeam=role.gKeeper.getObj(self.lJoinRole[0]).getTeamObj()
		if not oTeam:
			raise Exception, '队伍信息丢失'
		lRoleId=[iRoleId] if iRoleId else self.lJoinRole
		if not self.iAiRoleId:
			self.iAiRoleId=lRoleId[0]
		for iRoleId_1 in lRoleId:
			ep=mainService.getEndPointByRoleId(iRoleId_1)
			if ep:
				ep.rpcChangeAiRoleId(self.iAiRoleId)	#切换AI玩家
		if not bSendTeamInfo:
			return
		for iRoleId in lRoleId:
			ep=mainService.getEndPointByRoleId(iRoleId)
			ep.rpcPushTeamInfo(oTeam.teamInfo())

	def sendHpBtnInfo(self, iRoleId=None):#血瓶信息
		#先做个最最简单的功能
		iHpPot=self.getConfig('hpbot', 0)
		if not self.dHpBottle:
			for iRoleId in self.lJoinRole:
				self.dHpBottle[iRoleId]=iHpPot
		if iHpPot<=0:
			return
		
		lRoleId=self.lJoinRole if iRoleId==None else [iRoleId]
		for iRoleId in lRoleId:
			oRole=role.gKeeper.getObj(iRoleId)
			# if not oRole or oRole.level<2:
			if not oRole:
				continue	
			ep=mainService.getEndPointByRoleId(iRoleId)
			if not ep:
				continue
			ep.rpcBarrierHpBtn(self.dHpBottle[iRoleId])	

	def tryPushEscortData(self, iRoleId=None):#发送保护npc对话数据
		if not getattr(self, 'bProtectEscort', False):
			return
		iEscortNo=escortData.getMonsterNo(self.no())
		dEscortData=escortData.gdDialogData.get(iEscortNo, {})
		if not dEscortData:
			return
		escortDialog=scene_pb2.escortDialog()
		escortDialog.bLoop=bool(dEscortData['loop'])
		escortDialog.iId=self.oEscortNpc.id
		for sDialog in dEscortData['dialog']:
			dialogMsg=escortDialog.talks.add()
			dialogMsg.sContent=sDialog
			dialogMsg.iDelay=dEscortData['duration']
		#发送npc对话到客户端	
		lRoleId = [iRoleId] if iRoleId else self.lJoinRole
		for iRoleId in lRoleId:
			ep=mainService.getEndPointByRoleId(iRoleId)
			if not ep:
				continue
			ep.rpcEscortDialog(escortDialog)	
			
	def tryPushPassProgressInfo(self, iRoleId):#下发通关进度消息
		if self.passKind()==1:#击杀boss通关  1:硬编码
			return
		msg=barrierData.getBarrierPassProgressInfo(self.no())	#通关进度信息
		ep=mainService.getEndPointByRoleId(iRoleId)
		if not ep:
			return
		if msg.lDetail:
			for lData in msg.lDetail:
				lData.iCurrAcount+=self.dPassReq.get(lData.iNo, 0)
		ep.rpcClientInsProgress(msg)

	def pushTaskStartTips(self,bBroadcast):
		for iRoleId in self.lJoinRole:
			oRole=role.gKeeper.getObj(iRoleId)
			if not oRole:
				continue	
			oRole.full(bBroadcast)#一进来就满红满蓝
			ep=mainService.getEndPointByRoleId(oRole.id)
			if not ep:
				continue
			tips=task_pb2.operateTips()
			tips.iState=0	#0表示未完成
			bSend=False
			for oTask in oRole.taskCtn.getAllValues():
				if not oTask.isFinished() and oTask.goalNo()==self.iNo:
					bSend=True
					tip=tips.taskTips.add()
					tip.iTaskType=oTask.taskType()
					tip.sTaskName=oTask.name
			if bSend:
				pass #屏蔽任务提示
				# ep.rpcClientTips(tips)

	def roleDisconnectHandler(self, who):
		if self.bRealTeam and who.id==self.iAiRoleId:#组队时AI玩家掉线了,AI转移
			for iRoleId in self.lJoinRole:
				ep=mainService.getEndPointByRoleId(iRoleId)
				if ep:
					self.iAiRoleId=iRoleId
					ep.rpcChangeAiRoleId(iRoleId)
					return
			self.iAiRoleId=0
			#表示所有的角色都断线了,定时副本停止计时???
			return
		if not self.bRealTeam and  getattr(self, 'bTimeLimit', False) and not self.iEndStamp:#单人限时副本且未通关
			self.cancleCountDownTimer()

	def roleReLogin(self,who):
		oCurrScene=self.getCurrScene()  #拿到当前场景对象,在怪物管理器中缓存有
		if not oCurrScene or not oCurrScene.isTempScene():#角色有可能在退出副本的过程中崩溃了,所以重连时有可能在安全区
			return
		if oCurrScene.hasPass():	#设置当前场景通过
			oCurrScene.openDoor()

		if self.no()==c.NEW_ROLE_BORN_BARRIER_NO and self.iEndStamp:#新手关卡通关
			self.exitInstance(who)
			return	

		iRoleId=who.id
		ep=mainService.getEndPointByRoleId(iRoleId)
		if not ep or who.isInTown():
			return	
		self.sendBornBarrierProg(oCurrScene.no())	#尝试发送新手关卡进度信息
		self.tryPushEscortData()	#发送保护npc对话信息
		self.sendHpBtnInfo(iRoleId)
		self.sendTeamAndAIInfo(iRoleId, True)	#发送队伍,AI角色信息

		#重连角色的加成死亡属性不在下发

		#角色重连,(结算界面,翻牌)恢复到掉线前的状态,新手关卡直接下发离开协议
		if not self.iEndStamp:	#如果当前关卡未通过,或者角色在安全区
			return
		iStage=self.dPassAndCardInfo[iRoleId][0]
		if iStage==BALANCE_STEP:	#结算阶段
			ep.rpcClientSlowMotion()
			bFail,bRes=ep.rpcClientBarrierPass(self.dPassAndCardInfo[iRoleId][1])	#bRes返回值代表结算显示完成
			if not bFail:
				self._dealCardLogic(iRoleId)	
		elif iStage==CARD_STEP:
			self._dealCardLogic(iRoleId)

	def roleRemoveEventHandler(self,who):#玩家踢出内存事件
		#当角色提出内存时,如果当前关卡也结束,并且没有翻任何牌则为角色翻出第一张免费牌
		if self.iEndStamp and False:#屏蔽翻牌
			iAwardGroup, iStep = None, self.dPassAndCardInfo.get(who.id,[-1,])[0]
			if iStep==BALANCE_STEP:	
				iAwardGroup=self.getConfig('freeaward')
			elif iStep==CARD_STEP and not self.dPassAndCardInfo[who.id][1].hasChoosed:
				iAwardGroup=self.getConfig('freeaward')
			if iAwardGroup:
				lAward,lItems=self.launchMng.launch(who,iAwardGroup),[]
				for (iPropsNo,iAmount,tPropsArgs,dPropsArgs,bIsBind,sAnnounce) in lAward:#通过邮件发放
					if iPropsNo in c.VIR_ITEM:
						lItems.append((iPropsNo,iAmount))
						continue
					oProps=props.new(iPropsNo)
					oProps.setStack(iAmount)
					lItems.append(oProps)
				mail.sendSysMail(who.id,'翻牌奖励','玩家掉线,系统自动为玩家翻牌',None,*lItems)

		self.exitInstance(who)#直接下线

	def Role_Login(self,who,iEvent,bIsInstead):#重新登录处理
		if who.hp==0 and bIsInstead:
			self.roleDieEventHandler(who,None)

	def passKind(self):
		return self.getConfig('passKind',1)

	def passReq(self):
		return self.getConfig('passReq',{})	#通关条件 

	def timeLimit(self):
		return self.getConfig('timeLimit',0)

	def mobHandler(self):
		return self.getConfig('mobHandler',0)

	def allowRelive(self):
		return self.getConfig('allowRelive',0)

	def freeReliveTimes(self):
		return self.getConfig('freeRelive',0)

	def maxReliveTimes(self):
		return self.getConfig('maxRelive',0)

	def reliveConsume(self):
		return self.getConfig('reliveReq',{})

	def _doRealRelive(self, who, iPropsNo, iAmount, sTips, failFunc, bUseDiamond=False):#返回(是否满足复活消耗,是否确认复活)
		dPay={iPropsNo:iAmount}
		oNeedConsume=consumeParser.cNeedConsume(dPay,who)
		iRoleId=who.id
		if bUseDiamond or not oNeedConsume.checkAll(who, '复活消耗'):#使用钻石不检查复活消耗
			ep=mainService.getEndPointByRoleId(who.id)
			reliveInfo=role_pb2.relive()
			reliveInfo.iAmount=iAmount
			reliveInfo.iTotal=misc.getAmountByNo(iPropsNo,who)
			reliveInfo.iIcon=misc.getIconByNo(iPropsNo)
			reliveInfo.iReinAtt=ROLE_ATT_REIN	#固定提升5
			reliveInfo.iTimeout=90*1000	#超时90 S
			bFail,oMsg=ep.rpcReliveConsume(reliveInfo)
			if bFail or oMsg.iValue!=0:#超时或者不同意复活
				who=role.gKeeper.getObj(iRoleId)
				if who and who.isInTown():
					return True, True
				ep=mainService.getEndPointByRoleId(iRoleId)
				if ep:
					ep.rpcClientShowAccount(getShowAccountBtn(iRoleId, self.no()))
					return True, True
				self.startTimer(failFunc, 1.5)	#failFunc取消回调函数
				return True, False
			if bUseDiamond and who.diamond<iAmount:
				ep.rpcTips('钻石不足')
				return False, False
			if not self.bRealTeam and getattr(self, 'bTimeLimit', False):
				self.cancleCountDownTimer()	#取消定时器
				if not getattr(self, 'bProtectEscort', False):#不是保护NPC类型,增加通关时间
					iAddTime=int(self.timeLimit()*0.5)
					self.iCancleStamp=timeU.getStamp()-iAddTime	#复活时间增加50%
				self.tryPushCountDown(who)	#重开定时器
				ep.rpcTips('通关时间增加{}秒'.format(iAddTime))
			oNeedConsume.doConsume(who,'复活消耗',None)
			reinforceAtt(who,ROLE_ATT_REIN,ATT_MAP)	#死亡复活对属性进行加成
			who.full()#满红满蓝
			ep.rpcRelive()
			return True, True
		return False, False

	# 返回值表示复活消耗是否允许复活,或者复活消耗是否足够	
	def _doRelive(self,who,failFunc):#failFunc复活失败回调函数,
		ep=mainService.getEndPointByRoleId(who.id)
		if not ep:
			self.exitInstance(who)
			return True
		if not self.allowRelive(): 	#不允许复活
			ep.rpcTips('请对角色进行强化,再次挑战')
			ep.rpcGameOverTips()
			failFunc=u.cFunctor(self.exitInstance,who)
			self.startTimer(failFunc, 4.5)	#
			return	True
		bAmple,bRelive=self._doRealRelive(who, 800, who.iDieTimes, '复活十字章x{}'.format(who.iDieTimes), failFunc)
		if not bAmple:#复活十字章消耗不够 
			bAmple,bRelive=self._doRealRelive(who, c.DIAMOND, who.iDieTimes*20, '钻石x{}'.format(who.iDieTimes*20), failFunc, True)
			ep=mainService.getEndPointByRoleId(who.id)
			if not ep:
				return False
			if not bAmple:#钻石消耗不足
				# ep.rpcTips('复活消耗不足')
				return False
		return True
				
	def relive(self,who):
		if not self._doRelive(who, u.cFunctor(self.exitInstance, who)):
			ep=mainService.getEndPointByRoleId(who.id)
			if ep:
				ep.rpcClientShowAccount(getShowAccountBtn(who.id, self.no()))

	def roleDieEventHandler(self,who,oAttacker):#玩家死亡处理函数
		iDeadRoleId=who.id
		self.flushScoreInfo(iDeadRoleId,DEAD_TIME,1)
		for iRoleId in self.lJoinRole: #下发角色死亡通知
			ep=mainService.getEndPointByRoleId(iRoleId)
			if ep:
				ep.rpcClientRoleDie(iDeadRoleId)

		# 		if self.iEndStamp:
		# 			who.addHp(1)
		# 			ep.rpcRelive()
		# 			return
		who.iDieTimes=getattr(who, 'iDieTimes', 0)+1 	#角色在副本内死亡次数
		if not self.iEndStamp:
			self.relive(who)
		log.log('ddic/roleDead', '\t{}\t{}\t{}\t{}'.format(who.id,who.name, oAttacker.name if oAttacker else '未知对象',self.name ))

	def exitFromMidway(self, who):
		self.exitInstance(who)

	def exitInstance(self,who):
		self.onLeave(who)	
		self.backToCity(who)

	#	if self.joinedRoleCnt() == 0:#没有玩家
			# log.log('ddic/barrierResult', '\t{}\t{}'.format(int(self.bSuccess), self.getConfig('degree', 0)))
				#数据字典日志:角色ID  用户来源   用户账号  关卡难度 是否通关 开始时间 结束时间 评分 奖励 关卡类型 关卡等级
			#log.log('ddic/enterInstance', '\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(who.iRoleId, who.sUserSource, who.sAccount, self.getConfig('degree', 1),self.bSuccess, self.iBeginStamp, self.iEndStamp,self.dScoreInfo(who.iRoleId), self.dAwardList(who.iRoleId), self.getConfig('barrierKind', 0), self.getConfig('limitLv', 0)))

	def roleBeAttackEventHandler(self,who,iHp):#玩家受击事件响应函数
		iRoldId=who.id
		if self.isPassed():#已经通关了
			return
		oScene=scene.gSceneProxy.getProxy(who.sceneId)
		if not oScene.isFightScene():
			return
		self.dRoleDamage[iRoldId]=self.dRoleDamage.get(iRoldId,0)+iHp

	def onLeave(self,who):#某玩家离开副本处理
		#ep.rpcDelClock()#移除客户端ui的倒计时器
		log.log('instanceLeave','{}({})离开了副本'.format(who.name,who.id))
		log.log('ddic/leaveInstance','\t{}\t{}\t{}\t{}'.format(who.id,who.name,self.no(),self.name))
		if getattr(who,'reliveCnt',0):#复活过,将复活次数清零
			who.reliveCnt=0
		if hasattr(who,'iPassBarrierStar'):
			del who.iPassBarrierStar
		who.iDieTimes=0 #将死亡次数清零
		who.setDieHandler(None) #不再关注死记亡事件
		#who.eBeAttack-=self.roleBeAttackEventHandler #不再关注玩家被打事件
		who.eRemove-=self.roleRemoveEventHandler #不再关注玩家remove事件
		#player.RemoveObserver(event.LOGIN,self.Role_Login,who)
		#scene.switchScene(who,*who.active.getLastRealPos())销毁副本前传送出去
		self.clearRecordByRoleId(who.id)#还要清除此人在副本内的成绩,他可能会再次进入此副本
		self.removeJoinRole(who.id)
		#不在监听重连复活
		who.eReLogin-=self.reLoginAliveCheck
		who.eReLogin-=self.roleReLogin	#不在关注重连事件
		who.eDisConnected-=self.roleDisconnectHandler	#不在关注角色掉线事件
		recoverAtt(who,ATT_MAP)	#离开副本去除死亡属性加成
		# who.eSceneMove-=self.monsterMng.triggerMonsterFlush
		if len(self.lJoinRole)==0: 	#副本里没有玩家了
			self.iEndStamp=timeU.getStamp()	#设置副本结束标记
		# recEquip.upRecEquip(who, '副本')#查看是否新获得比当前穿戴装备更好的装备,若有则提示角色穿戴

		if hasattr(who,'iFightHelperId'):	#去除援护助战者ID属性
			del who.iFightHelperId
		if hasattr(who,'oHelper'):	#去除援护助战者实体
			del who.oHelper
		if hasattr(who, 'iWesteSecond'):	#去除切换场景和掉线消耗时间总数属性
			del who.iWesteSecond

		if not self.bSuccess:#通关失败,返还次数
			iCostRest= min(1, self.getConfig('vitality', 0)) ##失败后扣除体力
			if iCostRest:
				who.addRest(-iCostRest, '失败关卡消耗', None)
			sFlag=barrierData.getCycTimesFlag(self.no())
			who.day.add(sFlag,-1)

	def openTurnCardUI(self,who):#开始翻牌小游戏
		iTurnCard=self.getConfig('turnCard',0)
		obj=miniGame.new(who,iTurnCard)		#create miniGame 1
		obj.addPlayer(who)
		obj.SendOpenUi(who)

	def addJoinRole(self,iRoleId):#副本队伍加入玩家
		self.lJoinRole.append(iRoleId)

	#移除玩家id
	def removeJoinRole(self,iRoleId):
		if iRoleId in self.lJoinRole:
			self.lJoinRole.remove(iRoleId)

	def start(self,who):#开始,返回第1个初始化好的场景
		#加入参与者
		oTeam=who.getTeamObj()
		if oTeam:
			for iRoleId in oTeam.memberIds():
				self.addJoinRole(iRoleId)
			self.setTeamId(oTeam.teamId())
		else:
			self.addJoinRole(who.id)
		if self.joinedRoleCnt()>1:
			self.bRealTeam=True
			self.iAiRoleId=who.id	#AI目标ID
		self.initFirstScene()
		iSceneNo,x,y=self.getInitPos()

		#保护本
		if getattr(self, 'bProtectEscort', False):	#生成保护NPC
			oCurrScene=self.getCurrScene()
			iEscortNo=escortData.getMonsterNo(self.no())
			self.oEscortNpc=monster.EscortMonster.cMonster(iEscortNo)
			tPos=escortData.getInitPos(self.no())
			if tPos:
				x,y=tPos
			oCurrScene.addEntity(self.oEscortNpc,x,y)
			self.oEscortNpc.x = x
			self.oEscortNpc.y = y

		#todo:只有一个场景的关卡,一进来就要关闭队伍列表显示	
		#触发限时任务
		# if not who.getTeamObj() :
		# 	iLimitTime=who.taskCtn.getLimitTime(self.no())
		# 	if iLimitTime:
		# 		self.dTimerId['time']=self.startTimer(self.timeOut,iLimitTime)

	def isStarted(self):#是否已经开打
		return self.iBeginStamp

	def getAiRoleId(self,*tArgs):#取得AI玩家ID
		return self.iAiRoleId	

	def getAiRoleList(self,*tArgs):#取得同步玩家列表
		return self.lJoinRole

	def getSceneIdByNo(self,iSceneNo):#用场景号获得场景第1个场景id,一个编号理论上有n个场景实例,实际上多数情况只有一个.
		lt=list(self.sceneMng.getSceneIdsByNo(iSceneNo))
		return lt[0] if lt else 0

	def getSceneObjByNo(self,iSceneNo):#根据场景号获得场景对象
		iSceneId=self.getSceneIdByNo(iSceneNo)
		if iSceneId==0:
			return None
		return scene.gSceneProxy.getProxy(iSceneId)

	def getInitPos(self):#策划配置的出生点
		iSceneNo=self.getConfig('firstmap')
		x,y=sceneData.getConfig(iSceneNo,'landingPoint')
		return iSceneNo,x,y

	@property
	def name(self):#关卡名
		return self.getConfig('name','')

	def SceneCnt(self):#本副本总共多少个场景
		return self.getConfig('SceneCnt',1)

	def hasOpenSceneCnt(self):#已经打通的场景个数
		return self.iHasOpenSceneCnt

	def addHasOpenSceneCnt(self,iCnt):#增加打通的场景个数
		self.iHasOpenSceneCnt+=iCnt

	def backToCity(self,who):
		iSceneNo,iX,iY=who.active.getLastRealPos()
		iRoleId = who.id
		oScene=scene.getScene(iSceneNo)
		iOldSceneId=who.sceneId
		if not scene.tryTransfer(who.id,oScene.id,iX,iY):
			return
		#切换场景过程中客户端掉线了,一定时间后角色被移除,之后在超时返回
		#所以此处的who可能不存在了
		who = role.gKeeper.getObj(iRoleId)
		if not who:#	角色也被移除出内存
			return
		# if who.sceneId==iOldSceneId:	#捕捉这个异常无用
		# 	try:
		# 		raise Exception,'退出场景时场景没有销毁'
		# 	except Exception:
		# 		u.logException()

		who.setInstanceObj(None)  #离开副本后解除对副本对象的引用
		who.setTeamObj(None)	#离开后直接退出队伍
		who.full()#离开这个副本了,免费加满油给玩家.
		# oTeam=who.getTeamObj()
		# if not oTeam:#找不到所在团队
		# 	return
		# oTeam.removeMember(who.id)


	def timeOut(self):
		self.stopTimer(self.dTimerId.get('time'))
		self.bTimeOut=True
		if self.iEndStamp:
			return
		for iRoleId in self.lJoinRole:  #遍历过程会删除,用keys
			who=role.gKeeper.getObj(iRoleId)
			if not who:
				continue
			ep=mainService.getEndPointByRoleId(iRoleId)
			if not ep:
				continue
			bFail,oMsg=ep.rpcConfirmBox(sTitle='副本超时',sContent='时间到,大侠请重新来过',sSelect='Q_确定')
			self.exitInstance(who)

	def liveTimeMeet(self):
		self.stopTimer(self.dTimerId.get('time'))
		self.setInstancePass()

	def reLoginAliveCheck(self,who): #重连死亡检测
		if who.hp<=0:
			#再次弹出复活确认框
			self.relive(who)

	#取消倒计时
	def cancleCountDownTimer(self):
		if self.dTimerId.get('live',0)==0 and self.dTimerId.get('time',0)==0:#无定时器
			return
		iPassKind=self.passKind()
		if self.dTimerId.get('live',0):
			self.stopTimer(self.dTimerId['live'])
		if self.dTimerId.get('time',0):
			self.stopTimer(self.dTimerId['time'])
		self.dTimerId['live'], self.dTimerId['time'] = 0, 0
		self.iCancleStamp=timeU.getStamp()	#记录取消定时器的时间戳,(单人模式iCancleStamp挂在副本上)

	#若有时间限制,则下发时间给客户端,并开启定时器
	def tryPushCountDown(self, oRole):
		if oRole.isInTown() or not getattr(self, 'bTimeLimit', False) :
			return
		iRoleId=oRole.id
		iCurStamp=timeU.getStamp()
		iCountDown=self.timeLimit()-iCurStamp+self.iBeginStamp
		if getattr(self, 'iCancleStamp', None):
			oRole.iWesteSecond=getattr(oRole, 'iWesteSecond', 0)	#关卡有效时间内角色掉线和切换场景所消耗的时间总数
			oRole.iWesteSecond += iCurStamp-self.iCancleStamp
			iCountDown += oRole.iWesteSecond
			self.iCancleStamp=None
		if iCountDown<=0:
			return
		#开启定时器
		iPassKind=self.passKind()
		if iPassKind==3:	#只要在关卡内保证自己存活，达到一定时间后，就可以弹出结算画面
			self.setUpTimer(iCountDown+2)
		else:
			self.dTimerId['time']=self.startTimer(self.timeOut,iCountDown+2)
			if iPassKind == 8:	#限时保护NPC
				self.dTimerId['live']=self.startTimer(self.liveTimeMeet,iCountDown)

		ep=mainService.getEndPointByRoleId(iRoleId)
		if ep:
			oMsg=scene_pb2.countDown()
			oMsg.iType=1
			oMsg.iSecond=iCountDown
			if getattr(oRole,'bDisConnect',None):
				oMsg.bReLogin=True
			ep.rpcPushCountDown(oMsg)

	def dieMonsterIsLastBoss(self, oMonster, *args):	#判断死亡的oMonster是否是最后一只boss
		if self.isLastBarrierScene() and self.currScenePass():	#若该关卡最后一只怪物死亡则无条件return True
			return True
		return isinstance(oMonster, monster.cMonster) and oMonster.isBoss() and not self.monsterMng.sBossId	
	
	def dieMonsterIsEscort(self, oMonster, *args):
		if not isinstance(oMonster, monster.cMonster):
			return True
		oEscortNpc=getattr(self,'oEscortNpc',None)
		if not oEscortNpc:		
			return True
		if oMonster!=oEscortNpc:		#oMonster不是被保护的对象
			return True
		oNpcScene=oMonster.getHolderScene()
		if oNpcScene and oNpcScene.hasPass():
			return True 				#场景通关
		#保护对象死亡
		self.iEndStamp=timeU.getStamp()
		sName=oEscortNpc.name
		for iRoleId in self.lJoinRole:  #遍历过程会删除,用keys
			who=role.gKeeper.getObj(iRoleId)
			if not who:
				continue
			ep=mainService.getEndPointByRoleId(iRoleId)
			if not ep:
				continue
			bFail,oMsg=ep.rpcConfirmBox(sTitle='{}死亡'.format(sName),sContent='{}死亡,大侠请重新来过'.format(sName),sSelect='Q_确定')
			self.exitInstance(who)
		return False

	def checkPassReq(self, *args):			
		if getattr(self,'dNeed',{}):
			bMeet=True
			for iNo,iAmount in self.dNeed.iteritems():
				if self.dPassReq.get(iNo, 0)<iAmount:
					bMeet=False
					break
			if bMeet and not self.bTimeOut:
				return True
		return False

	def currScenePass(self, *args):
		oCurrScene=self.monsterMng.getCurrScene()  #拿到当前场景对象,在怪物管理器中缓存有
		return oCurrScene.hasPass()

	def inTimeScope(self, *args):
		return not self.bTimeOut	
		
	def addPassReq(self, oEtt, bMonster, oAttacker):
		if not oAttacker:
			return
		oAttacker.triggerEvent(event.KILL_MONSTER if bMonster else event.COLLECT_GOODS, oEtt.no())
		if not getattr(self,'dNeed',{}):
			return
		# self.dPassReq[oEtt.no()]=self.dPassReq.get(oEtt.no(), 0)+1
		# return	#屏蔽通关进度消息
		ep=mainService.getEndPointByRoleId(oAttacker.id)
		if not ep:
			return
		#下发通关进度消息
		#此处需要区分移除的是怪物还是物品,物品编号和怪物编号可能重叠
		#所以需要根据通关类型和实体类型来做处理
		bSend=(
			(getattr(self, 'bCollectProps', False) and not bMonster and oEtt.no() in getattr(self, 'dNeed', {})) 
			or (getattr(self, 'bKillAssignMons', False) and bMonster and oEtt.no() in getattr(self, 'dNeed', {}))
			)
		if bSend:
			self.dPassReq[oEtt.no()]=self.dPassReq.get(oEtt.no(), 0)+1
			bSendProMsg=barrier_pb2.passProgressMsg()	
			detail=bSendProMsg.lDetail.add()
			detail.iNo=oEtt.no()
			detail.iCurrAcount=self.dPassReq[oEtt.no()]
			ep.rpcClientInsProgress(bSendProMsg)	

	def incrMoneterBrew(self,iMonsterDisNo):#增加关卡刷怪批次,iMonsterDisNo已消灭的批次	
		if not getattr(self, 'bKillMonstBrew', False):
			return
		sKey=str(monsterdisData.getConfig(iMonsterDisNo,'preNo'))
		iSceneNo=self.getCurrScene().no()
		if not getattr(self, 'dKllMonsDisNo', None):
			self.dKllMonsDisNo={}
		self.dKllMonsDisNo.setdefault(iSceneNo,{}).setdefault(sKey,set([])).add(iMonsterDisNo)
		if self.dKllMonsDisNo.get(iSceneNo,{}).get(sKey,set([]))!=monsterdisData.gdSceneAndProDis.get(iSceneNo, {}).get(sKey,None):
			return
		iNo=self.dNeed.keys()[0]
		self.dPassReq[iNo]=self.dPassReq.get(iNo, 0)+1
		if self.dPassReq[iNo]>=self.dNeed.values()[0]:	#
			self.setInstancePass()	
			return
		if self.monsterMng.isCurrSceneSpawnOver():
			return
		for iRoleId in self.lJoinRole:
			self.tryPushPassProgressInfo(iRoleId)
				
	def setUpTimer(self, iLimitTime):
		self.dTimerId['live']=self.startTimer(self.liveTimeMeet,iLimitTime)
		self.dTimerId['time']=self.startTimer(self.timeOut,iLimitTime+1) #time和live共用一个时间值,timeout为判断失败,因此当time和live共存时,应保证其在live函数之后执行

	def isLiveTimeMeet(self, *args):
		#存活时间到设置通关由liveTimeMeet()函数处理,所以此处返回False
		return False	
		#return getattr(self, 'bLiveTime', False)

	def isKillMonsBrew(self,*tArgs):
		return False


def storyChat(iRoleId,iSceneNo,iType):
	if iSceneNo not in storyChatData.gdNoByScene:
		return False
	if iType not in storyChatData.gdNoByScene.get(iSceneNo):
		return False
	ep=mainService.getEndPointByRoleId(iRoleId)
	who=role.gKeeper.getObj(iRoleId)
	if not ep or not who:
		return False
	lStoryChat=who.lazy.fetch('schat',[])
	iChatNo=storyChatData.gdNoByScene.get(iSceneNo).get(iType)
	if iChatNo in lStoryChat:
		return False
	lStoryChat.append(iChatNo)
	who.lazy.set('schat',lStoryChat)
	ep.rpcClientPlotStart(iChatNo)
	return True

def create(iNo):#创建副本实例
	if iNo not in gdBarrierModule:
		obj=cInstance(iNo)
	else:
		obj=gdBarrierModule[iNo].cInstance(iNo)
	iPassKind=obj.passKind()	#通关类型
	#若是限时关卡,开启定时的功能移到tryPushCountDown函数实现
	if iPassKind==1:	#只要把关卡中的关底BOSS击杀,就可以弹出结算画面。
		obj.lCheckPassFunc.extend([u.cFunctor(obj.dieMonsterIsLastBoss)])
	elif iPassKind==2:	#只要在关卡内击杀了要求数量的某种怪物，或某几种怪物，就可以弹出结算画面。
		obj.dNeed=obj.passReq()
		obj.lCheckPassFunc.extend([u.cFunctor(obj.checkPassReq)])
	elif iPassKind==3:	#只要在关卡内保证自己存活，达到一定时间后，就可以弹出结算画面
		obj.lCheckPassFunc.extend([u.cFunctor(obj.isLiveTimeMeet)])
	elif iPassKind==4:	#全灭怪物：必须把关卡中所有的怪物（包括BOSS在内）全部击杀，弹出结算画面。
		obj.lCheckPassFunc.extend([u.cFunctor(obj.isLastBarrierScene),u.cFunctor(obj.currScenePass)])
	elif iPassKind==5:	#限时全杀：在一定时间之内，把关卡中所有的怪物（包括BOSS在内）全部击杀，弹出结算画面。如果超时，则算闯关失败。
		obj.lCheckPassFunc.extend([u.cFunctor(obj.inTimeScope),u.cFunctor(obj.isLastBarrierScene), u.cFunctor(obj.currScenePass)])
	elif iPassKind==6:	#限时BOSS：在一定时间之内，只要把关卡中的关底BOSS击杀，其余小怪无论当时是否存活，都可弹出结算画面。如果超时BOSS没有死亡，则算闯关失败。
		obj.lCheckPassFunc.extend([u.cFunctor(obj.inTimeScope),u.cFunctor(obj.dieMonsterIsLastBoss)])
	elif iPassKind==7:	#保护
		obj.lCheckPassFunc.extend([u.cFunctor(obj.dieMonsterIsEscort),u.cFunctor(obj.isLastBarrierScene),u.cFunctor(obj.currScenePass)])
	elif iPassKind==8:	#限时保护(在一定时间内，不要让被保护的目标死亡/损坏)
		obj.lCheckPassFunc.extend([u.cFunctor(obj.inTimeScope),u.cFunctor(obj.dieMonsterIsEscort),u.cFunctor(obj.isLastBarrierScene),u.cFunctor(obj.currScenePass)])
	elif iPassKind==9:	#收集：获得指定数量的物品（采集/击杀怪物获得）
		obj.dNeed=obj.passReq()
		obj.lCheckPassFunc.extend([u.cFunctor(obj.checkPassReq)])
	elif iPassKind in (10,):#破坏指定物品
		obj.dNeed=obj.passReq()
		obj.lCheckPassFunc.extend([u.cFunctor(obj.checkPassReq)])
	elif iPassKind==11:	#只要在一定时间内在关卡内击杀了要求数量的某种怪物，或某几种怪物，就可以弹出结算画面。
		obj.dNeed=obj.passReq()
		obj.lCheckPassFunc.extend([u.cFunctor(obj.inTimeScope), u.cFunctor(obj.checkPassReq)])
	elif iPassKind==12:	#只要在一定时间内在关卡内获取了要求数量的某种物品，或某几种物品，就可以弹出结算画面。
		obj.dNeed=obj.passReq()
		obj.lCheckPassFunc.extend([u.cFunctor(obj.inTimeScope), u.cFunctor(obj.checkPassReq)])
	elif iPassKind==13:	#消灭多少波怪物通关
		obj.dNeed=obj.passReq()
		obj.lCheckPassFunc.extend([u.cFunctor(obj.isKillMonsBrew)])
	elif iPassKind==14:	#指定时间内消灭多少波怪物
		obj.dNeed=obj.passReq()
		obj.lCheckPassFunc.extend([u.cFunctor(obj.inTimeScope),u.cFunctor(obj.isKillMonsBrew)])
		
	obj.bTimeLimit 		= 	iPassKind in (3, 5, 6, 11, 12, 8, 14,) #表示此副本是限时副本
	obj.bCollectProps	=	iPassKind in (9, 12,)		#表示此副本是收集物品通关
	obj.bKillAssignMons	=	iPassKind in (2, 11, 10)	#表示此副本是杀死指定怪物通关(破坏对象也算怪物)
	obj.bProtectEscort	=	iPassKind in (7, 8,)		#保护目标
	obj.bKillMonstBrew 	=	iPassKind in (13, 14,)		#是否是击杀指定波数通关

	return obj

if 'gdBarrierModule' not in globals():#关卡编号映射关卡实例
	gdBarrierModule={}

THIS_MODULE=__import__(__name__)



def init():
	pass


INFINITY=60*60*24
#todo:做一个指令,可以快速放出传送点,oInstance.makeDoor(iSceneNo,iDoorNo)

BALANCE_STEP=1 #结算阶段
CARD_STEP=2 	#翻牌阶段

#评分统计项		dScoreInfo={iRoleId1:{1:3,2:255,3:{1000:1,1001:2},4:{12:4}}}
DEAD_TIME=1  #死亡次数
HURT_TOTAL=2  #伤害总量
MONSTER_KILLED=3  #击杀怪物{编号:数量}
ATT_TIME=4	#角色被各类型的怪物攻击次数

gdStar={0:0,1:0,2:1,3:2,4:2,5:3}

ROLE_ATT_REIN=5	

ATT_MAP={'att':'iAtt', 'defense':'iDef', 'hpMax':'iHpMax'}

def reinforceAtt(who, iReinForce, dAttMap):#复活对属性进行加成,iReinForce%, dAttMap需要加成的属性
	fRein = iReinForce*1.0/100
	lNoticAttr = []
	for sAttName, sAtt in dAttMap.iteritems():
		if getattr(who, sAtt, False):
			iBaseAtt = getattr(who, sAtt)
			setattr(who,sAtt, iBaseAtt + int(iBaseAtt*fRein))
			lNoticAttr.append(sAttName)
	who.attrChange(*lNoticAttr)

def recoverAtt(who,dAttMap):
	who.reCalcAttr()
	who.attrChange(*dAttMap.keys())

def getShowAccountBtn(iRoleId, iBarrierNo):#取得回城界面显示的按钮
	oRole = role.gKeeper.getObj(iRoleId)
	if not oRole:	#角色不存在
		return 0
	iBtnValue = 4	#默认显示回城按钮
	if oRole.getTeamObj():
		return iBtnValue
	
	iNeedRest = barrierData.getConfig(iBarrierNo, 'vitality', 0)
	bEnterAgain = True 	#在来一次按钮
	if oRole.rest() < iNeedRest:#检查体力
		bEnterAgain = False
	if bEnterAgain:	#检查进入次数
		sFlag = barrierData.getCycTimesFlag(iBarrierNo)
		if oRole.day.fetch(sFlag, 0) >= barrierData.getConfig(iBarrierNo, 'limitentertime'):
			bEnterAgain = False
	iBtnValue |= ([0,2][bEnterAgain])	#显示在来一次按钮
	iBtnValue |= int(block.blockTask.hasSubmitMainTask(oRole))
	return iBtnValue

import weakref
import copy
import role
import mainService
import timeU
import timer


import event
import findSort
import resume
import miniGame
import consumeParser
import scene
import helperClass
import sceneData
import c
import log
import common_pb2

import random
import block.blockTask

import task_pb2
import team
import launchData




# import monster
import scene_pb2
import props



import sysConfigData
import findSort

import consumeParser

import role_pb2
import entity_pb2
import mail
import taskData


init()
ENHANCE=sysConfigData.getConfig('iCanEnhance')

