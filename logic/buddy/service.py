# -*- coding: utf-8 -*-
# 伙伴服务
import endPoint
import buddy_pb2

class cService(buddy_pb2.terminal2main):

	@endPoint.result
	def rpcReqUpBattle(self, ep, who, reqMsg): return rpcReqUpBattle(who,reqMsg)  #伙伴上阵

	@endPoint.result
	def rpcReqDownBattle(self, ep, who, reqMsg): return rpcReqDownBattle(who,reqMsg) #伙伴下阵

	@endPoint.result
	def rpcSetUseBattle(self, ep, who, reqMsg): return rpcSetUseBattle(who,reqMsg)  #设置参战阵容

	@endPoint.result
	def rpcExchangePos(self, ep, who, reqMsg): return rpcExchangePos(who,reqMsg) #交换位置

	@endPoint.result
	def rpcChangeLineup(self, ep, who, reqMsg): return rpcChangeLineup(who,reqMsg) #切换阵法

	@endPoint.result
	def rpcUpgradeBuddy(self, ep, who, reqMsg): return rpcUpgradeBuddy(who,reqMsg) #获得/升阶伙伴

	@endPoint.result
	def rpcLearnSkill(self, ep, who, reqMsg): return rpcLearnSkill(who,reqMsg) #学习技能

	@endPoint.result
	def rpcSetRent(self, ep, who, reqMsg): return rpcSetRent(who,reqMsg) #设置好友助战

	@endPoint.result
	def rpcFriendBuddyReq(self, ep, who, reqMsg): return rpcFriendBuddyReq(who,reqMsg) #请求好友伙伴

	@endPoint.result
	def rpcFriendBuddyRent(self, ep, who, reqMsg): return rpcFriendBuddyRent(who,reqMsg) #租借好友伙伴

	@endPoint.result
	def rpcGetRentMoney(self, ep, who, reqMsg): return rpcGetRentMoney(who,reqMsg) #一键领取租金

	@endPoint.result
	def rpcRentInfoReq(self, ep, who, reqMsg): return rpcRentInfoReq(who,reqMsg) #租借信息请求

def rpcReqUpBattle(who,reqMsg):
	iBattleNo = reqMsg.iBattleNo
	iBuddyNo  = reqMsg.buddy.iBuddyNo
	iFriendId = reqMsg.buddy.iFriendId
	iPos = reqMsg.iPos
	if not 1<=iBattleNo<=3:
		return
	iOldLen = who.buddyCtn.itemCount(iBattleNo)
	if not 1<=iPos<=iOldLen+1 or iPos>4:
		return
		
	if iFriendId:
		oFriend = who.buddyCtn.getFriendBuddy(iFriendId)
		if not oFriend or oFriend.no != iBuddyNo:
			message.tips(who,"未租用，无法上阵")
			return
		if who.buddyCtn.hasFriendBuddyInBattle(iBattleNo):
			message.tips(who,"阵容中只能使用一个好友伙伴")
			return
		iNo = iFriendId
	else:
		if not who.buddyCtn.getItem(iBuddyNo):
			message.tips(who,"该伙伴尚未解锁")
			return
		iNo = iBuddyNo

	if who.buddyCtn.hasSameBuddyInBattle(iBattleNo,iBuddyNo,iFriendId,iPos):
		message.tips(who,"阵容中已有同样的助战伙伴，不能上阵")
		return

	who.buddyCtn.upBattle(iBattleNo,iNo,iPos-1)
	who.buddyCtn.updateBuddyListToTeam(iBattleNo)
	who.endPoint.rpcUpBattle(reqMsg)
	iLen = who.buddyCtn.itemCount(iBattleNo)
	if iOldLen == iLen:
		return
	if iLen == 4:
		message.tips(who,"#C04第%d阵容#n已经上阵了#C04%d位#n伙伴，阵容已满" % (iBattleNo,iLen))
	else:
		message.tips(who,"#C04第%d阵容#n已经上阵了#C04%d位#n伙伴，还可邀请#C04%d位#n伙伴" % (iBattleNo,iLen,4-iLen))

def rpcReqDownBattle(who,reqMsg):
	iBattleNo = reqMsg.iValue1
	iPos  = reqMsg.iValue2
	if not 1<=iBattleNo<=3:
		return
	iLen = who.buddyCtn.itemCount(iBattleNo)
	if not 0<iPos<=iLen:
		return
	who.buddyCtn.downBattle(iBattleNo,iPos-1)
	who.buddyCtn.updateBuddyListToTeam(iBattleNo)
	who.endPoint.rpcDownBattle(reqMsg)
	message.tips(who,"第%d阵容已经上阵了%d位伙伴，还可邀请%d位伙伴" % (iBattleNo,iLen-1,5-iLen))

