# -*- coding: utf-8 -*-
'''
染色服务
'''
import endPoint
import dye_pb2
from role.defines import *

glRoleDyeList = [SHAPE_PART_TYPE_HAIR, SHAPE_PART_TYPE_CLOTHES, SHAPE_PART_TYPE_HAT]#角色可染色部位列表

class cService(dye_pb2.terminal2main):
	@endPoint.result
	def rpcRoleDyeSchemeReq(self, ep, who, reqMsg): return rpcRoleDyeSchemeReq(who, reqMsg)

	@endPoint.result
	def rpcRoleDye(self, ep, who, reqMsg): return rpcRoleDye(who, reqMsg)

	@endPoint.result
	def rpcPetDye(self, ep, who, reqMsg): return rpcPetDye(who, reqMsg)

	@endPoint.result
	def rpcRideDye(self, ep, who, reqMsg): return rpcRideDye(who, reqMsg)

	@endPoint.result
	def rpcRoleDyeSaveScheme(self, ep, who, reqMsg): return rpcRoleDyeSaveScheme(who, reqMsg)

	@endPoint.result
	def rpcRoleDyeDelScheme(self, ep, who, reqMsg): return rpcRoleDyeDelScheme(who, reqMsg)

	@endPoint.result
	def rpcRoleDyeUseScheme(self, ep, who, reqMsg): return rpcRoleDyeUseScheme(who, reqMsg)


def isSameScheme(shapeParts1, scheme1, shapeParts2, scheme2):
	for part in glRoleDyeList:
		color1 = scheme1.get(part)
		color2 = scheme2.get(part)
		if shapeParts1 == shapeParts2:
			if color1 != color2:
				return False
		else:
			part1 = shapeParts1.get(part)
			part2 = shapeParts2.get(part)
			if part1 != part2:
				return False
			elif color1 != color2:
				return False
	return True

def checkDyeScheme(who, scheme):
	'''检测指定方案是否保存过
	'''
	dyeScheme = who.fetch("dyeScheme", {})
	shapeParts = who.fetch("shapeParts", {})
	if not dyeScheme:
		return None
	for iNo, (fashionNo, dyeInfo) in dyeScheme.iteritems():
		fashion = who.fashionCtn.getFashion(fashionNo)
		if not fashion:
			raise Exception, "染色方案对应的时装{}不存在".format(fashionNo)
		shapeParts2 = fashion.fetch("parts")
		if isSameScheme(shapeParts, scheme, shapeParts2, dyeInfo):
			return iNo
	return None

def isSchemeOne(who, scheme):
	'''是否是默认的方案一
	'''
	for schemeNo in scheme.itervalues():
		if schemeNo:
			return False
	return True

def subDyeProps(who, dProps, iCash):
	'''扣除染色材料
	'''
	for iPropsId, cnt in dProps.iteritems():
		who.propsCtn.subtractPropsByNo(iPropsId, cnt, "染色消耗", None)
	if iCash:
		who.addCash(-iCash, "染色消耗", None)

def checkDyeProps(who, dProps):
	'''检查染色材料是否足够
	'''
	for iPropsId, cnt in dProps.iteritems():
		iOwn = who.propsCtn.getPropsAmountByNos(iPropsId)[0]
		if iOwn < cnt:
			return False
	return True

def doSub(who, dProps, iCash):
	'''检查并扣除消耗
	'''
	if iCash > 0:
		if not money.checkCash(who, iCash):
			message.tips(who, "染色材料不足，不能染色哦")
			return False
		who = getRole(pid)
		if not who:
			return False
	if not checkDyeProps(who, dProps):
		message.tips(who, "染色材料不足，不能染色哦")
		return False
	subDyeProps(who, dProps, iCash)
	return True

def getSaveSchemeCost(who, scheme):
	shapeParts = who.fetch("shapeParts", {}) # 只能用fetch，用属性取可能会取得变身部位
	curParts = transToShapePartList(shapeParts) # 当前部位方案
	iCost, iShape = 0, who.shape
	for part, schemeNo in scheme.iteritems():
		suit = curParts[part]
		tKey = (iShape, part+1, suit, schemeNo)
		if tKey in dyeData.gdData:
			iCost += dyeData.getConfig(tKey, "保存方案消耗")
	return iCost

def rpcRoleDyeSchemeReq(who, reqMsg):
	'''请求角色保存的染色方案
	'''
	rpcRoleDyeSchemeResponse(who)

