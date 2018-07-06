#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import product
import controller
import u
import productKeeper
import misc
import config
import propsData

MaxHelpPoint = 500

class cRole(product.cProduct,controller.cController):
	def __init__(self,iRoleId):
		product.cProduct.__init__(self,'虚拟数据(玩家)',iRoleId)
		entity.gEntityProxy.addObj(self, iRoleId)
		self.lSeeMe=[] #在地图上,全部看得见我的角色id
		self.lSeeOther=[] #在地图上,我看得到的角色id
		self.iCanSee=0
		self.iRoleId=iRoleId
		self.sUserSource=self.sAccount=''
		self.taskCtn=None #任务容器
		self.propsCtn=None #物品容器
		self.equipCtn=None #装备容器(穿在身上的)
		self.petCtn=None #宠物容器		
		self.rideCtn=None #坐骑容器
		self.multiField1=None #多列属性
		self.lazy=None #玩家惰性数据1
		self.active=None #玩家活跃数据
		self.cycData=self.hour=self.day=self.week=self.month=None #玩家周期数据
		self.friendCtn=None #好友容器
		self.skillCtn=None#技能容器
		self.titleCtn=None#称号容器
		self.buffCtn=None#buff容器
		self.schemeCtn=None #加点方案容器
		self.buddyCtn=None # 助战伙伴容器
		self.lineupCtn=None#阵法容器
		self.storage=None#仓库
		self.stateCtn=None#状态容器
		self.words=None#对白数据
		self.alchemyCtn=None#炼丹容器
		self.eyeCtn=None#阵眼数据
		self.achvCtn=None#成就容器
		self.fashionCtn=None#时装容器
		self.dFtr={#各种工厂
			0:factoryConcrete.multiField1Ftr,
			1:factoryConcrete.propsCtnFtr,
			2:factoryConcrete.taskCtnFtr,
			3:factoryConcrete.lazyFtr,
			4:factoryConcrete.cycFtr,
			5:factoryConcrete.friendCtnFtr,
			6:factoryConcrete.skillFtr,
			7:factoryConcrete.activeFtr,
			8:factoryConcrete.titleCtnFtr,
			9:factoryConcrete.buffCtnFtr,
			10:factoryConcrete.equipCtnFtr,
			12:factoryConcrete.petCtnFtr,
 			13:factoryConcrete.buddyCtnFtr,
 			14:factoryConcrete.lineupFtr,
 			15:factoryConcrete.storageFtr,
 			16:factoryConcrete.stateFtr,
 			17:factoryConcrete.wordsFtr,
 			18:factoryConcrete.eyeFtr,
 			19:factoryConcrete.achvFtr,
 			20:factoryConcrete.rideCtnFtr,
		}
		self.lLoginSend=[]
		self.lLoginSetup=[]
		self.dEvent={}
		self.sSerialized1=None
		self.iDisConnectStamp=0 #最后断线时间
		self.eRemove=u.cEvent() #角色对象被清除事件
		self.eSceneMove=u.cEvent() #监听角色在场景上的移动事件
		self.eDisConnected,self.eReConnected=u.cEvent(),u.cEvent() #连接断开事件,连接重新建立事件
		self.eReLogin=u.cEvent()
		self.eHpChange=u.cEvent() #hp发生变化事件
		self.eDegreeChange=u.cEvent() #阶数变化事件
		#self.bGuildAttrDirty=True #创建角色时计算公会附加属性
		self.applyMgr = container.ApplyMgr()  # 附加效果
		#这个类里面没有x,y,hp,mp属性,这些都放在了multiField1类里面
		
		self.con=0 # 体质
		self.mag=0 # 魔力
		self.str=0 # 力量
		self.res=0 # 耐力
		self.spi=0 # 精神
		self.dex=0 # 敏捷

		#中间变量,不存盘的
		self.phyDam=0 # 物理伤害
		self.magDam=0 # 法术伤害
		self.phyDef=0 # 物理防御
		self.magDef=0 # 法术防御
		self.spe=0 # 速度
		self.cure=0 # 治疗强度

		self.phyCrit = 0 #物理暴击
		self.magCrit = 0 #法术暴击
		self.phyReCrit = 0 #物理抗暴
		self.magReCrit = 0 #法术抗暴
		
		self.sealHit = 0 # 封印命中
		self.reSealHit = 0 # 抵抗封印

		self.hpMax=0 # 生命上限
		self.mpMax=0 # 真气上限
		self.huoliMax=0 # 活力上限
		self.spMax=0 # 愤怒上限
		self.fightPower=0 # 战力
		self.reserveHpMax = 100000 # 储备生命上限
		self.reserveMpMax = 100000 # 储备真气上限
	
		self.__oTeam = None
		self.__oInstance = None
		self.handlerListForWarEnd = {} # 战斗后处理的操作
		self.timerMgr = timer.cTimerMng() # 定时器
		self.equipSkillCtn = block.equipSkill.cContainer(self.id)
		self.expStateCtn = block.expState.cContainer(self.id)
		
		self.denyTeam = {} # 禁止组队
		self.action = 0 # 动作

	@property
	def id(self):
		return self.iRoleId
	
	@property
	def endPoint(self):
		return mainService.getEndPointByRoleId(self.iRoleId)
	
	def isDisconnected(self):
		'''是否已掉线
		'''
		if not self.endPoint:
			return True
		return False
	
	def inTeam(self):
		'''是否在队
		'''
		teamObj = self.getTeamObj()
		if teamObj and self.id in teamObj.getInTeamList():
			return teamObj
		return None
	
	def isSingle(self):
		'''是否单人
		'''
		if self.inTeam():
			if len(self.getTeamObj().getInTeamList()) == 1:
				return 1
			return 0
		return 1

	def getTeamObj(self):#队伍proxy
		if self.__oTeam:
			return weakref.proxy(self.__oTeam)
		return None

	def setTeamObj(self, teamObj):#队伍实例
		self.__oTeam = teamObj
		self.broadcastAttrChange("teamId","teamState")
		
		if teamObj:
			teamId = teamObj.id
		else:
			teamId = 0
		role.register.updateRole(self, teamId=teamId)
		
	def getTeamState(self):
		teamObj = self.getTeamObj()
		if not teamObj:
			return -1
		return teamObj.getState(self.id)

	def validInTeamSize(self, minSize, maxSize=0):
		'''校验在线队员数量
		'''
		if not self.inTeam():
			return 0
		if self.isTestMan():
			return 1
		if not maxSize:
			return minSize <= self.getTeamObj().inTeamSize
		return minSize <= self.getTeamObj().inTeamSize <= maxSize
	
	def isTestMan(self):
		'''是否测试员
		'''
		return self.fetch("testman")

	def getInstanceObj(self):#副本proxy
		if self.__oInstance:
			return weakref.proxy(self.__oInstance)
		return None

	def setInstanceObj(self,oInstance):#副本对象
		self.__oInstance=oInstance

	def setUserSourceAccount(self,sUserSource,sAccount):
		self.sUserSource,self.sAccount=sUserSource,sAccount
	
	@property
	def accountObj(self):
		return account.gKeeper.getObj(self.sUserSource,self.sAccount)
	
	def _insertToDB(self,*itNoRowInsertValues,**dData):#override
		iRoleId=self.iRoleId
		lJobs=[]
		for i in self.lNoRecordset:#新建角色下面的分支会全部进入,后期运营加入的表只走某几个分支.
			if i==0:
				self.multiField1=multiFieldRole.cMultiField1(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.multiField1._insertToDB,*itNoRowInsertValues))
			elif i==1:
				self.propsCtn= block.blockPackage.cPropsContainer(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.propsCtn._insertToDB,iRoleId))
			elif i==2:
				self.taskCtn=block.blockTask.cTaskContainer(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.taskCtn._insertToDB,iRoleId))
			elif i==3:
				self.lazy=block.blockLazy.cRoleLazyBlock(iRoleId)
				self.schemeCtn=self.lazy.schemeCtn
				self.alchemyCtn=self.lazy.alchemyCtn
				self.fashionCtn=self.lazy.fashionCtn
				lJobs.append(myGreenlet.cGreenlet.spawn(self.lazy._insertToDB,iRoleId))
			elif i==4:
				self.cycData=block.blockCycle.cCycDataBlock(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.cycData._insertToDB,iRoleId))
				self.hour=self.cycData.hour
				self.day=self.cycData.day
				self.week=self.cycData.week
				self.month=self.cycData.month
			elif i==5:
				self.friendCtn=block.blockFriend.cFriendContainer(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.friendCtn._insertToDB,iRoleId))
			elif i==6:
				self.skillCtn=block.blockSkill.cSkillContainer(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.skillCtn._insertToDB,iRoleId))
			elif i==7:
				self.active=block.active.cActive(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.active._insertToDB,iRoleId))
			elif i==8:
				self.titleCtn= block.blockTitle.cTitleContainer(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.titleCtn._insertToDB,iRoleId))
			elif i==9:
				self.buffCtn=block.blockBuff.cBuffContainer(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.buffCtn._insertToDB,iRoleId))
			elif i==10:
				self.equipCtn=block.containerEquip.cEquipContainer(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.equipCtn._insertToDB,iRoleId))
			elif i==11:
				pass
			elif i==12:
				self.petCtn = block.blockPetCtn.cPetContainer(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.petCtn._insertToDB,iRoleId))
			elif i==13:
				self.buddyCtn = block.blockBuddy.BuddyContainer(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.buddyCtn._insertToDB,iRoleId))
			elif i==14:
				self.lineupCtn=block.blockLineup.cLineupContainer(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.lineupCtn._insertToDB,iRoleId))
			elif i==15:
				self.storage = block.storage.cStorage(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.storage._insertToDB,iRoleId))
			elif i==16:
				self.stateCtn = block.blockState.cStateContainer(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.stateCtn._insertToDB, iRoleId))
			elif i==17:
				self.words=block.blockWords.cWords(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.words._insertToDB,iRoleId))
			elif i==18:
				self.eyeCtn=block.blockEye.cEyeContainer(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.eyeCtn._insertToDB,iRoleId))
			elif i==19:
				self.achvCtn=block.blockAchv.AchvContainer(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.achvCtn._insertToDB,iRoleId))
			elif i==20:
				self.rideCtn=block.blockRideCtn.cRideContainer(iRoleId)
				lJobs.append(myGreenlet.cGreenlet.spawn(self.rideCtn._insertToDB,iRoleId))
		gevent.joinall(lJobs,None,True)
		#放入工厂管理
		for iKey in self.lNoRecordset:
			if 0==iKey:
				factoryConcrete.multiField1Ftr.addProduct(self.multiField1,iRoleId)
			elif 1==iKey:
				factoryConcrete.propsCtnFtr.addProduct(self.propsCtn,iRoleId)
				self.lLoginSend.append(self.propsCtn)
			elif 2==iKey:
				factoryConcrete.taskCtnFtr.addProduct(self.taskCtn,iRoleId)
				self.lLoginSend.append(self.taskCtn)
			elif 3==iKey:
				factoryConcrete.lazyFtr.addProduct(self.lazy,iRoleId)
			elif 4==iKey:
				factoryConcrete.cycFtr.addProduct(self.cycData,iRoleId)
			elif 5==iKey:
				factoryConcrete.friendCtnFtr.addProduct(self.friendCtn,iRoleId)
				self.lLoginSend.append(self.friendCtn)
			elif 6==iKey:
				factoryConcrete.skillFtr.addProduct(self.skillCtn,iRoleId)
				self.lLoginSend.append(self.skillCtn)
			elif 7==iKey:
				factoryConcrete.activeFtr.addProduct(self.active,iRoleId)	
			elif 8==iKey:
				factoryConcrete.titleCtnFtr.addProduct(self.titleCtn,iRoleId)
				self.lLoginSend.append(self.titleCtn)
			elif 9==iKey:
				factoryConcrete.buffCtnFtr.addProduct(self.buffCtn,iRoleId)
				self.lLoginSend.append(self.buffCtn)
			elif 10==iKey:
				factoryConcrete.equipCtnFtr.addProduct(self.equipCtn,iRoleId)
				self.lLoginSend.append(self.equipCtn)
			elif 11==iKey:
				pass
			elif 12==iKey:
				factoryConcrete.petCtnFtr.addProduct(self.petCtn, iRoleId)
				self.lLoginSend.append(self.petCtn)
			elif 13==iKey:
				factoryConcrete.buddyCtnFtr.addProduct(self.buddyCtn, iRoleId)
				self.lLoginSend.append(self.buddyCtn)
			elif 14==iKey:
				factoryConcrete.lineupFtr.addProduct(self.lineupCtn, iRoleId)
			elif 15==iKey:
				factoryConcrete.storageFtr.addProduct(self.storage, iRoleId)
				self.lLoginSend.append(self.storage)
			elif 16==iKey:
				factoryConcrete.stateFtr.addProduct(self.stateCtn, iRoleId)
				self.lLoginSend.append(self.stateCtn)
			elif 17==iKey:
				factoryConcrete.wordsFtr.addProduct(self.words, iRoleId)
			elif 18==iKey:
				factoryConcrete.eyeFtr.addProduct(self.eyeCtn, iRoleId)
			elif 19==iKey:
				factoryConcrete.achvFtr.addProduct(self.achvCtn, iRoleId)
			elif 20==iKey:
				factoryConcrete.rideCtnFtr.addProduct(self.rideCtn, iRoleId)
				self.lLoginSend.append(self.rideCtn)
				self.lLoginSend.append(self.achvCtn)
		del self.lNoRecordset

	def _loadFromDB(self):#override
		oMultiField1=factoryConcrete.multiField1Ftr.getProductFromDB(factory.NO_ROW_RETURN_NONE,self.iRoleId)
		if not oMultiField1:#如果连这个都不存在,可以认为其他全部不存在,是新角色
			self.lNoRecordset=self.dFtr.keys()
			return False

		dJobs={i:myGreenlet.cGreenlet.spawn(self.dFtr[i].getProductFromDB,factory.NO_ROW_RETURN_NONE,self.iRoleId) for i in self.dFtr.keys()}
		gevent.joinall(dJobs.values(),None,True)		
		self.lNoRecordset=[i for i,job in dJobs.iteritems() if not job.value]

		#下面有些value其实是None,因为上面用了参数是NO_ROW_RETURN_NONE
		for iKey,job in dJobs.iteritems():
			if not job.value:
				continue
			if 0==iKey:
				self.multiField1=job.value
			elif 1==iKey:
				self.propsCtn=job.value
				self.lLoginSend.append(self.propsCtn)
				self.lLoginSetup.append(self.propsCtn)
			elif 2==iKey:
				self.taskCtn=job.value
				self.lLoginSend.append(self.taskCtn)
				self.lLoginSetup.append(self.taskCtn)
			elif 3==iKey:
				self.lazy=job.value
				self.schemeCtn=self.lazy.schemeCtn
				self.alchemyCtn=self.lazy.alchemyCtn
				self.fashionCtn=self.lazy.fashionCtn
			elif 4==iKey:
				self.cycData=job.value
				self.hour=self.cycData.hour
				self.day=self.cycData.day
				self.week=self.cycData.week
				self.month=self.cycData.month
			elif 5==iKey:
				self.friendCtn=job.value
				self.lLoginSend.append(self.friendCtn)
				self.lLoginSetup.append(self.friendCtn)
			elif 6==iKey:
				self.skillCtn=job.value
				self.lLoginSend.append(self.skillCtn)
				self.lLoginSetup.append(self.skillCtn)
			elif 7==iKey:
				self.active=job.value
			elif 8==iKey:
				self.titleCtn=job.value
				self.lLoginSend.append(self.titleCtn)
				self.lLoginSetup.append(self.titleCtn)
			elif 9==iKey:
				self.buffCtn=job.value
				self.lLoginSend.append(self.buffCtn)
				self.lLoginSetup.append(self.buffCtn)
			elif 10==iKey:
				self.equipCtn=job.value
				self.lLoginSend.append(self.equipCtn)
				self.lLoginSetup.append(self.equipCtn)
			elif 11==iKey:
				pass
			elif 12==iKey:
				self.petCtn=job.value
				self.lLoginSend.append(self.petCtn)
				self.lLoginSetup.append(self.petCtn)
			elif 13==iKey:
				self.buddyCtn = job.value
				self.lLoginSend.append(self.buddyCtn)
				self.lLoginSetup.append(self.buddyCtn)
			elif 14==iKey:
				self.lineupCtn=job.value
				self.lLoginSetup.append(self.lineupCtn)
			elif 15==iKey:
				self.storage=job.value
				self.lLoginSend.append(self.storage)
				self.lLoginSetup.append(self.storage)
			elif 16==iKey:
				self.stateCtn=job.value
				self.lLoginSend.append(self.stateCtn)
				self.lLoginSetup.append(self.stateCtn)
			elif 17==iKey:
				self.words=job.value
			elif 18==iKey:
				self.eyeCtn=job.value
			elif 19==iKey:
				self.achvCtn=job.value
				self.lLoginSend.append(self.achvCtn)
				self.lLoginSetup.append(self.achvCtn)
			elif 20==iKey:
				self.rideCtn=job.value
				self.lLoginSend.append(self.rideCtn)
				self.lLoginSetup.append(self.rideCtn)
		return not self.lNoRecordset #有任意一个没有数据集都返回失败,好让转而执行_insertToDB

	def _saveToDB(self):#override,
		iRoleId=self.iRoleId
		lJobs=[]
		for ftr in self.dFtr.itervalues():
			if ftr.isWait2schedule(iRoleId):
				job=myGreenlet.cGreenlet.spawn(ftr.saveProduct2db,iRoleId)
				lJobs.append(job)
			else:
				oProduct=ftr.getProductFromMemory(iRoleId)
				if oProduct:
					oProduct.checkMarkDirty()

		gevent.joinall(lJobs,None,True)
		return all([job.value for job in lJobs])#全部真才为真
		
	def _deleteFromDB(self):#override
		lJobs=[myGreenlet.cGreenlet.spawn(ftr.deleteProductFromDB,self.iRoleId) for ftr in self.dFtr.itervalues()]
		gevent.joinall(lJobs,None,True)

	def checkMarkDirty(self):#override 角色对象从productKeeper移除时会调用到这里
		iRoleId=self.iRoleId
		for ftr in self.dFtr.itervalues():
			oProduct=ftr.getProductFromMemory(iRoleId)
			if oProduct:
				oProduct.checkMarkDirty()
	
	def add(self,uKey,uValue,uDefault=0):
		self.lazy.add(uKey,uValue,uDefault)
		
	def set(self,uKey,uValue):
		self.lazy.set(uKey,uValue)
	
	def fetch(self,uKey,uDefault=0):
		return self.lazy.fetch(uKey,uDefault)
	
	def delete(self,uKey):
		self.lazy.delete(uKey)

	def title(self):
		return self.titleCtn.getTitleName()

	def titleEffect(self):
		return self.titleCtn.getTitleEffect()

