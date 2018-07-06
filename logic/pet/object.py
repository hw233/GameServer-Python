# -*- coding: utf-8 -*-
import pst

# if "gPetLastID" not in globals():
# 	gPetLastID = 0
	
# def _newPetID():
# 	global gPetLastID
# 	gPetLastID += 1
# 	return gPetLastID

class Pet(pst.cEasyPersist):
	def __init__(self):
		pst.cEasyPersist.__init__(self)
		self.id = 0
		self.ownerId = 0
		self.applyMgr = container.ApplyMgr()  # 附加效果
		self.month = cycleData.cCycMonth(1, self.markDirty)
		self.day = cycleData.cCycDay(1, self.markDirty)
		
		self.con = 0  # 体质
		self.mag = 0  # 魔力
		self.str = 0  # 力量
		self.res = 0  # 耐力
		self.spi = 0  # 精神
		self.dex = 0  # 敏捷
		
		self.hp = self.hpMax = 0  # 生命/生命上限
		self.mp = self.mpMax = 0  # 真气/真气上限
		
		self.phyDam = 0  # 物理伤害
		self.magDam = 0  # 法术伤害
		self.phyDef = 0  # 物理防御
		self.magDef = 0  # 法术防御
		self.spe = 0  # 速度
		
		self.phyCrit = 0 # 物理暴击
		self.magCrit = 0 # 法术暴击
		self.phyReCrit = 0 # 物理抗暴
		self.magReCrit = 0 # 法术抗暴
		
		self.exp = 0 # 经验

	def onBorn(self, data, level, star, **args):  # override
		self.id = block.sysActive.gActive.genPetId()
		self.set("name", data["名称"])
		self.set("level", level)
		self.set("star", star)
		self.set("birthday", timeU.getDayNo())
		
		if self.isHolyPet():  # 神兽
			_newPetDataFoHoly(self, data, **args)
		else:
			_newPetData(self, data, **args)
		# 技能处理
		if args.get("skill"):  # 指定技能
			for skId in args["skill"]:
				self.setSkill(skId, 1, False)
		else:  # 天生技能
			for skId in data["必带技能"]:
				self.setSkill(skId, 1, False)
			for skId in data["特性技能"]:
				self.setSkill(skId, 1, False)
		self.reCalcAttr(False)
		self.hp = self.hpMax
		self.mp = self.mpMax

	def getConfig(self, key):
		return petData.getConfig(self.idx, key)

	@property
	def key(self):
		return self.id

	@property
	def name(self):
		name = self.fetch("name")
		if not name:
			name = pet.getPetName(self.idx)
		return name

	@property
	def shape(self):
		'''造型
		'''
		shape = self.fetch("shape")
		if not shape:
			shape = self.getConfig("造型")
		return shape
	
	@property
	def shapeParts(self):
		'''造型部位
		'''
		shapeParts = self.fetch("shapeParts", {})
		return role.defines.transToShapePartListForPet(shapeParts)
	
	def setShapeParts(self, shapePartType, shapePart, refresh=True):
		'''设置造型部位
		'''
		shapeParts = self.fetch("shapeParts", {})
		shapeParts[shapePartType] = shapePart
		self.set("shapeParts", shapeParts)
		if refresh:
			self.attrChange("shapeParts")
		
	def getColors(self):
		'''染色
		'''
		colors = self.fetch("colors", {})
		return role.defines.transToColorListForPet(colors)

	def setColors(self, colorList):
		'''设置染色
		'''
		colors = self.fetch("colors", {})
		for shapePartType, color in colorList.items():
			colors[shapePartType] = color
		self.set("colors", colors)
		self.attrChange("colors")

	@property
	def idx(self):
		'''导表索引
		'''
		return self.fetch("idx", 1001)
	
	def getOwnerObj(self):
		return getRole(self.ownerId)

	@property
	def level(self):
		'''等级
		'''
		return self.fetch("level", 0)
	
	def getMaxLevel(self):
		'''最大等级
		'''
		return openLevel.getOpenLevel() + 10

	def getRealLevel(self):
		'''实际等级
		'''
		exp = self.exp
		level = self.level

		if self.exp > self.expNext:
			for i in xrange(level,petExpData.MAX_PET_LV+1):
				exp -= petExpData.gdData[level]["升级经验"]
				if exp < 0 :
					break
				level += 1

		return level

	def getStar(self):
		'''星级
		'''
		return self.fetch("star", 1)

	def getRace(self):
		'''种类
		'''
		race = self.getConfig("种类")
		if not race:
			race = "无"
		return race

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

	def getScore(self):
		'''评分
		'''
		return grade.gradePet(self)

	def getSpecialSKills(self):
		'''获取特性技能
		'''
		spcSkls = self.getConfig("特性技能")
		return [] if not spcSkls else list(spcSkls)

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
		
	# def getTraceID(self):
	# 	'''追踪ID
	# 	'''
	# 	lst = self.fetch("traceNo")
	# 	if lst:
	# 		return lst[1]
	# 	return 0

	def reCalcAttr(self, bRefresh=True):
		'''计算属性
		'''
		oldHpMax = self.hpMax
		oldMpMax = self.mpMax
		
		refreshList = {}
		attrData = pet.calattr.calcAttr(self)
		for attr, val in attrData.iteritems():
			if bRefresh and getattr(self, attr, 0) != val:
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
		
		if bRefresh and refreshList:
			self.attrChange(*refreshList)

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
		'''加、扣魔法
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
	
	def recover(self, bRefresh):
		who = self.getOwnerObj()
		if not who:
			return
		iAddHp = self.hpMax-self.hp
		iAddHp = min(who.reserveHp,iAddHp)
		if iAddHp:
			who.addReserveHp(-iAddHp,True)
			self.addHP(iAddHp,bRefresh)

		iAddMp = self.mpMax-self.mp
		iAddMp = min(who.reserveMp,iAddMp)
		if iAddMp:
			who.addReserveMp(-iAddMp,True)
			self.addMP(iAddMp,bRefresh)

	def setSkill(self, skillId, level=1, refresh=True):
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
		
		if refresh:
			self.generateSkillList()
			who = self.getOwnerObj()
			if who:
				if level > 0:
					who.endPoint.rpcPetSkillAdd(self.id, skillId)
				else:
					who.endPoint.rpcPetSkillDel(self.id, skillId)

	def querySkillLevel(self, skillId):
		'''查询技能等级
		'''
		if skillId in self.getSkillList():
			return 1
		return 0

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
	
	def generateSkillList(self):
		'''生成技能列表，临时的
		'''
		self.skillList = {}
		for skillId in self.fetch("skillList", []):
			skillObj = skill.new(skillId)
			if not skillObj:
				continue
			skillObj.level = 1
			self.skillList[skillId] = skillObj
	
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
	
	def getPerformListByOrder(self):
		'''有序法术列表
		'''
		performList = []
		skillList = self.getSkillListByOrder()
		for skillId, skillObj in skillList:
			if skill.getHigh(skillId) in skillList:  # 如此存在对应的高级技能，忽略该低级技能
				continue
			performList.extend(skillObj.getPerformList(self))
		
		return performList

	def getCarryLevel(self, star=1):
		'''携带等级
		'''
		levelList = self.getConfig("携带等级")
		return levelList[star - 1]

	def getUpgradeCost(self, star=1):
		'''升星消耗
		'''
		costList = list(self.getConfig("升星消耗"))
		return costList[star-1]

	def save(self):  # override
		dData = pst.cEasyPersist.save(self)
		dData["id"] = self.id
		dData["exp"] = self.exp
		dData["hp"] = self.hp
		dData["mp"] = self.mp
		dData["month"] = self.month.save()
		dData["day"] = self.day.save()
		return dData

	def load(self, dData):  # override
		pst.cEasyPersist.load(self, dData)
		self.id = dData.pop("id", 0)
		self.exp = dData.pop("exp", 0)
		self.hp = dData.pop("hp", 0)
		self.mp = dData.pop("mp", 0)
		self.month.load(dData.pop("month", {}))
		self.day.load(dData.pop("day", {}))

	def upLevel(self):  # 升级
		iExpNext = self.expNext
		self.exp -= iExpNext
		self.add("level", 1)
		writeLog("pet/uplevel", "[%d]%d %d %d" % (self.ownerId, self.id, self.level, iExpNext))
		
		# 潜力点
		self.addPoint(5, "升级")
		for attr in role.defines.baseAttrList:
			self.add(attr, 1)
		self.reCalcAttr()
		self.hp = self.hpMax
		self.mp = self.mpMax
		self.attrChange("exp", "expNext", "level","hp","mp")
		pet.business.autoAddPoint(self)
		listener.doListen("宠物升级", self.ownerId, petId=self.id, level=self.level)

	@property
	def expNext(self):  # 升级所需要的经验
		return petExpData.getConfig(self.level, "升级经验")
	
	def rewardExp(self, iVal, sReason, sTips=""):
		'''奖励经验
		'''
		if not iVal or not self.checkRewardExp(sReason):
			return
		self.addExp(iVal, sReason, sTips)
		
	def checkRewardExp(self, sReason, showTips=True):
		who = self.getOwnerObj()
		
		if self.getRealLevel() >= self.getMaxLevel():
			if showTips:
				message.tips(who, "已达当前服务器异兽最大等级，不需要再使用")
			return 0
		if (self.level - who.level >= 5) and sReason not in ("宠物培养",):
			if showTips:
				message.tips(who, "异兽超过人物#C045级#n，无法继续获得经验")
			return 0
		
		return 1

	def addExp(self, iVal, sReason, sTips=""):
		if not isinstance(iVal, int):
			raise Exception, "非法的经验值:%s" % iVal
		if self.exp + iVal < 0:
			raise Exception, '不能把经验扣成负数,否则{}+({})={}.'.format(self.exp, iVal, self.exp + iVal)
		
		oldExp = self.exp
		self.exp += iVal
		self.markDirty()
		self.attrChange("exp")
		writeLog("pet/exp", "[%d]%d %d%+d->%d %s" % (self.ownerId, self.id, oldExp, iVal, self.exp, sReason))
		
		if hasattr(self, "addExpResult"):
			self.addExpResult += iVal
		
		if sTips != None:
			if iVal > 0:
				sTips = sTips if sTips else "你的#C02$pet#n获得#C02$exp#n经验"
			elif iVal < 0:
				sTips = sTips if sTips else "你的$pet扣除$exp经验"
			else:
				return
			sTips = sTips.replace("$pet", self.name)
			sTips = sTips.replace("$exp", "%d" % abs(iVal))
			message.tips(self.ownerId, sTips)
			message.message(self.ownerId, sTips)

		who = self.getOwnerObj()
		while self.exp >= self.expNext and self.expNext:
			if self.level - who.level >= 10:
				return
			self.upLevel()
		
# 	def isBinded(self):
# 		'''是否绑定
# 		'''
# 		if self.fetch("bind"):
# 			return 1
# 		return 0

	def attrChange(self, *attrNameList):
		'''刷新属性
		'''
		msg = {"petId": self.id}
		for attrName in attrNameList:
			if attrName in ("grow","growExt"):
				msg[attrName] = "%.2f" % self.getValByName(attrName)
			else:
				msg[attrName] = self.getValByName(attrName)

		who = self.getOwnerObj()
		if who:
			who.endPoint.rpcPetAttrChange(**msg)
			
	def getValByName(self, attrName):
		'''根据属性名获取属性值
		'''
		return getValByName(self, attrName)

	def refreshState(self):
		'''刷新状态
		'''
		self.attrChange("hp", "hpMax", "mp", "mpMax")
		
	def addPoint(self, iVal, sReason, bRefresh=True):
		'''增加潜力点
		'''
		oldVal = self.fetch("point")
		self.add("point", iVal)
		writeLog("pet/point", "[%d]%d %d%+d->%d %s" % (self.ownerId, self.id, oldVal, iVal, self.fetch("point"), sReason))
		if bRefresh:
			self.attrChange("point")

	def addAttrPoint(self, sAttr, iVal, sReason, bRefresh=False):
		'''增加属性点
		'''
		sAttrPoint = "%sAllot" % sAttr
		iOldVal = self.fetch(sAttrPoint)
		self.add(sAttrPoint, iVal)
		writeLog("pet/attrpoint", "[%d]%d %s %d%+d->%d %s" % (self.ownerId, self.id, sAttrPoint, iOldVal, iVal, self.fetch(sAttrPoint), sReason))
		if bRefresh:
			self.attrChange(sAttr)

	def refreshAllotAttr(self, lAttr):
		lAllotAttr = []
		for sAttr in lAttr:
			# 增加体质或法力，对应的血气、真气补满
			if sAttr == "con":
				self.hp = self.hpMax
				lAllotAttr.append("hp")
			elif sAttr == "mag":
				self.mp = self.mpMax
				lAllotAttr.append("mp")
			lAllotAttr.append("%sAllot" % sAttr)
		self.attrChange(*lAllotAttr)

	def addStar(self, iVal, sReason, bRefresh=True):
		'''增加星数
		'''
		oldVal = self.fetch("star")
		self.add("star", iVal)
		writeLog("pet/star", "[%d]%d %d%+d->%d %s" % (self.ownerId, self.id, oldVal, iVal, self.fetch("star"), sReason))
		if bRefresh:
			self.attrChange("star", "score","hpGen","phyAttGen","magAttGen","phyDefGen","magDefGen","speGen","grow")
			
	def getLife(self):
		'''寿命
		'''
		return self.fetch("life", 0)
	
	def getLifeMax(self):
		return 9999

	def addLife(self, val, sReason, sTips=""):
		'''增加寿命
		'''
		if val == 0:
			return
		if self.isHolyPet():#神兽不增加也不减少寿命
			return
		if not self.checkAddLife(sReason):
			return
		
		if sReason in ("宠物培养",):
			val = (val + self.queryApply("life")) * (100 + self.queryApply("lifeRatio")) / 100

		oldVal = self.fetch("life")
		newVal = oldVal + val
		lifeMax = self.getLifeMax()
		if newVal > lifeMax:
			newVal = lifeMax
		self.set("life", newVal)
		self.attrChange("life")
		writeLog("pet/life", "[%d]%d %d%+d->%d %s" % (self.ownerId, self.id, oldVal, val, newVal, sReason))
		
		if hasattr(self, "addLifeResult"):
			self.addLifeResult += val
		
		if sTips != None:
			if val > 0:
				sTips = sTips if sTips else "你的$pet增加$life寿命"
			else:
				sTips = sTips if sTips else "你的$pet减少$life寿命"
			sTips = sTips.replace("$pet", self.name)
			sTips = sTips.replace("$life", "%d" % abs(val))
			message.tips(self.ownerId, sTips)
			message.message(self.ownerId, sTips)

		if self.getLife() <= 50:
			who = self.getOwnerObj()
			if who:
				who.petCtn.setFighter(self, False)
			
	def checkAddLife(self, sReason, showTips=True):
		if self.getLife() >= self.getLifeMax():
			if showTips:
				message.tips(self.ownerId, "异兽寿命已达最大值，不能再增加寿命")
			return 0
		return 1

	def getSklPoint(self):
		'''技能潜力点
		'''
		return self.fetch("sklPoint", 0)

	def addSklPoint(self, iVal, sReason, bRefresh=True):
		'''增加技能潜力点
		'''
		oldVal = self.fetch("sklPoint")
		self.add("sklPoint", iVal)
		writeLog("pet/skillPoint", "[%d]%d %d%+d->%d %s" % (self.ownerId, self.id, oldVal, iVal, self.fetch("sklPoint"), sReason))
		if bRefresh:
			self.attrChange("sklPoint")

	def getSklSlotExpAll(self):
		'''升级完技能格所需的总剩余经验
		'''
		return pet.business.fillSkillSlotExp(self)

	def getSklSlotExpNxt(self):
		'''升级所需技能格经验
		'''
		sklCnt = len(self.getSkillList())+1
		return petSkillSlotsExp.getExp(sklCnt)

	def getSklSlotExp(self):
		'''技能格经验
		'''
		return self.fetch("sklSlotExp", 0)

	def addSklSlotExp(self, iVal, sReason, bRefresh=True):
		'''增加技能格经验
		'''
		oldVal = self.fetch("sklSlotExp")
		self.add("sklSlotExp", iVal)
		writeLog("pet/skillSlotExp", "[%d]%d %d%+d->%d %s" % (self.ownerId, self.id, oldVal, iVal, self.fetch("sklSlotExp"), sReason))
		if bRefresh:
			self.attrChange("sklSlotExp")

	def getStarAttr(self, star, key):
		'''宠物星级的属性
		'''
		star -= 1 # 导表数据下标从0开始，0即为1星
		return self.getConfig(key)[star]

	def getHpGen(self):
		'''生命资质
		'''
		hpGen = self.getStarAttr(self.getStar(), "生命资质")
		hpGenExt = self.fetch("hpGenExt")
		return hpGen + hpGenExt

	def getPhyAttGen(self):
		'''物攻资质
		'''
		phyAttGen = self.getStarAttr(self.getStar(), "物攻资质")
		phyAttGenExt = self.fetch("phyAttGenExt")
		return phyAttGen + phyAttGenExt

	def getMagAttGen(self):
		'''法攻资质
		'''
		magAttGen = self.getStarAttr(self.getStar(), "法攻资质")
		magAttGenExt = self.fetch("magAttGenExt")
		return magAttGen + magAttGenExt

	def getPhyDefGen(self):
		'''物防资质
		'''
		phyDefGen = self.getStarAttr(self.getStar(), "物防资质")
		phyDefGenExt = self.fetch("phyDefGenExt")
		return phyDefGen + phyDefGenExt

	def getMagDefGen(self):
		'''法防资质
		'''
		magDefGen = self.getStarAttr(self.getStar(), "法防资质")
		magDefGenExt = self.fetch("magDefGenExt")
		return magDefGen + magDefGenExt

	def getSpeGen(self):
		'''速度资质
		'''
		speGen = self.getStarAttr(self.getStar(), "速度资质")
		speGenExt = self.fetch("speGenExt")
		return speGen + speGenExt

	def getGrow(self):
		'''成长
		'''
		grow = self.getStarAttr(self.getStar(), "成长")
		growExt = self.fetch("growExt")
		return grow + growExt

	def __setattr__(self, name, value):
		object.__setattr__(self, name, value)
		if name in ("hp", "mp",):
			self.markDirty()

	def getDefaultPerform(self):
		'''获取默认法术
		'''
		performId = self.fetch("defaultPerform")
		if performId >= 100:
			if performId in self.getPerformList():
				return performId
		elif performId in (CMD_TYPE_PHY, CMD_TYPE_DEFEND):
			return performId
		else:
			for performId in self.getPerformListByOrder():
				if not perform.isPassive(performId):
					return performId

		return CMD_TYPE_PHY

	def setDefaultPerform(self, performId):
		'''设置默认法术
		'''
		if performId >= 100:
			if performId not in self.getPerformList():
				return
		elif performId not in (CMD_TYPE_PHY, CMD_TYPE_DEFEND):
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
		else:
			for performId in self.getPerformListByOrder():
				if not perform.isPassive(performId):
					return performId

		return CMD_TYPE_PHY

	def setOfflinePerform(self, performId):
		'''设置离线挂机法术
		'''
		if performId >= 100:
			if performId not in self.getPerformList():
				return
		elif performId not in (CMD_TYPE_PHY, CMD_TYPE_DEFEND):
			return
		self.set("offlinePerform",performId)
		
	def isFighter(self):
		'''是否参战中
		'''
		who = self.getOwnerObj()
		if who:
			return who.petCtn.isFighter(self.id)
		return 0
	
	def isCarry(self):
		'''是否携带中
		'''
		who = self.getOwnerObj()
		if who:
			return who.petCtn.isCarry(self.id)
		return 0

	def isHolyPet(self):
		if PET_HOLY == self.getConfig("异兽类型"):
			return True
		return False

