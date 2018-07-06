# -*- coding: utf-8 -*-
# 宠物服务
import endPoint
import pet_pb2

def handleLock(oldFunc):
	def newFunc(self,ep,who,reqMsg):
		import role.roleConfig
		if role.roleConfig.isLock(who):
			who.endPoint.rpcSecurityUnlock()
			return
		try:
			return oldFunc(self,ep,who,reqMsg)
		except Exception:
			raise
	return newFunc

class cService(pet_pb2.terminal2main):
	@endPoint.result
	def rpcPetRename(self, ep, who, reqMsg): return rpcPetRename(who, reqMsg)

	@endPoint.result
	def rpcPetFighter(self, ep, who, reqMsg): return rpcPetFighter(who, reqMsg)

	@endPoint.result
	def rpcPetCarry(self, ep, who, reqMsg): return rpcPetCarry(who, reqMsg)

	@endPoint.result
	@handleLock
	def rpcPetAttrPointReset(self, ep, who, reqMsg): return rpcPetAttrPointReset(who, reqMsg)

	@endPoint.result
	@handleLock
	def rpcPetAttrPointAdd(self, ep, who, reqMsg): return rpcPetAttrPointAdd(who, reqMsg)

	@endPoint.result
	def rpcPetAttrPointScheme(self, ep, who, reqMsg): return rpcPetAttrPointScheme(who, reqMsg)

	@endPoint.result
	def rpcPetAttrPointSchemeRequest(self, ep, who, reqMsg): return rpcPetAttrPointSchemeRequest(who, reqMsg)

	@endPoint.result
	def rpcPetUseItem(self, ep, who, reqMsg): return rpcPetUseItem(who, reqMsg)

	@endPoint.result
	@handleLock
	def rpcPetUpgrade(self, ep, who, reqMsg): return rpcPetUpgrade(who, reqMsg)

	@endPoint.result
	@handleLock
	def rpcPetLearnSkill(self, ep, who, reqMsg): return rpcPetLearnSkill(who, reqMsg)

	@endPoint.result
	@handleLock
	def rpcPetUseSkillBook(self, ep, who, reqMsg): return rpcPetUseSkillBook(who, reqMsg)

	@endPoint.result
	def rpcPetWashReq(self, ep, who, reqMsg): return rpcPetWashReq(who, reqMsg)

	@endPoint.result
	@handleLock
	def rpcPetWash(self, ep, who, reqMsg): return rpcPetWash(who, reqMsg)

	@endPoint.result
	def rpcPetWashReplace(self, ep, who, reqMsg): return rpcPetWashReplace(who, reqMsg)

	@endPoint.result
	@handleLock
	def rpcPetWashLock(self, ep, who, reqMsg): return rpcPetWashLock(who, reqMsg)

	@endPoint.result
	def rpcPetHolyExchange(self, ep, who, reqMsg): return rpcPetHolyExchange(who, reqMsg)

	@endPoint.result
	def rpcPetGet(self, ep, who, reqMsg): rpcPetGet(who, reqMsg)

def checkPet(who, petId):
	'''检查异兽是否存在
	'''
	petObj = who.petCtn.getItem(petId)
	if not petObj:
		message.tips(who, "该异兽不存在")
		return None
	return petObj

def rpcPetRename(who, reqMsg):
	'''宠物改名
	'''
	petId = reqMsg.petId
	nameNew = reqMsg.name
	petObj = checkPet(who, petId)
	if not petObj:
		return
	iLen = calLen(nameNew)
	if iLen > 6:
		message.tips(who, "名字过长，改名失败，请重新输入")
		return
	elif iLen < 2:
		message.tips(who, "异兽名字不能少于#C042个#n字")
		return
	if trie.fliter(nameNew) != nameNew or u.isInvalidText(nameNew):
		message.tips(who, "名字不符合规定，改名失败，请重新输入")
		return
	nameOld = petObj.name
	writeLog("pet/rename", "[%d]%d %s->%s" % (petObj.ownerId, petObj.id, nameOld, nameNew))
	petObj.set("name", nameNew)
	petObj.attrChange("name")
	message.tips(who, "异兽改名成功")
	rank.updatePetScoreRank(who, petObj, False)

