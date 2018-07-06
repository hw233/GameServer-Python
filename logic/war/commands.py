# -*- coding: utf-8 -*-
from war.defines import *

PET_FIGHT_LIMIT = 1

#===============================================================================
# 设置出招指令相关
#===============================================================================
def setCommand(warObj, w, cmdType, **args):
	'''设置出招指令
	'''
	cmdFunc = cmdSetHandlerList.get(cmdType)
	if not cmdFunc:
		message.debugClientMsg(w.getPID(), "%s下达了非法的指令:%s %s" % (w.name, cmdType, args))
		setCommand(warObj, w, CMD_TYPE_PHY, **args)
		return

	w.targetIdx = args.get("targetIdx", 0)
	cmdFunc(warObj, w, **args)

def setCommand_Phy(warObj, w, **args):
	'''设置指令:物理攻击
	'''
	w.command = doPhyAttack
	
def setCommand_Mag(warObj, w, **args):
	'''设置指令:法术
	'''
	performId = args["performId"]
	performObj = w.getPerform(performId)
	if not performObj:
		message.debugClientMsg(w.getPID(), "%s设置法术指令时，找不到法术%s" % (w.name, performId))
		setCommand(warObj, w, CMD_TYPE_PHY, **args)
		return

	w.command = doPerform
	w.targetPerformId = performId
			
def setCommand_SE(warObj, w, **args):
	'''设置指令:特技
	'''
	performId = args["performId"]
	performObj = w.getPerform(performId)
	if not performObj:
		message.debugClientMsg(w.getPID(), "%s设置特技指令时，找不到特技%s" % (w.name, performId))
		setCommand(warObj, w, CMD_TYPE_PHY, **args)
		return
	
	w.command = doPerformSE
	w.targetPerformId = performId
			
def setCommand_Props(warObj, w, **args):
	'''设置指令:使用物品
	''' 
	w.targetPropsId = args["itemId"]
	w.command = doUseProps
	
def setCommand_Defend(warObj, w, **args):
	'''设置指令:防御
	'''
# 	w.command = doDefend
	w.command = doWait
	doDefend(w)
		
def setCommand_Wait(warObj, w, **args):
	'''设置指令:等待
	'''
	w.command = doWait
	
def setCommand_Protect(warObj, w, **args):
	'''设置指令:保护
	'''
# 	w.command = doProtect
	w.command = doWait
	doProtect(w)
	
def setCommand_Summon(warObj, w, **args):
	'''设置指令:召唤
	'''
	w.command = doSummon
	
def setCommand_Escape(warObj, w, **args):
	'''设置指令:逃跑
	'''
	w.command = doEscape
	w.setBoutApply("逃跑指令", True)
	
def setCommand_Capture(warObj, w, **args):
	'''设置指令:逃跑
	'''
	w.command = doCapture
	
def setCommand_AI(warObj, w, **args):
	'''设置指令:AI
	'''
	w.command = doAI

		
#===============================================================================
# 设置出招指令的处理函数
#===============================================================================
cmdSetHandlerList = {
	CMD_TYPE_PHY: setCommand_Phy, # 物理攻击
	CMD_TYPE_MAG: setCommand_Mag, # 法术攻击
	CMD_TYPE_SE: setCommand_SE, # 特技攻击
	CMD_TYPE_ITEM: setCommand_Props, # 使用物品
	CMD_TYPE_DEFEND: setCommand_Defend, # 防御
	CMD_TYPE_WAIT: setCommand_Wait, # 等待
	CMD_TYPE_PROTECT: setCommand_Protect, # 保护
	CMD_TYPE_SUMMON: setCommand_Summon, # 召唤
	CMD_TYPE_ESCAPE: setCommand_Escape, # 逃跑
	CMD_TYPE_CAPTURE: setCommand_Capture, # 捕捉
	CMD_TYPE_AI: setCommand_AI, # AI
}



#===============================================================================
# 出招指令相关
#===============================================================================
def doPerform(att):
	'''法术
	'''
	warObj = att.war
	targetIdx = att.targetIdx
	performId = att.targetPerformId

	pfObj = att.getPerform(performId)
	if not pfObj:
		try:
			raise Exception("[perform]not found perform: %s %s" % (att.getPID(), performId))
		except:
			logException()
		return
	
	if targetIdx:
		vic = warObj.getWarrior(targetIdx, notDead=False)
	else:
		vic = warObj.getCommandTarget(att, performId)
	
	if att.hasApply("禁止法术") and not hasattr(pfObj, "breakSeal"):
		message.tips(att.getPID(), "技能已被封禁，无法使用")
		return

	pfObj.tryPerform(att, vic)
	
