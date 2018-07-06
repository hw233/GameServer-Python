# -*- coding: utf-8 -*-
'''
打造服务
'''
import endPoint
import equipMake_pb2

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

class cService(equipMake_pb2.terminal2main):
	@endPoint.result
	def rpcEquipMakeInfoReq(self, ep, who, reqMsg): return rpcEquipMakeInfoReq(who, reqMsg)

	@endPoint.result
	def rpcEquipMakeReq(self, ep, who, reqMsg): return rpcEquipMakeReq(who, reqMsg)

	@endPoint.result
	def rpcEquipRecastAttr(self, ep, who, reqMsg): return equipMake.recast.rpcEquipRecastAttr(who, reqMsg)

	@endPoint.result
	@handleLock
	def rpcEquipRecast(self, ep, who, reqMsg): return equipMake.recast.rpcEquipRecast(who, reqMsg)

	@endPoint.result
	def rpcEquipRecastReplace(self, ep, who, reqMsg): return equipMake.recast.rpcEquipRecastReplace(who, reqMsg)

	@endPoint.result
	def rpcGemInfoReq(self, ep, who, reqMsg): return rpcGemInfoReq(who, reqMsg)

	@endPoint.result
	def rpcAddGem(self, ep, who, reqMsg): return rpcAddGem(who, reqMsg)#镶嵌宝石

	@endPoint.result
	@handleLock
	def rpcRemoveGem(self, ep, who, reqMsg): return rpcRemoveGem(who, reqMsg)#从装备取出宝石

	@endPoint.result
	def rpcEquipRepaired(self, ep, who, reqMsg): return rpcEquipRepaired(who, reqMsg)#从装备取出宝石


def equipMakeInfo(who, equipNo):
	oTemplate = props.getCacheProps(equipNo)
	if not oTemplate:
		message.tips(who, "没有该装备的打造信息")
		return
	packData = make.packEquipMakeInfo(oTemplate)
	if not packData:
		return
	who.endPoint.rpcEquipMakeInfoResponse(packData)

def gemInfo(who):
	gemMsg = equipMake_pb2.gemInfo()
	gems = []
	for i in xrange(10):
		iNo = 246001 + i
		iCashType, iCash = trade.getGoodsPrice(iNo)
		msg = equipMake_pb2.materialInfo()
		msg.iNo = iNo
		msg.iCash = iCash
		msg.iCashType = iCashType - 1
		gems.append(msg)
	gemMsg.gems.extend(gems)
	who.endPoint.rpcGemInfoResponse(gemMsg)

def rpcGemInfoReq(who, reqMsg):
	'''宝石售价信息
	'''
	gemInfo(who)

def rpcAddGem(who, reqMsg):
	'''镶嵌宝石
	'''
	iEquipId=reqMsg.iEquipId
	iHoleNo=reqMsg.iHoleNo
	iGemNo=reqMsg.iGemNo #要镶嵌的宝石类型
	pid = who.id
	if not 1<=iHoleNo<=2:
		message.tips(who, "宝石孔休眠中，请重新操作")
		return
	oEquip=who.propsCtn.getItem(iEquipId)
	if not oEquip:
		oEquip = who.equipCtn.getItem(iEquipId)
		if not oEquip:
			message.tips(who, "装备不存在")
			return
	oTemplate = props.getCacheProps(iGemNo)
	if not oTemplate:
		message.tips(who, "不存在此类宝石")
		return
	if not iGemNo in oEquip.getConfig("镶嵌宝石", []):
		message.tips(who, "此装备不能镶嵌该宝石")
		return
	if oEquip.level < 60 and iHoleNo > 1:
		message.tips(who, "装备#C04≥60级#n可开启第二个宝石孔")
		return
	#宝石不可以镶到这件装备
	iGemNo2,iAmount=oEquip.getGemInfo(iHoleNo)#返回两个0表示此孔没有宝石
	if iGemNo2!=0 and iGemNo!=iGemNo2:#与已镶上的宝石不相同
		message.tips(who, "此宝石孔已镶嵌了宝石，请卸下后再更换")
		return
	if iAmount==0:
		iCurLevel=0
	else:
		iCurLevel=int(round(math.log(iAmount,2)))+1
	if iCurLevel >= int(oEquip.level / 10) + 1:
		message.tips(who, "此装备能镶嵌该宝石的等级已达上限，无法镶嵌")
		return
	iNeedAmount=2**iCurLevel-iAmount #下一级所需数量
	iHave, =who.propsCtn.getPropsAmountByNos(iGemNo) # 返回的是一个列表
	if iHave<iNeedAmount:
		ctype, price = trade.getGoodsPrice(iGemNo)
		count = iNeedAmount - iHave
		iCash = count * price
		if ctype == 1:
			if not money.checkCash(who, iCash):
				return
			who = getRole(pid)
			if not who:
				return
			who.addCash(-iCash, "镶嵌银币兑换宝石消耗", None)
		elif ctype == 2:
			if not money.checkTradeCash(who, iCash):
				return
			who = getRole(pid)
			if not who:
				return
			who.addTradeCash(-iCash, "镶嵌元宝兑换宝石消耗", None)
		who.propsCtn.subtractPropsByNo(iGemNo, iHave, "镶进装备", None)
		trade.wave(iGemNo, price, count)
	else:
		who.propsCtn.subtractPropsByNo(iGemNo,iNeedAmount,"镶进装备", None)
	oEquip.addGem(iHoleNo,iGemNo,iNeedAmount)
	if iCurLevel == 0:
		message.tips(who, "成功镶嵌#C02{}#n".format(oTemplate.name))
	else:
		message.tips(who, "#C02{}#n等级#C04+1#n".format(oTemplate.name))
	# 如果是已穿戴装备，要刷新角色属性
	if oEquip.isWear():
		oEquip.refreshApply(who)
		who.endPoint.rpcModEquip(oEquip.getMsg4Item(who.equipCtn,"gem", "score"))
	else:
		who.endPoint.rpcModProps(oEquip.getMsg4Package(who.propsCtn,"gem", "score"))
	rpcGemInfoReq(who, None)