def rpcRoleDyeSaveScheme(who, reqMsg):
	'''请求保存染色方案
	dyeScheme==>{1:(时装号,颜色字典),2:,3:,4:,5:,6:}总共可保存6套，方案号递增
	'''
	dyeScheme = who.fetch("dyeScheme", {})
	if len(dyeScheme) >=6:
		message.tips(who, "最多只能保存6套方案")
		return
	scheme = copy.copy(who.fetch("colors", {}))
	if isSchemeOne(who, scheme):
		message.tips(who, "你还没染色，没有方案可以保存哦")
		return
	if checkDyeScheme(who, scheme):
		message.tips(who, "当前方案已经保存过了")
		return
	iCost, pid = getSaveSchemeCost(who, scheme), who.id
	if iCost > 0:
		if not money.checkCash(who, iCost):
			message.tips(who, "#IS#n不足，不能保存此方案哦")
			return
		who = getRole(pid)
		if not who:
			return
		who.addCash(-iCost, "保存染色方案消耗", None)
	schemeNos = dyeScheme.keys()
	schemeNos.sort()
	schemeNo = 1 if len(schemeNos) < 1 else schemeNos[-1] + 1
	fashionNo = who.fashionCtn.getCurFashionNo()
	dyeScheme.update({schemeNo:(fashionNo, scheme)})
	who.set("dyeScheme", dyeScheme)
	rpcRoleDyeSchemeResponse(who)

def rpcRoleDyeDelScheme(who, reqMsg):
	'''删除保存的染色方案
	'''
	dyeInfo = reqMsg.dyeInfo
	schemeNo = reqMsg.schemeNo
	dyeScheme = who.fetch("dyeScheme", {})
	if schemeNo not in dyeScheme:
		message.tips(who, "该方案还未保存")
		return
	dyeScheme.pop(schemeNo)
	who.set("dyeScheme", dyeScheme)
	rpcRoleDyeSchemeResponse(who)

def rpcRoleDyeUseScheme(who, reqMsg):
	'''使用保存的染色方案染色
	'''
	dyeInfo = reqMsg.dyeInfo
	schemeNo = reqMsg.schemeNo
	dyeScheme = who.fetch("dyeScheme", {})
	if schemeNo not in dyeScheme:
		message.tips(who, "该方案还未保存")
		return
	scheme = dyeScheme[schemeNo]
	fashionNo = scheme[0]
	colors = scheme[1]
	fashion = who.fashionCtn.getFashion(fashionNo)
	if not fashion:
		raise Exception, "染色方案对应的时装{}不存在".format(fashionNo)
	shapeParts = fashion.fetch("parts")
	if isSameScheme(shapeParts, colors, who.fetch("shapeParts"), who.fetch("colors")):
		message.tips(who, "染色方案和现有相同，不用再染了哦")
		return
	pid, iShape, iCash, dProps = who.id, who.shape, 0, {}
	for idx, color in colors.iteritems():
		tKey = (iShape, idx+1, shapeParts[idx], color)
		dCost = dyeData.getConfig(tKey, "方案染色材料", {})
		for propsId, cnt in dCost.iteritems():
			if propsId == 200001:
				iCash += cnt
			else:
				iSum = dProps.setdefault(propsId, 0)
				dProps[propsId] = iSum + cnt
	if not doSub(who, dProps, iCash):
		return
	who.setColors(colors)
	if shapeParts != who.fetch("shapeParts", {}):
		who.set("shapeParts", shapeParts)
		who.attrChange("shapeParts")
		resume.updateResume(who)
	who.fashionCtn.switchFashion(fashionNo, shapeParts, colors)
	message.tips(who, "你成功染色，快出去让小伙伴们见识一下吧！")
	who.endPoint.rpcDyeDone()

def rpcRoleDye(who, reqMsg):
	'''请求角色染色
	'''
	shapeParts = who.fetch("shapeParts", {}) # 只能用fetch，用属性取可能会取得变身部位
	curParts = transToShapePartList(shapeParts) # 当前部位方案
	curColors = who.getColors() # 当前颜色方案
	dyeInfo = reqMsg.dyeInfo
	dyeLen = len(dyeInfo)
	if dyeLen < 1:
		return
	sameScheme = 0
	pid, iShape, iCash, dProps, dChange = who.id, who.shape, 0, {}, {}
	for dyeMsg in dyeInfo:
		if dyeMsg.color == curColors[dyeMsg.key-1]:
			sameScheme += 1
			continue
		part = dyeMsg.key
		color = dyeMsg.color
		suit = dyeMsg.suit
		dChange[part-1] = color
		tKey = (iShape, part, suit, color)
		dCost = dyeData.getConfig(tKey, "染色材料", {})
		for propsId, cnt in dCost.iteritems():
			if propsId == 200001:
				iCash += cnt
			else:
				iSum = dProps.setdefault(propsId, 0)
				dProps[propsId] = iSum + cnt
	if sameScheme == dyeLen:
		message.tips(who, "染色方案和现有相同，不用再染了哦")
		return
	if not doSub(who, dProps, iCash):
		return
	who.setColors(dChange)
	fashionNo = who.fashionCtn.getCurFashionNo()
	who.fashionCtn.updateFashion(fashionNo, shapeParts, dChange)
	message.tips(who, "你成功染色，快出去让小伙伴们见识一下吧！")
	who.endPoint.rpcDyeDone()