def rpcPetFighter(who, reqMsg):
	'''宠物参战或休息
	'''
	petId = reqMsg.petId
	isFighter = reqMsg.fighter
	petObj = checkPet(who, petId)
	if not petObj:
		return
	if not petObj.isCarry():
		message.tips(who, "你并没有携带该异兽")
		return
	if petObj.getLife()<=50:
		message.tips(who, "#C04异兽寿命≤50#n，无法出战")
		return
	if isFighter:  # 参战
		who.petCtn.setFighter(petObj, True)
	else:  # 休息
		who.petCtn.setFighter(petObj, False)
	activity.guaji.rpcPetChange(who)

def rpcPetCarry(who, reqMsg):
	'''宠物携带或取消
	'''
	petId = reqMsg.petId
	isCarry = reqMsg.carry
	petObj = checkPet(who, petId)
	if not petObj:
		return
	if isCarry:  # 携带
		if petObj.getCarryLevel() > who.level:
			message.tips(who, "你的等级未达到携带等级")
			return
		if who.petCtn.carryCount() >= who.petCtn.carrayCountMax():
			who.petCtn.setCarry(petObj, False)
			message.tips(who, "可携带的异兽已达上限，请将部分异兽放下再操作")
			return
		who.petCtn.setCarry(petObj, True)
	else:  # 取消携带
		if who.petCtn.carryCount() <= 1:
			message.tips(who, "至少要携带一只异兽")
			return
		if petObj.isFighter():
			who.petCtn.setFighter(petObj, False)
			activity.guaji.rpcPetChange(who)
		who.petCtn.setCarry(petObj, False)

def rpcPetAttrPointReset(who, reqMsg):
	'''重置属性点
	'''
	petId = reqMsg.iValue
	petObj = checkPet(who, petId)
	if not petObj:
		return
	if petObj.fetch("resetCnt") < 2:
		cnt = petObj.fetch("resetCnt") + 1
		message.confirmBoxNew(who, functor(responsePointReset, petId), "每只异兽一生中前#C04两次#n重置属性是免费的，重置后所有属性点变回潜力点，是否要重置？\nQ取消#20\nQ重置")
		return
	else:
		cnt = petObj.day.fetch("resetCnt") + 1
		cost = petResetCost.getCost(cnt)
		message.confirmBoxNew(who, functor(responsePointReset, petId), "该异兽重置需#IS#n#C07%s#n，是否需要重置？\n（价格每天刷天时重置）\nQ取消#20\nQ重置" % (cost))
		return
	
def responsePointReset(who, yes, petId):
	if not yes:
		return
	petObj = checkPet(who, petId)
	if not petObj:
		return
	if petObj.fetch("resetCnt") < 2: # 免费
		cnt = petObj.fetch("resetCnt") + 1
		writeLog("pet/attrpointreset", "[%d]%d free %d" % (petObj.ownerId, petObj.id, cnt))
		petObj.add("resetCnt", 1)
	else:
		cnt = petObj.day.fetch("resetCnt") + 1
		cost = petResetCost.getCost(cnt)
		if who.cash < cost:
			message.tips(who, "需要%d银币" % cost)
			return
		writeLog("pet/attrpointreset", "[%d]%d cost %d %d" % (petObj.ownerId, petObj.id, cost, cnt))
		who.costCash(cost, "重置宠物属性点")
		petObj.day.add("resetCnt", 1)
	point = 0
	for attr in role.defines.baseAttrList:
		attrPoint = "%sAllot" % attr
		point += petObj.delete(attrPoint, 0)
	petObj.addPoint(point, "重置")
	petObj.refreshAllotAttr(role.defines.baseAttrList)
	petObj.reCalcAttr()
	message.tips(who, "该异兽属性已经重置！")