def rpcRemoveGem(who, reqMsg):
	'''从装备取出宝石
	'''
	iEquipId=reqMsg.iEquipId
	iHoleNo=reqMsg.iHoleNo
	if not 1<=iHoleNo<=2:
		message.tips(who, "宝石孔非法")
		return
	oEquip=who.propsCtn.getItem(iEquipId)
	if not oEquip:
		oEquip = who.equipCtn.getItem(iEquipId)
		if not oEquip:
			message.tips(who, "装备不存在")
			return
	iGemNo,iAmount=oEquip.getGemInfo(iHoleNo)
	if iGemNo==0 or iAmount==0:
		message.tips(who, "客户端异常,装备并没有镶嵌着宝石")
		return
	oTemplate = props.getCacheProps(iGemNo)
	if not oTemplate:
		message.tips(who, "不存在此类宝石")
		return
	iMaxStack=props.getCacheProps(iGemNo).maxStack()#宝石最大叠加数量
	iNeedGrid=int(math.ceil(iAmount / float(iMaxStack)))
	if iNeedGrid>who.propsCtn.leftCapacity():#包裹空间不足了,无法存放取出的全部宝石
		message.tips(who, "背包空间不足，为避免宝石丢失，请先整理后再拆卸")
		return
	iGemNo,iAmount=oEquip.removeGem(iHoleNo)
	oGem=props.new(iGemNo)
	oGem.setStack(iAmount)
	oGem.bind() # 卸下的宝石绑定，不能出售
	# launch.launchProps(who, oGem, '从装备取下', None)不走投放接口
	who.endPoint.rpcAddPropsFlash(oGem.getMsg4Package(None,*oGem.MSG_FIRST))
	who.addProps(who.propsCtn, oGem, "从装备取下")
	message.tips(who, "拆卸成功，获得#C02{}×{}#n".format(oTemplate.name, iAmount))
	# 如果是已穿戴装备，要刷新角色属性
	if oEquip.isWear():
		oEquip.refreshApply(who)
		who.endPoint.rpcModEquip(oEquip.getMsg4Item(who.equipCtn,"gem", "score"))
	else:
		who.endPoint.rpcModProps(oEquip.getMsg4Package(who.propsCtn,"gem", "score"))

def rpcEquipMakeInfoReq(who, reqMsg):
	'''装备打造信息请求
	'''
	equipNo = reqMsg.equipNo
	equipMakeInfo(who, equipNo)