def rpcSetUseBattle(who,reqMsg):
	iNo = reqMsg.iValue
	if not 1<=iNo<=3:
		return False
	who.buddyCtn.setBattle(iNo)
	who.buddyCtn.updateBuddyListToTeam(iNo)
	return True

def rpcExchangePos(who,reqMsg):
	iBattleNo = reqMsg.iBattleNo
	iPos1 = reqMsg.iPos1
	iPos2 = reqMsg.iPos2
	if not who.buddyCtn.exchangePos(iBattleNo,iPos1,iPos2):
		return False
	who.buddyCtn.updateBuddyListToTeam(iBattleNo)
	return True

def rpcChangeLineup(who,reqMsg): #切换阵法
	iBattleNo = reqMsg.iBattleNo
	iLineup = reqMsg.iLineup

	if not 1 <= iBattleNo <=3:
		return

	if iLineup != 0 and not who.lineupCtn.getItem(iLineup):
		message.tips(who,"阵法还未学习")
		return

	who.buddyCtn.setLineup(iBattleNo,iLineup)
	who.endPoint.rpcBattleMod(iBattleNo,iLineup)

def rpcUpgradeBuddy(who,reqMsg): #获得/升阶伙伴
	iBuddyNo = reqMsg.iBuddyNo
	oBuddy = who.buddyCtn.getItem(iBuddyNo)
	if not oBuddy:
		getBuddy(who, iBuddyNo)
	else:
		upgradeBuddy(who, oBuddy)

def rpcLearnSkill(who,reqMsg): #学习技能
	iBuddyNo = reqMsg.iBuddyNo
	propsId1 = reqMsg.iPropsId1
	propsId2 = reqMsg.iPropsId2
	oBuddy = who.buddyCtn.getItem(iBuddyNo)
	if not oBuddy:
		return
	if not propsId1 and not propsId2:
		return
	skillList = oBuddy.getSkillList()
	initSkillCount = oBuddy.getInitSkillCount()
	if propsId1 and propsId2:
		if oBuddy.getQuality() < 5:
			message.tips(who,"#C045阶#n可解锁")
			return
		oProps1 = who.propsCtn.getItem(propsId1)
		if not oProps1:
			return
		oProps2 = who.propsCtn.getItem(propsId2)
		if not oProps2:
			return
		if oProps1.no() not in buddyData.glSkillList["可学技能"]:
			return
		if oProps2.no() not in buddyData.glSkillList["可学技能"]:
			return
		skillId1 = oProps1.getPetSkill()
		skillId2 = oProps2.getPetSkill()
		if skillId1 == skillId2:
			message.tips(who, "不能学习相同的技能")
			return
		skillObj1 = skill.new(skillId1)
		skillObj2 = skill.new(skillId2)
		sameSkillName = []
		if skillId1 in skillList:
			sameSkillName.append(skillObj1.name)
		if skillId2 in skillList:
			sameSkillName.append(skillObj2.name)
		if sameSkillName:
			message.tips(who,"#C02%s#n已学会#C02%s#n，不需要重新学习" % (oBuddy.name,",".join(sameSkillName)))
			return
		who.propsCtn.addStack(oProps1,-1)
		learnSkill(who,oBuddy,skillObj1,2+initSkillCount)
		who.propsCtn.addStack(oProps2,-1)
		learnSkill(who,oBuddy,skillObj2,3+initSkillCount)
	else:
		if propsId1:
			propsId = propsId1
			needQuality = 4
			pos = 2+initSkillCount
		else:
			propsId = propsId2
			needQuality = 5
			pos = 3+initSkillCount
		oProps = who.propsCtn.getItem(propsId)
		if not oProps:
			return
		if oBuddy.getQuality() < needQuality:
			message.tips(who,"#C04%d阶#n可解锁" % needQuality)
			return
		if oProps.no() not in buddyData.glSkillList["可学技能"]:
			return
		skillId = oProps.getPetSkill()
		skillObj = skill.get(skillId)
		if skillId in skillList:
			message.tips(who,"#C02%s#n已学会#C02%s#n，不需要重新学习" % (oBuddy.name,skillObj.name))
			return
		who.propsCtn.addStack(oProps,-1)
		learnSkill(who,oBuddy,skillObj,pos)
		
	oBuddy.reCalcAttr()
	oBuddy.attrChange("skillList")