def rpcPetAttrPointAdd(who, reqMsg):
	'''加属性点
	'''
	petId = reqMsg.petId
	petObj = checkPet(who, petId)
	if not petObj:
		return
	pointList = {}
	for attr in role.defines.baseAttrList:
		val = getattr(reqMsg, attr, 0)
		if val > 0:
			pointList[attr] = val
	pointCost = sum(pointList.values())
	pointTotal = petObj.fetch("point")
	if pointCost <= 0:
		return
	elif pointCost > pointTotal:  # 错误，点数不足！
		message.tips(who, "该异兽潜力点数不足")
		return
	writeLog("pet/attrpointadd", "[%d]%d %d %d%s" % (petObj.ownerId, petObj.id, pointTotal, pointCost, pointList))
	petObj.addPoint(-pointCost, "加点")
	for attr, val in pointList.iteritems():
		petObj.addAttrPoint(attr, val, "加点")
	petObj.reCalcAttr()
	petObj.refreshAllotAttr(pointList.keys())
	message.tips(who, "分配属性点成功")

def rpcPetAttrPointScheme(who, reqMsg):
	'''自动加点方案
	'''
	petId = reqMsg.petId
	petObj = checkPet(who, petId)
	if not petObj:
		return

	#只能是0 1 2 3
	if reqMsg.schemeIndex > 3 or reqMsg.schemeIndex < 0:
		message.tips(who, "自动加点方案不存在")
		return


	pointscheme = {}
	for attr in role.defines.baseAttrList:
		val = getattr(reqMsg, attr, 0)
		if val > 0:
			pointscheme[attr] = val
	pointCost = sum(pointscheme.values())
	if pointCost < 10:
		message.tips(who, "需分配完#C0410点#n属性，才能启用方案")
		return
	writeLog("pet/attrpointscheme", "[%d]%d %d%s" % (petObj.ownerId, petObj.id, pointCost, pointscheme))
	petObj.set("pointscheme", pointscheme)
	petObj.set("schemeIndex", reqMsg.schemeIndex)
	who.endPoint.rpcPetAttrChange(**{"petId": petObj.id, "bAutoPoint":True})
	message.tips(who, "新的自动加点方案启用成功")

def rpcPetAttrPointSchemeRequest(who, reqMsg):
	'''请求自动加点方案
	'''
	petId = reqMsg.iValue
	petObj = checkPet(who, petId)
	if not petObj:
		return
	schemeObj = packPetPointScheme(petObj)
	who.endPoint.rpcPetAttrPointSchemeResponse(schemeObj)

def rpcPetUseItem(who, reqMsg):
	'''宠物使用物品
	'''
	petId = reqMsg.petId
	propsNo = reqMsg.propsNo
	useCnt = reqMsg.useCnt
	if useCnt <= 0:
		return
	petObj = checkPet(who, petId)
	if not petObj:
		return
	
	propsObjList = getPropsByNo(who, propsNo)
	if not propsObjList:
		message.tips(who, "你身上没有此物品")
		return
	
	propsObj = propsObjList[0]
	if propsObj.isExp():
		if not petObj.checkRewardExp("宠物培养"):
			return
		petObj.addExpResult = 0
		tryAddExp(who, petObj, propsObjList, useCnt)
		result = petObj.addExpResult
		del petObj.addExpResult
		message.tips(who, "本异兽增加了#C04{}#n经验".format(result))
	elif propsObj.isLife():
		if not petObj.checkAddLife("宠物培养"):
			return
		petObj.addLifeResult = 0
		tryAddLife(who, petObj, propsObjList, useCnt)
		result = petObj.addLifeResult
		del petObj.addLifeResult
		message.tips(who, "本异兽增加了#C04{}#n寿命".format(result))


def getPropsByNo(who, propsNo):
	'''根据物品编号获取物品
	'''
	propsObjList = []
	propsObjListBinded = []
	for propsObj in who.propsCtn.getPropsGroupByNo(propsNo):
		if propsObj.isBind():
			propsObjListBinded.append(propsObj)
		else:
			propsObjList.append(propsObj)
			
	return propsObjListBinded + propsObjList

def tryAddExp(who, petObj, propsObjList, useCnt):
	'''给异兽增加经验
	'''
	for propsObj in propsObjList:
		effectList = propsObj.getEffect()
		exp = int(effectList["异兽经验"])
		
		while propsObj.stack() > 0:
			if not petObj.checkRewardExp("宠物培养", False):
				return
			who.propsCtn.addStack(propsObj, -1)
			petObj.rewardExp(exp, "宠物培养", None)
			useCnt -= 1
			if useCnt <= 0:
				return