# 	@property
# 	def sceneId(self):#场景id
# 		return self.active.iSceneId
# 	
# 	@sceneId.setter
# 	def sceneId(self, sceneId):
# 		self.active.iSceneId = sceneId
# 		
# 	def sceneNo(self):
# 		return self.active.sceneNo
		
	@property
	def sceneObj(self):
		return scene.gSceneProxy.getProxy(self.sceneId)

# 	def getX(self):
# 		return self.active.getX()
# 
# 	def setX(self,x):
# 		self.active.setX(x)
# 
# 	def getY(self):
# 		return self.active.getY()
# 
# 	def setY(self,y):
# 		self.active.setY(y)

	def getGuildId(self):#公会id
		return self.fetch("guildId", 0)

	def setGuildId(self, guildId):#玩家加入退出公会，属性重新计算放在这里如何？
		if guildId == 0:
			self.set("lastGuildId", self.fetch("guildId"))
			self.delete("guildId")
			guild.onQuitGuild(self)
		else:
			self.set("guildId", guildId)
			if guildId != self.fetch("lastGuildId"):
				self.set("ttGuildPoint", self.getGuildPoint())
				guild.updateMemberInfo(self)
		resume.updateResume(self)
		self.reCalcAttr()
		self.attrChange("guildId", "guildName")
		role.register.updateRole(self, guildId=guildId, guildName=self.getGuildName())

	def getGuildObj(self):
		guildId = self.getGuildId()
		if guildId:
			return guild.getGuild(guildId)
		return None

	def getGuildName(self):
		guildObj = self.getGuildObj()
		if guildObj:
			return guildObj.name
		return ""

	def guildTitle(self):#公会职位
		guildObj = self.getGuildObj()
		if guildObj:
			return guild.getStrGuildPosition(guildObj, self.id)
		return ""

	def getSignature(self):
		'''个性签名
		'''
		return self.fetch("signature","")

	def getOfflineTime(self):
		'''离线时间
		'''
		return self.fetch("offlineTime")

	def addActPoint(self, iVal, reason=""):
		'''增加活跃
		'''
		actPointOld = self.day.fetch("actPoint")
		actPoint = actPointOld + iVal
		self.day.set("actPoint", actPoint)
		writeLog("role/actPoint", "%d %d%+d->%d %s" % (self.id, actPointOld, iVal, actPoint, reason))
		guild.updateMemberInfo(self)
		self.endPoint.rpcActCenterMod(activity.center.packActPoint(self))
		
		# 刷新可接任务
		activity.center.refreshTaskNpc(self)

	def getActPoint(self):
		return self.day.fetch("actPoint")

	def addDiamond(self,iAdd,sLogReason,sTips=''):#sTips为None表示不提示#增减钻石
		iNum=self.accountObj.accountMf.addDiamond(iAdd,sLogReason,sTips)
		if iNum<0: #记录玩家一共花费了多少钻石
			self.active.add('diamondCost',-iNum)
			self.triggerEvent(event.USE_DIAMOND)
		
		self.attrChange('diamond')
		return iNum

	def addMoneyCash(self,iVal, sReason, sTips=""):
		'''增加或减少龙纹玉
		'''
		if not isinstance(iVal, (int,long)):
			raise Exception, "非法的龙纹玉值:%s" % iVal
		if self.moneyCash + iVal < 0:
			raise Exception, '不能把龙纹玉扣成负数,否则{}+({})={}.'.format(self.moneyCash, iVal, self.moneyCash + iVal)

		writeLog("role/moneyCash", "%d %d%+d->%d %s" % (self.id, self.moneyCash, iVal, self.moneyCash + iVal, sReason))
		self.moneyCash += iVal
		self.attrChange("moneyCash")
		
		if sTips != None:
			if iVal > 0:
				sTips = sTips if sTips else "获得龙纹玉#R<$moneyCash,1,2>#n"
			elif iVal < 0:
				sTips = sTips if sTips else "消耗龙纹玉#R<$moneyCash,1,2>#n"
			else:
				return 0
			sTips = sTips.replace("$moneyCash",str(abs(iVal)))
			message.tips(self, sTips)
			message.message(self, sTips)
		
		return iVal

	def addCash(self,iVal, sReason, sTips=""):
		'''增加或减少银币
		
		玩法相关的逻辑需要写在rewardCash或costCash
		'''
		if not isinstance(iVal, (int,long)):
			raise Exception, "非法的银币值:%s" % iVal
		if self.cash + iVal < 0:
			raise Exception, '不能把银币扣成负数,否则{}+({})={}.'.format(self.cash, iVal, self.cash + iVal)

		writeLog("role/cash", "%d %d%+d->%d %s" % (self.id, self.cash, iVal, self.cash + iVal, sReason))
		self.cash += iVal
		self.attrChange("cash")
		
		if sTips != None:
			if iVal > 0:
				sTips = sTips if sTips else "获得银币#R<$cash,3,2>#n"
			elif iVal < 0:
				sTips = sTips if sTips else "消耗银币#R<$cash,3,2>#n"
			else:
				return 0
			sTips = sTips.replace("$cash", str(abs(iVal)))
			message.tips(self, sTips)
			message.message(self, sTips)
			
		import listener
		if iVal > 0:
			listener.doListen("增加银币", self, cash=iVal)
		
		return iVal

	def rewardCash(self, iVal, sReason, sTips=""):
		'''奖励银币
		'''
		if iVal < 0:
			raise Exception, '奖励的银币不能是负数{}'.format(iVal)
		return self.addCash(iVal, sReason, sTips)

	def costCash(self, iVal, sReason, sTips=""):
		'''消耗银币
		'''
		if iVal < 0:
			raise Exception, '消耗的银币不能是负数{}'.format(iVal)
		return self.addCash(-iVal, sReason, sTips)

	def addTradeCash(self, iVal, sReason, sTips=""):
		'''增加或减少交易币
		
		玩法相关的逻辑需要写在rewardTradeCash或costTradeCash
		'''
		if not isinstance(iVal, (int,long)):
			raise Exception, "非法的元宝值:%s" % iVal
		if self.tradeCash + iVal < 0:
			raise Exception, '不能把元宝扣成负数,否则{}+({})={}.'.format(self.tradeCash, iVal, self.tradeCash + iVal)

		writeLog("role/tradeCash", "%d %d%+d->%d %s" % (self.id, self.tradeCash, iVal, self.tradeCash + iVal, sReason))
		self.tradeCash += iVal
		self.attrChange("tradeCash")
		
		if sTips != None:
			if iVal > 0:
				sTips = sTips if sTips else "获得元宝#R<$tradeCash,2,2>#n"
			elif iVal < 0:
				sTips = sTips if sTips else "消耗元宝#R<$tradeCash,2,2>#n"
			else:
				return 0
			sTips = sTips.replace("$tradeCash",str(abs(iVal)))
			message.tips(self, sTips)
			message.message(self, sTips)
		
		return iVal

	def rewardTradeCash(self, iVal, sReason, sTips=""):
		'''奖励元宝
		'''
		if iVal < 0:
			raise Exception, '奖励的元宝不能是负数{}'.format(iVal)
		return self.addTradeCash(iVal, sReason, sTips)

	def costTradeCash(self, iVal, sReason, sTips=""):
		'''消耗元宝
		'''
		if iVal < 0:
			raise Exception, '消耗的元宝不能是负数{}'.format(iVal)
		return self.addTradeCash(-iVal, sReason, sTips)

	def ettType(self):#实体类型
		import entity
		return entity.ETT_TYPE_ROLE
	
	# def getLeaveMsgSerialized(self):#序列化后的离开消息(离开场景时广播给周围的玩家)
	# 	if not getattr(self,'sLeaveMsgSerialized',None):#防止重复序列化
	# 		oLeaveMsg=scene_pb2.entityLeave()
	# 		oLeaveMsg.iEttId=self.iRoleId
	# 		#oLeaveMsg.iEttType=self.ettType()
	# 		self.sLeaveMsgSerialized=endPoint.makePacket('rpcEttLeave',oLeaveMsg)
	# 	return self.sLeaveMsgSerialized
		
	# def getSerializedGroup(self):#duck type func for entity 场景广播数据
	# 	infoList = []
	# 	entityInfo = role.roleHelper.getEntityEnter(self)
	# 	infoList.append(endPoint.makePacket('rpcEttEnter', entityInfo))
		
	# 	import team.service
	# 	teamObj = self.getTeamObj()
	# 	if teamObj and teamObj.isLeader(self.id):
	# 		teamMakeInfo = team.service.packTeamMakeInfo(teamObj)
	# 		infoList.append(endPoint.makePacket('rpcTeamBroadcastMake', teamMakeInfo))

	# 	return infoList

	def getEttBaseSerialized(self):
		return role.roleHelper.getSerializedEtt(self)
			
	# def onEntityEnter(self,oEtt,itPacket):#将oEtt的信息发给自己
	# 	ep=self.endPoint
	# 	if ep:
	# 		for sPacket in itPacket:
	# 			ep.send(sPacket)

	# def onEntityLeave(self,oEtt):#将oEtt离开的信息发给自己		
	# 	ep=self.endPoint
	# 	if ep:
	# 		ep.send(oEtt.getLeaveMsgSerialized())

	def send(self,sPacket):
		ep=self.endPoint
		if ep:
			ep.send(sPacket)

	def disConnectedEventHandler(self,ep):#事件响应函数,channel断线后调用到这里来的,顶号也会调用到此处来
		self.eDisConnected(self)#触发事件.
		self.iDisConnectStamp=timeU.getStamp()
		self.setDestroyLater()
		print '角色对象disConnectedEventHandler:{},{}'.format(self.iRoleId,self.name)
		log.log('loginLogout','({},{}),id={}角色断线了'.format(self.sUserSource,self.sAccount,self.iRoleId))

	def setDestroyLater(self):
		ft=u.cFunctor(role.gKeeper.removeObj,self.iRoleId)
		role.gTimingWheel.addCallback(ft,self.iRoleId)#一段时间后再remove

	def onReLogin(self):
		self.eReLogin(self)#触发事件.	
		role.geReLogin(self)
		self.iDisConnectStamp=0 #重置最后断线时间戳	
		self.cancelDestroyLater()
		print '角色对象onReLogin:{}'.format(self.name)
		log.log('loginLogout','({},{}){}角色重连了'.format(self.sUserSource,self.sAccount,self.iRoleId))

	def cancelDestroyLater(self):
		role.gTimingWheel.removeCallback(self.iRoleId)
	
	def full(self,bBroadcast=True):#满红满蓝
		iAddHp=self.hpMax-self.hp
		self.hp=self.hpMax
		self.mp=self.mpMax
		if bBroadcast:		
			self.attrChange('hp','mp')#刷新界面,通知周边玩家,重置sSerialized..
		if iAddHp>0:
			self.eHpChange(self,iAddHp)#触发hp变化事件
		#触发复活事件

	def getRoleAttrByCurLv(self,sKey,uDefalut=0):#根据当前等级拿属性
		return roleExpData.getConfig(self.level,sKey,uDefalut)
	
	def addObserver(self,iEvent,func):#增加观察者
		if iEvent not in self.dEvent:
			self.dEvent[iEvent]=u.cEvent()
		self.dEvent[iEvent]+=func

	def removeObserver(self,iEvent,func):#清除观察者
		if iEvent not in self.dEvent:
			return
		self.dEvent[iEvent]-=func
		if self.dEvent[iEvent].observerCount()<=0:#一个观察者都没,把事件也清掉吧
			self.dEvent.pop(iEvent,None)
	
	def triggerEvent(self,iEvent,*tArgs,**dArgs):#触发事件
		if iEvent in self.dEvent:
			self.dEvent[iEvent](iEvent,self,*tArgs,**dArgs)
			
	def addExp(self,iVal, sReason, sTips="", **kwargs):
		'''增加或减少经验
		
		玩法相关的逻辑需要写在rewardExp或costExp
		'''
		if not isinstance(iVal, int):
			raise Exception, "非法的经验值:%s" % iVal
		if self.exp + iVal < 0:
			raise Exception, '不能把经验扣成负数,否则{}+({})={}.'.format(self.exp, iVal, self.exp + iVal)
		
		writeLog("role/exp", "%d %d%+d->%d %s" % (self.id, self.exp, iVal, self.exp + iVal, sReason))
		self.exp += iVal
		
		if sTips != None:
			if iVal > 0:
				sAdditionTips = kwargs.get("sAdditionTips", "")
				sTips = sTips if sTips else "获得#C02$exp#n点经验{}".format(sAdditionTips)
			elif iVal < 0:
				sTips = sTips if sTips else "消耗#C02$exp#n点经验"
			else:
				return 0
			sTips = sTips.replace("$exp", str(abs(iVal)))
			message.tips(self, sTips)
			message.message(self, sTips)
		
		if self.exp >= self.expNext and self.expNext > 0 and self.level < self.getMaxLevel():
			self.upLevel()
		self.attrChange("exp")
		openLevel.checkExpRatio(self)
		rank.changeExpUpdateRank(self)

		return iVal

	def rewardExp(self, iVal, sReason, sTips=""):
		'''奖励经验
		'''
		if iVal < 0:
			raise Exception, '奖励的经验不能是负数{}'.format(iVal)
		iTotalVal = iVal
		lAdditionTips = []	#经验加成提示

		if not sReason.startswith("task4"):
			ratio = self.getExpRatio()
			iTotalVal = int(iVal * ratio / 100)
			if ratio > 100:
				lAdditionTips.append('#C02福泽天下#n加成#C02{}#n点'.format(int(iVal*(ratio-100)/100.0)))
			
		#历练经验转化
		iTransfromExp =	tougheningExp.tougheningExpTransform(self, iVal, sReason)
		if iTransfromExp:
			iTotalVal += iTransfromExp
			lAdditionTips.append('#C02历练经验#n转化#C02{}#n点'.format(iTransfromExp))
		
		sAdditionTips = ''
		if lAdditionTips:
			sAdditionTips = '('+'，'.join(lAdditionTips)+')'
		return self.addExp(iTotalVal, sReason, sTips, sAdditionTips=sAdditionTips)

	def costExp(self, iVal, sReason, sTips=""):
		'''消耗经验
		'''
		if iVal < 0:
			raise Exception, '消耗的经验不能是负数{}'.format(iVal)
		return self.addExp(-iVal, sReason, sTips)

	@property
	def expNext(self):#升级所需经验
		return self.getRoleAttrByCurLv('升级经验',0)
	
	def upLevel(self):#升级
		self.exp -= self.expNext
		self.add("level", 1)
		oAccount=self.accountObj
		if oAccount:
			oAccount.setLv(self.iRoleId,self.fetch("level"))
		log.log('lv','id:{},name:{},lv:{},school:{},userSource:{},account:{}'.format(self.iRoleId,self.name,self.fetch("level"),self.school,self.sUserSource,self.sAccount))

		self.addPoint()
		self.reCalcAttr()
		self.hp = self.hpMax
		self.mp = self.mpMax
		self.attrChange('level','expNext','point','hp','mp',)#刷新到客户端
		self.triggerEvent(event.ROLE_UP)
		
		role.geUpLevel(self)
		resume.updateResume(self)
		self.onUpLevel()
		scene.playSceneEffect(self, EFFECT_UPGRADE, self.id)#
		scene.broadcastEttEffect(EFFECT_UPGRADE_OTHER, self.id)
		openLevel.checkOpenNewLevel(self.level)
		listener.doListen("人物升级", self, level=self.level)
			
	def onUpLevel(self):
		skill.onUpLevel(self)
		task.onUpLevel(self)
		activity.onUpLevel(self)
		team.onUpLevel(self)
		guild.onUpLevel(self)
		#props.onUpLevel(self)
		buddy.onUpLevel(self)
		ride.onUpLevel(self)
		role.onUpLevel(self)
		role.register.updateRole(self, level=self.level)

	def addPoint(self):
		for oScheme in self.schemeCtn.getAllScheme():
			if self.level<40:
				dPoint = pointAllot.getPointInfo(self.school)
				for key,value in role.defines.attrDescList.iteritems():
					iAdd = dPoint.get(value,0)
					if iAdd:
						oScheme.add(key,iAdd)
			else: 
				oScheme.add('point',5)

		for attr in role.defines.baseAttrList:
			self.add(attr,1)#加基础属性点