#===============================================================================
# 新建宠数据
#===============================================================================
def _newPetData(petObj, data, **args):
	'''新建普通宠数据
	'''
	# 属性点
	level = petObj.level
	star = petObj.getStar()
	point = 5 * level
	base = 20 + level
	petObj.set("point", point)
	for attr in role.defines.baseAttrList:
		petObj.set(attr, base)
	for idx, genExt in enumerate(genExtAttrList):
		genMax = petObj.getConfig(genExtMaxNameList[idx])
		genMin = petObj.getConfig(genExtMinNameList[idx])
		genInit = (genMax - genMin) / 2 + genMin
		petObj.set(genExt, genInit)
	petObj.set("life", data["寿命"])
	petObj.set("sklPoint", data["技能潜力点"])

def _newPetDataFoHoly(petObj, data, **args):
	'''新建神兽数据
	'''
	# 属性点
	level = petObj.level
	star = petObj.getStar()
	point = 5 * level
	base = 20 + level
	petObj.set("point", point)
	for attr in role.defines.baseAttrList:
		petObj.set(attr, base)
	for idx, genExt in enumerate(genExtAttrList):
		genMax = petObj.getConfig(genExtMaxNameList[idx])
		genMin = petObj.getConfig(genExtMinNameList[idx])
		genInit = (genMax - genMin) / 6 * 5 + 10 + genMin
		print genExt, genMax, genMin, genInit
		petObj.set(genExt, genInit)
	petObj.set("life", data["寿命"])
	petObj.set("sklPoint", data["技能潜力点"])


from common import *
from pet.defines import *
import role.defines
import skill
import container
import petData
import timeU
import block.sysActive
import pet
import pet.calattr
import u
import message
import cycleData
import pet_pb2
import petSkillSlotsExp
import pet.business
import petExpData
import grade
import block.parameter
import openLevel
from war.defines import *
import listener
import perform