def tryAddLife(who, petObj, propsObjList, useCnt):
	'''给异兽增加寿命
	'''
	if not petObj.checkAddLife("宠物培养"):
		return
		
	petObj.addLifeResult = 0
	for propsObj in propsObjList:
		effectList = propsObj.getEffect()
		life = int(effectList["寿命"])
		
		while propsObj.stack() > 0:
			if not petObj.checkAddLife("宠物培养", False):
				return
			who.propsCtn.addStack(propsObj, -1)
			petObj.addLife(life, "宠物培养", None)
			useCnt -= 1
			if useCnt <= 0:
				return
		

def rpcPetUpgrade(who, reqMsg):
	'''宠物升星
	'''
	petId = reqMsg.iValue
	petObj = checkPet(who, petId)
	if not petObj:
		return
	star = petObj.getStar()
	if star >= 5:
		message.tips(who, "此异兽已是最高星级，不需要再升星")
		return
	if petObj.getCarryLevel(star+1) > who.level:
		message.tips(who, "此异兽下一星级携带等级将大于人物等级，还是迟些日子再来提升吧！")
		return
	# 判断升星道具条件
	costNo,costCnt = petObj.getUpgradeCost(star)
	ownCnt, = who.propsCtn.getPropsAmountByNos(costNo) #返回一个列表,不想用ownCnt[0]获取
	if ownCnt < costCnt:
		message.tips(who, "升星所需#C02固元灵胶#n数量不足")
		return
	who.propsCtn.subPropsByNo(costNo, costCnt, "宠物升星")
	petObj.addStar(1, "升星")
	petObj.reCalcAttr()
	message.tips(who, "升星成功")
	writeLog("pet/starUpgrade", "roleId:%d, petId:%d star:%d->%d" % (petObj.ownerId, petObj.id, star, petObj.getStar()))
	rank.updatePetScoreRank(who, petObj)
	
def rpcPetLearnSkill(who, reqMsg):
	'''宠物学习技能
	'''
	petId = reqMsg.petId
	itemId = reqMsg.itemId
	petObj = checkPet(who, petId)
	if not petObj:
		return
	propsObj = who.propsCtn.getItem(itemId)
	if not itemId or not propsObj or propsObj.kind != props.defines.ITEM_PET_SKILL_BOOK:
		message.tips(who, "请放进技能书")
		return
	skillId = propsObj.getPetSkill()
	if not skillId:
		message.tips(who, "该技能记录的技能不存在")
		return
	elif skillId in petObj.getSkillList():
		message.tips(who, "该异兽已有此技能，不需再学习")
		return
	if propsObj.stack() < 1:
		message.tips(who, "技能书数量不足")
		return
	who.propsCtn.addStack(propsObj, -1)
	oldSkill = pet.business.learnSkill(who, petObj, skillId)
	petObj.reCalcAttr()
	petObj.attrChange("score")
	rank.updatePetScoreRank(who, petObj)
	writeLog("pet/learnSkill", "[%d]%d %d %d->%d" % (petObj.ownerId, petObj.id, itemId, oldSkill, skillId))
	message.tips(who, "学习成功！#C02{}#n被替换为#C02{}#n".format(skill.get(oldSkill).name, skill.get(skillId).name))

