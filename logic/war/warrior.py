# -*- coding: utf-8 -*-
from war.defines import *

class Warrior(object):
	'''战士基类
	'''
	type = 0
	
	def __init__(self):
		self.id = 0
		self.ownerId = 0
		
		# 需要设置的属性
		self.name = "未知战士"
		self.level = 1
		self.school = 0 # 门派
		self.shape = 1111
		self.shapeParts = [0, 1, 0, 0, 0, 0] # 造型部位
		self.colors = [0, 0, 0, 0, 0, 0] # 染色
		
		self.hp = self.hpMax = 1  # 生命/生命上限
		self.mp = self.mpMax = 1  # 真气/真气上限
		
		self.sp = self.spMax = 0 # 愤怒/愤怒上限
		self.fuwen = 0 # 符能
		self.fuwenMax = 100 # 符能上限
		
		self.con = 10 # 体质
		self.mag = 10 # 魔力
		self.str = 10 # 力量
		self.res = 10 # 耐力
		self.dex = 10 # 敏捷
		
		self.phyDam = 1 # 物理伤害
		self.magDam = 1 # 法术伤害
		self.phyDef = 1 # 物理防御
		self.magDef = 1 # 法术防御
		self.spe = 1 # 速度
		self.cure = 0 # 治疗强度
		
		self.phyCrit = 0 # 物理暴击
		self.magCrit = 0 # 法术暴击
		self.phyReCrit = 0 # 物理抗暴
		self.magReCrit = 0 # 法术抗暴
		
		self.phyRest = 0  # 物理抗性
		self.magRest = 0  # 法术抗性
		
		self.sealHit = 0 # 封印命中
		self.reSealHit = 0 # 抵抗封印
		
		self.gender = 0 # 性别
		
		# 附加效果
		self.applyMgr = container.ApplyMgr()
		self.boutApplyMgr = container.ApplyMgr()  # 回合效果
		
		# 附加处理函数
		self.funcList = {}

		self.status = WARRIOR_STATUS_NORMAL
		self.bout = 0  # 第几回合
		self.command = None  # 指令
		self.isAct = False  # 是否已出招
		self.targetIdx = 0  # 攻击目标
		self.targetPerformId =  0 # 使用的法术
		self.targetPropsId = 0 # 使用的物品
		self.protecterList = []  # 保护者
		
		self.skillList = {}
		self.performList = {} # 主动法术
		self.performListPassive = {} # 被动法术
		self.buffList = {
			1: [None, None, None, None, None],
			2: [None, None, None, None, None],
			3: [None, None, None, None, None],
			4: [None, None, None, None, None],
		}
		self.expSkillList = [0, 0, 0, 0, ]
		
		self.defaultPerform = CMD_TYPE_PHY # 默认法术
		self.attackedIdx = 0  # 被攻击序号

		self.fiveElAttack = FIVE_EL_NONE # 攻击五行
		self.fiveElDefend = FIVE_EL_NONE # 防御五行
		
	def getPID(self):
		if self.isPet():
			return self.ownerId
		if self.isRole() or self.isWatcher():
			return self.id
		return 0
	
	def setup(self, obj, warObj, side):
		'''配置，初始化后调用
		'''
		self.war = weakref.proxy(warObj)
		self.side = side
		
		if hasattr(obj, "id"):
			self.id = obj.id
		if hasattr(obj, "ownerId"):
			self.ownerId = obj.ownerId
		self.name = obj.name
		self.level = obj.level
		if hasattr(obj, "school"):
			self.school = obj.school
		self.shape = obj.shape # 造型
		self.shapeParts = obj.shapeParts # 造型部位
		if hasattr(obj, "getColors"): # 染色
			self.colors = obj.getColors()

		self.hp = obj.hp # 生命
		self.hpMax = obj.hpMax # 生命上限
		self.mp = obj.mp # 真气
		self.mpMax = obj.mpMax # 真气上限
		
		if hasattr(obj, "sp"):
			self.sp = obj.sp # 愤怒
			self.spMax = obj.spMax # 愤怒上限
		
		if hasattr(obj, "con"):
			self.con = obj.con
			self.mag = obj.mag
			self.str = obj.str
			self.res = obj.res
			self.dex = obj.dex
		
		self.phyDam = obj.phyDam # 物理伤害
		self.magDam = obj.magDam # 法术伤害
		self.phyDef = obj.phyDef # 物理防御
		self.magDef = obj.magDef # 法术防御
		self.spe = obj.spe # 速度
		if hasattr(obj, "cure"):
			self.cure = obj.cure # 治疗强度
		
		self.phyCrit = obj.phyCrit #物理暴击
		self.magCrit = obj.magCrit #法术暴击
		self.phyReCrit = obj.phyReCrit #物理抗暴
		self.magReCrit = obj.magReCrit #法术抗暴
		
		if hasattr(obj, "sealHit"): # 封印命中
			self.sealHit = obj.sealHit * 0.01
		if hasattr(obj, "reSealHit"): # 抵抗封印
			self.reSealHit = obj.reSealHit * 0.01
			
		if hasattr(obj, "gender"): # 性别
			self.gender = obj.gender
			
		if hasattr(obj, "fiveElAttack"):
			self.fiveElAttack = obj.fiveElAttack
		if hasattr(obj, "fiveElDefend"):
			self.fiveElDefend = obj.fiveElDefend
		
		# 技能
		import skill
		self.skillList = {}
		for skillId, skillObj in obj.getSkillList().iteritems():
			if skill.isPetPraticeSkill(skillId): # 宠物修炼技能
				continue
			self.skillList[skillId] = skillObj
		
		# 法术
		for performId in obj.getPerformList():
			performObj = perform.new(performId)
			if not performObj:
				continue
			if performObj.isPassive():
				self.performListPassive[performId] = performObj
			else:
				self.performList[performId] = performObj
			performObj.setup(self)
			
		if hasattr(warObj, "needOfflinePerform"):
			if hasattr(obj, "getOfflinePerform"):
				self.defaultPerform = obj.getOfflinePerform()
		elif hasattr(obj, "getDefaultPerform"):
			self.defaultPerform = obj.getDefaultPerform()
			
		# AI集
		if hasattr(obj, "aiSetList"):
			self.aiSetList = obj.aiSetList
		
		# 精通法术
		if hasattr(obj, "masterPerformList"):
			self.masterPerformList = obj.masterPerformList
		elif hasattr(obj, "getMasterPerformList"):
			self.masterPerformList = obj.getMasterPerformList()
			
	def hasApply(self, name):
		val = self.applyMgr.has(name)
		if val:
			return val
		val = self.boutApplyMgr.has(name)
		if val:
			return val
		return 0
	
	def queryApplyAll(self, name):
		return self.applyMgr.query(name) + self.boutApplyMgr.query(name)
	
	def queryApplyListAll(self, name):
		return self.applyMgr.queryList(name) + self.boutApplyMgr.queryList(name)
	
	def addApply(self, name, val, flag="flag"):
		self.applyMgr.add(name, val, flag)
		
	def setApply(self, name, val, flag="flag"):
		self.applyMgr.set(name, val, flag)
		
	def removeApply(self, name, flag="flag"):
		self.applyMgr.remove(name, flag)
				
	def removeApplyByFlag(self, flag):
		self.applyMgr.removeByFlag(flag)
				
	def addBoutApply(self, name, val, flag="flag"):
		self.boutApplyMgr.add(name, val, flag)
		
	def setBoutApply(self, name, val, flag="flag"):
		self.boutApplyMgr.set(name, val, flag)
		
	def removeBoutApply(self, name, flag="flag"):
		self.boutApplyMgr.remove(name, flag)
				
	def removeBoutApplyByFlag(self, flag):
		self.boutApplyMgr.removeByFlag(flag)

	def getMPMax(self):
		'''真气上限
		'''
		return int((self.mpMax + self.queryApplyAll("真气上限")) * (100 + self.queryApplyAll("真气上限加成")) / 100)
	
	def getHPMax(self):
		'''生命上限
		'''
		return int((self.hpMax + self.queryApplyAll("生命上限")) * (100 + self.queryApplyAll("生命上限加成")) / 100)
	
	def getPhyDamAll(self):
		'''物理伤害
		'''
		return int((self.phyDam + self.queryApplyAll("物理伤害")) * (100 + self.queryApplyAll("物理伤害加成")) / 100)
	
	def getMagDamAll(self):
		'''法术伤害
		'''
		return int((self.magDam + self.queryApplyAll("法术伤害")) * (100 + self.queryApplyAll("法术伤害加成")) / 100)

	def getPhyDefAll(self, att=None):
		'''物理防御
		'''
		add = self.queryApplyAll("物理防御")
		ratio = self.queryApplyAll("物理防御加成")
		if att:
			add -= att.queryApplyAll("无视物理防御")
			ratio -= att.queryApplyAll("无视物理防御加成")
		
		return int((self.phyDef + add) * (100 + ratio) / 100)
	
	def getMagDefAll(self, att=None):
		'''法术防御
		'''
		add = self.queryApplyAll("法术防御")
		ratio = self.queryApplyAll("法术防御加成")
		if att:
			add -= att.queryApplyAll("无视法术防御")
			ratio -= att.queryApplyAll("无视法术防御加成")

		return int((self.magDef + add) * (100 + ratio) / 100)
	
	def getMaxDefAll(self, att=None):
		'''最高防御
		'''
		return max(self.getMagDefAll(att), self.getPhyDefAll(att))
	
	def getCureAll(self):
		'''治疗强度
		'''
		return int((self.cure + self.queryApplyAll("治疗强度")) * (100 + self.queryApplyAll("治疗强度加成")) / 100)
	
	def getPhyCritAll(self):
		'''物理暴击
		'''
		return int((self.phyCrit + self.queryApplyAll("物理暴击")) * (100 + self.queryApplyAll("物理暴击加成")) / 100)
	
	def getMagCritAll(self):
		'''法术暴击
		'''
		return int((self.magCrit + self.queryApplyAll("法术暴击")) * (100 + self.queryApplyAll("法术暴击加成")) / 100)
	
	def getPhyReCritAll(self):
		'''物理抗暴
		'''
		return int((self.phyReCrit + self.queryApplyAll("物理抗暴")) * (100 + self.queryApplyAll("物理抗暴加成")) / 100)
	
	def getMagReCritAll(self):
		'''法术抗暴
		'''
		return int((self.magReCrit + self.queryApplyAll("法术抗暴")) * (100 + self.queryApplyAll("法术抗暴加成")) / 100)
	
	def getSealHitAll(self):
		'''封印命中
		'''
		return (self.sealHit + self.queryApplyAll("封印命中")) * (100 + self.queryApplyAll("封印命中加成")) / 100
	
	def getReSealHitAll(self):
		'''抵抗封印
		'''
		return (self.reSealHit + self.queryApplyAll("抵抗封印")) * (100 + self.queryApplyAll("抵抗封印加成")) / 100
	
	def getSpeAll(self):
		'''速度
		'''
		return int((self.spe + self.queryApplyAll("速度")) * (100 + self.queryApplyAll("速度加成")) / 100)
	
	def getSpeCmdAll(self):
		'''出招速度
		'''
		if not hasattr(self, "speCmdAll"):
			self.calSpeed()
		return self.speCmdAll
	
	def calSpeed(self):
		'''计算出招速度
		'''
		speAll = self.getSpeAll()
		speCmdAll = speAll
		
		ratioExtra = 0