def rpcPetDye(who, reqMsg):
	'''请求异兽染色
	'''
	petId = reqMsg.petId
	schemeNo = reqMsg.schemeNo
	petObj = who.petCtn.getItem(petId)
	if not petObj:
		message.tips(who, "该异兽不存在")
		return
	if not isinstance(schemeNo, int):
		message.tips(who, "染色方案应该是个整型")
		return
	if petObj.getColors()[1] == schemeNo:
		message.tips(who, "染色方案和现有相同，不用再染了哦")
		return
	pid, iCash, dProps = who.id, 0, {}
	dCost = dyeData.getConfig((petObj.shape, 2, 1, schemeNo), "染色材料")
	for propsId, cnt in dCost.iteritems():
		if propsId == 200001:
			iCash += cnt
		else:
			iSum = dProps.setdefault(propsId, 0)
			dProps[propsId] = iSum + cnt
	if iCash > 0:
		if not money.checkCash(who, iCash):
			message.tips(who, "染色材料不足，不能染色哦")
			return
		who = getRole(pid)
		if not who:
			return
	if not checkDyeProps(who, dProps):
		message.tips(who, "染色材料不足，不能染色哦")
		return
	subDyeProps(who, dProps, iCash)
	petObj.setColors({SHAPE_PART_TYPE_BODY:schemeNo})
	message.tips(who, "异兽染色成功")
	who.endPoint.rpcDyeDone()

def rpcRideDye(who, reqMsg):
	'''请求坐骑染色
	'''
	rideId = reqMsg.rideId
	dyeInfo = reqMsg.dyeInfo
	rideObj = who.rideCtn.getItem(rideId)
	if not rideObj:
		message.tips(who, "该坐骑不存在")
		return
	colors = rideObj.getColors()
	dyeLen = len(dyeInfo)
	if dyeLen < 1:
		return
	sameScheme = 0
	pid, iShape, iCash, dProps, dChange = who.id, rideObj.shape, 0, {}, {}
	for dyeMsg in dyeInfo:
		if dyeMsg.color == colors[dyeMsg.shape-1]:
			sameScheme += 1
			continue
		part = dyeMsg.shape
		color = dyeMsg.color
		dChange[part-1] = color
		tKey = (iShape, part, 1, color)
		dCost = dyeData.getConfig(tKey, "染色材料", {})
		for propsId, cnt in dCost.iteritems():
			if propsId == 200001:
				iCash += cnt
			else:
				iSum = dProps.setdefault(propsId, 0)
				dProps[propsId] = iSum + cnt
	if sameScheme == dyeLen:
		message.tips(who, "染色方案和现有相同，不用再染了哦")
		return
	if not doSub(who, dProps, iCash):
		return
	rideObj.setColors(dChange)
	message.tips(who, "坐骑染色成功")
	who.endPoint.rpcDyeDone()


def rpcRoleDyeSchemeResponse(who):
	'''下发角色染色方案信息
	'''
	dyeScheme = who.fetch("dyeScheme", {})
	schemeList = []
	msg = dye_pb2.roleDyeScheme()
	for iNo, scheme in dyeScheme.iteritems():
		dyeMsg = packDyeScheme(who, iNo, scheme)
		schemeList.append(dyeMsg)
	msg.dyeScheme.extend(schemeList)
	who.endPoint.rpcRoleDyeSchemeResponse(msg)

def rpcDyeUI(who):
	'''打开染色界面
	'''
	who.endPoint.rpcDyeUI()

def packDyeScheme(who, schemeNo, scheme):
	'''打包角色染色方案
	'''
	lst = []
	fashion = who.fashionCtn.getFashion(scheme[0])
	colors = scheme[1]
	shapeParts = fashion.fetch("parts", {})
	msg = dye_pb2.roleDyeInfo()
	msg.schemeNo = schemeNo
	for part, suit in shapeParts.iteritems():
		dyeMsg = dye_pb2.dyeMsg()
		dyeMsg.key = part + 1
		dyeMsg.suit = suit
		dyeMsg.color = colors.get(part, 0)
		lst.append(dyeMsg)
	msg.dyeInfo.extend(lst)
	return msg


import copy
import message
from common import *
import dyeData
import money
import resume
