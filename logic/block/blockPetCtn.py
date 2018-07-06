# -*- coding: utf-8 -*-
import ctn
import block

MAX_DEFAULT = 50 # 宠物数默认上限
MAX_CARRY= 8 # 携带数上限


class cPetContainer(ctn.cContainerBase,block.cCtnBlock):
	def __init__(self, iOwnerId):
		block.cCtnBlock.__init__(self,'宠物容器',iOwnerId)
		ctn.cContainerBase.__init__(self,iOwnerId)
		self.setIsStm(sql.PET_CTN_INSERT)
		self.setDlStm(sql.PET_CTN_DELETE)
		self.setUdStm(sql.PET_CTN_UPDATE)
		self.setSlStm(sql.PET_CTN_SELECT)

		self.carryList = [] # 携带的宠物
		self.fighter = 0 # 参战宠物的id
		self.expandSize = 0 # 扩展大小
	
	def _dirtyEventHandler(self):#override
		factoryConcrete.petCtnFtr.schedule2tail4save(self.ownerId)

	def save(self):#override
		dData=ctn.cContainerBase.save(self)
		dData["carryList"] = self.carryList
		dData["fighter"] = self.fighter
		dData["expandSize"] = self.expandSize
		return dData
	
	def load(self,dData):#override  
		ctn.cContainerBase.load(self,dData)
		self.carryList = dData.pop("carryList", [])
		self.fighter = dData.pop("fighter", 0)
		self.expandSize = dData.pop("expandSize", 0)

	def _createAndLoadItem(self,iIndex,uData):#override
		idx, dData = uData
		return pet.createAndLoad(dData)
	
	def _saveItem(self,iIndex,obj):#override
		return obj.idx, obj.save()

	def _rpcAddItem(self,obj):#override
		who = self.getOwnerObj()
		pet.service.rpcPetAdd(who, obj)
	
	def _rpcRemoveItem(self,obj):#override
		self.endPoint.rpcPetDel(obj.id)

	def _rpcRefresh(self):
		who = self.getOwnerObj()
		pet.service.rpcPetList(who)

	@property
	def endPoint(self):
		import mainService
		return mainService.getEndPointByRoleId(self.ownerId)
	
	def itemCountMax(self):
		'''宠物数上限
		'''
		return MAX_DEFAULT + self.expandSize
	
	def carryCount(self):
		'''携带数
		'''
		return len(self.carryList)
	
	def carrayCountMax(self):
		'''携带上限
		'''
		return MAX_CARRY

	def expand(self, size=1):
		'''扩展大小
		'''
		self.markDirty()
		self.expandSize += size
		# toDo 刷新客户端
		
	def setFighter(self, petObj, isFighter):
		'''参战或休息
		'''
		petId = petObj.id
		if isFighter:
			if petId == self.fighter:
				return
			if self.fighter: # 把旧参战宠取消
				oldFightPet = self.getItem(self.fighter)
				if oldFightPet:
					self.setFighter(oldFightPet, False)
			self.fighter = petId
			petObj.attrChange("fighter")
			
		else:
			if petId != self.fighter:
				return
			self.fighter = 0
			petObj.attrChange("fighter")
		
		self.markDirty()
		
	def getFighter(self):
		'''获取参战宠物
		'''
		if self.fighter:
			return self.getItem(self.fighter)
		return None
		
	def isFighter(self, petId):
		'''是否参战中
		'''
		return petId == self.fighter
		
	def setCarry(self, petObj, isCarry):
		'''设置或撤消携带
		'''
		petId = petObj.id
		if isCarry: #携带
			if petId in self.carryList:
				return
			self.carryList.append(petId)
		else: # 撤消携带
			if petId not in self.carryList:
				return
			self.carryList.remove(petId)
		self.markDirty()
		petObj.attrChange("carry")
		
	def isCarry(self, petId):
		'''是否携带中
		'''
		return petId in self.carryList
	
	def hasPetByIdx(self, petIdx):
		'''是否有指定编号的宠物
		'''
		for petObj in self.getAllValues():
			if petObj.idx == petIdx:
				return petObj
		return None
	
	def getFirstCarry(self):
		'''获取携带的第一个异兽
		'''
		for petId in self.carryList:
			petObj = self.getItem(petId)
			if petObj:
				return petObj
		
		return None


import sql
import factoryConcrete
import c
import u
import pet
import pet_pb2
import props
import log
import role
import pet.service