def rpcPetUseSkillBook(who, reqMsg):
	petId = reqMsg.petId
	books = reqMsg.books
	petObj = checkPet(who, petId)
	if not petObj:
		return
	iExps = 0
	for book in books:
		propsId = book.propsId
		useCnt = book.useCnt
		if petObj.getSklPoint() < 1:
			message.tips(who, "该异兽已经没有任何潜力")
			return
		if useCnt <= 0:
			continue
		propsObj = who.propsCtn.getItem(propsId)
		if not propsObj or propsObj.kind != props.defines.ITEM_PET_SKILL_BOOK:
			continue
		elif propsObj.stack() < useCnt:
			continue
		skillExp = petWashData.getSkillBookExp(propsObj.no())
		if not skillExp:
			message.tips(who, "错误：该技能书所加经验为0")
			return
		useCnt, val = pet.business.checkSkillBookUseCount(petObj, useCnt, skillExp)
		if not useCnt:
			message.tips(who, "该异兽技能格达到上限了")
			return
		who.propsCtn.addStack(propsObj, -useCnt)
		# 开启新的技能格会随机给一个较差的技能
		petObj.addSklSlotExp(val, "异兽使用技能书", False)
		iExps += val
		iAddSlot = 0
		while pet.business.canAddSkillSlot(petObj):
			petObj.addSklSlotExp(-petObj.getSklSlotExpNxt(), "增加技能格扣除", False)
			petObj.addSklPoint(-1, "增加技能格", False)
			pet.business.addRandomSkill(petObj)
			iAddSlot += 1
		if iAddSlot:
			petObj.reCalcAttr()
			petObj.attrChange("sklSlotExp", "sklSlotExpNxt", "sklPoint", "score", "sklSlotExpAll")
			message.tips(who, "#C02{}#n成功开启#C04{}个#n新技能格".format(petObj.name, iAddSlot))
			rank.updatePetScoreRank(who, petObj)
		else:
			petObj.attrChange("sklSlotExp", "sklSlotExpAll")
		writeLog("pet/useSkillBook", "[%d]%d %d" % (petObj.ownerId, petObj.id, propsId))
	message.tips(who,"#C02{}#n增加#C04{}点#n技能经验".format(petObj.name, iExps))

def rpcPetWashReq(who, reqMsg):
	'''请求洗炼信息
	'''
	petId = reqMsg.petId
	petObj = checkPet(who, petId)
	if not petObj:
		return
	washData = packPetWash(petObj)
	who.endPoint.rpcPetWashResponse(washData)

def rpcPetWash(who, reqMsg):
	'''宠物洗炼
	'''
	petId = reqMsg.petId
	wtype = reqMsg.wash
	petObj = checkPet(who, petId)
	if not petObj:
		return
	if petObj.isHolyPet():
		message.tips(who, "神兽资质极佳，无需洗练")
		return
	if wtype == 1 and not pet.business.isWashed(petObj):
		message.tips(who, "先洗炼获得基本属性，再进行保底洗炼吧！")
		return
	washPropsId = 230103 if petObj.fetch("status") else 230101
	costCnt1 = petObj.getConfig("洗炼消耗")
	washPropsId2 = 230102
	costCnt2 = petObj.getConfig("保底洗炼消耗")
	ownCnt1, ownCnt2 = who.propsCtn.getPropsAmountByNos(washPropsId, washPropsId2) #返回一个列表
	if ownCnt1 < costCnt1:
		message.tips(who, "洗炼道具数量不足，请补足后再洗炼")
		return
	if wtype == 1:
		if ownCnt2 < costCnt2:
			message.tips(who, "#C02择骨丹#n数量不足，请补足后再洗炼")
			return
		who.propsCtn.subPropsByNo(washPropsId2, costCnt2, "宠物洗炼属性")
	who.propsCtn.subPropsByNo(washPropsId, costCnt1, "宠物洗炼属性") # 可能会存在策划要求优先使用绑定物品的BUG
	dWash = pet.business.wash(petObj)
	if wtype == 1: # 保底洗炼先存数据，是否替换由玩家做主
		for k, v in dWash.iteritems():
			petObj.set(k, v)
	else:
		pet.business.updateExtGenDirect(petObj, dWash)
		rank.updatePetScoreRank(who, petObj)
	washData = packPetWash(petObj)
	who.endPoint.rpcPetWashResponse(washData)
	writeLog("pet/wash", "[%d]%d %d %s" % (petObj.ownerId, petObj.id, wtype, dWash))
	message.tips(who, "洗炼成功")

def rpcPetWashReplace(who, reqMsg):
	'''洗炼替换
	'''
	petId = reqMsg.petId
	petObj = checkPet(who, petId)
	if not petObj:
		return
	if not pet.business.hasWashNew(petObj):
		message.tips(who, "没有任何洗炼可替换")
		return
	pet.business.updateExtGen(petObj)
	washData = packPetWash(petObj)
	who.endPoint.rpcPetWashResponse(washData)
	rank.updatePetScoreRank(who, petObj)

