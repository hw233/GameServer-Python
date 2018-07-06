# -*- coding: utf-8 -*-
from perform.defines import *

class Perform(object):
	'''法术基类
	'''
	type = PERFORM_TYPE_NONE  # 法术类型
	passive = 1  # 被动技能
	id = 0 # 法术编号
	name = ""
	targetType = PERFORM_TARGET_NONE  # 目标类型
	targetCount = 0
	fiveEl = FIVE_EL_NONE  # 五行
	consumeList = {  # 消耗
# 		"真气": "LV*2+10",
# 		"生命": "LV*2+10",
	}

	recoverList = {  # 恢复
# 		"符能": "20",
	}
	
	applyList = {  # 法术效果
# 		"禁止法术": True,
# 		"禁止物理攻击": "1",
	}
	
	speRatio = 100 # 速率
	readyBout = 0 # 准备回合
	frozenBout = 0 # 冷却回合
	
	def __init__(self):
		self.lastPerformBout = 0 # 上次出招回合
		
	def getMagId(self, idx=None):
		'''法术动画id
		'''
		if idx is not None:
			return self.id * 10 + idx
		return self.id
	
	def getAttackType(self):
		'''攻击类型
		'''
		if not hasattr(self, "_attackTypeObj"):
			if self.type == PERFORM_TYPE_MAG:
				attackType = ATTACK_TYPE_PERFORM_MAG
			elif self.type == PERFORM_TYPE_PHY:
				attackType = ATTACK_TYPE_PERFORM_PHY
			elif self.type == PERFORM_TYPE_PHY_REMOTE:
				attackType = ATTACK_TYPE_PERFORM_PHY_REMOTE
			else:
				attackType = ATTACK_TYPE_PERFORM_NONE
				
			attackTypeObj = AttackType(attackType)
			attackTypeObj.performId = self.id
			attackTypeObj.fiveEl = self.fiveEl
			attackTypeObj.isMultiTarget = self.isMultiTarget()
			self._attackTypeObj = attackTypeObj
			
		return self._attackTypeObj
	
	def initAttackType(self):
		'''初始化攻击类型
		'''
		attackTypeObj = self.getAttackType()
		attackTypeObj.initTemp()

	def isPassive(self):
		'''是否被动技能
		'''
		return self.passive
	
	def isMultiTarget(self):
		'''是否群体法术
		'''
		if hasattr(self, "targetCountMax") and self.targetCountMax > 1:
			return True
		if isinstance(self.targetCount, int) and self.targetCount < 1:
			return False
		return True
	
	def getCommandTarget(self, att):
		'''指令目标
		'''
		if self.targetType == PERFORM_TARGET_ENEMY:
			return att.getEnemyTarget(None, self)
		else:
			return att.getFriendTarget(None, self)
		
	def getFlag(self):
		'''标识
		'''
		flag = 0
		if self.isPassive():
			flag |= 0x1
		return flag
		
	def save(self):
		return {}
		
	def load(self, data):
		pass
		
	def setup(self, w):
		'''设置
		'''
		for name, val in self.applyList.iteritems():
			if isinstance(val, bool):
				self.setApply(w, name, val)
			else:
				val = int(self.transCode(val, w))
				self.addApply(w, name, val)
		self.onSetup(w)
	
	def onSetup(self, w):
		'''设置时
		'''
		pass
	
	def getSkillId(self):
		'''法术所对应的技能
		'''
		if hasattr(self, "skillId"):
			return self.skillId
		return self.id

	def getLevel(self, w):
		'''法术等级
		'''
		import skill
		skillId = self.getSkillId()
		if skill.isPraticeSkill(skillId): # 修炼技能
			return w.querySkillLevel(skillId)
		if w.isRole():
			return w.querySkillLevel(skillId)
		return w.level

	def consume(self, att, vic, consumeList):
		'''消耗
		'''
		debugMsg = []
		for consumeName, consumeVal in consumeList.iteritems():
			for func in att.getFuncList("onConsume"):
				consumeVal = func(att, vic, consumeName, consumeVal, self.getAttackType())
			if not consumeVal:
				continue
			doConsume(att, consumeName, consumeVal)
			debugMsg.append("%s%s" % (consumeName, consumeVal))
			
		att.war.printDebugMsg("\t消耗[%s]" % ",".join(debugMsg))
	
	def checkConsume(self, att, vic=None, needTips=False, consumeList=None):
		'''检查消耗
		'''
		if consumeList is None:
			consumeList = self.calConsume(att, vic)
		for name, val in consumeList.iteritems():
			attrName = addHandleList[name]["属性名"]
			if val > getattr(att, attrName, 0):
				if needTips:
					if att.isRole():
						message.tips(att.getPID(), "你需要#C02%s#n#C04%d点#n" % (name, val))
					elif att.isPet():
						message.tips(att.getPID(), "你的异兽需要#C02%s#n#C04%d点#n" % (name, val))
				return 0
			
		return 1
			
	def calConsume(self, att, vic=None):
		'''计算消耗
		'''
		if not (att.isRole() or att.isPet() or att.isBuddy()) :  # 玩家、宠物、助战伙伴才消耗
			return {}

		consumeList = {}
		for consumeName, consumeVal in self.consumeList.iteritems():
			if not consumeVal:
				continue
			if consumeName == "真气":
				if not (att.isRole() or att.isPet()):
					continue
			elif consumeName == "愤怒":
				if not att.isRole():
					continue
			elif consumeName == "符能":
				if not (att.isRole() or att.isBuddy()):
					continue
			
			consumeVal = self.transCode(consumeVal, att, vic)
			add = att.queryApplyAll(consumeName + "消耗")
			ratio = att.queryApplyAll(consumeName + "消耗加成")
			consumeVal = (consumeVal + add) * (100 + ratio) / 100
			consumeList[consumeName] = consumeVal

		return consumeList
		
	def tryPerform(self, att, vicCast):
		'''尝试施法
		'''
		if not self.validPerform(att, True):
			return

		warObj = att.war
		self.lastPerformBout = warObj.bout
		self.initAttackType()

		# 检查施法目标
		vicCast = self.checkCastTarget(att, vicCast)
		if not vicCast:
			return
		
		# 检查消耗
		consumeList = self.calConsume(att, vicCast)
		if not self.checkConsume(att, vicCast, True, consumeList):
			return
		
		if vicCast:
			warObj.printDebugMsg("\n[%s]对[%s]使用了法术[%s]" % (att.name, vicCast.name, self.name))
		else:
			warObj.printDebugMsg("\n[%s]使用了法术[%s]" % (att.name, self.name,))
		
		self.consume(att, vicCast, consumeList)
		self.perform(att, vicCast)
		warObj.rpcWarCmdEnd(att)
		self.recover(att)
		self.afterPerform(att, vicCast)
		
	def validPerform(self, att, needTips):
		'''检查施法
		'''
		if self.inFrozen(att): # 冷却中
			return False
		return True
		
	def inFrozen(self, att):
		'''是否在冷却期
		'''
		warObj = att.war
		if self.readyBout:
			if warObj.bout < self.readyBout:
				return True
		if self.frozenBout and self.lastPerformBout:
			if (warObj.bout - self.lastPerformBout) < self.frozenBout:
				return True
		return False

	def perform(self, att, vicCast):
		'''施法
		'''
		pass
	
	def afterPerform(self, att, vicCast):
		'''施法后
		'''
		att.onPerform(vicCast, self.getAttackType())
		vicCast.onPerformed(att, self.getAttackType())
			
	def recover(self, att):
		'''恢复
		'''
		recoverList = self.calRecover(att)
		for name, val in recoverList.iteritems():
			methodName = addHandleList[name]["方法名"]
			func = getattr(att, methodName)
			func(val)
		
		att.war.printDebugMsg("\t回复[%s]\n" % ",".join(["%s%d" % (k,v) for k,v in recoverList.items()]))
			
	def calRecover(self, att):
		'''计算恢复
		'''
		recoverList = {}
		for name, val in self.recoverList.iteritems():
			if name == "符能":
				if not att.isRole():
					continue
			recoverList[name] = self.transCode(val, att, None)
		return recoverList
	
	def checkCastTarget(self, att, vicCast):
		'''检查施法目标
		'''
		if not vicCast:
			message.tips(att.getPID(), "没有指定作用目标")
			return None
		
		if self.targetType == PERFORM_TARGET_NONE:
			return None
		elif self.targetType == PERFORM_TARGET_ENEMY:
			if vicCast.side == att.side:
				message.tips(att.getPID(), "只能作用于敌方")
				return None
		elif self.targetType == PERFORM_TARGET_FRIEND:
			if vicCast.side != att.side:
				message.tips(att.getPID(), "只能作用于已方")
				return None
		elif self.targetType == PERFORM_TARGET_SELF:
			if vicCast is not att:
				message.tips(att.getPID(), "只能作用于自己")
				return None

		return vicCast

	def getPerformTargetList(self, att, vicCast, targetCount=0):
		'''获取作用目标列表
		'''
		if targetCount == 0:  # 不指定目标数，则使用配置的
			targetCount = self.calTargetCount(att)
		if hasattr(self, "customPerformTargetList"):  # 自定义
			return self.customPerformTargetList(att, vicCast, targetCount)
			
		targetList = []
		for w in vicCast.getFriendList():
			if w is vicCast:
				continue
			if not self.checkTarget(att, w, vicCast):
				continue
			targetList.append(w)
			
		if targetList and targetCount > 1:
			targetList = self.sortTargetList(att, vicCast, targetList)
		
		if vicCast.isVisible(att) and self.checkTarget(att, vicCast, vicCast) and vicCast not in targetList:
			targetList.insert(0, vicCast)
		
		return targetList[:targetCount]
	
	def checkTarget(self, att, vic, vicCast):
		return 1
	
	def sortTargetList(self, att, vicCast, targetList):
		'''给攻击目标排序
		'''
		if targetList:
			targetList.sort(key=self.keyForSortTarget)
		return targetList
	
	def keyForSortTarget(self, w):
		if self.type == PERFORM_TYPE_CURE:
			hasBuff = 0
			if getattr(self, "buffId", 0) and buff.has(w, self.buffId):
				hasBuff = 1
			return w.hp, hasBuff

		if getattr(self, "buffId", 0):
			if buff.has(w, self.buffId):
				hasBuff = 1
			else:
				hasBuff = 0
			return hasBuff, -w.getSpeAll()

		return -w.getSpeAll()
	
	def calTargetCount(self, att):
		'''计算目标数
		'''
		targetCount = self.transCode(self.targetCount, att)
		if hasattr(self, "targetCountMax"):
			targetCount = min(targetCount, self.targetCountMax)
		targetCount = att.onCalTargetCount(self, targetCount)
		return max(1, int(targetCount))
			
	def calBout(self, att, vic=None, buffId=0):
		'''计算buff回合数
		'''
		bout = self.transCode(self.bout, att, vic)
		if hasattr(self, "boutMax"):
			bout = min(bout, self.boutMax)
		return max(1, int(bout))
	
	def calHit(self, att, vic):
		'''计算命中
		'''
		return True
	
	def getDamage(self, att, vic):
		'''获取伤害
		'''
		if not hasattr(self, "damage"):
			return 0
		return int(self.transCode(self.damage, att, vic))
	
	def calDamageRatio(self, att, vic, vicCast, targetCount):
		'''计算伤害率
		'''
		ratioList = {
			1: 100,
			2: 65,
			3: 50,
			4: 40,
			5: 34,
			6: 30,
			7: 27,
		}
		
		if targetCount not in ratioList:
			targetCount = max(ratioList.keys())
		
		return ratioList[targetCount]
	
	def transCode(self, code, att=None, vic=None):
		import common
		return common.transCode(self, code, att, vic)
	
	def getValueByVarName(self, varName, att=None, vic=None):
		if varName == "SLV":
			return self.getLevel(att)
		return getValueByVarName(varName, att, vic)
	
	def addApply(self, w, name, val):
		w.addApply(name, int(self.transCode(val, w)), "pf%d" % self.id)
		
	def setApply(self, w, name, val):
		w.setApply(name, self.transCode(val, w), "pf%d" % self.id)
		
	def addFunc(self, w, name, func):
		w.addFunc(name, func, "pf%d" % self.id)
		
	def removeFunc(self, w, name):
		w.removeFunc(name, "pf%d" % self.id)
		
	def performSay(self, w):
		'''被动法术喊招
		'''
		if self.name.startswith("高级"):
			name = self.name.replace("高级", "")
		else:
			name = self.name
		w.war.say(w, name, 9)
		