def doPerformSE(att):
	'''特技
	'''
	warObj = att.war
	targetIdx = att.targetIdx
	performId = att.targetPerformId

	pfObj = att.getPerform(att.targetPerformId)
	if not pfObj:
		try:
			raise Exception("[performSE]not found perform: %s %s" % (att.getPID(), att.targetPerformId))
		except:
			logException()
		return
	
	if targetIdx:
		vic = warObj.getWarrior(targetIdx, notDead=False)
	else:
		vic = warObj.getCommandTarget(att, performId)
	
	if att.hasApply("禁止特技"):
		message.tips(att.getPID(), "特技已被封禁，无法使用")
		return

	pfObj.tryPerform(att, vic)


def doPhyAttack(att, isBack=False):
	'''物理攻击
	'''
	warObj = att.war
	targetIdx = att.targetIdx
	if targetIdx:
		vic = warObj.getWarrior(targetIdx)
		vic = att.getEnemyTarget(vic, CMD_TYPE_PHY)
	else:
		vic = warObj.getCommandTarget(att, CMD_TYPE_PHY)

	if not vic:
		return
	if att == vic:	
		message.tips(att.getPID(), "不能攻击自己")
		return
	if att.hasApply("禁止物理攻击"):
		message.tips(att.getPID(), "物理攻击已被封禁，无法使用")
		return

	hitTimes = 1
	if rand(100) < att.queryApplyAll("双击机率"):
		hitTimes = 2
	if hitTimes == 1:
		warObj.printDebugMsg("\n[%s]攻击[%s]" % (att.name, vic.name))
	
	attackType = perform.object.AttackType(ATTACK_TYPE_PHY)
	attackType.isBack = isBack
	
	for i in range(hitTimes):
		att.hitTimes = i  # 第几次连击
		_phyAttack(att, vic, attackType)
		if att.isDead() or vic.isDead():
			break
		
	if hasattr(att, "hitTimes"):
		del att.hitTimes
	
	att.onPhyAttack(vic, attackType)
	vic.onPhyAttacked(att, attackType)
	warObj.rpcWarCmdEnd(att)

def _phyAttack(att, vic, attackType):
	'''物理攻击
	'''
	warObj = att.war
	warObj.rpcWarPerform(att, MAGIC_PHY, vic)
	att.attacking = 1  # 此标记用于出招结束时通知客户端
	if att.calHitForPhy(vic):
		dp = att.calDamageForPhy(vic, 0, 100, 100, attackType)
		if att.side != vic.side:
			dp = protect(att, vic, dp)
		dp = vic.calDamageForDefend(att, dp, attackType)
		vic.receiveDamage(dp, att, attackType)
		if vic.inDefend():
			vic.onDefend(att, attackType)
	else:
		warObj.rpcWarWarriorStatus(idx=vic.idx, action=ATTACKED_ACTION_DODGE)  # 躲闪
		dp = 0
		
	_onAttack(att, vic, vic, dp, attackType)


def protect(att, vic, dp):
	protecterList = []
	warObj = att.war
	
	# 主动保护
	for idx in vic.protecterList:
		w = warObj.getWarrior(idx)
		if not w:
			continue
		protecterList.append((idx, 60, 40, 0))
	
	# 自动保护
	if vic.isRole() and vic.petIdx not in vic.protecterList:
		sw = warObj.getWarrior(vic.petIdx)
		if sw and hasattr(sw, "protectOwnerRatio"):
			if rand(100) < sw.protectOwnerRatio:
				protecterList.append((sw.idx, 60, 40, 0))
					
	protecterList = shuffleList(protecterList)
	for idx, ratio1, ratio2, ratio3 in protecterList:
		w = warObj.getWarrior(idx)
		if not w:
			continue
		if w.hasApply("禁止指令"):
			continue
		
		hp1 = max(1, dp * ratio1 / 100)  # 被保护者的伤害
		hp2 = max(1, dp * ratio2 / 100)  # 保护者的伤害
		hp3 = max(1, w.hpMax * ratio3 / 100)  # 保护者的生命下限
		if vic.hp <= hp1:  # 被保护也会死亡 
			continue
		if w.hp <= hp2:  # 保护者会死亡
			continue
		if hp3 and w.hp < hp3:
			continue
		if idx in vic.protecterList:
			vic.protecterList.remove(idx)
		
		warObj.rpcWarPerform(w, MAGIC_PROTECT, vic)
		att.war.printDebugMsg("\t[%s]保护了[%s]" % (w.name, vic.name))
		w.addHP(-hp2, att)
		dp = hp1
		words.triggerEvent(w, "保护")
		if w.isPet() and vic.isBuddy():
			vic.beProteced = True
		break
	
	return dp
		

