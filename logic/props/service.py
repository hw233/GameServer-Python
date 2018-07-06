# -*- coding: utf-8 -*-
from props.defines import *
import props_pb2
import endPoint

def handleLock(oldFunc):
	def newFunc(who, oProps, reqMsg):
		import role.roleConfig
		if role.roleConfig.isLock(who):
			who.endPoint.rpcSecurityUnlock()
			return
		try:
			return oldFunc(who, oProps, reqMsg)
		except Exception:
			raise
	return newFunc

#包裹服务
class cService(props_pb2.terminal2main):	
	@endPoint.result
	def rpcPropsDetail(self,ep,who,reqMsg):return rpcPropsDetail(who,reqMsg)#道具信息

	@endPoint.result	
	def rpcClickButton(self,ep,who,reqMsg):return rpcClickButton(who,reqMsg)#点击按钮

	@endPoint.result 
	def rpcAddCapacity(self,ep,who,reqMsg):return rpcAddCapacity(who,reqMsg)#背包解锁

	@endPoint.result 
	def rpcGetBackProps(self,ep,who,reqMsg):return rpcGetBackProps(who,reqMsg)#从临时背包取回物品

	@endPoint.result 
	def rpcExchangeEquipScheme(self,ep,who,reqMsg):return rpcExchangeEquipScheme(who,reqMsg)#切换装备区方案

	@endPoint.result
	def rpcReqOpenStorage(self,ep,who,reqMsg):return rpcReqOpenStorage(who,reqMsg)#请求打开仓库

	@endPoint.result
	def rpcBuyStorage(self,ep,who,reqMsg):return rpcBuyStorage(who,reqMsg)#购买仓库

def getPropsByPackageNo(who,iPackageNo,iPropsId):
	if iPackageNo == PACKAGE:
		oProps = who.propsCtn.getItem(iPropsId)
	elif iPackageNo == EQUIPCTN:
		oProps = who.equipCtn.getItem(iPropsId)
	elif iPackageNo == STORAGE:
		oProps = who.storage.getItem(iPropsId)
	elif iPackageNo == NUMENBAG:
		oProps = who.tempCtn.getItem(iPropsId)
	else:
		message.tips(who,"错误的物品位置")
		return None

	return oProps 

def rpcClickButton(who,reqMsg):#点击按钮
	oProps = getPropsByPackageNo(who, reqMsg.pos.iPackageNo,reqMsg.pos.iPropsId)
	if not oProps:
		return

	iButtonType = reqMsg.iButtonType
	iPackageNo = reqMsg.pos.iPackageNo
	data = dButtonFunc.get(iButtonType)
	if not data:
		return
	if data.get("packageNo") and data.get("packageNo") != iPackageNo:
		return

	func = data["func"]
	func(who, oProps, reqMsg)

def clickWear(who, oProps, reqMsg):#穿上
	if not hasattr(oProps,"doWear"):
		return
	if oProps.kind == ITEM_EQUIP:
		doWearForEquip(who, oProps)
	else:
		oProps.doWear(who)
	
def doWearForEquip(who, oProps):#穿上
	oWearEquip = who.equipCtn.getEquipByWearPos(oProps.wearPos())
	# 需要检查比对两件是否有宝石，替换规则
	if oWearEquip and oWearEquip.gems() and not oProps.gems():
		message.confirmBoxNew(who, functor(responseWear, oProps.id), "是否将旧装备上的宝石转移到新装备上？\nQ取消#10\nQ转移")
		return
	oProps.doWear(who)

def responseWear(who, yes, propsId):
	propsObj = who.propsCtn.getItem(propsId)
	if not propsObj:
		return
	equipObj = who.equipCtn.getEquipByWearPos(propsObj.wearPos())
	if not equipObj:
		return
	if propsObj is equipObj:
		return
	if yes and equipObj and equipObj.gems() and not propsObj.gems():
		bGemReplace = True
	else:
		bGemReplace = False
	propsObj.doWear(who, bGemReplace)

def clickDoff(who, oProps, reqMsg):#卸下
	if not hasattr(oProps,"doDoff"):
		return
	oProps.doDoff(who)