class AttackPerformBase(Perform):
	'''攻击法术基类
	'''
	targetType = PERFORM_TARGET_ENEMY
	passive = 0
	damage = 0  # 法术额外伤害
	power = 100  # 威力
	
	def checkCastTarget(self, att, vicCast):
		vicCast = att.getEnemyTarget(vicCast, self.id)
		if not vicCast:
			message.tips(att.getPID(), "没有指定作用目标")
			return None
		if vicCast.side == att.side:
			message.tips(att.getPID(), "只能作用于敌方")
			return None
		return vicCast
	
	def perform(self, att, vicCast):
		'''施法
		'''
		targetList = self.getPerformTargetList(att, vicCast)
		targetCount = len(targetList)
		
		att.war.rpcWarPerform(att, self.getMagId(), targetList)
		for idx, vic in enumerate(targetList):
			if vic.isDead():
				continue
			vic.attackedIdx = idx # 被攻击序号
			self.attack(att, vic, vicCast, targetCount)
			if att.isDead():
				break
				
	def attack(self, att, vic, vicCast, targetCount):
		if self.calHit(att, vic):
			damRatio = self.calDamageRatio(att, vic, vicCast, targetCount)
			dp = self.calDamage(att, vic, damRatio)
			vic.receiveDamage(dp, att, self.getAttackType())
		else:
			att.war.rpcWarWarriorStatus(idx=vic.idx, action=ATTACKED_ACTION_DODGE)  # 躲闪
			dp = 0
			
		self.afterAttack(att, vic, vicCast, dp, targetCount)
		
	def calHit(self, att, vic):
		'''计算命中
		'''
		return att.calHitForMag(vic)

	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		magDam = self.getDamage(att, vic)
		dp = att.calDamageForMag(vic, magDam, self.power, damRatio, self.getAttackType())
		return dp
	
	def afterAttack(self, att, vic, vicCast, dp, targetCount):
		'''攻击后
		'''
		att.onAttack(vic, vicCast, dp, self.getAttackType())
		vic.onAttacked(att, vicCast, dp, self.getAttackType())