# 	def att(self):
# 		return self.iAtt
# 
# 	def defense(self):
# 		return self.iDef
# 
# 	def hit(self):
# 		return self.iHit
# 
# 	def crit(self):
# 		return self.iCrit
# 
# 	def dodge(self):
# 		return self.iDodge
# 
# 	def spi(self):
# 		return self.iSpi
# 
# 	def hpMax(self):
# 		return self.iHpMax
# 
# 	def mpMax(self):
# 		return self.iMpMax
# 
# 	def hp(self):
# 		return self.iHp
# 
# 	def mp(self):
# 		return self.iMp

# 	def addHp(self,iAdd,oAttacker=None):#增加,扣减血量
# 		iAdd=int(iAdd)
# 		if self.iHp+iAdd>self.hpMax():
# 			iAdd=self.hpMax()-self.iHp
# 		elif self.iHp+iAdd<0:
# 			iAdd=-self.iHp
# 		if iAdd==0:
# 			return 0
# 		# log.log('hp','{} add {}'.format(self.iRoleId,iAdd))
# 		self.iHp+=iAdd
# 		self.attrChange('hp')#通知到客户端和周围玩的玩家
# 		if self.iHp==0 and self.cDieHandler:
# 			for func in self.cDieHandler:
# 				func(self,oAttacker)#调用死亡处理函数
# 		self.eHpChange(self,iAdd)#触发hp变化事件
# 		return iAdd
# 
# 	def addMp(self,iAdd):
# 		iAdd=int(iAdd)
# 		if self.iMp+iAdd>self.mpMax():
# 			iAdd=self.mpMax()-self.iMp
# 		elif self.iMp+iAdd<0:
# 			iAdd=-self.iMp
# 		if iAdd==0:
# 			return 0
# 		log.log('mp','{} add {}'.format(self.iRoleId,iAdd))
# 		self.iMp+=iAdd
# 		self.attrChange('mp')

	# def addVirtualTool(self,iVirtualNo,iAmount,sLogReason='',sTips=''):  #添加虚拟物品 ,元宝,钻石,竞技点等等
	# 	if iVirtualNo not in c.VIR_ITEM:#虚拟道具
	# 		raise Exception,'不是虚拟道具,程序员检查错误'
	# 	if iVirtualNo in gdVirtuaNoMap:
	# 		getattr(self, gdVirtuaNoMap[iVirtualNo])(iAmount,sLogReason,sTips)	
	# 	else:
	# 		raise Exception,'漏写代码支持虚拟物品编号{}'.format(iVirtualNo)

	def log4report(self,sLogName,**dExtra):
		try:
			dBase={}
			dBase['t']=timeU.stamp2str() #时间
			dBase['ser']=config.ZONE_ID #区id
			dBase['rid']=self.iRoleId #角色id
			dBase['rn']=self.fetch("name") #角色名字
			dBase['school']=self.school #角色职业
			oAcnt=self.accountObj
			dBase['os']=oAcnt.osType() #客户端操作系统类型
			#self.sUserSource #用户来源(xx说不用记录,他那边可以根据登录子渠道反推出来)
			dBase['ep']=oAcnt.sLoginAppId #当前登录所用客户端标识(登录子渠道)
			dBase['uid']=self.sAccount #uid,用户账号		
			
			dBase.update(dExtra)#基础信息补上额外信息
			log.log(sLogName,'{}'.format(json.dumps(dBase)))
		except Exception:
			misc.logException()
			
	def queryApply(self, name):
		return self.applyMgr.query(name)
	
	def addApply(self, name, val, flag="flag"):
		self.applyMgr.add(name, val, flag)
		
	def setApply(self, name, val, flag="flag"):
		self.applyMgr.set(name, val, flag)
		
	def removeApply(self, name, flag="flag"):
		self.applyMgr.remove(name, flag)
				
	def removeApplyByFlag(self, flag):
		self.applyMgr.removeByFlag(flag)
	
	@property
	def name(self):
		return self.fetch("name", "玩家%d" % self.id)

	@name.setter
	def name(self, name):
		self.set("name", name)
		resume.updateResume(self)
		role.register.updateRole(self, name=name)

	@property
	def shape(self):
		'''造型
		'''
		if hasattr(self, "shapeTmp"):
			return self.shapeTmp
		return self.fetch("shape", 1111)
	
	@property
	def shapeParts(self):
		'''造型部位
		'''
		if hasattr(self, "shapePartsTmp"):
			shapeParts = self.shapePartsTmp
		else:
			shapeParts = self.fetch("shapeParts", {})
		return transToShapePartList(shapeParts)
	
	def setShapeParts(self, shapePartType, shapePart, refresh=True):
		'''设置造型部位
		'''
		shapeParts = self.fetch("shapeParts", {})
		shapeParts[shapePartType] = shapePart
		self.set("shapeParts", shapeParts)
		if refresh:
			self.attrChange("shapeParts")
		resume.updateResume(self)

	def getColors(self):
		'''染色
		'''
		colors = self.fetch("colors", {})
		return role.defines.transToColorList(colors)
	
	def setColors(self, colorList):
		'''设置染色
		'''
		colors = self.fetch("colors", {})
		for shapePartType, color in colorList.items():
			colors[shapePartType] = color
		self.set("colors", colors)
		self.attrChange("colors")
		resume.updateResume(self)

	def getRideShape(self):
		rideObj = self.rideCtn.getRindCurrent()
		if rideObj:
			return rideObj.shape
		return 0
		
	def getRideShapePart(self):
		rideObj = self.rideCtn.getRindCurrent()
		if rideObj:
			return rideObj.shapeParts
		return None

	def getRideColors(self):
		rideObj = self.rideCtn.getRindCurrent()
		if rideObj:
			return rideObj.getColors()
		return None

	@property
	def gender(self):
		'''性别
		'''
		if self.fetch("shape", 1111) in role.defines.maleList:
			return role.defines.MALE
		return role.defines.FEMALE

	@property
	def level(self):
		'''等级
		'''
		return self.fetch("level", 0)

	def getExpRatio(self):
		'''经验加成
		'''
		if not hasattr(self,"ratio"):
			self.ratio = openLevel.getExpRatio(self)

		return self.ratio
	
	def getMaxLevel(self):
		'''最大等级
		'''
		return roleExpData.MAX_ROLE_LV

	def getRealLevel(self):
		'''实际等级
		'''
		exp = self.exp
		level = self.level

		if self.exp > self.expNext:
			for i in xrange(level,roleExpData.MAX_ROLE_LV+1):
				exp -= roleExpData.gdData[level]["升级经验"]
				if exp < 0 :
					break
				level += 1

		return level

	@property
	def school(self):
		'''门派
		'''
		return self.fetch("school", 11)
	
	@school.setter
	def school(self, schoolId):
		self.set("school", schoolId)
		self.attrChange("school")
		role.register.updateRole(self, schoolId=schoolId)

	@property
	def point(self):
		'''潜力点
		'''
		return self.schemeCtn.getScheme().fetch('point')

	def reCalcAttr(self,bRefresh=True):
		'''计算属性
		'''
		oldHpMax = self.hpMax
		oldMpMax = self.mpMax
		oldFightPower = self.fightPower

		refreshList = {}
		attrData = role.calattr.calcAttr(self)
		for attr,val in attrData.iteritems():
			if getattr(self, attr, 0) != val:
				refreshList[attr] = 1
			setattr(self, attr, val)

		if oldHpMax and oldHpMax != self.hpMax:
			subHpMax = self.hpMax - oldHpMax
			self.hp += subHpMax
			refreshList["hp"] = 1
		if self.hp > self.hpMax:
			self.hp = self.hpMax
			refreshList["hp"] = 1
		elif self.hp < 0:
			self.hp = 0
			refreshList["hp"] = 1
		
		if oldMpMax and oldMpMax != self.mpMax:
			subMpMax = self.mpMax - oldMpMax
			self.mp += subMpMax
			refreshList["mp"] = 1
		if self.mp > self.mpMax:
			self.mp = self.mpMax
			refreshList["mp"] = 1
		elif self.mp < 0:
			self.mp = 0
			refreshList["mp"] = 1

		if self.sp > self.spMax:
			self.sp = self.spMax
			refreshList["sp"] = 1
		
		if bRefresh and refreshList:
			self.attrChange(*refreshList)

		#更新排行榜
		#记录最高战力
		oldHighestFightPower =  self.fetch("highestScore", 0)
		if self.fightPower > oldHighestFightPower:
			self.set("highestScore", self.fightPower)
		if oldFightPower and self.fightPower > oldHighestFightPower:
			rank.updateRoleFightRank(self)

	def addHP(self, val, bRefresh=True):
		'''加、扣生命
		'''
		self.hp += val
		if val > 0:
			if self.hp > self.hpMax:
				self.hp = self.hpMax
		elif val < 0:
			if self.hp < 0:
				self.hp = 0
		if bRefresh:
			self.attrChange("hp")
		
	def addMP(self, val, bRefresh=True):
		'''加、扣真气
		'''
		self.mp += val
		if val > 0:
			if self.mp > self.mpMax:
				self.mp = self.mpMax
		elif val < 0:
			if self.mp < 0:
				self.mp = 0
		if bRefresh:
			self.attrChange("mp")

	def addSP(self, val, bRefresh=True):
		'''加、扣愤怒
		'''
		self.sp += val
		if val > 0:
			if self.sp > self.spMax:
				self.sp = self.spMax
		elif val < 0:
			if self.sp < 0:
				self.sp = 0
		if bRefresh:
			self.attrChange("sp")
		
	def addHuoli(self, val, reason, tips="", bRefresh=True):
		'''加、扣活力
		'''
		writeLog("role/huoli", "%d %d%+d->%d %s" % (self.id, self.huoli, val, self.huoli + val, reason))
		self.huoli += val
		if val < 0:
			if self.huoli < 0:
				self.huoli = 0
		if bRefresh:
			self.attrChange("huoli")
		if tips != None:
			if val > 0:
				tips = tips if tips else "获得活力#R<$huoli,9,2>#n点"
			elif val < 0:
				tips = tips if tips else "消耗活力#R<$huoli,9,2>#n点"
			else:
				return 0
			tips = tips.replace("$huoli",str(abs(val)))
			message.tips(self, tips)
			message.message(self, tips)	
	
	def getDemonPoint(self):
		'''降魔积分
		'''
		return self.fetch("demonPoint")

	def addDemonPoint(self, val, reason, tips="", bRefresh=True):
		'''加、扣降魔积分
		'''
		writeLog("role/domonpoint", "%d %d%+d->%d %s" % (self.id, self.fetch("demonPoint"), val, self.fetch("demonPoint") + val, reason))
		self.add("demonPoint", val)
		if val < 0 and self.fetch("demonPoint") < 0:
			self.delete("demonPoint", 0)
		if bRefresh:
			self.attrChange("demonPoint")
		if tips != None:
			if val > 0:
				tips = tips if tips else "获得降魔积分#R<$demonPoint,4,2>#n点"
			elif val < 0:
				tips = tips if tips else "消耗降魔积分#R<$demonPoint,4,2>#n点"
			else:
				return 0
			tips = tips.replace("$demonPoint",str(abs(val)))
			message.tips(self, tips)
			message.message(self, tips)	
			
	def getSchoolPoint(self):
		'''门贡
		'''
		return self.fetch("schoolPoint")

	def addSchoolPoint(self, val, reason, tips="", bRefresh=True):
		'''加、扣门贡
		'''
		writeLog("role/schoolpoint", "%d %d%+d->%d %s" % (self.id, self.fetch("schoolPoint"), val, self.fetch("schoolPoint") + val, reason))
		self.add("schoolPoint", val)

		if val < 0 and self.fetch("schoolPoint") < 0:
			self.delete("schoolPoint", 0)
		if bRefresh:
			self.attrChange("schoolPoint")
		if tips != None:
			if val > 0:
				tips = tips if tips else "获得师门贡献#R<$schoolPoint,5,2>#n点"
			elif val < 0:
				tips = tips if tips else "消耗师门贡献#R<$schoolPoint,5,2>#n点"
			else:
				return 0
			tips = tips.replace("$schoolPoint",str(abs(val)))
			message.tips(self, tips)
			message.message(self, tips)
			
	def addGuildPoint(self, val, reason, bRefresh=True):
		'''加、扣帮贡
		'''
		pointOld = self.fetch("guildPoint")
		point = pointOld + val
		if point < 0:
			point = 0
		self.set("guildPoint", point)
		writeLog("role/guildpoint", "%d %d%+d->%d %s" % (self.id, pointOld, val, point, reason))
		if bRefresh:
			self.attrChange("guildPoint")
		if val > 0:
			tips = "获得仙盟贡献#R<{},7,2>#n点".format(abs(val))
			self.add("ttGuildPoint", val) # 增加历史贡献
			self.week.add("guildPoint", val) # 本周贡献
		elif val < 0:
			tips = "消耗仙盟贡献#R<{},7,2>#n点".format(abs(val))
		message.tips(self, tips)
		message.message(self, tips)
		guild.updateMemberInfo(self)

	def getGuildPoint(self):
		return self.fetch("guildPoint")

	def getTtGuildPoint(self):
		'''总帮贡(历史帮贡)
		'''
		return self.fetch("ttGuildPoint")

	def addHolidayPoint(self, val, reason, bRefresh=True):
		'''加、扣节日积分
		'''
		writeLog("role/holidaypoint", "%d %d%+d->%d %s" % (self.id, self.fetch("holidayPoint"), val, self.fetch("holidayPoint") + val, reason))
		self.add("holidayPoint", val)
		if val < 0 and self.fetch("holidayPoint") < 0:
			self.delete("holidayPoint", 0)
		if bRefresh:
			self.attrChange("holidayPoint")

	def addMasterPoint(self, val, reason, bRefresh=True):
		'''加、扣良师值
		'''
		writeLog("role/masterpoint", "%d %d%+d->%d %s" % (self.id, self.fetch("masterPoint"), val, self.fetch("masterPoint") + val, reason))
		self.add("masterPoint", val)
		if val < 0 and self.fetch("masterPoint") < 0:
			self.delete("masterPoint", 0)
		if bRefresh:
			self.attrChange("masterPoint")
			
	def getPKPoint(self):
		'''获取武勋值
		'''
		return self.fetch("pkPoint")

	def addPKPoint(self, val, reason, tips="", refresh=True):
		'''加、扣武勋值
		'''
		if val == 0:
			return
		writeLog("role/pkpoint", "%d %d%+d->%d %s" % (self.id, self.fetch("pkPoint"), val, self.fetch("pkPoint") + val, reason))
		point = self.fetch("pkPoint") + val
		if point < 0:
			point = 0
		self.set("pkPoint", point)
		if refresh:
			self.attrChange("pkPoint")
		
		if tips != None:
			if val > 0:
				tips = tips if tips else "获得武勋值#R<$pkPoint,8,2>#n点"
			elif val < 0:
				tips = tips if tips else "消耗武勋值#R<$pkPoint,8,2>#n点"
			else:
				return 0
			tips = tips.replace("$pkPoint",str(abs(val)))
			message.tips(self, tips)
			message.message(self, tips)
	
	def getHelpPoint(self):
		'''获取侠义值
		'''
		return self.fetch("helpPoint")

	def addHelpPoint(self, val, reason, tips="", bRefresh=True):
		'''加、扣侠义值
		'''
		if val > 0:#只限制增加
			dayhelpPoint = self.day.fetch("dayhelpPoint")
			if MaxHelpPoint <=dayhelpPoint:
				val = 0
			if MaxHelpPoint<=(dayhelpPoint + val):
				self.day.set("dayhelpPoint", MaxHelpPoint)
				val  = MaxHelpPoint-dayhelpPoint
			else:
				self.day.add("dayhelpPoint", val)

		if not val:
			return
		writeLog("role/helppoint", "%d %d%+d->%d %s" % (self.id, self.fetch("helpPoint"), val, self.fetch("helpPoint") + val, reason))
		self.add("helpPoint", val)
		if val < 0 and self.fetch("helpPoint") < 0:
			self.delete("helpPoint", 0)
		if bRefresh:
			self.attrChange("helpPoint")
		if tips != None:
			if val > 0:
				tips = tips if tips else "获得侠义值#R<$helpPoint,6,2>#n点"
			elif val < 0:
				tips = tips if tips else "消耗侠义值#R<$helpPoint,6,2>#n点"
			else:
				return 0
			tips = tips.replace("$helpPoint",str(abs(val)))
			message.tips(self, tips)
			message.message(self, tips)		

	def getFlowerPoint(self):
		'''获取献花积分
		'''
		return self.fetch("flowerPoint")
		
	def addFlowerPoint(self, val, reason, tips="", bRefresh=True):
		'''加、扣献花积分
		'''
		writeLog("role/flowerpoint", "%d %d%+d->%d %s" % (self.id, self.fetch("flowerPoint"), val, self.fetch("flowerPoint") + val, reason))
		self.add("flowerPoint", val)
		if val < 0 and self.fetch("flowerPoint") < 0:
			self.delete("flowerPoint", 0)
		if bRefresh:
			self.attrChange("flowerPoint")
		if tips != None:
			if val > 0:
				tips = tips if tips else "获得献花积分#R<$flowerPoint,6,2>#n点"
			elif val < 0:
				tips = tips if tips else "消耗献花积分#R<$flowerPoint,6,2>#n点"
			else:
				return 0
			tips = tips.replace("$flowerPoint",str(abs(val)))
			message.tips(self, tips)
			message.message(self, tips)			

	def addDoublePoint(self, val, reason, bRefresh=True):
		'''加、扣双倍点数
		'''
		if val == 0:
			return
		if self.doublePoint + val < 0:
			raise Exception, '不能把双倍点扣成负数,否则{}+({})={}'.format(self.doublePoint,val,self.doublePoint+val)
		self.doublePoint += val
		state.checkDoublePointState(self)
		writeLog('role/doublePoint','{} add {},remain {},reason={}'.format(self.id,val,self.doublePoint,reason))
		if bRefresh:
			activity.center.centerChange(self,"doublePoint")

	def getFrozenDoublePoint(self):
		'''未领取的双倍点
		'''
		frozenDoublePoint = self.week.fetch("fDoublePoint")
		lastWDay = self.week.fetch("fdpwDay")
		wDay = getDatePart()["wday"]
		if wDay > lastWDay:
			addPoint = (wDay - lastWDay) * 40
			self.addFrozenDoublePoint(addPoint, "%d天共赠送%d点双倍点" % (wDay-lastWDay,addPoint))
			self.week.set("fdpwDay",wDay)

		return frozenDoublePoint

	def addFrozenDoublePoint(self, iVal, sReason):
		'''加、扣未领取的双倍点
		'''
		if iVal == 0:
			return
		frozenDoublePoint = self.week.fetch("fDoublePoint")
		if frozenDoublePoint + iVal <0:
			raise Exception,"未领取的双倍点不可能少于0"
		frozenDoublePoint += iVal
		if frozenDoublePoint > 280:
			frozenDoublePoint = 280
		self.week.set("fDoublePoint",frozenDoublePoint)
		writeLog("role/doublePoint", "未领取的双倍点数: {} add {},remain {},reason={}".format(self.id, iVal, frozenDoublePoint, sReason))
		return iVal

	def addRacePoint(self, val, reason):
		'''加、扣竞技积分
		'''
		self.checkRacePoint()
		valOld = self.fetch("racePoint")
		valNew = valOld + val
		if valNew < 0:
			valNew = 0
		self.set("racePoint", valNew)
		writeLog("role/racepoint", "%d %d%+d->%d %s" % (self.id, valOld, val, valNew, reason))
		
	def getRacePoint(self):
		'''竞技积分
		'''
		self.checkRacePoint()
		return self.fetch("racePoint")
	
	def checkRacePoint(self):
		actObj = activity.getActivity("race")
		if not actObj:
			return
		termNo = actObj.getTermNo()
		if self.fetch("raceTermNo") != termNo:
			self.set("raceTermNo", termNo)
			self.delete("racePoint")

	def addTeamRacePoint(self, val, reason):
		'''加、扣组队竞技积分
		'''
		self.checkTeamRacePoint()
		weekNo = getWeekNo()
		teamRacePoint = self.fetch("teamRacePoint", {})
		valOld = teamRacePoint.get(weekNo, 0)
		valNew = valOld + val
		if valNew < 0:
			valNew = 0
		teamRacePoint[weekNo] = valNew
		self.set("teamRacePoint", teamRacePoint)
		writeLog("role/teamracepoint", "%d %d%+d->%d %s|%s" % (self.id, valOld, val, valNew, reason, teamRacePoint))

	def getTeamRacePoint(self):
		'''组队竞技积分
		'''
		self.checkTeamRacePoint()
		actObj = activity.getActivity("teamRace")
		if not actObj:
			return 0
		teamRacePoint = self.fetch("teamRacePoint", {})
		return actObj.calcAttrTeamRacePoint(teamRacePoint)

	def checkTeamRacePoint(self):
		'''只保存最近4周的组队竞技积分
		'''
		actObj = activity.getActivity("teamRace")
		if not actObj:
			return
		teamRacePoint = self.fetch("teamRacePoint", {})
		change = actObj.checkTeamRacePoint(teamRacePoint)
		if change:
			self.set("teamRacePoint", teamRacePoint)
			
	def addAchvPoint(self, val, reason):
		'''加、扣成就点
		'''
		if val == 0:
			return
		
		oldPoint = self.fetch("achvPoint")
		point = oldPoint + val
		if point < 0:
			point = 0
		self.set("achvPoint", point)
		writeLog("role/achvPoint", "%d %d%+d->%d %s" % (self.id, oldPoint, val, point, reason))

	def getTougheningExp(self):
		return self.fetch("tougheningExp")
		
	def addTougheningExp(self, val, reason, bRefresh=True):
		'''加、扣历练经验
		'''
		if val == 0:
			return
		
		oldToughengingExp = self.fetch("tougheningExp")
		tougheningExp = oldToughengingExp + val
		if tougheningExp < 0:
			tougheningExp = 0
		self.set("tougheningExp", tougheningExp)
		if bRefresh:
			self.attrChange('tougheningExp')
		writeLog("role/tougheningExp", "%d %d%+d->%d %s" % (self.id, oldToughengingExp, val, tougheningExp, reason))

	def addReserveHp(self,val,bRefresh=True):
		self.reserveHp += val
		if self.reserveHp<0:
			self.reserveHp = 0
		if bRefresh:
			self.attrChange('reserveHp')
		self.stateCtn.updateItemByKey(102)

	def addReserveMp(self,val,bRefresh=True):
		self.reserveMp += val
		if self.reserveMp<0:
			self.reserveMp = 0
		if bRefresh:
			self.attrChange('reserveMp')
		self.stateCtn.updateItemByKey(103)

	def recover(self, bRefresh):
		iAddHp = self.hpMax-self.hp
		iAddHp = min(self.reserveHp,iAddHp)
		if iAddHp:
			self.addReserveHp(-iAddHp,bRefresh)
			self.addHP(iAddHp,bRefresh)

		iAddMp = self.mpMax-self.mp
		iAddMp = min(self.reserveMp,iAddMp)
		if iAddMp:
			self.addReserveMp(-iAddMp,bRefresh)
			self.addMP(iAddMp,bRefresh)

	def attrChange(self, *attrs):
		if hasattr(self, "isClientInited") and not self.isClientInited: # 客户端未初始化前不刷新
			return
		role.roleHelper.attrChange(self, *attrs)
		
	def broadcastAttrChange(self, *attrs):
		if hasattr(self, "isClientInited") and not self.isClientInited: # 客户端未初始化前不刷新
			return
		role.roleHelper.broadcastAttrChange(self, *attrs)
		
	def inWar(self):
		'''是否在参战或观战中
		'''
		return getattr(self, "war", None)
	
	def inWatchWar(self):
		'''是否在观战中
		'''
		if not self.inWar():
			return None
		if self.warrior.isWatcher():
			return self.war
		return None
		
	def enterWar(self, warObj, w):
		'''进入战斗
		'''
		self.war = warObj
		self.warrior = w
		self.broadcastAttrChange("addon")
		role.register.updateRole(self, warId=warObj.id)
		
	def leaveWar(self):
		'''离开战斗
		'''
		if hasattr(self, "war"):
			del self.war
		if hasattr(self, "warrior"):
			del self.warrior
		if hasattr(self, "lastFightPetId"):
			del self.lastFightPetId
		self.broadcastAttrChange("addon")
		role.register.updateRole(self, warId=0)
		self.executeHandlerForWarEnd()
		
		import task.offlineTask
		if task.offlineTask.inOfflineTask(self):
			if self.hp < self.hpMax or self.mp < self.mpMax:
				task.offlineTask.quitOfflineTask(self)
		
	def addHandlerForWarEnd(self, flag, handler):
		'''增加战后处理
		'''
		self.handlerListForWarEnd[flag] = handler
		
	def executeHandlerForWarEnd(self):
		'''执行战后处理
		'''
		funcList = self.handlerListForWarEnd.values()
		self.handlerListForWarEnd = {}
		for func in funcList:
			func(self)
		
	def setSkill(self, skillId, level):
		'''设置技能等级
		'''
		return self.skillCtn.setLevel(skillId, level)
	
	def addEquipSkill(self, propsId, *skillIdList):
		'''增加装备技能(特技特效)
		'''
		import skill
		for skillId in skillIdList:
			skillObj = skill.new(skillId)
			if not skillObj:
				continue
			skillObj.level = 1
			self.equipSkillCtn.addItem(propsId, skillObj)

	def removeEquipSkill(self, propsId):
		'''移除装备技能(特技特效)
		'''
		self.equipSkillCtn.removeItemByPropsId(propsId)
	
	def querySkillLevel(self, skId):
		'''查询技能等级
		'''
		if skId / 1000 in (3, 4,):
			return self.equipSkillCtn.getLevel(skId)
		return self.skillCtn.getLevel(skId)
	
	def getSkillList(self):
		'''技能列表
		'''
		skillList = {}
		for skObj in self.skillCtn.getAllValues():
			skillList[skObj.id] = skObj
		for skObj in self.equipSkillCtn.getAllValues():
			skillList[skObj.id] = skObj
		return skillList
	
	def getPerformList(self):
		'''法术列表
		'''
		performList = []
		skillList = self.getSkillList()
		for skillId, skillObj in skillList.iteritems():
			if skill.getHigh(skillId) in skillList:  # 如此存在对应的高级技能，忽略该低级技能
				continue
			performList.extend(skillObj.getPerformList(self))
		
		return performList

	def getPracticeGuildLevel(self):
		'''修炼帮派级影响
		'''
		return 25
		guildObj = self.getGuildObj()
		if not guildObj:
			return 0
		return guildObj.getPraticeLevel()
	
	def getPracticeRoleLevel(self):
		'''修炼人物等级影响
		'''
		return skillPraticeLevelData.getRoleLevelLimit(self.level)

	def getPracticeGuildPoint(self):
		'''修炼帮派历史贡献影响
		'''
		return min(25,self.fetch("guildPoint")/150 + 5)
		guildObj = self.getGuildObj()
		if not guildObj:
			return 0
		return min(25,guildObj.getHistoryPoint(self)/150 + 5)

	def getMaxPracticeLevel(self):
		'''人物修炼到等级上限
		'''
		guildLevel = self.getPracticeGuildLevel()
		roleLevel = self.getPracticeRoleLevel()
		guildPoint = self.getPracticeGuildPoint()
		return min(guildLevel,roleLevel,guildPoint)

	def getReviveScene(self):
		'''复活场景
		'''			
		if self.level < 15:
			return (1010, 31, 52)
		return (1020, 112, 122)
			
	def revive(self):
		'''复活
		'''
		self.hp = 1
		self.mp = self.mpMax
		
	def refreshState(self):#"鸭子类型"接口
		'''刷新状态
		'''
		self.attrChange("hp", "hpMax", "mp", "mpMax", "sp", "spMax","reserveHp","reserveMp")
		
	def __getattr__(self, name):
		return object.__getattribute__(self.active, name)
	
	def __setattr__(self, name, value):
		if hasattr(self, "active") and hasattr(self.active, name):
			object.__setattr__(self.active, name, value)
			
			if name in ("x", "y"):
				if not hasattr(self, "lastChange"):
					self.lastChange = getSecond()
				elif getSecond() - self.lastChange < 300:
					return
				self.lastChange = getSecond()

			self.active.markDirty()
		else:
			object.__setattr__(self, name, value)
			
	def addTask(self, taskObj):
		'''增加任务
		'''
		self.taskCtn.addItem(taskObj)

		# 刷新可接任务
		activity.center.refreshTaskNpc(self)
		
	def removeTask(self, taskObj):
		'''移除任务
		'''
		self.taskCtn.removeItem(taskObj)
		
		# 刷新可接任务
		activity.center.refreshTaskNpc(self)
		
	def newDay(self):
		'''刷天
		'''
		self.checkDayNo()
		task.onNewDay(self)
		activity.onNewDay(self)
		state.onNewDay(self)
		tougheningExp.onNewDay(self)
		
	def checkDayNo(self):
		dayNo = self.fetch("dayNo")
		dayNoNow = getDayNo()
		if dayNo == dayNoNow:
			return

		self.set("dayNo", dayNoNow)
		# 业务逻辑
		if self.huoli > self.huoliMax:
			self.huoli = self.huoliMax	# 活力超过上限清理
			self.attrChange("huoli")

	def isAutoFight(self):
		'''是否自动战斗
		'''
		if self.fetch("autoFight", 1):
			return True
		return False
	
	def setAutoFight(self, isAuto):
		'''设置是否自动战斗
		'''
		if isAuto:
			self.set("autoFight", 1)
		else:
			self.set("autoFight", 0)