def clickUse(who, oProps, reqMsg):#使用
	if not hasattr(oProps,"use"):
		return
	oProps.use(who)
	listener.doListen("使用物品", who, propsNo=oProps.no())

def clickSell(who, oProps, reqMsg):#出售
	message.tips(who,"本功能尚未开启")

@handleLock
def clickResolve(who, oProps, reqMsg):#分解
	if not hasattr(oProps,"decompose"):
		return
	oProps.decompose(who)

def clickCompound(who, oProps, reqMsg):#合成
	if not hasattr(oProps,"compound"):
		return
	oProps.compound(who)

@handleLock
def clickDiscard(who, oProps, reqMsg):#丢弃
	content = "丢弃#C07{}×{}#n？\nQ取消\nQ丢弃".format(oProps.name,oProps.stack())
	message.confirmBoxNew(who, functor(responseDiscard, oProps.id), content)
		
def responseDiscard(who, yes, propsId):
	if not yes:
		return
	oProps = who.propsCtn.getItem(propsId)
	if not oProps:
		return
	if not oProps.canDiscard():
		message.tips(who,"此物品无法丢弃")
		return
	who.propsCtn.removeItem(oProps)
	message.tips(who,"丢弃成功")

def clickRepaired(who, oProps, reqMsg):#修理
	if oProps.kind != ITEM_EQUIP:
		return
	iPackageNo = reqMsg.pos.iPackageNo
	iPropsId = oProps.key
	iCostCash = oProps.lifeRepairPrice()
	if not iCostCash:
		return
	sContent = ""
	if iPackageNo == PACKAGE:
		sContent = "装备已无耐久，无法穿戴\n是否修理(需要#R<{},3,2>#n)？\nQ取消\nQ修理".format(iCostCash)
	elif iPackageNo == EQUIPCTN:
		sContent = "花费#R<{},3,2>#n修理#C07{}#n？\nQ取消\nQ修理".format(iCostCash,oProps.name)

	if not sContent:
		return
	message.confirmBoxNew(who, functor(responseRepaire, iPackageNo, iPropsId), sContent)
		
def responseRepaire(who, yes, iPackageNo, iPropsId):
	oProps = getPropsByPackageNo(who,iPackageNo,iPropsId)
	if not oProps:
		return
	iCostCash = oProps.lifeRepairPrice()
	if not money.checkCash(who,iCostCash):
		return
	who.addCash(-iCostCash,"修理装备",None)
	oProps.recoverLife()
	message.tips(who,"装备修理成功")

def clickStorageIn(who, oProps, reqMsg):#移入仓库
	if not who.storage.leftCapacity():
		message.tips(who,"仓库已满，无法存入")
		return
	oPropsFork = props.fork(oProps)
	who.propsCtn.removeItem(oProps)
	who.addProps(who.storage,oPropsFork,"移入仓库")
	message.tips(who,"存入成功")

def clickStorageOut(who, oProps, reqMsg):#移出仓库
	if not who.propsCtn.leftCapacity():
		message.tips(who,"背包已满，无法取出")
		return
	oPropsFork = props.fork(oProps)
	who.storage.removeItem(oProps)
	who.endPoint.rpcAddPropsFlash(oPropsFork.getMsg4Package(who.propsCtn,*oPropsFork.MSG_FIRST))
	who.addProps(who.propsCtn,oPropsFork,"移出仓库")

def clickInlay(who, oProps, reqMsg):#镶嵌
	message.tips(who,"本功能尚未开启")

def clickStall(who, oProps, reqMsg):#摆摊出售
	message.tips(who,"本功能尚未开启")

def clickGetBack(who, oProps, reqMsg):#取回
	if not who.propsCtn.leftCapacity():
			message.tips(who,"背包已满，无法取出")
			return
	who.tempCtn.removeItem(oProps)
	oPropsFork = props.fork(oProps)
	who.endPoint.rpcAddPropsFlash(oPropsFork.getMsg4Package(who.propsCtn,*oPropsFork.MSG_FIRST))
	who.addProps(who.propsCtn,oPropsFork,"临时背包取回物品")
	