# 		if self.command in (war.commands.doDefend, war.commands.doProtect):
# 			ratioExtra = 1000
# 		elif self.command == war.commands.doCapture:
# 			ratioExtra = 1000 + rand(100)
# 		if ratioExtra:
# 			speCmdAll = speCmdAll * ratioExtra
			
		if self.command in (war.commands.doPerform, war.commands.doPerformSE):
			pfObj = self.getPerform(self.targetPerformId)
			if pfObj and hasattr(pfObj, "calSpeed"):
				speCmdAll = pfObj.calSpeed(self, speCmdAll)
				
		self.speCmdAll = speCmdAll
		self.war.printDebugMsg("\t[%s]计算出招速度  --->速度%d/%d,额外加成%d%%,最终出招速度%d" % (self.name, self.spe, speAll, ratioExtra, speCmdAll))
		self.war.needSort = True
		
# 	def getAttAll(self):
# 		'''命中
# 		'''
# 		return int( (self.att + self.queryApplyAll("命中")) * (100 + self.queryApplyAll("命中加成")) / 100 )
# 	
# 	def getDodAll(self):
# 		'''闪避
# 		'''
# 		return int( (self.att + self.queryApplyAll("闪避")) * (100 + self.queryApplyAll("闪避加成")) / 100 )
	
	def getEnemyTarget(self, vic=None, pfId=0):
		'''敌方目标
		'''
		targetList = []
		if vic and vic.isVisible(self):
			targetList = [vic,]
		else:
			side = self.side ^ 1
			for w in self.war.teamList[side].itervalues():
				if not w.isVisible(self):
					continue
				targetList.append(w)
			
		if not targetList:
			return None
		return targetList[rand(len(targetList))]
		
	def getFriendTarget(self, vic=None, pfId=0):
		'''友方目标
		'''
		targetList = []
		if vic and vic.isVisible(self):
			targetList = [vic,]
		else:
			side = self.side
			for w in self.war.teamList[side].itervalues():
				if not w.isVisible(self):
					continue
				targetList.append(w)
		
		if not targetList:
			return None
		return targetList[rand(len(targetList))]
	
	def getEnemyList(self, isAll=False):
		'''敌方列表
		'''
		targetList = []
		side = self.side ^ 1
		for w in self.war.teamList[side].itervalues():
			if not isAll:
				if not w.isVisible(self):
					continue
			targetList.append(w)
		
		targetList = shuffleList(targetList)
		return targetList
	
	def getFriendList(self, isAll=False):
		'''友方列表
		'''
		targetList = []
		side = self.side
		for w in self.war.teamList[side].itervalues():
			if not isAll:
				if not w.isVisible(self):
					continue
			targetList.append(w)
		
		targetList = shuffleList(targetList)
		return targetList
		
	def getFuncList(self, name):
		'''获取处理函数
		'''
		if name in self.funcList:
			return self.funcList[name].values()
		return []
	
	def addFunc(self, name, func, flag="flag"):
		'''增加处理函数
		'''
		import types
		if type(func) == types.MethodType: # 实例方法
			func = functor(func)

		if name not in self.funcList:
			self.funcList[name] = {}
		self.funcList[name][flag] = func
		
	def removeFunc(self, name, flag="flag"):
		'''移除处理函数
		'''
		if name in self.funcList:
			if flag in self.funcList[name]:
				del self.funcList[name][flag]
	
	def removeFuncByFlag(self, flag):
		'''根据标识移除处理函数
		'''
		for name in self.funcList.iterkeys():
			if flag in self.funcList[name]:
				del self.funcList[name][flag]
	
	def getPerform(self, pfId):
		'''获取法术对象
		'''
		return self.performList.get(pfId)
	
	def getPerformList(self):
		'''获取法术列表
		'''
		for performObj in self.performList.itervalues():
			if not performObj.validPerform(self, False):
				continue
			yield performObj
	
	def getPerformListByType(self, *performTypeList):
		'''根据类型获取法术列表
		'''
		performList = []
		for performObj in self.performList.itervalues():
			if performObj.type not in performTypeList:
				continue
			if not performObj.validPerform(self, False):
				continue
			performList.append(performObj)
		return performList
	
	def querySkillLevel(self, skillId):
		'''查询技能等级
		'''
		skillObj = self.skillList.get(skillId)
		if skillObj:
			return skillObj.level
		return 0
	
	def rpcValStatus(self, **kwArgs):
		args = {"idx": self.idx}
		for k,v in kwArgs.items():
			args[k] = v
		
		self.war.rpcWarWarriorValStatus(**args)

	def addMP(self, val, attacker=None):
		'''扣、加真气
		'''
		if not (self.isRole() or self.isPet()):
			return 0
		
		val = int(val)
		if val > 0:
			if self.mp + val > self.getMPMax():
				val = self.getMPMax() - self.mp
		elif val < 0:
			if self.mp + val < 0:
				val = -self.mp
				
		if val == 0: # 不处理
			return 0
				
		self.mp += val
		self.attrChange("mp")
		self.rpcValStatus(mp=val)
		self.war.printDebugMsg("\t\t[%s]真气变化%+d" % (self.name, val))
		return val
	
	def addHP(self, val, att=None):
		'''扣、加生命
		'''
		if self.isLineupEye():
			return 0

		val = int(val)
		valSrc = val # 原值
		warObj = self.war
		
		if val > 0:
			if self.hp + val > self.getHPMax():
				val = self.getHPMax() - self.hp
		elif val < 0:
			if self.hp + val < 0:
				val = -self.hp
				
		if val == 0: # 不处理
			return 0
				
		self.hp += val
		self.attrChange("hp")
		warObj.printDebugMsg("\t\t[%s]血量变化%+d" % (self.name, val))
		self.checkStatus()
		
		# 扣血显示原值，加血显示真实值
		if val < 0:
			self.rpcStatus(valSrc)
		else:
			self.rpcStatus(val)
			
		if self.isDead():
			if self.hasApply("鬼魂"):
				self.ghostBout = self.bout
			else:
				self.tryRevive(att)
		
		if self.isDead():
			for func in self.getFuncList("beforeDie"):
				func(self, att)
		
		if self.isNeedKickout():
			warObj.addDeadTime = 1
			warObj.kickWarrior(self)
		elif self.isDead():
			warObj.addDeadTime = 2
			words.triggerEvent(self, "倒地")
			if self.isRole():
				self.addSP(-self.sp)

		return val
	
	def rpcStatus(self, hp):
		action = ATTACKED_ACTION_NONE # 受击动作, 0.无  1.被击中  2.防御  3.躲闪
		if hasattr(self, "attackAction"):
			action = self.attackAction
			del self.attackAction
			
		effect = 0 # 受击效果, 0.无  1.暴击
		if hasattr(self, "attackEffect"):
			effect = self.attackEffect
			del self.attackEffect
			
		args = {
			"idx": self.idx,
			"hp": hp,
			"status": self.status, #状态, 0.正常  1.死亡
			"action": action,
			"effect": effect,
			"kickout": self.isNeedKickout(),
		}
		
		self.war.rpcWarWarriorStatus(**args)
		self.war.printDebugMsg("\t\t$type战士[%s]状态:%s" % (self.name, args), self)
	
	def checkStatus(self):
		'''检查状态
		'''
		status = self.status
		if self.hp < 1:
			self.status = WARRIOR_STATUS_DEAD
			self.war.needCheckEnd = True
			if status != self.status:
				self.attrChange("status")
				self.war.printDebugMsg("\t\t$type战士[%s]死亡!!!!" % self.name, self)
				if self.type == WARRIOR_TYPE_ROLE:
					pass
				
		else:
			self.status = WARRIOR_STATUS_NORMAL
			if status != self.status:
				self.war.needSort2 = True
				self.attrChange("status")
				self.war.printDebugMsg("\t\t$type战士[%s]复活!!!!" % self.name, self)
				self.setBoutApply("已复活", True)
				if self.type == WARRIOR_TYPE_ROLE:
					pass
				
	def tryRevive(self, att=None):
		'''尝试复活
		'''
		if self.hasApply("禁止复活"):
			return
		if att and att.hasApply("破神"):
			return

		for func in self.getFuncList("onRevive"):
			func(self, att)

	def receiveDamage(self, dp, att, attackType):
		'''受到伤害
		'''
		if self.isLineupEye():
			return 0
		if self.isDead():
			return 0
		
		warObj = self.war
		if dp < 1: # 至少要扣一点血
			dp = 1
		
		# 附加、加成
		add = 0
		ratio = 0
		
		for func in self.getFuncList("onReceiveDamage"):
			v = func(att, self, dp, attackType)
			if v:
				add += v[0]
				ratio += v[1]
		for func in att.getFuncList("onTargetReceiveDamage"):
			v = func(att, self, dp, attackType)
			if v:
				add += v[0]
				ratio += v[1]
		
		tmpMsg = "附加%s,加成%s%%" % (add, ratio)
		dp = (dp + add) * (100 + ratio) / 100
		
		dpSrc = dp
		dp = self.absorbDamage(dp, att, attackType)

		# 伤害反转
		invertDam = None
		for func in att.getFuncList("invertDamage"):
			invertDam = func(att, self, dp, attackType)
			break
		if invertDam:
			dp = invertDam
			self.war.printDebugMsg("\t结果给[%s]恢复%s点生命值(%s)" % (self.name, dp, tmpMsg))
			dp = self.addHP(dp, att)
			self.wordsOnReceiveDamage()
			return dp

		if dp != dpSrc:
			if dp == 0:
				warObj.printDebugMsg("\t结果给[%s]造成%s点伤害(%s),被完全吸收%s!!" % (self.name, dp, tmpMsg, dpSrc))
				return 0
			dpSub = dpSrc - dp
			warObj.printDebugMsg("\t结果给[%s]造成%s点伤害(%s),被吸收%s" % (self.name, dp, tmpMsg, dpSub))
		else:	
			warObj.printDebugMsg("\t结果给[%s]造成%s点伤害(%s)" % (self.name, dp, tmpMsg))
		
		if self.hasApply("防御"):  # 防御中
			self.attackAction = ATTACKED_ACTION_DEFEND
		else:
			self.attackAction = ATTACKED_ACTION_HIT # 被击中

		dp = -self.addHP(-dp, att)
		self.addSPOnReceiveDamage(dpSrc)
		self.wordsOnReceiveDamage()
		return dp
	
	def addSPOnReceiveDamage(self, dp):
		if not self.isRole():
			return
		if self.isDead():
			return

		ratio = dp * 100 / self.getHPMax()
		if ratio < 10:
			sp = 5
		elif ratio < 20:
			sp = 10
		elif ratio < 30:
			sp = 20
		elif ratio < 50:
			sp = 30
		else:
			sp = 40
			
		self.addSP(sp)
		
	def wordsOnReceiveDamage(self):
		if hasattr(self, "beProteced"):
			del self.beProteced
			beProteced = True
		else:
			beProteced = False
			
		if not self.isDead():
			if not (beProteced and self.isBuddy()):
				words.triggerEvent(self, "挨打")
	
	def absorbDamage(self, dp, att, attackType):
		'''吸收伤害
		'''