def rpcPetWashLock(who, reqMsg):
	'''洗炼加锁，取消加锁edit by peng 20160830
	'''
	petId = reqMsg.petId
	lock = reqMsg.lock
	petObj = checkPet(who, petId)
	if not petObj:
		return
	if not lock:
		message.tips(who, "请选择需要加锁的属性")
		return
	elif len(lock) > 1:
		message.tips(who, "一次只可以锁一个属性")
		return
	if lock[0] > 7 or lock[0] < 0:
		message.debugClientMsg(who, "加锁的参数有误，传了%s上来" % lock[0])
		return
	lockList = petObj.fetch("washLock", [])
	if lock[0] in lockList:
		#该属性已经加锁了，再点表示解锁
		lockList.remove(lock[0])
	else:
		if len(lockList) >= 4:
			message.tips(who, "最多只能锁定#C044个#n属性")
			return
		lCost = petObj.getConfig("锁属性消耗")
		costCnt = lCost[len(lockList)]
		ownCnt, = who.propsCtn.getPropsAmountByNos(230102) #返回一个列表,不想用ownCnt[0]获取
		if ownCnt < costCnt:
			message.tips(who, "#C02锁骨丹#n数量不足，无法锁定")
			return
		who.propsCtn.subPropsByNo(230102, costCnt, "宠物洗炼锁属性") # 可能会存在策划要求优先使用绑定物品的BUG
		lockList.append(lock[0])
		writeLog("pet/washLock", "[%d]%d %s %d" % (petObj.ownerId, petObj.id, lockList, lock[0]))
	petObj.set("washLock", lockList)
	washData = packPetWash(petObj)
	who.endPoint.rpcPetWashResponse(washData)

def rpcPetList(who):
	'''发送宠物列表
	'''
	petDataList = []
	for petObj in who.petCtn.getAllValues():
		petDataList.append(packPetData(petObj))
	
	petList = pet_pb2.petList()
	petList.petDataList.extend(petDataList)
	who.endPoint.rpcPetList(petList)
	
def rpcPetAdd(who, petObj):
	'''增加宠物
	'''
	petData = packPetData(petObj)
	who.endPoint.rpcPetAdd(petData)
	

def packPetData(petObj):
	skillList = [skillId for skillId,skillObj in petObj.getSkillListByOrder()]

	petData = pet_pb2.petData()
	petData.petId = petObj.id
	petData.petAttr.CopyFrom(packPetAttr(petObj))
	petData.skillList.extend(skillList)
	return petData

def packPetPointScheme(petObj):
	pointScheme = pet_pb2.points()
	scheme = petObj.fetch("pointscheme", {})
	pointScheme.petId = petObj.id
	pointScheme.con = scheme.get("con", 0)
	pointScheme.mag = scheme.get("mag", 0)
	pointScheme.str = scheme.get("str", 0)
	pointScheme.res = scheme.get("res", 0)
	pointScheme.spi = scheme.get("spi", 0)
	pointScheme.dex = scheme.get("dex", 0)
	pointScheme.schemeIndex = petObj.fetch("schemeIndex", 0)
	return pointScheme

def packPetAttr(petObj):
	attrNameList = ["idx", "shape", "name", "level", "exp", "expNext", "star", "fighter", "carry", "score",
				"sklSlotExp", "sklSlotExpNxt", "sklSlotExpAll", "status", "hp", "hpMax", "mp", "mpMax", "phyDam", "magDam",
				"phyDef", "magDef", "spe", "phyCrit", "magCrit", "phyReCrit", "magReCrit", "con", "mag", "str",
				"res", "spi", "dex", "conAllot", "magAllot", "strAllot", "resAllot", "spiAllot", "dexAllot",
				"point", "life", "sklPoint", "hpGen", "phyAttGen", "magAttGen", "phyDefGen", "magDefGen", "speGen",
				"hpGenExt", "phyAttGenExt", "magAttGenExt", "phyDefGenExt", "magDefGenExt", "speGenExt", "defaultPerform"]
	petAttr = pet_pb2.petAttr()
	for attrName in attrNameList:
		setattr(petAttr, attrName, petObj.getValByName(attrName))
	# 以下属性比较特殊的另外设置
	petAttr.petId = petObj.id
	petAttr.shapeParts.extend(petObj.shapeParts)
	petAttr.colors.extend(petObj.getColors())
	petAttr.grow = "%.2f" % petObj.getValByName("grow")
	petAttr.growExt = "%.2f" % petObj.getValByName("growExt")
	petAttr.bAutoPoint = True if petObj.fetch("pointscheme") else False
	return petAttr