def _onAttack(att, vic, vicCast, dp, attackType):
	att.onAttack(vic, vicCast, dp, attackType)
	vic.onAttacked(att, vicCast, dp, attackType)


def doDefend(att):
	'''防御
	'''
	att.setBoutApply("防御", True)
	att.war.rpcWarPerform(att, MAGIC_DEFEND, att)

def doProtect(att):
	'''保护
	'''
	vic = att.war.getWarrior(att.targetIdx)
	if not vic:
		return
	if vic == att:
		message.tips(att.getPID(), "不可以自己保护自己")
		return
	vic.protecterList.append(att.idx)


def doWait(att):
	'''等待
	'''
	pass


def doCapture(att):
	'''捕捉
	'''
	warObj = att.war
	vic = warObj.getWarrior(att.targetIdx)
	if not vic:
		return
	who = getRole(att.getPID())
	if not who:
		return

	# 自定义捕捉
	if hasattr(warObj.game, "customCapture") and warObj.game.customCapture(who, att, vic):
		warObj.rpcWarCmdEnd(att)
		return
	if not _checkCapture(who, att, vic):
		return	
	
	# 消耗
	mp = att.level + 2
	att.addMP(-mp)
	
	# 计算捕捉机率
	ratio = _calCaptureRatio(att, vic)
	if rand(100) < ratio:
		warObj.rpcWarPerform(att, MAGIC_CAPTURE_WIN, vic)  # 播放捕捉成功动画
		warObj.kickWarrior(vic)
		_addPet(who, att, vic)
	else:
		warObj.rpcWarPerform(att, MAGIC_CAPTURE_FAIL, vic)  # 播放捕捉失败动画
		pass
	warObj.rpcWarCmdEnd(att)
		
			
def _checkCapture(who, att, vic):
	if not vic.isCatchable():
		message.tips(att.getPID(), "%s不能捕捉" % vic.name)
		return 0
	if hasattr(vic, "carryLevel") and vic.carryLevel > att.level:
		message.tips(att.getPID(), "你的等级不够%d，不能捕捉" % vic.carryLevel)
		return 0
	if att.level < vic.level - 20:
		message.tips(att.getPID(), "目标对于你来说过于强大，不能捕捉")
		return 0
	mp = att.level + 2
	if att.mp < mp:
		message.tips(att.getPID(), "你的真气值不够%d，不能捕捉" % mp)
		return 0
	if who.petCtn.itemCount() >= who.petCtn.itemCountMax():
		message.tips(att.getPID(), "你身上的宠物已满，不能捕捉")
		return 0
	
	return 1

def _calCaptureRatio(att, vic):
	ratio = vic.catchRatio
	if vic.level == 0:  # 宝宝
		ratio += 40
	else:
		if vic.hp < vic.hpMax / 20:
			ratio = ratio * 3 + 40
		elif vic.hp < vic.hpMax / 5:
			ratio = ratio * 25 / 10 + 15
		elif vic.hp < vic.hpMax * 5 / 10:
			ratio = ratio * 2 + 10
		elif vic.hp < vic.hpMax * 8 / 10:
			ratio = ratio * 15 / 10 + 5

		ratio = ratio * (100 + att.queryApplyAll("捕捉加成")) / 100
		
		# 等级差影响
		ratio += min(20, max(0, att.level - vic.level))
	return ratio

def _addPet(who, att, vic):
	if vic.level:
		level = vic.level * rand(70, 101) / 100
	petObj = pet.createByShape(vic.shape, level, skill=vic.skillList.keys())
	pet.addPet(who, petObj)