# 		# 宝石吸收
# 		ratio = self.queryApplyAll("onAbsorb")
# 		if ratio and rand(100) < ratio:
# 			self.addHP(dp, att)
# 			return 0

		# 法术吸收
		for func in self.getFuncList("onAbsorb"):
			dp = func(att, self, dp, attackType)
			if dp <= 0:
				return 0  # 完全吸收
			
		return dp

	def receiveCure(self, dp, att, attackType):
		'''受到治疗
		'''
		if self.isLineupEye():
			return
		if self.isDead():
			return
		if dp < 0:
			return

		# 附加、加成
		add = 0
		ratio = 0
		
		for func in self.getFuncList("onReceiveCure"):
			v = func(att, self, dp, attackType)
			if v:
				add += v[0]
				ratio += v[1]
		for func in att.getFuncList("onTargetReceiveCure"):
			v = func(att, self, dp, attackType)
			if v:
				add += v[0]
				ratio += v[1]
		
		dp = (dp + add) * (100 + ratio) / 100
		
		# 治疗反转
		invertCure = None
		for func in att.getFuncList("invertCure"):
			invertCure = func(att, self, dp, attackType)
			break
		if invertCure:
			dp = invertCure
			self.war.printDebugMsg("\t结果给[%s]造成%s点伤害(附加%s,加成%s%%)" % (self.name, dp, add, ratio))
			self.addHP(-dp, att)
			return

		self.war.printDebugMsg("\t结果给[%s]恢复%s点生命值(附加%s,加成%s%%)" % (self.name, dp, add, ratio))
		self.addHP(dp, att)

	def addSP(self, val):
		'''扣、加愤怒
		'''
		if not self.isRole():
			return 0

		if val > 0:
			if self.sp + val > self.spMax:
				val = self.spMax - self.sp
		elif val < 0:
			if self.sp + val < 0:
				val = -self.sp
				
		if val == 0: # 不处理
			return 0

		self.sp += val
		self.attrChange("sp")
		self.rpcValStatus(sp=val)
		self.war.printDebugMsg("\t\t[%s]愤怒变化%+d" % (self.name, val))
		return val

	def addFuWen(self, val):
		'''扣、加符能
		'''
		if not (self.isRole() or self.isBuddy()):
			return 0

		if val > 0:
			if self.fuwen + val > self.fuwenMax:
				val = self.fuwenMax - self.fuwen
		elif val < 0:
			if self.fuwen + val < 0:
				val = -self.fuwen

		self.fuwen += val
		self.war.printDebugMsg("\t\t[%s]符能变化%+d" % (self.name, val))
		return val
		
	def isDead(self):
		'''是否死亡
		'''
		if self.isLineupEye():
			return False
		return self.status == WARRIOR_STATUS_DEAD
	
	def isNeedKickout(self):
		'''是否需要从战场中踢出
		'''
		if not self.isDead(): # 未死亡
			return 0
		if not self.inWar(): # 已踢出战场，不需要再踢
			return 0
		if self.type in (WARRIOR_TYPE_ROLE, WARRIOR_TYPE_BUDDY,): # 玩家和伙伴死亡不踢出场景
			return 0
		if hasattr(self, "ghostBout"): # 鬼魂效果
			return 0
		if self.hasApply("不出场"):
			return 0
		return 1
	
	def inWar(self):
		'''是否在战场中
		'''
		if hasattr(self, "released"): # 已被踢出场景并释放
			return None
		return self.war
	
	def isVisible(self, att=None):
		'''是否对人可见
		'''
		if self.isDead():
			return 0
		if self.isLineupEye(): # 阵眼不可见
			return 0
		if self.hasApply("隐身"):
			if not (att and att.hasApply("破隐")):
				return 0
		return 1
	
	def isRole(self):
		'''是否玩家
		'''
		return self.type == WARRIOR_TYPE_ROLE
	
	def isMonster(self):
		'''是否普通怪物
		'''
		return self.type in (WARRIOR_TYPE_NORMAL, WARRIOR_TYPE_BOSS)
	
	def isBoss(self):
		'''是否主怪
		'''
		return self.type == WARRIOR_TYPE_BOSS
	
	def isPet(self):
		'''是否宠物
		'''
		return self.type == WARRIOR_TYPE_PET
	
	def isWatcher(self):
		'''是否观战玩家
		'''
		return self.type == WARRIOR_TYPE_WATCH
	
	def isBuddy(self):
		'''是否助战伙伴
		'''
		return self.type == WARRIOR_TYPE_BUDDY
	
	def isLineupEye(self):
		'''是否阵眼
		'''
		return self.type == WARRIOR_TYPE_LINEUPEYE
	
	def release(self):
		'''释放
		'''
		self.released = True
		self.command = None
		
	def newRound(self):
		'''新回合
		'''
		self.bout += 1
		
		for func in self.getFuncList("onNewRound"):
			func(self)
		for lst in self.buffList.values():
			for bfObj in lst:
				if bfObj:
					bfObj.newRound(self)
					
	def endRound(self):
		'''回合结束
		'''
		for func in self.getFuncList("onEndRound"):
			func(self)

	def cleanRound(self):
		'''清除回合
		'''
		self.boutApplyMgr.clear()
		self.command = None
		self.targetIdx = 0
		self.targetPerformId =  0
		self.targetPropsId = 0
		self.protecterList = []
	
		for lst in self.buffList.values():
			for idx, bfObj in enumerate(lst):
				if not bfObj:
					continue
				bfObj.cleanRound(self)
				if bfObj.bout <= 0:
					lst[idx] = None
					
		if hasattr(self, "ghostBout") and self.bout - self.ghostBout >= 5: # 鬼魂复活
			del self.ghostBout
			self.addHP(self.getHPMax(), self)
					
	def calDamageForMag(self, vic, magDam, power, damRatio, attackType):
		'''计算法术攻击伤害
		'''
		magDamAll = self.getMagDamAll()
		magDefAll = vic.getMagDefAll(self)
		if vic.hasApply("最高防御"):
			defAll = max(magDefAll, vic.getPhyDefAll())
		else:
			defAll = magDefAll

		dam = (magDamAll - defAll + magDam) * (power * 0.01) * ((100 - vic.magRest) * 0.01)
		dam = int(dam * damRatio / 100)
		
		# 附加、加成
		add = 0
		ratio = 0
		for func in self.getFuncList("onCalDamage"):
			v = func(self, vic, dam, attackType)
			if v:
				add += v[0]
				ratio += v[1]
				
		# 五行克制
		ratio += self.calDamageRatioForFiveEl(vic)

		add += self.queryApplyAll("法术伤害结果") + vic.queryApplyAll("被法术伤害结果")
		ratio += self.queryApplyAll("法术伤害结果加成") + vic.queryApplyAll("被法术伤害结果加成")
		if attackType.isMultiTarget:
			ratio += vic.queryApplyAll("被群体法术伤害结果加成")
		dam = int((dam + add) * (100 + ratio) / 100)
		dam = max(self.level + 10, dam) # 保底
		
		# 默认波动
		rnd = rand(98, 102)
		dam = dam * rnd / 100
		
		rndExtra = 0
		if self.hasApply("额外法术伤害结果波动"):
			minNum, maxNum = self.hasApply("额外法术伤害结果波动")
			rndExtra = rand(minNum, maxNum)
			dam = int(dam * rndExtra / 100)
		
		dam = max(1, dam)
		
		if vic.hasApply("免疫暴击"):
			tmpMsg = "[%s]攻击[%s],[%s]免疫暴击!!!" % (self.name, vic.name, vic.name)
		else:
			critRatio = self.calMagCritRatio(vic, attackType)
			if rand(100) < critRatio: # 发生暴击
				dam = dam * 2
				vic.attackEffect = ATTACKED_EFFECT_CRIT
				attackType.isCrit = True
				tmpMsg = "[%s]攻击[%s],发生暴击!!!" % (self.name, vic.name)
			else:
				tmpMsg = "[%s]攻击[%s]" % (self.name, vic.name)
		
		if hasattr(self, "debugMsgForCrit"):
			debugMsgForCrit = self.debugMsgForCrit
			del self.debugMsgForCrit
		else:
			debugMsgForCrit = ""
			
		self.war.printDebugMsg("\t%s  --->法术伤害%d,法术威力%d%%,伤害率%d%%,攻击者法术伤害%d,受害者防御%d(法术防御%d),法术抗性%d,法术伤害结果附加%d,法术伤害结果加成%d%%,波动%d%%,额外波动%d%%,%s,最终伤害%d" % 
							(tmpMsg, magDam, power, damRatio, magDamAll, defAll, magDefAll, vic.magRest, add, ratio, rnd, rndExtra, debugMsgForCrit, dam))
		return dam
	
	def calDamageForPhy(self, vic, magDam=0, power=100, damRatio=100, attackType=None):
		'''计算物理攻击伤害
		
		magDam: 法术伤害，平砍为0
		power: 法术威力，平砍为100
		damRatio: 伤害率，平砍为100
		attackType: 攻击类型
		'''
		if not attackType:
			attackType = perform.object.AttackType(ATTACK_TYPE_PHY)
			
		phyDamAll = self.getPhyDamAll()
		phyDefAll = vic.getPhyDefAll(self)
		if vic.hasApply("最高防御"):
			defAll = max(phyDefAll, vic.getMagDefAll())
		else:
			defAll = phyDefAll
			
		dam = (phyDamAll - defAll + magDam) * (power * 0.01) * ((100 - vic.phyRest) * 0.01)
		dam = int(dam * damRatio / 100)
		
		# 附加、加成
		add = 0
		ratio = 0
		for func in self.getFuncList("onCalDamage"):
			v = func(self, vic, dam, attackType)
			if v:
				add += v[0]
				ratio += v[1]
		
		# 五行克制
		ratio += self.calDamageRatioForFiveEl(vic)
		
		add += self.queryApplyAll("物理伤害结果") + vic.queryApplyAll("被物理伤害结果")
		ratio += self.queryApplyAll("物理伤害结果加成") + vic.queryApplyAll("被物理伤害结果加成")
		dam = int((dam + add) * (100 + ratio) / 100)
		dam = max(self.level + 10, dam) # 保底
		
		# 默认波动
		rnd = rand(98, 102)
		dam = dam * rnd / 100
		
		rndExtra = 0
		if self.hasApply("额外物理伤害结果波动"):
			minNum, maxNum = self.hasApply("额外物理伤害结果波动")
			rndExtra = rand(minNum, maxNum)
			dam = int(dam * rndExtra / 100)
		
		dam = max(1, dam)
		
		if vic.hasApply("免疫暴击"):
			tmpMsg = "[%s]攻击[%s],[%s]免疫暴击!!!" % (self.name, vic.name, vic.name)
		else:
			critRatio = self.calPhyCritRatio(vic, attackType)
			if rand(100) < critRatio: # 发生暴击
				dam = dam * 2
				vic.attackEffect = ATTACKED_EFFECT_CRIT
				attackType.isCrit = True
				tmpMsg = "[%s]攻击[%s],发生暴击!!!" % (self.name, vic.name)
			else:
				tmpMsg = "[%s]攻击[%s]" % (self.name, vic.name)
			
		if hasattr(self, "debugMsgForCrit"):
			debugMsgForCrit = self.debugMsgForCrit
			del self.debugMsgForCrit
		else:
			debugMsgForCrit = ""
		
		self.war.printDebugMsg("\t%s  --->法术伤害%d,法术威力%d%%,伤害率%d%%,攻击者物理伤害%d,受害者防御%d(物理防御%d),物理抗性%d,物理伤害结果附加%d,物理伤害结果加成%d%%,波动%d%%,额外波动%d%%,%s,最终伤害%d" % 
							(tmpMsg, magDam, power, damRatio, phyDamAll, defAll, phyDefAll, vic.phyRest, add, ratio, rnd, rndExtra, debugMsgForCrit, dam))
		return dam
	
	def inDefend(self):
		'''是否防御中
		'''
		if self.hasApply("防御"):
			return True
		return False
	
	def calDamageForDefend(self, att, dam, attackType):
		'''计算防御时的伤害
		'''
		if self.inDefend() and dam > 0:  # 防御中
			dam = dam * 50 / 100
		return dam
	
	def calDamageRatioForFiveEl(self, vic):
		'''计算五行克制伤害加成
		'''
		import fiveElData
		if not vic:
			return 0
		return fiveElData.getDamageRatio(self.fiveElAttack, vic.fiveElDefend)
	
	def calCure(self, vic, magDam, power, damRatio, attackType):
		'''计算治疗
		'''
		cure = self.getCureAll()
		dam = int((cure + magDam) * power * 0.01 * damRatio / 100)

		# 附加、加成
		add = 0
		ratio = 0
		for func in self.getFuncList("onCalCure"):
			v = func(self, vic, dam)
			if v:
				add += v[0]
				ratio += v[1]
		
		add += self.queryApplyAll("治疗结果")
		ratio += self.queryApplyAll("治疗结果加成") + vic.queryApplyAll("被治疗结果加成")
		dam = int((dam + add) * (100 + ratio) / 100)
		
		# 默认波动
		rnd = rand(98, 102)
		dam = dam * rnd / 100
		
		rndExtra = 0
		if self.hasApply("额外治疗结果波动"):
			minNum, maxNum = self.hasApply("额外治疗结果波动")
			rndExtra = rand(minNum, maxNum)
			dam = int(dam * rndExtra / 100)
		
		dam = max(1, dam)
		
		critRatio = self.calMagCritRatio(None, attackType)
		if rand(100) < critRatio: # 发生暴击
			dam = dam * 2
			vic.attackEffect = ATTACKED_EFFECT_CRIT
			attackType.isCrit = True
			tmpMsg = "[%s]治疗[%s],发生暴击!!!" % (self.name, vic.name)
		else:
			tmpMsg = "[%s]治疗[%s]" % (self.name, vic.name)
			
		if hasattr(self, "debugMsgForCrit"):
			debugMsgForCrit = self.debugMsgForCrit
			del self.debugMsgForCrit
		else:
			debugMsgForCrit = ""
		
		self.war.printDebugMsg("\t%s  --->治疗强度%d,法术伤害%d,法术威力%d%%,伤害率%d%%,治疗结果附加%d,治疗结果加成%d%%,波动%d%%,额外波动%d%%,%s,最终治疗%d" %
						 (tmpMsg, cure, magDam, power, damRatio, add, ratio, rnd, rndExtra, debugMsgForCrit, dam))
		return dam
	
	def calPhyCritRatio(self, vic, attackType):
		'''计算物理暴击率
		'''
		phyCrit = self.getPhyCritAll()
		
		# 附加、加成
		add = 0
		ratio = 0
		for func in self.getFuncList("onCalPhyCritRatio"):
			v = func(self, vic, attackType)
			if v:
				add += v[0]
				ratio += v[1]
			
		phyCrit = (phyCrit + add) * (100 + ratio) / 100
		debugMsg = "攻击者物理暴击%d" % phyCrit
		
		if vic: # 计算抗暴
			phyReCrit = vic.getPhyReCritAll()
			phyCrit = max(0, phyCrit - phyReCrit)
			debugMsg += ",受害者物理抗暴%d" % phyReCrit

		self.debugMsgForCrit = "暴击率%d%%(%s)" % (phyCrit, debugMsg)
		return phyCrit
	
	def calMagCritRatio(self, vic, attackType):
		'''计算法术暴击率
		'''
		magCrit = self.getMagCritAll()
		
		# 附加、加成
		add = 0
		ratio = 0
		for func in self.getFuncList("onCalMagCritRatio"):
			v = func(self, vic, attackType)
			if v:
				add += v[0]
				ratio += v[1]
			
		magCrit = (magCrit + add) * (100 + ratio) / 100
		debugMsg = "攻击者法术暴击%d" % magCrit
		
		if vic: # 计算抗暴
			magReCrit = vic.getMagReCritAll()
			magCrit = max(0, magCrit - magReCrit)
			debugMsg += ",受害者法术抗暴%d" % magReCrit

		self.debugMsgForCrit = "暴击率%d%%(%s)" % (magCrit, debugMsg)
		return magCrit
	
	def calHitForPhy(self, vic):
		'''计算物理攻击命中
		'''
		warObj = self.war
		ratio = vic.queryApplyAll("物理躲闪率")
		warObj.printDebugMsg("\t物理躲闪率%d%%" % ratio)
		if rand(100) < ratio:
			warObj.printDebugMsg("\t结果被[%s]躲了过去" % vic.name)
			return False
		return True
	
	def calHitForMag(self, vic):
		'''计算法术攻击命中
		'''
		warObj = self.war
		ratio = vic.queryApplyAll("法术躲闪率")
		warObj.printDebugMsg("\t法术躲闪率%d%%" % ratio)
		if rand(100) < ratio:
			warObj.printDebugMsg("\t结果被[%s]躲了过去" % vic.name)
			return False
		return True
	
	def calSealHit(self, vic, attackType, performHitRatio=0):
		'''计算封印命中
		'''
		sealHitAll = self.getSealHitAll()
		reSealHitAll = vic.getReSealHitAll()
		hitRatio = performHitRatio + sealHitAll - reSealHitAll
		if hitRatio < 20:
			hitRatio = 20
		elif hitRatio > 80:
			hitRatio = 80
			
		# 附加、加成
		add = 0
		ratio = 0
		for func in self.getFuncList("onCalSealHit"):
			v = func(self, vic, hitRatio, attackType)
			if v:
				add += v[0]
				ratio += v[1]
				
		hitRatio = (hitRatio + add) * (100 + ratio) / 100
		self.war.printDebugMsg("\t[%s]对[%s]的封印命中%s(法术命中%s,攻击者封印命中%s,附加%s,加成%s,受害者抵抗封印%s)" % (self.name, vic.name, hitRatio, performHitRatio, sealHitAll, add, ratio, reSealHitAll))
		return hitRatio		
	
	def onPhyAttack(self, vic, attackType):
		'''普通物理攻击时
		'''
		for func in self.getFuncList("onPhyAttack"):
			func(self, vic, attackType)
	
	def onPhyAttacked(self, att, attackType):
		'''被普通物理攻击时
		'''
		for func in self.getFuncList("onPhyAttacked"):
			func(att, self, attackType)
	
	def onPerform(self, vicCast, attackType):
		'''施法时
		'''
		for func in self.getFuncList("onPerform"):
			func(self, vicCast, attackType)
	
	def onPerformed(self, att, attackType):
		'''被施法时
		'''
		for func in self.getFuncList("onPerformed"):
			func(att, self, attackType)
					
	def onAttack(self, vic, vicCast, dp, attackType):
		'''攻击时
		'''
		for func in self.getFuncList("onAttack"):
			func(self, vic, vicCast, dp, attackType)
	
	def onAttacked(self, att, vicCast, dp, attackType):
		'''被攻击时
		'''
		if hasattr(self, "attackAction"):
			del self.attackAction
		if hasattr(self, "attackEffect"):
			del self.attackEffect
			
		for func in self.getFuncList("onAttacked"):
			func(att, self, vicCast, dp, attackType)
			