def rpcSetRent(who,reqMsg): #设置好友助战
	iBuddyNo = reqMsg.iBuddyNo
	isRent = reqMsg.isRent

	oBuddy = who.buddyCtn.getItem(iBuddyNo)
	if not oBuddy:
		return

	who.buddyCtn.setRent(oBuddy,isRent)

def rpcFriendBuddyReq(who,reqMsg): #请求好友伙伴
	sendFriendBuddy(who)

def sendFriendBuddy(who):
	lst = []
	for oBuddy in who.buddyCtn.getAllFriendBuddy():
		oMsg = oBuddy.getMsg()
		lst.append(oMsg)

	for oFriend in who.friendCtn.getAllValues():
		if not oFriend.isFriend() or not oFriend.isSameService():
			continue
		iFriendId = oFriend.friendRoleId
		oBuddy = who.buddyCtn.getFriendBuddy(iFriendId)
		if not oBuddy:
			buddyCtn = block.blockBuddy.getBuddyCtn(iFriendId)
			if not buddyCtn:
				continue
			oBuddy = buddyCtn.getRentBuddy()
			if not oBuddy:
				continue

			lst.append(packFriendBuddy(who,oBuddy,oFriend))

	msg = {}
	msg["buddyList"] = lst
	who.endPoint.rpcFriendBuddySend(**msg)

def rpcFriendBuddyRent(who,reqMsg): #租借好友伙伴
	iFriendId = reqMsg.iFriendId
	iBuddyNo = reqMsg.iBuddyNo
	oFriend = who.friendCtn.getItem(iFriendId)
	if not oFriend or not oFriend.isSameService():
		return
	if who.buddyCtn.getFriendBuddy(iFriendId):
		message.tips(who,"你已经租借了该伙伴")
		return
	buddyCtn = block.blockBuddy.getBuddyCtn(iFriendId)
	if not buddyCtn or buddyCtn.rent != iBuddyNo:
		message.tips(who,"你的好友不再租借该伙伴")
		sendFriendBuddy(who)
		return
	oBuddy = buddyCtn.getRentBuddy()
	attrData = buddy.calattr.calcAttr(oBuddy,who.level)
	iFright = getFightByAttr(oBuddy,attrData)
	iCost = getRentCost(who,iFright)
	if not iCost:
		return
	if who.cash < iCost:
		if not money.checkCash(who,iCost):
			return
		buddyCtn = block.blockBuddy.getBuddyCtn(iFriendId)
		if not buddyCtn or buddyCtn.rent != iBuddyNo:
			message.tips(who,"你的好友不再租借该伙伴")
			return
	who.costCash(iCost,"租借好友伙伴",None)
	addRentPrice(buddyCtn,oFriend.level,iCost)
	buddyCtn.endPoint.rpcRentPriceMod(buddyCtn.getPrice())
	oNewBuddy = who.buddyCtn.addFriendBuddy(oFriend,oBuddy,iCost,attrData)
	buddyCtn.addRentMsg(getSecond(),who.name,oBuddy.name,iCost)
	addRentTimes(who,iFriendId)
	who.endPoint.rpcFriendBuddyMod(oNewBuddy.getMsg())

def rpcGetRentMoney(who,reqMsg): #一键领取租金
	iPrice = who.buddyCtn.getPrice()
	if not iPrice:
		return

	who.buddyCtn.addPrice(-iPrice,who.level)
	who.rewardCash(iPrice,"伙伴租金领取")
	who.endPoint.rpcRentPriceMod(who.buddyCtn.getPrice())

def rpcRentInfoReq(who,reqMsg): #租借信息请求
	iPage = reqMsg.iPage
	msg = packRentInfo(who,iPage)
	who.endPoint.rpcRentInfoSend(**msg)

def getBuddy(who, iBuddyNo):
	propsNo = buddyData.getBuddyInfo(iBuddyNo,"碎片")
	need = buddyData.getBuddyInfo(iBuddyNo,"升阶数量")[0]
	has, = who.propsCtn.getPropsAmountByNos(propsNo)
	if has < need:
		message.tips(who, "碎片补足")
		return
	who.propsCtn.subPropsByNo(propsNo,1,"获得伙伴")
	buddyObj = buddy.add(who,iBuddyNo)
	message.tips(who,"成功召唤#C02%s#n" % buddyObj.name)