class PhyAttackPerform(AttackPerformBase):
	'''物理近攻法术
	'''
	type = PERFORM_TYPE_PHY
	
	def perform(self, att, vicCast):
		targetList = self.getPerformTargetList(att, vicCast)
		targetCount = len(targetList)
		
		att.war.rpcWarPerform(att, self.getMagId(), targetList[0])
		for idx, vic in enumerate(targetList):
			if vic.isDead():
				continue
			att.war.rpcWarPerform(att, self.getMagId(idx), vic)
			vic.attackedIdx = idx # 被攻击序号
			self.attack(att, vic, vicCast, targetCount)
			if vic.inDefend():
				vic.onDefend(att, self.getAttackType())
			if att.isDead():
				break
		
	def calHit(self, att, vic):
		'''计算命中
		'''
		return att.calHitForPhy(vic)
		
	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		magDam = self.getDamage(att, vic)
		dp = calDamageForPhyMag(att, vic, magDam, self.power, damRatio, self.getAttackType())
		return dp

	
class RemotePhyAttackPerform(AttackPerformBase):
	'''物理远攻法术
	'''
	type = PERFORM_TYPE_PHY_REMOTE
	
	def calHit(self, att, vic):
		'''计算命中
		'''
		return att.calHitForPhy(vic)
		
	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		magDam = self.getDamage(att, vic)
		dp = calDamageForPhyMag(att, vic, magDam, self.power, damRatio, self.getAttackType())
		return dp