def rpcEquipMakeReq(who, reqMsg):
	'''打造请求
	'''
	pid = who.id
	equipNo = reqMsg.equipNo
	makeType = reqMsg.makeType
	if not makeType in (0, 1):
		message.tips(who, "非法打造方式")
		return
	oTemplate = props.getCacheProps(equipNo)
	if not oTemplate:
		message.tips(who, "该装备不存在，无法打造")
		return
	elif oTemplate.level < 40:
		message.tips(who, "低于#C0440级#n的装备无法打造")
		return
	elif oTemplate.level > int(who.level / 10 + 1) * 10:
		message.tips(who, "装备等级超过当前可打造的最高等级，无法打造")
		return
	if who.propsCtn.leftCapacity() < 1:
		message.tips(who, "背包已满，无法打造，请先清理背包")
		return
	dMaterial = oTemplate.getConfig("打造材料", {})
	iMoney, dOwn, dLack = make.checkEquipMake(who, dMaterial)
	if makeType == 0:
		# 普通打造，检查打造所需材料
		if iMoney:
			message.tips(who, "材料不足，无法打造")
			return
	elif makeType == 1:
		# 快捷打造，检查打造所需材料和元宝
		if not money.checkTradeCash(who, iMoney):
			return
	else:
		return
	who = getRole(pid)
	if not who:
		return
	# 扣除打造消耗材料或元宝
	for iNo, iAmount in dOwn.iteritems():
		if not iAmount:
			continue
		who.propsCtn.subtractPropsByNo(iNo, iAmount, "打造消耗", None)
	if iMoney:
		who.addTradeCash(-iMoney, "快捷打造消耗", None)
		for iPropsId, iAmount in dLack.iteritems():
			ctype, price = trade.getGoodsPrice(iPropsId)
			trade.wave(iPropsId, price, iAmount)
	# 生成装备随机属性
	oEquip = make.makeEquip(equipNo)
	# 加到玩家背包
	launch.launchProps(who, oEquip, "装备打造", None)
	packData = make.packEquipInfo(oEquip)
	who.endPoint.rpcEquipMakeResponse(packData)
	message.tips(who, "打造成功，获得#C02{}×1#n".format(oEquip.name))
	equipMakeInfo(who, equipNo)
	
	import listener
	listener.doListen("打造装备", who, propsNo=oEquip.no(), propsId=oEquip.id)

def rpcEquipRepaired(who, reqMsg):
	'''装备修理
	'''
	iType,iEquipId = reqMsg.iType,reqMsg.iEquipId

	iCost,dEquipLife,sTips = getCost4Repaired(who,iType,iEquipId)

	if not iCost:
		return
	if not money.checkCash(who,iCost):
		return

	lEquip = []
	for iEquipId,iLife in dEquipLife.iteritems():
		oEquip = who.equipCtn.getItem(iEquipId)
		if not oEquip:
			oEquip = who.propsCtn.getItem(iEquipId)
			if not oEquip:
				return
		if oEquip.getLife() != iLife:
			return
		lEquip.append(oEquip)

	who.addCash(-iCost,"装备修理",None)
	for oEquip in lEquip:
		oEquip.recoverLife()
	who.endPoint.rpcEquipRepairedSuccess(iEquipId=dEquipLife.keys())
	message.tips(who,sTips)

def getCost4Repaired(who,iType,iEquipId):
	iCost = 0
	dEquipLife = {}
	sTips = ""
	if iType == 1:#全部
		for iPropsId,oProps in who.propsCtn.getAllItems():
			if oProps.kind != props.defines.ITEM_EQUIP:
				continue
			dEquipLife[iPropsId] = oProps.getLife()
			iCost += oProps.lifeRepairPrice()

		for oProps in who.equipCtn.getAllWearEquip():
			dEquipLife[oProps.id] = oProps.getLife()
			iCost += oProps.lifeRepairPrice()
		sTips = "花费#R<{},3,2>#n修理全部装备".format(iCost)
	elif iType == 2: #修理身上的
		for oProps in who.equipCtn.getAllWearEquip():
			dEquipLife[oProps.id] = oProps.getLife()
			iCost += oProps.lifeRepairPrice()
		sTips = "花费#R<{},3,2>#n修理所有已穿戴的装备".format(iCost)
	elif iType == 3: #修理某一件
		oEquip = who.equipCtn.getItem(iEquipId)
		if not oEquip:
			oEquip = who.propsCtn.getItem(iEquipId)
		if oEquip:
			iCost += oEquip.lifeRepairPrice()
			dEquipLife[oEquip.id] = oEquip.getLife()
			sTips = "花费#R<{},3,2>#n修理#C02{}#n".format(iCost,oEquip.name)

	return iCost,dEquipLife,sTips


import math
import message
import props
import launch
import make
import money
from common import *
import props.defines
import equipMake.recast
import trade