def clickUsePet(who, oProps, reqMsg):#使用
	if not hasattr(oProps, "useForPet"):
		return
	petObj = who.petCtn.getItem(reqMsg.targetId)
	if not petObj:
		return
	count = reqMsg.count if reqMsg.count else 1
	oProps.useForPet(who, petObj, count)

dButtonFunc = {
	BUTTON_WEAR: {"func":clickWear, "packageNo":PACKAGE,},
	BUTTON_DOFF: {"func":clickDoff, "packageNo":EQUIPCTN,},
	BUTTON_USE: {"func":clickUse, "packageNo":PACKAGE,},
	BUTTON_SELL: {"func":clickSell, "packageNo":PACKAGE,},
	BUTTON_RESOLVE: {"func":clickResolve, "packageNo":PACKAGE,},
	BUTTON_COMPOUND: {"func":clickCompound, "packageNo":PACKAGE,},
	BUTTON_DISCARD: {"func":clickDiscard, "packageNo":PACKAGE,},
	BUTTON_REPAIRED: {"func":clickRepaired,},
	BUTTON_STORAGE_IN: {"func":clickStorageIn, "packageNo":PACKAGE,},
	BUTTON_STORAGE_OUT: {"func":clickStorageOut, "packageNo":STORAGE,},
	BUTTON_INLAY: {"func":clickInlay, "packageNo":STORAGE,},
	BUTTON_STALL: {"func":clickStall, "packageNo":PACKAGE,},
	BUTTON_OPEN: {"func":clickUse, "packageNo":PACKAGE,},
	BUTTON_GETBACK: {"func":clickGetBack, "packageNo":NUMENBAG,},
	BUTTON_USE_PET: {"func":clickUsePet, "packageNo":PACKAGE,},
}

def	rpcPropsDetail(who,reqMsg):#道具信息
	iPackageNo,iPropsId = reqMsg.iPackageNo,reqMsg.iPropsId
	if iPackageNo == PACKAGE:
		oProps = who.propsCtn.getItem(iPropsId)
		if oProps:
			who.endPoint.rpcModProps(oProps.getMsg4Package(who.propsCtn,*oProps.MSG_DETAIL))
	elif iPackageNo == EQUIPCTN:
		oProps = who.equipCtn.getItem(iPropsId)
		if oProps:
			who.endPoint.rpcModEquip(oProps.getMsg4Item(who.equipCtn,*oProps.MSG_DETAIL))
	elif iPackageNo == STORAGE:
		oProps = who.storage.getItem(iPropsId)
		if oProps:
			who.endPoint. rpcMod2Storage(oProps.getMsg4Item(who.storage,*oProps.MSG_DETAIL))
	elif iPackageNo == NUMENBAG:
		oProps = who.tempCtn.getItem(iPropsId)
		if oProps:
			who.endPoint.rpcMod2NumenBag(oProps.getMsg4Item(who.tempCtn,*oProps.MSG_DETAIL))

def rpcAddCapacity(who,reqMsg):#背包解锁
	iNowStamp = getSecond()
	if iNowStamp - getattr(who,"iAddCapacityStamp",0) < 1 :
		return
	who.iAddCapacityStamp = iNowStamp
	iCount = reqMsg.iValue
	if not 0< iCount <= 20:
		return
	needCash = 0
	iRow = who.getCapacity()/5
	for i in xrange(iRow,iCount):
		needCash += lockPackageData.getConfig(i+1,"消耗银币")
	if not needCash:
		return
	iAddCount = iCount - iRow
	content = "解锁#C07{}格#n包裹空间需要#IS#n#C07{:,}#n，是否解锁？\nQ取消\nQ解锁".format(iAddCount*5,needCash)
	message.confirmBoxNew(who, functor(responseAddCapacity, iCount), content)
		