def packPetAttr4Hyperlink(petObj):
	return packPetAttr(petObj)

def packet4Hyperlink(petObj):
	skillList = [skillId for skillId,skillObj in petObj.getSkillListByOrder()]
	petData = pet_pb2.petData()
	petData.petId = petObj.id
	petData.petAttr.CopyFrom(packPetAttr4Hyperlink(petObj))
	petData.skillList.extend(skillList)
	return petData

def packPetWash(petObj):
	attrNameList = ["hpGenWashNew", "phyAttGenWashNew", "magAttGenWashNew", "phyDefGenWashNew",
					"magDefGenWashNew", "speGenWashNew", "sklPointWashNew"]
	washData = pet_pb2.petWash()
	for attrName in attrNameList:
		setattr(washData, attrName, petObj.getValByName(attrName))
	washData.petId = petObj.id
	return washData

def rpcPetHolyExchange(who,reqMsg): #兑换神兽
	petId = reqMsg.iValue
	propsNo,amount = petExchangeInfo(petId)
	
	if amount > who.propsCtn.getPropsAmountByNos(propsNo)[0]:
		message.tips(who, "道具数量不够无法兑换")
		return
	if who.petCtn.hasPetByIdx(petId):
		message.tips(who, "你已拥有此神兽，不能重复获得")
		return
	if who.petCtn.itemCount() >= who.petCtn.itemCountMax():
		message.tips(who, "玩家身上的宠物满了 不能在增加了")
		return
	petObj = pet.new(petId,0)
	who.propsCtn.subPropsByNo(propsNo, amount, "兑换神兽")
	petObj = pet.addPet(who, petObj)
	if who.petCtn.carryCount() < who.petCtn.carrayCountMax():
		who.petCtn.setCarry(petObj, True)#携带宠物
	openUIPanel.openPetRewardUi(who, petObj.id)
	sTips = '''#C01$player#n使用#C02$props#n，在#L1<true,3015>*[宝相夫人]*02#n处兑换了千年难遇的神兽#C01$petgod#n！恭喜#C01$player#n又多一卓越战力，修行之路必定更加顺畅！'''
	sTips = sTips.replace("$player", who.name)
	sTips = sTips.replace("$props", propsData.getConfig(propsNo,"名称"))
	sTips = sTips.replace("$petgod", petObj.name)
	message.sysMessageRoll(sTips)
	
def petExchangeInfo(petId):
	needList =  holyPetExchangeData.getConfig(petId)
	return needList["物品编号"],needList["消耗"]

def rpcPetGet(who, reqMsg): #前往领取宠物
	petId = reqMsg.iValue
	if task.hasTask(who, task.pett.PET_TASK_PARENTID):
		message.tips(who, "异兽任务尚未完成，还是先完成任务吧")
		return
	if who.petCtn.hasPetByIdx(petId):
		message.tips(who, "你已获得该异兽，无法再次前往接取任务")
		return
	petObj = pet.new(petId,0)
	if not petObj:
		return
	if petObj.isHolyPet():
		npcObj = npc.getNpcByIdx(10213)
		if not npcObj:
			return
		scene.walkToEtt(who, npcObj)
		return
	lvKeys,groupTask = task.pett.getPetGroupTask()
	if not lvKeys or not groupTask:
		return
	taskLv = 0
	for lv in groupTask:
		for info in groupTask[lv]:
			if info["宠物编号"] == petId:
				taskLv = lv
				break
		if taskLv != 0:
			break
	if taskLv > who.level:
		message.tips(who, "你尚未达到接取该异兽任务的等级")
		return
	task.goAhead(who.id, 50000)

from common import *
import message
import trie
import pet
import role
import petResetCost
import pet.business
import props.defines
import skill
import activity.guaji
import rank
import u
import petWashData
import holyPetExchangeData
import openUIPanel
import propsData
import task
import npcData
import scene
import npc