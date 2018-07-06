# -*- coding: utf-8 -*-
import pst

INIT_QUALITY = 1 #初始阶级

class Buddy(pst.cEasyPersist):
	
	def __init__(self, iNo):
		pst.cEasyPersist.__init__(self)
		self.iNo = iNo
		self._ownerId = 0
		self.applyMgr = container.ApplyMgr()  # 附加效果
		self.relationList = {}  #羁绊列表
		
		self.shape = 1111 # 造型
		self.shapeParts = [1, 0, 0, 0, 0, 0] # 造型部位
		self.colors = [0, 0, 0, 0, 0, 0] # 染色
		
		self.hp = self.hpMax = 0  # 生命/生命上限
		self.mp = self.mpMax = 99  # 真气/真气上限
		
		self.phyDam = 0  # 物理伤害
		self.magDam = 0  # 法术伤害
		self.phyDef = 0  # 物理防御
		self.magDef = 0  # 法术防御
		self.spe = 0  # 速度
		self.cure = 0 #治疗
		
		self.phyCrit = 3 # 物理暴击
		self.magCrit = 3 # 法术暴击
		self.phyReCrit = 0 # 物理抗暴
		self.magReCrit = 0 # 法术抗暴
		self.sealHit = 0 #封印
		self.reSealHit = 0 #抗封

		self.oTimerMng = timer.cTimerMng()
		self.uTimerId = 0
		
	def onBorn(self):
		pass
		# self.reCalcAttr()
	
	@property
	def id(self):
		return self.iNo

	@property
	def key(self):
		return self.iNo
	
	@property
	def no(self):
		'''编号
		'''
		return self.iNo

	@property
	def ownerId(self):
		return self._ownerId
	
	@ownerId.setter
	def ownerId(self, ownerId):
		self._ownerId = ownerId
		
	@property
	def name(self):
		return self.getConfig("名称")

	@property
	def level(self):
		'''等级
		'''
		who = getRole(self.ownerId)
		if who:
			return who.level
		return 0
	
	@property
	def kind(self):
		'''类型
		'''
		return self.getConfig("类型")
	
	@property
	def gender(self):
		'''性别
		'''
		return self.getConfig("性别")

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

	def setupMajor(self, obj):
		attrData = obj.getMajor(self.kind)
		for attr,value in attrData.iteritems():
			attr = descAttrList[attr]
			self.addApply(attr,value,"major")

	def setupRelation(self, relationNo, quality):
		data = buddyData.getRelation(relationNo)
		attrData = data["效果"][quality-1]
		for attr,value in attrData.iteritems():
			attr = descAttrList[attr]
			self.addApply(attr,value,"relation%d" % relationNo)
		self.relationList[relationNo] = quality

	def checkRelation(self, who):
		'''检查羁绊
		'''
		for relationNo in self.getConfig("羁绊"):
			quality = self.relationList.get(relationNo,0)
			if quality < self.getQuality() - 1:
				continue
			lst =  buddyData.getRelation(relationNo)["伙伴"]
			minQuality = who.buddyCtn.getMinQuality(lst)
			if minQuality == quality:
				continue
			for buddyNo in lst:
				buddyObj = who.buddyCtn.getItem(buddyNo)
				buddyObj.removeApplyByFlag("relation%d" % relationNo)
				buddyObj.setupRelation(relationNo, minQuality)
				if buddyNo != self.id:
					buddyObj.reCalcAttr()

	def attrChange(self,*tArgs):
		'''属性改变
		'''
		msg = {}
		msg["iBuddyNo"] = self.id
		for attr in tArgs:
			if attr == "skillList":
				msg[attr] = self.fetch("skillList",[])
			else:
				msg[attr] = getValByName(self,attr)

		who = getRole(self.ownerId)
		if who:
			who.endPoint.rpcModBuddy(**msg)

	def getMsg(self):
		msg = buddy_pb2.buddyMsg()
		msg.iBuddyNo = self.iNo
		msg.quality = self.getQuality()
		msg.isRent = self.isRent()
		msg.fight = self.getFight()
		msg.iFriendId = self.fetch("friendId")
		msg.skillList.extend(self.fetch("skillList", []))
		for attr in gBuddyAttrFreshList:
			value = self.getAttr(attr)
			setattr(msg,attr,value)
		if self.fetch("endTime"):
			msg.iTime = self.fetch("endTime") - getSecond()
			msg.sFriendName = self.fetch("friendName","")
			msg.iMoney = self.fetch("money")
		return msg

	def maxQuality(self):
		return len(buddyData.gdQuality)

	def getUpgradeNeed(self):
		'''升阶数量
		'''
		return self.getConfig("升阶数量")[self.getQuality()]

	def getMaterial(self):
		'''材料
		'''
		return self.getConfig("碎片")

	def getScore(self):
		'''评分
		'''
		return buddyData.getQuality(self.getQuality(),"评分")

	def getFight(self):
		'''战力
		'''
		return grade.gradeBuddy(self)

	def getHpGen(self):
		return self.getGen("生命资质")

	def getPhyAttGen(self):
		return self.getGen("物理伤害资质")

	def getMagAttGen(self):
		return self.getGen("法术伤害资质")

	def getPhyDefGen(self):
		return self.getGen("物理防御资质")

	def getMagDefGen(self):
		return self.getGen("法术防御资质")

	def getSpeGen(self):
		return self.getGen("速度资质")
	
	def getCureGen(self):
		return self.getGen("治疗资质")

	def getGen(self, key):
		'''获得资质
		'''
		return self.getConfig(key)[self.getQuality()-1]

	def getQuality(self):
		'''阶级
		'''
		return self.fetch("quality",INIT_QUALITY)

	def addQuality(self, value):
		'''升阶
		'''
		if self.getQuality() == INIT_QUALITY:
			value = INIT_QUALITY + value
		self.add("quality",value)

	def isRent(self):
		'''是否好友助战
		'''
		who = getRole(self.ownerId)
		if not who:
			return 0
		return who.buddyCtn.isRent(self.id)

	def getInitSkillCount(self):
		'''主动技能的数量
		'''
		return len(self.getConfig("主动技能"))

	def setSkill(self, skillId, level=1):
		'''设置技能
		'''
		skillList = self.fetch("skillList", [])
		if level > 0: # 增加
			if skillId not in skillList: 
				skillList.append(skillId)
		else: # 删除
			if skillId in skillList:
				skillList.remove(skillId)

		self.set("skillList", skillList)
		self.generateSkillList()
		self.generateValidSkillList()
	
	def getValidSkillList(self):
		'''有效的技能
		'''
		if not hasattr(self,"validSkillList"):
			self.generateValidSkillList()
		return self.validSkillList

	def getSkillList(self):
		'''技能列表
		'''
		if not hasattr(self, "skillList"):
			self.generateSkillList()
		return self.skillList

	def getSkillListByOrder(self):
		'''有顺序的技能列表
		'''
		if not hasattr(self, "skillList"):
			self.generateSkillList()
		
		skillList = []
		for skillId in  self.fetch("skillList", []):
			skillObj = self.skillList[skillId]
			skillList.append((skillId, skillObj))
			
		return skillList

	def generateValidSkillList(self):
		'''生成有效技能列表，临时的
		'''
		self.validSkillList = {}
		qualit = self.getQuality()
		initSkillCount = self.getInitSkillCount()
		skillList = self.getSkillList()
		for skillId in self.fetch("skillList",[])[:initSkillCount+qualit-1]:
			self.validSkillList[skillId] = skillList[skillId]

	def generateSkillList(self):
		'''生成技能列表，临时的
		'''
		self.skillList = {}
		for skillId in self.fetch("skillList", []):
			skillObj = skill.new(skillId)
			if not skillObj:
				continue
			skillObj.level = self.level
			self.skillList[skillId] = skillObj
	
	def getPerformList(self):

		'''法术列表
		'''
		performList = []
		skillList = self.getValidSkillList()
		for skillId, skillObj in skillList.iteritems():
			if skill.getHigh(skillId) in skillList:  # 如此存在对应的高级技能，忽略该低级技能
				continue
			performList.extend(skillObj.getPerformList(self))
			
		return performList
	
	def getMasterPerformList(self):
		'''精通的法术
		'''
		performList = []
		skillId = self.getConfig("专有技能")
		if skillId:
			skillObj = skill.new(skillId)
			if skillObj:
				skillObj.level = self.level
				performList.extend(skillObj.getPerformList(self))
		return performList
	
	def reCalcAttr(self, bRefresh=True):
		'''计算属性
		'''
		attrData = buddy.calattr.calcAttr(self)
		refreshList = ["fight"]
		for attr,val in attrData.iteritems():
			if getattr(self, attr, 0) != val and attr in gBuddyAttrFreshList:
				refreshList.append(attr)
			setattr(self, attr, val)

		self.hp = self.hpMax
		self.mp = self.mpMax

		if bRefresh:
			self.attrChange(*refreshList)
		
	def getColors(self):
		'''染色
		'''
		return self.colors

	def getConfig(self, key):
		return buddyData.getBuddyInfo(self.iNo, key)
	
	@property
	def fiveElAttack(self):
		'''攻击五行
		'''
		return self.getConfig("五行")
	
	@property
	def fiveElDefend(self):
		'''防御五行
		'''
		return self.getConfig("五行")

	def startTimer(self):
		if self.uTimerId:  #如果原来有，先取消
			self.oTimerMng.cancel(self.uTimerId)
			self.uTimerId = 0
		now = getSecond()
		endTime = self.fetch("endTime")
		if not endTime:
			self.set("endTime",now + 2*60*60)

		if endTime - now <= 0:
			self.__timeOut()
		else:
			self.uTimerId = self.oTimerMng.run(self.__timeOut,endTime-now)

	def __timeOut(self):
		self.isTimeOut = 1
		self.uTimerId = 0
		who = getRole(self.ownerId)
		if not who:
			return
		iFriendId = self.fetch("friendId")
		who.buddyCtn.autoChangeBuddy(iFriendId)
		who.buddyCtn.removeFriendBuddy(iFriendId)

	def updateAttr(self,attrData):
		for attr,value in attrData.iteritems():
			if attr in gBuddyAttrFreshList:
				self.set(attr,value)
				setattr(self,attr,value)

		self.hp = self.hpMax
		self.mp = self.mpMax

	def initAttr(self):
		for attr in gBuddyAttrFreshList:
			value = self.fetch(attr)
			setattr(self,attr,value)

		self.hp = self.hpMax
		self.mp = self.mpMax

	def getAttr(self, name):
		if name in gBuddyAttrFreshList:
			if self.hasKey(name):
				return self.fetch(name)

		return getattr(self,name,0)

from common import *
from buddy.defines import *
from role.defines import *
import buddyData
import buddy.calattr
import skill
import buddy_pb2
import container
import grade
import timer