class MagAttackPerform(AttackPerformBase):
	'''魔法攻击法术
	'''
	type = PERFORM_TYPE_MAG


class BuffPerform(Perform):
	''' 增益法术
	'''
	type = PERFORM_TYPE_BUFF
	passive = 0
	buffId = 0
	bout = 0  # 回合数
	
	def perform(self, att, vicCast):
		targetList = self.getPerformTargetList(att, vicCast)
		targetCount = len(targetList)
		
		att.war.rpcWarPerform(att, self.getMagId(), targetList)
		for idx, vic in enumerate(targetList):
			if vic.isDead():
				continue
			vic.attackedIdx = idx # 被攻击序号
			self.buff(att, vic, targetCount)
			if att.isDead():
				break
			
	def buff(self, att, vic, targetCount):
		bfObj = None
		if self.buffId:
			bout = self.calBout(att, vic, self.buffId)
			bfObj = buff.addOrReplace(vic, self.buffId, bout, att)
		self.afterBuff(att, vic, bfObj, targetCount)

	def afterBuff(self, att, vic, bfObj, targetCount):
		'''加buff时
		'''
		pass
# 		if bfObj:
# 			att.onBuff(vic, bfObj, self)
# 			vic.onBuffed(att, bfObj, self)


class MPBuffPerform(BuffPerform):
	''' 增益真气法术
	'''
	type = PERFORM_TYPE_BUFF_MP