def responseAddCapacity(who, yes, iCount):
	if not yes:
		return
	needCash = 0
	iRow = who.getCapacity()/5
	for i in xrange(iRow,iCount):
		needCash += lockPackageData.getConfig(i+1,"消耗银币")
	if not needCash:
		return
	iAddCount = iCount - iRow
	
	if who.getCapacity()/5 + iAddCount != iCount:
		return
	if not money.checkCash(who,needCash):
		return
	who.addCash(-needCash,"解锁包裹")
	who.propsCtn.add("row",iAddCount)
	who.attrChange("capacity")
	message.tips(who,"包裹空间#C04+{}#n".format(iAddCount*5))

def rpcGetBackProps(who,reqMsg):#从临时背包取回物品
	for iPropsId in reqMsg.iPropsIds:
		oProps = who.tempCtn.getItem(iPropsId)
		if not oProps:
			message.tips(who,"没有该物品")
			continue
		if not who.propsCtn.leftCapacity():
			message.tips(who,"包裹已满，无法取出")
			return
		who.tempCtn.removeItem(oProps)
		oPropsFork = props.fork(oProps)
		who.endPoint.rpcAddPropsFlash(oPropsFork.getMsg4Package(who.propsCtn,*oPropsFork.MSG_FIRST))
		who.addProps(who.propsCtn,oPropsFork,"临时背包取回物品")

def rpcExchangeEquipScheme(who,reqMsg):#切换装备区方案
	iScheme = reqMsg.iValue
	if not 0 < iScheme <= 2:
		message.tips(who,"错误的加点方案")
		return
	if iScheme==2 and who.level<60 and not config.IS_INNER_SERVER:
		message.tips(who,"#C0460级#n开启第二套装")
		return
	if iScheme == who.equipCtn.iScheme:
		return
	iNowStamp = getSecond()
	if iNowStamp - getattr(who,"exchangeEquipStamp",0) < 5:
		message.tips(who,"切换过于频繁，请先休息一下")
		return
	for oEquip in who.equipCtn.getAllWearEquip():
		oEquip.cancelSetup(who)
	who.equipCtn.setScheme(iScheme)
	for oEquip in who.equipCtn.getAllWearEquip():
		oEquip.setup(who)
	who.equipCtn.refresh()
	who.reCalcAttr()#重新计算人物属性
	who.exchangeEquipStamp = iNowStamp

def rpcReqOpenStorage(who,reqMsg):#请求打开仓库
	msg = who.storage.getMsg()
	who.endPoint.rpcStorageInfo(msg)

def rpcBuyStorage(who,reqMsg):  #购买仓库
	iNowStamp = getSecond()
	if iNowStamp - getattr(who,"iBuyStorageStamp",0) < 1 :
		return
	who.iBuyStorageStamp = iNowStamp
	iNo = who.storage.fetch("count")+3
	if not 0<iNo<=9:
		return
	iNeedCash = who.storage.getCostCash(iNo)
	sName = who.storage.getName(iNo)
	if not iNeedCash:
		return
	content = "解锁#C07{}#n需要#IS#n#C07{:,}#n，是否解锁？\nQ取消\nQ解锁".format(sName,iNeedCash)
	message.confirmBoxNew(who, responseBuyStorage, content)
		
def responseBuyStorage(who, yes):
	if not yes:
		return
	
	iNo = who.storage.fetch("count")+3
	iNeedCash = who.storage.getCostCash(iNo)
	if not 0<iNo<=9:
		return
	if not iNeedCash:
		return
	if not money.checkCash(who,iNeedCash):
		return
	if iNo != who.storage.fetch("count")+3:
		return

	who.costCash(iNeedCash,"购买仓库")
	who.storage.add("count",1)
	
	sName = who.storage.getName(iNo)
	msg = props_pb2.storageName()
	msg.iNo = iNo
	msg.sName = sName
	who.endPoint.rpcAddStorage(msg)
	message.tips(who,"成功解锁#C02{}#n".format(sName))

from common import *
import message

import props
import role
import c
import propsData
import props_pb2
import u
import block.blockPackage
import factory
import event

import findSort
import log
import equipData
import misc
import gevent
import timeU
import svcHyperLink
import launch
import block.storage
import money
import block.numenBag
import lockPackageData
import config
import listener