# 	def onCure(self, vic, effectList, pfObj):
# 		'''治疗时
# 		'''
# 		for func in self.getFuncList("onCure"):
# 			func(self, vic, effectList, pfObj)
# 			
# 	def onCured(self, att, effectList, pfObj):
# 		'''被治疗时
# 		'''
# 		for func in self.getFuncList("onCured"):
# 			func(att, self, effectList, pfObj)
			
# 	def onBuff(self, vic, bfObj, pfObj):
# 		'''加buff时
# 		'''
# 		for func in self.getFuncList("onBuff"):
# 			func(self, vic, bfObj, pfObj)
# 			
# 	def onBuffed(self, att, bfObj, pfObj):
# 		'''被加buff时
# 		'''
# 		for func in self.getFuncList("onBuffed"):
# 			func(att, self, bfObj, pfObj)

	def attrChange(self, attrName):
		'''刷新属性
		'''
		val = getValByName(self, attrName)
			
		args = {
			"idx": self.idx,
			attrName: val,
		}
		
		if attrName in ("hp", "mp", "sp", "fuwen", "status",):
			self.war.rpcWarChangeAttr(None, **args)
		else:
			self.war.rpcWarChangeAttr(self, **args)
	
	def isCatchable(self):
		'''是否可捕捉
		'''
		if not hasattr(self, "catchRatio"):
			return 0
		if not hasattr(self, "carryLevel"):
			return 0
		return 1
	
	def getWarMsg(self):
		txtList = []
		txtList.append("等级:%s" % self.level)
		txtList.append("生命:%s/%s" % (self.hp, self.getHPMax()))
		txtList.append("真气:%s/%s" % (self.mp, self.getMPMax()))
		txtList.append("愤怒:%s/%s" % (self.sp, self.spMax))
		txtList.append("符能:%s/%s" % (self.fuwen, self.fuwenMax))
		txtList.append("物理伤害:%s/%s" % (self.phyDam, self.getPhyDamAll()))
		txtList.append("法术伤害:%s/%s" % (self.magDam, self.getMagDamAll()))
		txtList.append("物理防御:%s/%s" % (self.phyDef, self.getPhyDefAll()))
		txtList.append("法术防御:%s/%s" % (self.magDef, self.getMagDefAll()))
		txtList.append("速度:%s/%s" % (self.spe, self.getSpeAll()))
		txtList.append("治疗强度:%s/%s" % (self.cure, self.getCureAll()))
		txtList.append("物理暴击:%s/%s" % (self.phyCrit, self.getPhyCritAll()))
		txtList.append("法术暴击:%s/%s" % (self.magCrit, self.getMagCritAll()))
		txtList.append("物理抗暴:%s/%s" % (self.phyReCrit, self.getPhyReCritAll()))
		txtList.append("法术抗暴:%s/%s" % (self.magReCrit, self.getMagReCritAll()))
		txtList.append("封印命中:%s/%s" % (self.sealHit, self.getSealHitAll()))
		txtList.append("抵抗封印:%s/%s" % (self.reSealHit, self.getReSealHitAll()))
		if self.fiveElAttack:
			txtList.append("五行:[%s,%s]" % (getFiveElDesc(self.fiveElAttack), getFiveElDesc(self.fiveElDefend)))
		
		skillList = [str(skillId) for skillId in self.skillList]
		skillList.sort()
		txtList.append("技能:[%s]" % ",".join(skillList))

		return " ".join(txtList)
		
	def getDefaultPerform(self):
		'''获取默认法术
		'''
		return self.defaultPerform
	
	def getEscapeRatio(self):
		'''逃跑率
		'''
		return self.queryApplyAll("逃跑率")
	
	def inSeal(self):
		'''是否被封印中
		'''
		for buffObj in self.buffList[BUFF_TYPEPOS_SEAL]:
			if buffObj:
				return True
		return False
	
	def getColors(self):
		return self.colors
	
	def onAddWarrior(self):
		'''增加到战斗中时
		'''
		for func in self.getFuncList("onAddWarrior"):
			func(self)
	
	def onSummon(self, vic):
		'''召唤时
		'''
		for func in self.getFuncList("onSummon"):
			func(self, vic)
	
	def onSummoned(self, att):
		'''被召唤时
		'''
		for func in self.getFuncList("onSummoned"):
			func(att, self)
			
	def onCalTargetCount(self, performObj, targetCount):
		'''计算目标数时
		'''
		add = 0
		ratio = 0
		for func in self.getFuncList("onCalTargetCount"):
			v = func(self, performObj, targetCount)
			if v:
				add += v[0]
				ratio += v[1]
		targetCount = (targetCount + add) * (100 + ratio) / 100
		return targetCount
	
	def onDefend(self, att, attackType):
		'''防御时
		'''
		for func in self.getFuncList("onDefend"):
			func(att, self, attackType)
		for func in att.getFuncList("onTargetDefend"):
			func(att, self, attackType)
			
	def setupPraticeSkill(self):
		'''设置修炼技能
		'''
		who = getRole(self.ownerId)
		if not who:
			return
		
		import skill
		for skillId, skillObj in who.getSkillList().iteritems():
			if not skill.isPetPraticeSkill(skillId): # 不是宠物修炼技能
				continue
			self.skillList[skillId] = skillObj

			performId = skillId
			performObj = perform.new(performId)
			if performObj:
				self.performListPassive[performId] = performObj
				performObj.setup(self)
		