class DeBuffPerform(BuffPerform):
	''' 减益法术
	'''
	type = PERFORM_TYPE_DEBUFF

	
class SealPerform(BuffPerform):
	''' 封印法术
	'''
	type = PERFORM_TYPE_SEAL
	hitRatio = 100

	def buff(self, att, vic, targetCount):
		bfObj = None
		if self.calHit(att, vic):
			bout = self.calBout(att, vic, self.buffId)
			bfObj = buff.addOrReplace(vic, self.buffId, bout, att)
		else:
			att.war.rpcWarWarriorStatus(idx=vic.idx, action=ATTACKED_ACTION_DODGE)  # 躲闪
		self.afterBuff(att, vic, bfObj, targetCount)
			
	def calHit(self, att, vic):
		'''计算命中
		'''
		if vic.hasApply("抗封"):
			att.war.printDebugMsg("\t受害者[%s]抗封,无视一切封印法术" % vic.name)
			return False
		performHitRatio = self.transCode(self.hitRatio, att, vic)
		hitRatio = att.calSealHit(vic, self.getAttackType(), performHitRatio)
		if rand(10000) >= hitRatio*100:
			return False
		return True
	

class ReSealPerform(BuffPerform):
	''' 解封法术
	'''
	type = PERFORM_TYPE_RESEAL

	
class CurePerform(Perform):
	'''治疗法术
	'''
	type = PERFORM_TYPE_CURE
	targetType = PERFORM_TARGET_FRIEND
	passive = 0
	
	def checkCastTarget(self, att, vicCast):
		vicCast = Perform.checkCastTarget(self, att, vicCast)
		if not vicCast:
			return None
		if vicCast.hasApply("禁止治疗"):
			message.tips(vicCast.getPID(), "目标不能接受治疗")
			return None
		if vicCast.isDead():
			message.tips(att.getPID(), "目标只接受复活")
			return None
		return vicCast
	
	def perform(self, att, vicCast):
		targetList = self.getPerformTargetList(att, vicCast)
		targetCount = len(targetList)
		
		att.war.rpcWarPerform(att, self.getMagId(), targetList)
		for idx, vic in enumerate(targetList):
			if vic.isDead():
				continue
			vic.attackedIdx = idx # 被攻击序号
			self.cure(att, vic, vicCast, targetCount)
			if att.isDead():
				break
		
	def cure(self, att, vic, vicCast, targetCount):
		damRatio = self.calDamageRatio(att, vic, vicCast, targetCount)
		dp = self.calDamage(att, vic, damRatio)
		dp = max(1, dp)
		vic.receiveCure(dp, att, self.getAttackType())
		self.onCure(att, vic, vicCast, dp, targetCount)
		
	def calDamage(self, att, vic, damRatio):
		'''计算伤害
		'''
		magDam = self.getDamage(att, vic)
		dp = att.calCure(vic, magDam, self.power, damRatio, self.getAttackType())
		return dp
		
	def onCure(self, att, vic, vicCast, dp, targetCount):
		'''治疗时
		'''
		pass
	

