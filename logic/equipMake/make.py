# -*- coding: utf-8 -*-
'''
打造属性生成
'''
#=============================================================================
#属性生成
#=============================================================================
def creatAddAttr(oEquip):
	'''#生成附加属性
读取“装备表”对应装备的“附加属性”字段
几率	第一属性	第二属性
80%	50%,100%	0
20%	35%,70%	35%,70%
	'''
	iAdd = oEquip.getConfig("附加属性",0)
	if not iAdd:
		return {}
	dAdd  = {}
	iRand = common.rand(1,100)
	lAttr = role.defines.baseAttrList
	if iRand<=80:
		sType  = lAttr[common.rand(len(lAttr))]
		iValue = iAdd * common.rand(50,100) / 100
		dAdd[sType] = max(iValue,1)
	else:
		lType = common.shuffleList(lAttr, 2)
		for sType in lType:
			iValue = iAdd * common.rand(35,70) / 100
			dAdd[sType] = max(iValue,1)
	return dAdd

def creatBaseAttr(oEquip):
	'''#生成基础属性
	二级属性属性值 = 导表属性值 * randint(90,110)/100
	'''
	dBase = {}
	for sType,sValue in  role.defines.attrDescList.iteritems():
		iValue = oEquip.getConfig(sValue,0)
		if not iValue:
			continue
		iValue = iValue * common.rand(90, 110) / 100
		dBase[sType] = iValue
	# 攻击力字段特殊 治疗数值是攻击力的一半，物攻=法攻=攻击力
	iAttack = oEquip.getConfig("攻击力",0)
	if iAttack:
		iAttack = iAttack * common.rand(90, 110) / 100
		dBase["phyDam"] = dBase["magDam"] = max(iAttack,1)
		dBase["cure"] = max(iAttack/2,1)
	return dBase

def creatFive(oEquip):
	'''生成五行属性,0没有1无2金3木4水5火6土
	'''
	if oEquip.wearPos() in (props.defines.EQUIP_WEAPON, props.defines.EQUIP_CLOTHES):
		return common.rand(1, 6)
	else:
		return 0

def createSpecialEffect(oEquip):
	'''生成特效
	'''
	iRate = common.rand(1, 100)
	if iRate > 10:
		return 0
	lSes = sesksData.getSpecialEffects(oEquip.level, oEquip.wearPos())
	lChoose = common.shuffleList(lSes, 1)
	return lChoose[0]

def createSpecialSkill(oEquip):
	'''生成特技
	'''
	iRate = common.rand(1, 100)
	if iRate > 10:
		return 0
	lSks = sesksData.getSpecialSkills(oEquip.level, oEquip.wearPos())
	lChoose = common.shuffleList(lSks, 1)
	return lChoose[0]

def checkMaterial(who, dMaterial):
	'''检查拥有与缺少的材料
	'''
	dLack = {}
	dOwn = {}
	for iPropsId, iAmount in dMaterial.iteritems():
		sType = propsData.getConfig(iPropsId, "类型")
		if sType == "制造符":
			lCompatible = equipMake.defines.getUpPropsNo(iPropsId)
			iTemp = iAmount
			for iCompatId in lCompatible:
				iOwn = who.propsCtn.getPropsAmountByNos(iCompatId)[0]
				iNeed = min(iOwn, iTemp)
				if iNeed > 0:
					iTemp -= iNeed
					dOwn[iCompatId] = iNeed
				if iTemp <= 0:
					break
			if iTemp > 0:
				dLack[iPropsId] = iTemp
		else:
			iOwn = who.propsCtn.getPropsAmountByNos(iPropsId)[0]
			if iOwn < iAmount:
				dLack[iPropsId] = iAmount - iOwn
				if iOwn > 0:
					dOwn[iPropsId] = iOwn
			else:
				dOwn[iPropsId] = iAmount
	return dLack, dOwn

def checkEquipMake(who, dMaterial):
	'''检查装备打造材料
	'''
	dLack, dOwn = checkMaterial(who, dMaterial)
	if not dLack:
		return 0, dOwn, {}
	iCost = 0
	for iPropsId, iAmount in dLack.iteritems():
		sType = propsData.getConfig(iPropsId, "类型")
		iLevel = propsData.getConfig(iPropsId, "等级")
		ctype, price = trade.getGoodsPrice(iPropsId)
		if sType == "模具":
			iPrice = price
		elif sType == "五金之精":
			iPrice = price / 100
		elif sType == "制造符":
			iPrice = price
		iCost += iPrice * iAmount
	return iCost, dOwn, dLack

def makeEquip(iNo):
	'''给装备生成打造属性
	'''
	oEquip = props.create(iNo)
	if not oEquip:
		return None
	if oEquip.kind != props.defines.ITEM_EQUIP:
		return None
	dArgs = {}
	dArgs["isMake"] = 1
	dArgs["baseAttr"] = creatBaseAttr(oEquip)
	dArgs["addAttr"] = creatAddAttr(oEquip)
	if oEquip.wearPos() in (props.defines.EQUIP_WEAPON, props.defines.EQUIP_CLOTHES):
		dArgs["fiveEl"] = creatFive(oEquip)
	iSe = createSpecialEffect(oEquip)
	iSk = createSpecialSkill(oEquip)
	if iSe:
		dArgs["spEffect"] = iSe
	if iSk:
		dArgs["spSkill"] = iSk
	oEquip.onBorn(**dArgs)
	return oEquip

def packEquipInfo(oEquip):
	'''打包装备的打造属性信息
	'''
	equipInfo = equipMake_pb2.equipInfo()
	equipInfo.iPropsId = oEquip.id
	equipInfo.iNo = oEquip.no()
	for k, v in oEquip.fetch("baseAttr", {}).iteritems():
		setattr(equipInfo, k, v)
	for k, v in oEquip.fetch("addAttr", {}).iteritems():
		setattr(equipInfo, k, v)
	iFive = oEquip.fiveEl
	spEffect = oEquip.fetch("spEffect")
	spSkill = oEquip.fetch("spSkill")
	if iFive:
		equipInfo.fiveAttr = iFive
	if spEffect:
		equipInfo.spEffect = spEffect
	if spSkill:
		equipInfo.spSkill = spSkill
	return equipInfo

def packEquipMakeInfo(oTemplate):
	'''打包装备的打造消耗信息
	'''
	dMaterial = oTemplate.getConfig("打造材料", {})
	if not dMaterial:
		return None
	makeInfo = equipMake_pb2.makeInfo()
	makeInfo.equipNo = oTemplate.no()
	materialList = []
	for iNo, iAmount in dMaterial.iteritems():
		sType = propsData.getConfig(iNo, "类型")
		iLevel = propsData.getConfig(iNo, "等级")
		ctype, price = trade.getGoodsPrice(iNo)
		iCashType = 1
		if sType == "模具":
			iPrice = price
		elif sType == "五金之精":
			iPrice = price
			iCashType = 0
		elif sType == "制造符":
			iPrice = price
		materialInfo = equipMake_pb2.materialInfo()
		materialInfo.iNo = iNo
		materialInfo.iAmount = iAmount
		materialInfo.iCashType = iCashType
		materialInfo.iCash = iPrice
		materialList.append(materialInfo)
	makeInfo.materials.extend(materialList)
	return makeInfo


import equipMake_pb2
import common
import props
import props.defines
import role.defines
import equipMake.defines
import sesksData
import propsData
import trade