class MonsterWarrior(Warrior):
	'''怪物战士
	'''
	type = WARRIOR_TYPE_NORMAL
	
	def setup(self, monsterObj, warObj, side):
		Warrior.setup(self, monsterObj, warObj, side)


class BossWarrior(Warrior):
	'''Boss战士
	'''
	type = WARRIOR_TYPE_BOSS
	
	def setup(self, monsterObj, warObj, side):
		Warrior.setup(self, monsterObj, warObj, side)
	
	
class LineupEyeWarrior(Warrior):
	'''阵眼战士
	'''
	type = WARRIOR_TYPE_LINEUPEYE
	
	def setup(self, monsterObj, warObj, side):
		Warrior.setup(self, monsterObj, warObj, side)
		
	def isVisible(self, att=None):
		'''是否对人可见
		'''
		return 0


class RoleWarrior(Warrior):
	'''玩家战士
	'''
	type = WARRIOR_TYPE_ROLE
	
	def setup(self, who, warObj, side):
		Warrior.setup(self, who, warObj, side)
		
		self.sp = who.sp
		self.spMax = who.spMax
		
		self.petIdx = 0  # 召唤宠物
		self.summonNumMax = 3  # 召唤次数上限
		self.summonNum = 0  # 已召唤次数
		
		self.propsNumMax = 10  # 物品使用次数上限
		self.propsNum = 0  # 已使用物品次数
		
	def addFuWen(self, val):
		'''扣、加符能
		'''
		val = Warrior.addFuWen(self, val)
		if val != 0:
			self.attrChange("fuwen")
			self.rpcValStatus(fuwen=val)
		return val
		
	def getAutoPerform(self, performId=0, targetIdx=0):
		'''自动战斗的法术
		'''
		warObj = self.war
		if not performId:
			performId = self.getDefaultPerform()
			if performId == CMD_TYPE_PHY:
				return CMD_TYPE_PHY

		if targetIdx:
			vic = warObj.getWarrior(targetIdx, False)
		else:
			vic = None

		tmpPerformIdList = (
			performId,
			performId / 10 * 10 + 1,
			self.school * 100 + 12,
			self.school * 100 + 11,
		)
		
		performIdList = []
		for performId in tmpPerformIdList:
			if performId not in performIdList:
				performIdList.append(performId)

		for performId in performIdList:
			performObj = self.getPerform(performId)
			if not performObj:
				continue
			if not performObj.checkConsume(self, vic):
				continue
			return performId

		return CMD_TYPE_PHY # 保底为普通物理攻击
	
	def getSummonNumMax(self):
		'''召唤次数上限
		'''
		return self.summonNumMax + self.queryApplyAll("召唤次数")
	
	def getPropsNumMax(self):
		'''物品使用次数上限
		'''
		return self.propsNumMax + self.queryApplyAll("物品使用次数")


class PetWarrior(Warrior):
	'''宠物战士
	'''
	type = WARRIOR_TYPE_PET
	
	def setup(self, petObj, warObj, side):
		Warrior.setup(self, petObj, warObj, side)
		self.setupPraticeSkill()


class WatchWarrior(RoleWarrior):
	'''观战玩家
	'''
	type = WARRIOR_TYPE_WATCH


class BuddyWarrior(Warrior):
	'''助战伙伴战士
	'''
	type = WARRIOR_TYPE_BUDDY
	
	def setup(self, buddyObj, warObj, side):
		Warrior.setup(self, buddyObj, warObj, side)
		self.setupPraticeSkill()

		self.fuwen = 20
		self.kind = buddyObj.kind
		
	def cleanRound(self):
		Warrior.cleanRound(self)
		if self.isDead() and not self.hasApply("回合末回复符能"):
			return

		self.addFuWen(20)


from common import *
from buff.defines import *
from war.defines import *
from perform.defines import *
import container
import perform
import perform.object
import war
import war.commands
import words
import task.offlineTask
import weakref