def doEscape(att):
	'''逃跑
	'''
	warObj = att.war
	if att.hasApply("禁止逃跑"):
		message.tips(att.getPID(), "禁止逃跑")
		return

	if warObj.isPVESingle() and att.isRole():
		ratio = 100
	else:
		ratio = None
		if hasattr(warObj.game, "customEscapeRatio"):
			ratio = warObj.game.customEscapeRatio(att)
		if ratio is None:
			ratio = 50 + att.getEscapeRatio()
			if ratio < 20:
				ratio = 20
			elif ratio > 80:
				ratio = 80

	if rand(100) < ratio:
		att.isEscaped = True
		targetList = [att]
		if att.isRole() and att.petIdx:
			sw = warObj.getWarrior(att.petIdx, False)
			if sw:
				targetList.append(sw)
		warObj.rpcWarPerform(att, MAGIC_ESCAPE_WIN, targetList)  # 播放逃跑成功动画
		warObj.printDebugMsg("[%s]逃跑了，成功率%d%%" % (att.name, ratio))
		att.war.kickWarrior(att)
	else:
		warObj.rpcWarPerform(att, MAGIC_ESCAPE_FAIL, att)  # 播放逃跑失败动画
		warObj.printDebugMsg("[%s]逃跑失败，成功率%d%%" % (att.name, ratio))
		words.triggerEvent(att, "逃跑失败")
	
	warObj.rpcWarCmdEnd(att)

def doUseProps(att):
	'''使用物品
	'''
	who = getRole(att.getPID())
	roleWarrior = who.warrior
	
	if roleWarrior.propsNum >= roleWarrior.getPropsNumMax():
		message.tips(att.getPID(), "本场战斗可使用物品的次数为0，无法继续使用")
		return

	warObj = att.war
	if att.hasApply("禁止物品"):
		message.tips(att.getPID(), "禁止使用物品")
		return
	
	vic = warObj.getWarrior(att.targetIdx, notDead=False)
	if not vic:
		return
	
	propsObj = who.propsCtn.getItem(att.targetPropsId)
	if not propsObj:
		message.tips(att.getPID(), "没有此物品")
		return
	if not hasattr(propsObj, "useInWar"):
		message.tips(att.getPID(), "此物品不能在战斗中使用")
		return
		
	if not propsObj.useInWar(who, att, vic):
		return
	listener.doListen("使用物品", who, propsNo=propsObj.no())
	roleWarrior.propsNum += 1
	warObj.rpcWarChange(roleWarrior, "propsNum")
	words.triggerEvent(att, "使用道具")
	warObj.rpcWarCmdEnd(att)
		
def doSummon(att):
	'''召唤
	'''
	pid = att.getPID()
	who = getRole(pid)
	if not who:
		return
	
	warObj = att.war
# 	if att.targetIdx == -1: # 召回
# 		summonBack(att)
# 		return
	
	if att.summonNum >= att.getSummonNumMax():
		message.tips(att.getPID(), "本场战斗可召唤异兽的次数为0，无法继续召唤")
		return
	
	# 尝试把现在的参战宠召回，如果失败则拒绝召唤新参战宠
	if att.petIdx:
		doSummonBack(att)
	if att.petIdx: # 召回失败
		return
	
	petObj = who.petCtn.getItem(att.targetIdx)
	if not petObj:
		message.tips(att.getPID(), "异兽不存在，无法召唤")
		return
	if warObj.petStat[pid].get(att.targetIdx, 0) >= PET_FIGHT_LIMIT:
		message.tips(att.getPID(), "此异兽已经参战过了")
		return
	
	att.summonNum += 1
	warObj.rpcWarChange(att, "summonNum")
	sw = warObj.addPetFight(att, petObj)
	warObj.rpcWarChange(att, "petIdList")
# 	who.petCtn.setFighter(petObj, True)
	
	warObj.rpcWarPerform(att, MAGIC_SUMMON, None)
	warObj.rpcAddWarrior(sw, None, True)
	warObj.rpcWarAllBuff(sw)
	words.triggerEvent(att, "换宠")
	warObj.rpcWarCmdEnd(att)
# 	message.tips(att.getPID(), "召唤成功！")
	warObj.onSummon(att, sw)
	
def doSummonBack(att):
	'''召回
	'''
	if not att.petIdx:
		return
	
	warObj = att.war
	sw = att.war.getWarrior(att.petIdx, False)
	if sw:
		if sw.isDead():
			message.tips(att.getPID(), "#C02%s#n无法召回" % sw.name)
			return
# 		warObj.rpcWarPerform(att, MAGIC_SUMMON_BACK, sw)
		att.war.kickWarrior(sw)
	
	att.petIdx = 0
# 	who = getRole(att.getPID())
# 	if who:
# 		petObj = who.petCtn.getFighter()
# 		if petObj:
# 			who.petCtn.setFighter(petObj, False)

def doAI(att):
	'''AI
	'''
	performId = war.ai.getPerform(att)
	if performId > 100:
		att.targetPerformId = performId
		doPerform(att)
	else:
		doPhyAttack(att)


from common import *
import pet
import message
import config
import war
import war.ai
import words
import listener
import perform.object