# 		self.attrChange("autoFight")
		
	def getDefaultPerform(self):
		'''获取默认法术
		'''
		performId = self.fetch("defaultPerform")
		if performId >= 100:
			if performId in self.getPerformList():
				return performId
		elif performId in (CMD_TYPE_PHY, CMD_TYPE_DEFEND):
			return performId

		return self.school * 100 + 11
	
	def setDefaultPerform(self, performId):
		'''设置默认法术
		'''
		if performId >= 100:
			if performId not in self.getPerformList():
				return
		elif performId not in (CMD_TYPE_PHY,CMD_TYPE_DEFEND):
			return
		self.set("defaultPerform", performId)

	def getOfflinePerform(self):
		'''获取离线挂机法术
		'''
		performId = self.fetch("offlinePerform")
		if performId >= 100:
			if performId in self.getPerformList():
				return performId
		elif performId in (CMD_TYPE_PHY, CMD_TYPE_DEFEND):
			return performId

		return self.school * 100 + 11
	
	def setOfflinePerform(self, performId):
		'''设置离线挂机法术
		'''
		if performId >= 100:
			if performId not in self.getPerformList():
				return
		elif performId not in (CMD_TYPE_PHY,CMD_TYPE_DEFEND):
			return
		self.set("offlinePerform", performId)

	def isOfflineTask(self):
		'''是否离线任务
		'''
		if self.fetch("isOfflineTask"):
			return True
		return False

	def setOfflineTask(self, isOfflineTask):
		'''设置离线任务
		'''
		if not self.fetch("isOfflineTask"):
			self.set("isOfflineTask", 1)
		else:
			self.delete("isOfflineTask")

	def getCapacity(self):
		'''获取背包容量
		'''
		return self.propsCtn.capacity()

	def getPointScheme(self):
		'''获取当前加点方案号
		'''
		return self.schemeCtn.getCurSchemeNo()
		
	def getValByName(self, attrName):
		'''根据属性名获取属性值
		'''	
		return getValByName(self, attrName)
	
	def getAddon(self):
		'''附加状态
		'''
		addon = 0
		teamObj = self.getTeamObj()
		if teamObj and teamObj.isLeader(self.id):
			addon |= role.defines.ADDON_TEAM_LEADER
		if self.inWar():
			addon |= role.defines.ADDON_FIGHT
		if self.inEscort():
			addon |= role.defines.ADDON_ESCORT
		if self.inTreasure():
			addon |= role.defines.ADDON_TREASURE
		return addon
	
	@property
	def tempCtn(self):
		'''临时背包
		'''
		import block.numenBag
		return block.numenBag.getNumenBag(self.id)
	
	def addProps(self, bagObj, propsObj, reason=""):
		writeLog("role/addprops", "%d %d*%d %s" % (self.id, propsObj.no(), propsObj.stack(), reason))
		propsIdList = []
		iLeft = propsObj.stack()
		iMaxStack = propsObj.maxStack()
		if propsObj.canAutoCombine():
			for obj in bagObj.getAllValues():
				if not propsObj.canAutoCombine(obj):
					continue
				iAdd = iMaxStack - obj.stack()
				if iAdd <= 0:
					continue
				if iAdd > iLeft:
					iAdd = iLeft
				iLeft -= iAdd
				bagObj.addStack(obj, iAdd)
				propsIdList.append(obj.id)
				if iLeft <= 0:
					break

		if iLeft:
			if iLeft != propsObj.stack():
				propsObj.setStack(iLeft)
			bagObj.addItem(propsObj)
			if bagObj == self.propsCtn and propsObj.shortcut(self):#弹出快捷使用
				self.endPoint.rpcShortcut(propsObj.getMsg4Package(None,*propsObj.MSG_FIRST))
			propsIdList.append(propsObj.id)
		return propsIdList
	
	def getProps(self, propsId):
		'''获取物品
		来源：包裹、临时背包、装备栏
		'''
		propsObj = self.propsCtn.getItem(propsId)
		if not propsObj:
			propsObj = self.tempCtn.getItem(propsId)
		if not propsObj:
			propsObj = self.equipCtn.getItem(propsId)
		return propsObj
	
	def isRobot(self):
		'''是否机器人角色
		'''
		return self.fetch("robot")
	
	def startTimer(self, func, ti, flag, interval=0):
		'''定时器开始
		'''
		self.timerMgr.run(func, ti, interval, flag)
		
	def stopTimer(self, flag):
		'''定时器结束
		'''
		self.timerMgr.cancel(flag)
		
	def hasTimer(self, flag):
		'''是否有定时器
		'''
		return self.timerMgr.hasTimerId(flag)
	
	def saveNow(self):
		'''即刻保存
		'''
		self.getFactory().saveProduct2db(self.id)
		
	def getLastFightPet(self):
		'''获取最后一次参战宠物
		'''
		petObj = None
		if hasattr(self, "lastFightPetId"):
			petObj = self.petCtn.getItem(self.lastFightPetId)
		else:
			petObj = self.petCtn.getFighter()
		if not petObj:
			petObj = self.petCtn.getFirstCarry()
		return petObj

	def inEscort(self):
		'''运镖状态
		'''
		return getattr(self, "escort", False)

	def setEscort(self, flag=True):
		'''设置运镖状态
		'''
		self.escort = flag
		self.attrChange("addon")

	def inTreasure(self):
		'''探宝状态
		'''
		return getattr(self, "treasure", False)

	def setTreasure(self, flag=True):
		'''设置探宝状态
		'''
		self.treasure = flag
		self.attrChange("addon")
		
	def inStory(self):
		'''是否在剧情中
		'''
		for taskObj in self.taskCtn.getAllValues():
			if taskObj.fetch("storyInfo"):
				return True
		
		teamObj = self.inTeam()
		if teamObj:
			for taskObj in teamObj.taskCtn.getAllValues():
				if taskObj.fetch("storyInfo"):
					return True

		return False
	
	@property
	def fiveElAttack(self):
		'''攻击五行
		'''		
		propsObj = self.equipCtn.getEquipByWearPos(props.defines.EQUIP_WEAPON)
		if propsObj and propsObj.isWearValid():
			return propsObj.fiveEl
		return perform.defines.FIVE_EL_NOT
	
	@property
	def fiveElDefend(self):
		'''防御五行
		'''
		propsObj = self.equipCtn.getEquipByWearPos(props.defines.EQUIP_CLOTHES)
		if propsObj and propsObj.isWearValid():
			return propsObj.fiveEl
		return perform.defines.FIVE_EL_NOT
	
	def getCubeCountMax(self):
		'''获取探宝骰子次数上限
		'''
		import activity
		countMax = self.day.fetch("cubeCountMax", -1)
		if countMax == -1:
			actObj = activity.getActivity("treasure")
			if not actObj:
				return 0
			countMax = actObj.calCubeCountMax(self)
			self.day.set("cubeCountMax", countMax)
		return countMax
	
	def getCubeCount(self, iWhichCyc=0):
		'''获取已使用探宝骰子次数
		'''
		return self.day.fetch("cubeCount", iWhichCyc=iWhichCyc)
	
	def addCubeCount(self, val):
		'''增加已使用探宝骰子次数
		'''
		self.day.add("cubeCount", val)
		
	def getLeftCubeCount(self):
		'''获取剩余探宝骰子次数
		'''
		count = self.getCubeCountMax() - self.getCubeCount()
		return max(0, count)


