#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#工厂子类与工厂实例
import factory


class cFactoryCheckRoleId(factory.cFactory):
	def getProductFromDB(self,itNoRowInsertValues,iRoleId,**dData):
		if not (0<iRoleId<=c.MAX_ROLE_ID):
			raise Exception,'角色id不符合0<{}<=MAX_ROLE_ID'.format(iRoleId)
		return factory.cFactory.getProductFromDB(self,itNoRowInsertValues,iRoleId,**dData)

#角色工厂
class cRoleFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return role.object.cRole(iRoleId).setFactory(self)
	#override目的:当role从keeper踢除时,需要对role的技能,包裹,任务....统一存一下盘
	#不然role被踢了,就没有机会存盘了,导致数据丢失.(虽然有安排到调度队列等待存盘,但是对象都没了也存不了啊)
	def isWait2schedule(self,iRoleId):#override 角色是否在存盘队列等待调度
		oRole=self.getProductFromMemory(iRoleId)
		for ftr in oRole.dFtr.itervalues():
			if ftr.isWait2schedule(iRoleId):#某一个调度到存盘队列,则认为是整一个角色调度到存盘队列
				return True
		return cFactoryCheckRoleId.isWait2schedule(self,iRoleId)#其实角色对象从来都不会被调度存盘,被调度的是其成员(包裹,任务,技能...)

#玩家活跃数据工厂
class cActiveFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.active.cActive(iRoleId).setFactory(self)

#基础数据工厂
class cLazyFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.blockLazy.cRoleLazyBlock(iRoleId).setFactory(self)

#装备容器工厂
class cEquipContainerFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.containerEquip.cEquipContainer(iRoleId).setFactory(self)

#包裹容器工厂
class cPropsContainerFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.blockPackage.cPropsContainer(iRoleId).setFactory(self)

#任务容器工厂
class cTaskContainerFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.blockTask.cTaskContainer(iRoleId).setFactory(self)

#玩家周期数据工厂
class cCycDataFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.blockCycle.cCycDataBlock(iRoleId).setFactory(self)

#多字段1工厂
class cMultiField1Factory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return multiFieldRole.cMultiField1(iRoleId).setFactory(self)

#邮箱容器工厂
class cMailBoxFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		import mail.object
		return mail.object.MailBox(iRoleId).setFactory(self)

#元宝管理器工厂
class cGoldCoinFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return goldCoin.cGoldCoin(iRoleId).setFactory(self)

#好友容器工厂
class cFriendFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.blockFriend.cFriendContainer(iRoleId).setFactory(self)

#技能容器工厂
class cSkillFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.blockSkill.cSkillContainer(iRoleId).setFactory(self)
	
#阵法容器工厂
class cLineupFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.blockLineup.cLineupContainer(iRoleId).setFactory(self)

#角色简要工厂
class cResumeFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return resume.cResume(iRoleId).setFactory(self)
		
#账号工厂
class cAccountFactory(factory.cFactory):
	def _createProduct(self,sUserSource,sAccount):#override
		return account.cAccount(sUserSource,sAccount).setFactory(self)
		
#称号容器工厂
class cTitleFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.blockTitle.cTitleContainer(iRoleId).setFactory(self)
#宠物容器工厂
class cPetCtnFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.blockPetCtn.cPetContainer(iRoleId).setFactory(self)

#助战伙伴容器工厂
class cBuddyCtnFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.blockBuddy.BuddyContainer(iRoleId).setFactory(self)

#公会容器工厂
class cGuildFactory(factory.cFactory):
	def _createProduct(self,iGuildId):#override
		return guild.object.Guild(iGuildId).setFactory(self)

class cBuffFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.blockBuff.cBuffContainer(iRoleId).setFactory(self)

#活动容器工厂
class cActivityFactory(factory.cFactory):
	def _createProduct(self,activityId):#override
		return activity.create(activityId).setFactory(self)

#仓库容器工厂
class cStorageFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.storage.cStorage(iRoleId).setFactory(self)

#临时包裹工厂
class numenBagFtr(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.numenBag.cNumenBag(iRoleId).setFactory(self)

#状态容器工厂
class cStateFactory(cFactoryCheckRoleId):
	def _createProduct(self, iRoleId):#override
		return block.blockState.cStateContainer(iRoleId).setFactory(self)

#对白容器工厂
class cWordsFactory(cFactoryCheckRoleId):
	def _createProduct(self, iRoleId):#override
		return block.blockWords.cWords(iRoleId).setFactory(self)
	
#离线玩家容器工厂
class OfflineFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		import offlineHandler.object
		return offlineHandler.object.Offline(iRoleId).setFactory(self)

#阵眼容器工厂
class cEyeFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.blockEye.cEyeContainer(iRoleId).setFactory(self)
	
#成就容器工厂
class cAchvFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.blockAchv.AchvContainer(iRoleId).setFactory(self)

#坐骑容器工厂
class cRideCtnFactory(cFactoryCheckRoleId):
	def _createProduct(self,iRoleId):#override
		return block.blockRideCtn.cRideContainer(iRoleId).setFactory(self)

roleFtr=cRoleFactory('role')#角色工厂不设定时存盘,由各个子数据块进行定时存盘.
lazyFtr=cLazyFactory('lazy')
activeFtr=cActiveFactory('active')
multiField1Ftr=cMultiField1Factory('multiField1')
taskCtnFtr=cTaskContainerFactory('task')
propsCtnFtr=cPropsContainerFactory('props')
equipCtnFtr=cEquipContainerFactory('equip')
cycFtr=cCycDataFactory('cyc')
mailBoxFtr=cMailBoxFactory('mail')
goldCoinFtr=cGoldCoinFactory('goldCoin')

friendCtnFtr=cFriendFactory('frd')
buffCtnFtr=cBuffFactory('buff')
petCtnFtr=cPetCtnFactory('petCtn')
buddyCtnFtr=cBuddyCtnFactory('buddyCtn')
accountFtr=cAccountFactory('account')
skillFtr=cSkillFactory('skill')
lineupFtr=cLineupFactory('lineup')
resumeFtr=cResumeFactory('resume')
titleCtnFtr=cTitleFactory('title')
guildFtr=cGuildFactory('guild')
activityFtr=cActivityFactory('activity')
storageFtr=cStorageFactory('storage')
numenBagFtr=numenBagFtr('numenBag')
stateFtr = cStateFactory('stateCtn')
wordsFtr = cWordsFactory('words')
offlineFtr = OfflineFactory('offline')
eyeFtr = cEyeFactory('eye')
achvFtr = cAchvFactory('achv')
rideCtnFtr=cRideCtnFactory('rideCtn')



import c
import u
import role.object
import block.blockPackage
import block.containerEquip
import block.blockTask
import block.blockSkill
import block.blockLineup
import block.blockFriend
import multiFieldRole
import block.blockLazy
import block.active
import block.blockCycle
import block.blockTitle
import block.blockPetCtn
import block.blockBuff
import block.blockBuddy
import block.storage
import block.numenBag
import block.blockState
import block.blockWords
import block.blockEye
import block.blockRideCtn

import friend
import resume
import account
import log
import guild.object
import goldCoin
import activity