def upgradeBuddy(who, oBuddy):
	if oBuddy.getQuality() == oBuddy.maxQuality():
		message.tips(who, "已达到最大阶级")
		return
	propsNo = oBuddy.getMaterial()
	need = oBuddy.getUpgradeNeed()
	has, = who.propsCtn.getPropsAmountByNos(propsNo)
	if has < need:
		return
	who.propsCtn.subPropsByNo(propsNo,need,"伙伴升阶")
	oBuddy.addQuality(1)
	oBuddy.checkRelation(who)
	who.buddyCtn.addMajor(oBuddy)
	if oBuddy.getQuality() <= 3:
		skillId = oBuddy.getConfig("天赋技能")[oBuddy.getQuality()-2]
		oBuddy.setSkill(skillId)
	oBuddy.reCalcAttr()
	oBuddy.attrChange("quality")
	message.tips(who,"升阶成功")

def learnSkill(who,oBuddy,skillObj,pos):
	skillList = oBuddy.fetch("skillList", [])
	if len(skillList) > pos:
		oldSkillId = skillList[pos]
		skillList[pos] = skillObj.id
		oBuddy.set("skillList", skillList)
		oBuddy.generateSkillList()
		oBuddy.generateValidSkillList()
		oldSkill = skill.get(oldSkillId)
		message.tips(who,"学习成功！#C02%s#n被替换为#C02%s#n" % (oldSkill.name,skillObj.name))
	else:
		oBuddy.setSkill(skillObj.id)
		message.tips(who,"#C02%s#n学会#C02%s#n" % (oBuddy.name,skillObj.name))

def packTeamBuddyInfo(pid,buddyList):
	oMsg = buddy_pb2.teamBuddyList()
	who = getRole(pid)
	if not who:
		return oMsg
	oMsg.iLevel = who.level
	oMsg.buddyList.extend(buddyList)
	return oMsg

def packFriendBuddy(who, oBuddy, oFriend):
	oMsg = buddy_pb2.buddyMsg()
	oMsg.iFriendId = oFriend.friendRoleId
	oMsg.iBuddyNo = oBuddy.id
	oMsg.quality = oBuddy.getQuality()
	oMsg.skillList.extend(oBuddy.fetch("skillList", []))
	oMsg.sFriendName = oFriend.name

	attrData = buddy.calattr.calcAttr(oBuddy,who.level)  #要用本人的等级计算
	for attr in buddy.object.gBuddyAttrFreshList:
		setattr(oMsg,attr,attrData[attr])
	iFight = getFightByAttr(oBuddy,attrData)
	oMsg.iMoney = getRentCost(who,iFight)
	oMsg.fight = iFight

	return oMsg

def packRentInfo(who, iPage):
	COUNT = 8
	rentMsg = who.buddyCtn.getRentMsg()
	msgCount = len(rentMsg)
	iMaxPage = (msgCount+COUNT-1)/COUNT
	msg = {}
	msg["iPage"] = iPage
	msg["iMaxPage"] = iMaxPage
	
	if iPage > iMaxPage:
		return msg

	lst = []
	iBegin = (iPage-1)*COUNT
	iEnd = iPage * COUNT
	for (iTime,sRoleName,sBuddyName,iPrice) in rentMsg[iBegin:iEnd]:
		oMsg = buddy_pb2.rentMsg()
		oMsg.iTime = iTime
		oMsg.sContent = "{}租用了你的{},你获得了#R<{},3,2>#n".format(sRoleName,sBuddyName,iPrice)
		lst.append(oMsg)

	msg["rentList"] = lst

	return msg

def getFightByAttr(oBuddy, attrData):
	return grade.gradeBuddyAttrByData(attrData) + grade.gradeBuddySkill(oBuddy)

def getRentCost(who, iFright):
	return iFright * 20
	iTmes = 0
	dTimes = who.day.fetch("fbRent",{})
	if iFriendId in dTimes:
		iTmes = dTimes[iFriendId]

	return buddyData.getCost(iTmes+1,who.level)

def addRentTimes(who, iFriendId, iTimes=1):
	dTimes = who.day.fetch("fbRent",{})
	dTimes[iFriendId] = dTimes.get(iFriendId,0) + iTimes
	who.day.set("fbRent",dTimes)

def addRentPrice(buddyCtn, iLevel, iPrice):
	iDayPrice = buddyCtn.day.fetch("price")
	iDayMaxPrice = buddyCtn.getDayMaxPrice(iLevel)
	iPrice = min(iDayMaxPrice-iDayPrice,iPrice)
	if iPrice:
		buddyCtn.addPrice(iPrice,iLevel)

from common import *
from role.defines import *
import buddy
import buddyData
import message
import skill
import block.blockBuddy
import buddy.calattr
import buddy.object
import money
import grade