import factoryConcrete
import timer
import c

# gdVirtuaNoMap = {
# 	c.GOLD 			: 	'addGold',
# 	c.EXP  			:	'addExp',
# 	c.DIAMOND 		:	'addDiamond',
# 	c.VOUCHER 		:	'addVoucher',
# 	#c.ARENA_POINT	: 'addArenaPoint',
# 	#c.FRIEND_POINT	: 'addFriendPoint',
# 	#c.LONGJING 		: 'addLongJing',
# }


from common import *
from role.defines import *
from scene.defines import *
import copy
import json
import weakref
import types
import gevent
import factory

import log
import block.blockLazy
import block.active
import block.blockPackage
import block.blockTask
import block.blockFriend
import block.blockSkill
import block.blockCycle
import block.blockTitle
import block.blockBuff
import block.blockPetCtn
import block.blockLineup
import block.blockEye
import block.blockRideCtn
import block.blockAchv

import role.roleHelper
import scene_pb2
import endPoint
import event
import log
import scene
import multiFieldRole
import timeU
import mainService
import resume
import account
import team
import roleExpData
import guild
import rank
import sql
import db4ms
import myGreenlet
import block.sysActive
import logReport
import props
import props.defines
import primitive
import container
import ctn
import role
import instance
import role.defines
import role.calattr
import message
import skill.upgrade
import block.blockBuddy
import pointAllot
import task.school
import task.main
import task
import activity
import qanda.object
import role.register
import block.parameter
import openLevel
import state
import activity.center
import block.equipSkill
import listener
import block.expState
import block.blockWords
from war.defines import *
import skillPraticeLevelData
import entity
import template
import ride
import rideData
import buddy
import perform.defines
import tougheningExp