class RevivePerform(CurePerform):
	''' 复活法术
	'''
	type = PERFORM_TYPE_REVIVE
	
	def getCommandTarget(self, att):
		'''指令目标
		'''
		targetList = []
		for w in att.getFriendList(isAll=True):
			if not w.isDead():
				continue
			targetList.append(w)
			
		if not targetList:
			return None
		return targetList[rand(len(targetList))]
	
	def checkCastTarget(self, att, vicCast):
		vicCast = Perform.checkCastTarget(self, att, vicCast)
		if not vicCast:
			return None
		if not vicCast.isDead():
			message.tips(att.getPID(), "目标不需要复活")
			return None
		if vicCast.hasApply("禁止治疗"):
			message.tips(att.getPID(), "目标不能接受治疗")
			return None
		if vicCast.hasApply("禁止复活"):
			message.tips(att.getPID(), "目标不能被复活")
			return None
		return vicCast
	
	def getPerformTargetList(self, att, vicCast, targetCount=0):
		'''获取作用目标列表
		'''
		if targetCount == 0:  # 不指定目标数，则使用配置的
			targetCount = self.calTargetCount(att)
		if hasattr(self, "customPerformTargetList"):  # 自定义
			return self.customPerformTargetList(att, vicCast, targetCount)
			
		targetList = []
		for w in vicCast.getFriendList(True):
			if w is vicCast:
				continue
			if not w.isDead():
				continue
			if not self.checkTarget(att, w, vicCast):
				continue
			targetList.append(w)
			
		if targetList and targetCount > 1:
			targetList = self.sortTargetList(att, vicCast, targetList)
		
		if vicCast.isDead() and self.checkTarget(att, vicCast, vicCast) and vicCast not in targetList:
			targetList.insert(0, vicCast)
		
		return targetList[:targetCount]
	
	def perform(self, att, vicCast):
		targetList = self.getPerformTargetList(att, vicCast)
		targetCount = len(targetList)
		
		att.war.rpcWarPerform(att, self.getMagId(), targetList)
		for idx, vic in enumerate(targetList):
			if not vic.isDead():
				continue
			vic.attackedIdx = idx # 被攻击序号
			self.revive(att, vic, vicCast, targetCount)
	
	def revive(self, att, vic, vicCast, targetCount):
		damRatio = self.calDamageRatio(att, vic, vicCast, targetCount)
		dp = self.calDamage(att, vic, damRatio)
		vic.addHP(dp, att)
		self.onRevive(att, vic, vicCast, dp, targetCount)
		
	def onRevive(self, att, vic, vicCast, dp, targetCount):
		'''复活时
		'''
		pass


class AttackType(object):
	'''攻击类型
	'''

	def __init__(self, attackType):
		self.attackType = attackType  # 攻击类型
		self.performId = 0 # 法术id
		self.fiveEl = FIVE_EL_NONE  # 五行
		self.isMultiTarget = False # 是否群体法术

		self.isBack = False # 是否反击
		self.isCrit = False # 是否暴击
		
	def initTemp(self):
		'''初始化临时数据
		'''
		self.isBack = False
		self.isCrit = False
		

def calDamageForPhyMag(att, vic, magDam, power, damRatio, attackType):
	'''计算物理法术攻击的伤害
	'''
	dp = att.calDamageForPhy(vic, magDam, power, damRatio, attackType)
	if attackType.attackType == ATTACK_TYPE_PERFORM_PHY: # 法术物理近攻会触发保护
		if att.side != vic.side:
			dp = war.commands.protect(att, vic, dp)
	dp = vic.calDamageForDefend(att, dp, attackType)
	return dp


from common import *
from perform.defines import *
from war.defines import *
import role.defines
import buff
import message
import war.commands
import perform
import types