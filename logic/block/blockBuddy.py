# -*- coding: utf-8 -*-
'''助战伙伴容器
'''


import block
import ctn

class BuddyContainer(ctn.cContainerBase, block.cCtnBlock):
	
	def __init__(self, ownerId):
		ctn.cContainerBase.__init__(self, self._dirtyEventHandler)
		block.cCtnBlock.__init__(self, "助战伙伴容器", ownerId)
		self.setIsStm(sql.BUDDY_CTN_INSERT)
		self.setDlStm(sql.BUDDY_CTN_DELETE)
		self.setUdStm(sql.BUDDY_CTN_UPDATE)
		self.setSlStm(sql.BUDDY_CTN_SELECT)

		self.ownerId=ownerId
		self.currentIdx = 1  # 当前阵容
		self.buddyList = {1:[], 2:[], 3:[]}  # 阵容列表
		self.lineupList = {}  # 阵法列表
		self.rent = 0  #租借伙伴
		self.majorList = {}  #专精列表
		self.frinedBuddy = {}  #好友助战
		self.price = 0   #获得租金
		self.rentMsg = []  #租借信息
		self.day = cycleData.cCycDay(2,self._dirtyEventHandler)#天变量

	def _dirtyEventHandler(self):
		factoryConcrete.buddyCtnFtr.schedule2tail4save(self.ownerId)

	def _createAndLoadItem(self,iIndex,uData):#override
		if isinstance(uData,tuple):
			idx, dData = uData
		else:
			idx,dData = uData,{}
		return buddy.createAndLoad(idx,dData)

	def save(self):
		data = ctn.cContainerBase.save(self)
		data["currentIdx"] = self.currentIdx
		data["buddyList"] = self.buddyList
		data["lineupList"] = self.lineupList
		data["rentMsg"] = self.rentMsg
		data["rent"] = self.rent
		data["price"] = self.price

		dDay=self.day.save()
		if dDay:
			data['d']=dDay

		d = {}
		for iFriendId,buddyObj in self.frinedBuddy.iteritems():
			d[iFriendId] = (buddyObj.iNo,buddyObj.save())

		if d:
			data["friendBuddy"] = d
		return data
	
	def load(self, data):  # override  
		ctn.cContainerBase.load(self, data)
		
		self.currentIdx = data.pop("currentIdx", 0)
		self.buddyList = data.pop("buddyList", {})
		self.lineupList = data.pop("lineupList", {})
		self.rentMsg = data.pop("rentMsg", [])
		self.rent = data.pop("rent", 0)
		self.price = data.pop("price", 0)
		self.day.load(data.pop('d',{}))

		for iFriendId,uData in data.pop("friendBuddy",{}).iteritems():
			iNo,dData = uData
			oBuddy = buddy.createAndLoad(iNo,dData,False)
			oBuddy.ownerId = self.ownerId
			self.frinedBuddy[iFriendId] = oBuddy
			oBuddy.initAttr()

	def onBorn(self,*tArgs,**dArgs):
		pass

	@property
	def endPoint(self):
		return mainService.getEndPointByRoleId(self.ownerId)

	def setRent(self, buddyObj, isRent, isTips=True):
		'''设置好友助战
		'''
		if self.rent == buddyObj.id:
			if not isRent:
				self.rent = 0
				buddyObj.attrChange("isRent")
				if isTips:
					message.tips(self.ownerId,"你取消了#C07%s#n的租借状态" % buddyObj.name)
		else:
			if not isRent:
				return
			if self.rent:
				oldRent = self.getItem(self.rent)
				self.setRent(oldRent,0,False)
			self.rent = buddyObj.id
			buddyObj.attrChange("isRent")
			if isTips:
				message.tips(self.ownerId,"设置租借成功")

		self.markDirty()

	def isRent(self, buddyNo):
		if self.rent == buddyNo:
			return 1
		return 0

	def getRentBuddy(self):
		return self.getItem(self.rent)

	def getFriendBuddy(self, iFriendId):
		if iFriendId in self.frinedBuddy:
			return self.frinedBuddy[iFriendId]

		return None

	def getAllFriendBuddy(self):
		return self.frinedBuddy.values()

	def addFriendBuddy(self, oFriend, oFribuddy, iMoney, attrData):
		oBuddy = buddy.create(oFribuddy.no)
		oBuddy.set("quality",oFribuddy.getQuality())
		oBuddy.set("friendId",oFriend.friendRoleId)
		oBuddy.set("friendName",oFriend.name)
		oBuddy.set("money",iMoney)
		oBuddy.set("skillList",oFribuddy.fetch("skillList",[]))
		oBuddy.updateAttr(attrData)
		oBuddy.startTimer()
		self.frinedBuddy[oFriend.friendRoleId] = oBuddy
		oBuddy.ownerId = self.ownerId
		self.markDirty()
		self.endPoint.rpcFriendBuddyAdd(oBuddy.getMsg())
		return oBuddy

	def hasFriendBuddyInBattle(self, iBattleNo):
		buddyList = self.getBuddyListByIdx(iBattleNo)
		for iBuddyNo in buddyList:
			if self.getFriendBuddy(iBuddyNo):
				return True

		return False

	def removeFriendBuddy(self, iFriendId):
		if iFriendId in self.frinedBuddy:
			oBuddy = self.frinedBuddy.pop(iFriendId)
			self.endPoint.rpcFriendBuddyDel(iBuddyNo=oBuddy.id,iFriendId=iFriendId)
			self.markDirty()

	def callSetup4allItem(self):
		self.setupRelation()
		self.setupMajor()
		for oBuddy in self.getAllFriendBuddy():
			oBuddy.startTimer()

	def addMajor(self, buddyObj):
		kind = buddyObj.kind
		score = self.majorList.get(kind,0)
		oldLevel = buddyData.getMajor(score,"等级")
		self.majorList[kind] = score + buddyObj.getScore()
		self._rpcModMajor(buddyObj)
		if oldLevel == buddyData.getMajor(self.majorList[kind],"等级"):
			return
		for obj in self.getAllValues():
			if obj.kind != kind:
				continue
			obj.removeApplyByFlag("major")
			obj.setupMajor(self)
			if obj != buddyObj:
				obj.reCalcAttr()

	def getMajor(self, kind):
		score = self.majorList.get(kind,0)
		return buddyData.getMajor(score,kind,{})

	def setupMajor(self):
		for buddyObj in self.getAllValues():
			score = buddyObj.getScore()
			self.majorList[buddyObj.kind] = self.majorList.get(buddyObj.kind,0)+score
		for buddyObj in self.getAllValues():
			buddyObj.setupMajor(self)
			buddyObj.reCalcAttr(False)

	def setupRelation(self):
		for relationNo,data in buddyData.gdRelation.iteritems():
			lst = data["伙伴"]
			minQuality = self.getMinQuality(lst)
			if not minQuality:
				continue
			for buddyNo in lst:
				buddyObj = self.getItem(buddyNo)
				buddyObj.setupRelation(relationNo,minQuality)

	def getMinQuality(self,lst):
		minQuality = 0
		for buddyNo in lst:
			buddyObj = self.getItem(buddyNo)
			if not buddyObj:
				minQuality = 0
				break
			buddyQuality = buddyObj.getQuality()
			if not minQuality or buddyQuality < minQuality:
				minQuality = buddyQuality

		return minQuality

	def updateBuddyListToTeam(self,idx):
		if idx != self.currentIdx:
			return
		who = getRole(self.ownerId)
		if not who:
			return
		teamObj = who.inTeam()
		if teamObj:
			teamObj.updateBuddyList()
		
	def getBuddyListByIdx(self,iIdx):
		return self.buddyList.get(iIdx,[])

	def getCurrentBuddyList(self):
		'''当前阵容的伙伴列表
		'''
		for iBuddyNo in self.buddyList.get(self.currentIdx, []):
			oBuddy = self.getItem(iBuddyNo)
			if not oBuddy:
				oBuddy = self.getFriendBuddy(iBuddyNo)

			yield oBuddy
		
	def itemCount(self , iIdx):
		return len(self.getBuddyListByIdx(iIdx))

	def _rpcAddItem(self,buddyObj):
		self.endPoint.rpcAddBuddy(buddyObj.getMsg())

	def _rpcRemoveItem(self,buddyObj):
		self.endPoint.rpcDelBuddy(buddyObj.no)

	def _rpcModMajor(self, buddyObj):
		kind = buddyObj.kind
		score = self.majorList[kind]
		self.endPoint.rpcModMajor(descKindList[kind],score)

	def exchangePos(self,iIdx,iPos1,iPos2): #两个伙伴交换位置
		buddyList = self.getBuddyListByIdx(iIdx)
		if iPos1 > len(buddyList) or iPos2 > len(buddyList):
			return False
		iBuddyNo1 = buddyList[iPos1-1]
		iBuddyNo2 = buddyList[iPos2-1]
		buddyList[iPos1-1] = iBuddyNo2
		buddyList[iPos2-1] = iBuddyNo1
		self.markDirty()
		return True

	def refresh(self):   #阵容列表
		msg = {}
		msg["iFightBattle"] = self.currentIdx
		msg["battleList"] = self.getBattleListMsg()
		msg["buddyList"] = [oBuddy.getMsg() for oBuddy in self.getAllValues()]
		msg["majorList"] = self.getMajorMsg()
		msg["friendList"] = [oBuddy.getMsg() for oBuddy in self.getAllFriendBuddy()]
		msg["iPrice"] = self.price
		self.endPoint.rpcBattleList(**msg)

	def getBattleListMsg(self):
		lst = []
		for iBattleNo,lBuddy in self.buddyList.iteritems():
			oMsg =  buddy_pb2.battleMsg()
			oMsg.iBattleNo = iBattleNo
			oMsg.iLineup = self.lineupList.get(iBattleNo,0)
			oMsg.buddyNoList.extend(self.getBuddyListMsg(lBuddy))
			lst.append(oMsg)
		return lst

	def getBuddyListMsg(self, lBuddy):
		lst = []
		for iBuddyNo in lBuddy:
			oMsg = buddy_pb2.baseInfo()
			oBuddy = self.getFriendBuddy(iBuddyNo)
			if oBuddy:
				oMsg.iBuddyNo = oBuddy.iNo
				oMsg.iFriendId = iBuddyNo
			else:
				oMsg.iBuddyNo = iBuddyNo
			lst.append(oMsg)

		return lst

	def getMajorMsg(self):
		lst = []
		for kind,score in self.majorList.iteritems():
			msg = buddy_pb2.majorMsg()
			msg.buddyType = descKindList[kind]
			msg.score = score
			lst.append(msg)
		return lst

	def getTeamBuddyListMsg(self,who):  #组队伙伴列表
		buddyList = self.getBuddyListByIdx(self.currentIdx)
		oMsg = buddy_pb2.teamBuddyList()
		oMsg.iLevel = who.level
		oMsg.buddyList.extend(self.getBuddyListMsg(buddyList))
		return oMsg

	def hasSameBuddyInBattle(self,iBattleNo,iBuddyNo,iFriendId,iPos):
		buddyList = self.getBuddyListByIdx(iBattleNo)
		for iIdx,iNo in enumerate(buddyList):
			if iIdx == iPos-1:
				continue
			if iNo == iBuddyNo or iNo == iFriendId:
				return True
			oBuddy = self.getFriendBuddy(iNo)
			if oBuddy and oBuddy.no == iBuddyNo:
				return True

		return False


	def inBattle(self,iBattleNo,iBuddyNo):
		'''是否在阵容中
		'''
		buddyList = self.getBuddyListByIdx(iBattleNo)
		return iBuddyNo in buddyList

	def autoChangeBuddy(self, iFriendId):
		'''自动替换超时伙伴
		'''
		for iBattleNo,lBuddy in self.buddyList.iteritems():
			if iFriendId not in lBuddy:
				continue
			index = lBuddy.index(iFriendId)
			for oBuddy in self.getAllValues():
				if oBuddy.no not in lBuddy:
					self.upBattle(iBattleNo,oBuddy.no,index)
					self.rpcUpBattle(iBattleNo,oBuddy.no,index)
					break
			else:
				self.downBattle(iBattleNo,index)
				self.rpcDownBattle(iBattleNo,index)

	def upBattle(self,iBattleNo,iBuddyNo,iPos):
		'''上阵
		'''
		buddyList = self.getBuddyListByIdx(iBattleNo)
		if iPos == len(buddyList):
			buddyList.append(iBuddyNo)
		else:
			buddyList[iPos] = iBuddyNo
		self.markDirty()

	def rpcUpBattle(self, iBattleNo, iBuddyNo, iPos):
		oMsg = buddy_pb2.posMsg()
		oMsg.iBattleNo = iBattleNo
		oMsg.iPos = iPos+1
		oBuddy = self.getItem(iBuddyNo)
		if oBuddy:
			oMsg.buddy.iBuddyNo = iBuddyNo
		else:
			oBuddy = self.getFriendBuddy(iBuddyNo)
			if oBuddy:
				oMsg.buddy.iBuddyNo = oBuddy.id
				oMsg.buddy.iFriendId = iBuddyNo

		self.endPoint.rpcUpBattle(oMsg)

	def upFightBattle(self,iBuddyNo):
		'''上阵到使用阵容
		'''
		self.upBattle(self.currentIdx,iBuddyNo,iPos)

	def downBattle(self,iBattleNo,iPos):
		'''下阵
		'''
		buddyList = self.getBuddyListByIdx(iBattleNo)
		buddyList.pop(iPos)
		self.markDirty()

	def rpcDownBattle(self,iBattleNo,iPos):
		self.endPoint.rpcDownBattle(iBattleNo,iPos+1)

	def setBattle(self,iNo):
		'''设置使用阵容
		'''
		self.currentIdx = iNo
		self.markDirty()

	def setLineup(self, idx, lineupId):
		'''设置阵法
		'''
		self.lineupList[idx] = lineupId
		self.markDirty()

	def getCurrentLineup(self):
		'''当前阵容的阵法
		'''
		lineupId = self.lineupList.get(self.currentIdx, 0)
		if lineupId:
			who = getRole(self.ownerId)
			if who:
				return who.lineupCtn.getItem(lineupId)
		return None

	def getMaxPrice(self, iLevel):
		'''累积上限
		'''
		return buddyData.getMax("累积上限",iLevel)

	def getDayMaxPrice(self, iLevel):
		'''每日上限
		'''
		return buddyData.getMax("每日上限",iLevel)

	def getPrice(self):
		'''获得租金
		'''
		return self.price

	def addPrice(self, iPrice, iLevel):
		'''增加租金
		'''
		self.markDirty()
		self.price += iPrice
		iMaxPrice = self.getMaxPrice(iLevel)
		if self.price > iMaxPrice:
			self.price = iMaxPrice

	def getRentMsg(self):
		'''获得租借信息
		'''
		return self.rentMsg

	def addRentMsg(self, iTime, sRoleName, sBuddyName, iPrice):
		'''增加租借信息
		'''
		self.markDirty()
		self.rentMsg.append((iTime,sRoleName,sBuddyName,iPrice))
		if len(self.rentMsg) > 50:
			self.rentMsg.pop(0)

from common import *
import sql
import factoryConcrete
import buddy
import buddy_pb2
import message
import buddyData
import mainService
import buddy.service
import config
import jitKeeper
import factory
import cycleData

def getBuddyCtn(iRoleId):
	return gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE, iRoleId)

descKindList = {
	"物攻型":1,
	"法攻型":2,
	"治疗型":3,
	"辅助型":4,
	"封印型":5,
}

#用于查看离线玩家的包裹/装备信息.一段时间后不访问,自动从容器上移除
if 'gKeeper' not in globals():
	KEEP_SECOND=30 if config.IS_INNER_SERVER else 60*5
	# gKeeper=productKeeper.cJITproductKeeper(factoryConcrete.friendCtnFtr,KEEP_SECOND)	临时屏蔽,测试jitKeeper
	gKeeper=jitKeeper.cJITproductKeeper(factoryConcrete.buddyCtnFtr)
