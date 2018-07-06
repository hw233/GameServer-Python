#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import ctn
import block

#玩家的包裹之一,普通物品容器
class cPropsContainer(ctn.cContainerBase,block.cCtnBlock):
	def __init__(self,iOwnerId):#override	
		block.cCtnBlock.__init__(self,"普通物品容器",iOwnerId)
		ctn.cContainerBase.__init__(self,iOwnerId)
		self.setIsStm(sql.PROPS_INSERT).setDlStm(sql.PROPS_DELETE)		
		self.setUdStm(sql.PROPS_UPDATE).setSlStm(sql.PROPS_SELECT)
		self.lSpecialProps = []  #特殊物品，不算容量的
		
	def _dirtyEventHandler(self):#override
		factoryConcrete.propsCtnFtr.schedule2tail4save(self.ownerId)

	def _createAndLoadItem(self,iIndex,uData):#override
		iNo,dData=uData
		obj=props.create(iNo)
		obj.load(dData)
		return obj

	def _saveItem(self,iIndex,obj):#override
		return obj.no(),obj.save()

	def _initItem4container(self,obj,uData=None):
		if obj.isTaskProps() or obj.kind == ITEM_BUDDY:
			self.lSpecialProps.append(obj.id)
		return ctn.cContainerBase._initItem4container(self,obj,uData)

	def removeItem(self,obj):
		if obj.isTaskProps() or obj.kind == ITEM_BUDDY:
			self.lSpecialProps.remove(obj.id)
		return ctn.cContainerBase.removeItem(self,obj)

	def capacity(self):#当前总共可用格子数()
		return 20 + self.fetch("row")*5

	def leftCapacity(self):#剩余容量
		return self.capacity()-self.itemCount()+len(self.lSpecialProps)
	
	def validCapacity(self, propsData):
		'''校验容量是否足够
		'''
		count = 0
		for propsNo, amount in propsData.iteritems():
			propsObj = props.getCacheProps(propsNo)
			if propsObj.isVirtual():
				continue
			maxStack = propsObj.maxStack()
			amount = (amount + maxStack - 1) / maxStack
			count += amount
			
		if self.leftCapacity() >= count:
			return True
		return False
	
	def validCapacityByObj(self, propsObjList):
		'''校验容量是否足够
		'''
		count = 0
		for propsObj in propsObjList:
			if propsObj.isVirtual():
				continue
			amount = propsObj.stack()
			maxStack = propsObj.maxStack()
			amount = (amount + maxStack - 1) / maxStack
			count += amount
			
		if self.leftCapacity() >= count:
			return True
		return False
	
	@property
	def endPoint(self):
		return mainService.getEndPointByRoleId(self.ownerId)

	def _rpcAddItem(self,obj):#override
		self.endPoint.rpcAddProps(obj.getMsg4Package(self,*obj.MSG_ALL))

	#override
	def _rpcRefresh(self):
		#默认实现是逐个下发,性能较差.子类可以override,进行优化处理,比如:全部子项拼成一个网络包下发
		# print "===cPropsContainer======_rpcRefresh====="
		allMsg=props_pb2.packageAllItem()
		for obj in self.getAllValues():
			itemMsg = allMsg.allItem.add()
			obj.setMsg4Package(itemMsg, self, *obj.MSG_ALL)
		self.endPoint.rpcAllProps(allMsg)

	def _rpcRemoveItem(self,obj):#override
		self.endPoint.rpcDelProps(obj.id)

	def addStack(self,obj,iAmount):#增加或扣除某个物品的叠加数量
		iBalance=obj.stack()+iAmount
		if iBalance<0:
			raise Exception,'扣除{}扣成负数了,{}个'.format(obj.name,iBalance)
		elif iBalance>obj.maxStack():
			raise Exception,'{}叠加数量超过{}个'.format(obj.name,iBalance)
		obj.setStack(iBalance)
		if iBalance==0:
			self.removeItem(obj)
			#todo 记log跟踪道具流向
		else:
			self.markDirty()
			self.endPoint.rpcModProps(obj.getMsg4Package(self,'stack'))

	def getPropsGroupByNo(self,*tNo):#根据tNo返回子项
		for obj in self.getAllValues():
			if obj.no() in tNo:
				yield obj
				
	def hasPropsByNo(self, propsNo):
		'''返回指定编号的物品
		'''
		for obj in self.getAllValues():
			if obj.no() == propsNo:
				return obj
		return None
	
	def getPropsAmountByNos(self,*tNo):#根据No返回物品数量 (一定返回列表)
		amountList = {}.fromkeys(tNo, 0)
		for obj in self.getAllValues():
			propsNo = obj.no()
			if propsNo not in amountList:
				continue
			amountList[propsNo] += obj.stack()
			
		return [amountList[propsNo] for propsNo in tNo]

	def discardItem(self, obj):
		'''丢弃物品
		'''
		# ToDo检查物品是否可以丢弃
		who = self.getOwnerObj()
		if not who:
			return
		content = "丢弃#C02$item×$number#n？\nQ取消\nQ丢弃".format(obj.name, obj.stack)
		message.confirmBoxNew(who, functor(self.responseDiscard, obj.id), content)
		
	def responseDiscard(self, who, yes, propsId):
		if not yes:
			return
		who = self.getOwnerObj()
		if not who:
			return
		obj = self.getItem(propsId)
		self.removeItem(obj)
		message.tips(who, "丢弃成功")

	def removePropsByNo(self,*tNo):#根据编号移除物品(小心,相同编号物品会全删)
		lRemoveObj = []
		for obj in self.getAllValues():
			if obj.no() in tNo:
				lRemoveObj.append(obj)
		for obj in lRemoveObj:
			self.removeItem(obj)

	def subPropsByNo(self,iNo,iAmount,sLogReason):#搜索包裹,扣除物品,返回实际扣除量
		iLeft=iAmount
		for obj in tuple(self.getAllValues()):
			if obj.no()!=iNo:
				continue
			if iLeft-obj.stack()>0:#不够扣,那一堆全部扣完
				iLeft-=obj.stack()
				self.addStack(obj,-obj.stack())
			else:
				self.addStack(obj,-iLeft)
				iLeft=0
				break
		return iAmount-iLeft


	def subtractPropsByNo(self,iNo,iAmount,sLogReason,sTips=''):#通过编号扣除道具
		oProp=props.getCacheProps(iNo)
		if oProp.isTaskProps():#是任务道具,转到任务专属包裹去
			raise Exception,'是任务道具,不得调用此接口'

		iReal=self.subPropsByNo(iNo,iAmount,sLogReason)
		oProps=props.getCacheProps(iNo)
		if oProps and iReal> 0 and sTips!=None:
			ep=mainService.getEndPointByRoleId(self.ownerId)
			if ep:
				if not sTips:
					sTips='扣除了{}×{}'.format(oProps.name,iReal)
				else:
					sTips=sTips.format(oProps.name,iReal)
				ep.rpcTips(sTips)
		return iReal

	# def calcMaxAdd(self,iNo):#某编号的道具最多能放多少个,商场购买会用到
	# 	oProp=props.new(iNo)

	# 	iMaxStack=oProp.maxStack()
	# 	iLeft=len(self.__getAllEmptyPos())
	# 	iMaxAdd=iMaxStack*iLeft
	# 	if not oProp.canAutoCombine():
	# 		return iMaxAdd
	# 	for obj in self.getPropsGroupByNo(iNo):
	# 		iMaxAdd+=iMaxStack-obj.stack()
	# 	return iMaxAdd

	# def getPropsByKind(self,iKind):#根据类型获取道具
	# 	for obj in self.getAllValues():
	# 		if obj.kind()==iKind:
	# 			yield obj	

	# def _getPos4AddProps(self,oProps):#override 增加道具时,获取一个空的格子
	# 	for iPos in self.__getPosGroup():
	# 		if iPos not in self.dPosMapProps:
	# 			return iPos
	# 	return 0

	# def getPropsAmountByNo(self,*tNo):#根据No返回物品数量
	# 	l=[]
	# 	for iNo in tNo:
	# 		iStack=0
	# 		for obj in self.getAllValues():
	# 			if iNo==obj.no():
	# 				iStack+=obj.stack()
	# 		l.append(iStack)
	# 	return l[0] if len(tNo)==1 else l

	#用指定参数计算能给予玩家的物品数量,返回可以给予个数	
	# def calcCanAddBySpecify(self,iNo,iAmount,bIsBind,*tArgs,**dArgs):
	# 	iAdd=0
	# 	while iAmount>0:
	# 		oProps=props.new(iNo,*tArgs,**dArgs)
	# 		iMaxStack=oProps.maxStack()
	# 		if iAmount>iMaxStack:
	# 			oProps.setStack(iMaxStack)
	# 			iAmount-=iMaxStack
	# 		else:
	# 			oProps.setStack(iAmount)
	# 			iAmount-=iAmount
	# 		if bIsBind and not oProps.isBind():
	# 			oProps.bind()
	# 		#好像有bug,因为道具没有真正塞进包裹,while循环中再次计算能给多少时是错的
	# 		i=self.calcCanAdd(oProps)
	# 		if i==0:
	# 			break
	# 		else:
	# 			iAdd+=i
	# 	return iAdd
		
	# def __getAllEmptyPos(self):
	# 	lEmptyPos=[]
	# 	for iPos in self.__getPosGroup():
	# 		if iPos not in self.dPosMapProps:
	# 			lEmptyPos.append(iPos)
	# 	return lEmptyPos

	#计算能放入包裹的物品个数,返回可以放入的个数	
	# def calcCanAdd(self,oProps):		
	# 	if oProps.isTaskProps():#是宠物道具,转到宠物专属包裹去
	# 		who=role.gKeeper.getObj(self.ownerId)
	# 		who.petPropsCtn.calcCanAdd(oProps)
	# 		return

	# 	iEmptyPos=self.__getEmptyPos()
	# 	if iEmptyPos!=0:#还有空格,全部能放入
	# 		return oProps.stack()
	# 	if not oProps.canAutoCombine():
	# 		return 0
	# 	iNo,iStack=oProps.no(),oProps.stack()
	# 	iLeft=iStack
	# 	for obj in self.getAllValues():
	# 		if obj.no()!=iNo:
	# 			continue
	# 		if obj.stack()>=obj.maxStack():
	# 			continue
	# 		if not obj.canAutoCombine():
	# 			continue
	# 		#走到这里说明可以进行叠加了
	# 		iSpace=obj.maxStack()-obj.stack()
	# 		if iSpace>=iLeft:
	# 			return iStack
	# 		else:
	# 			iLeft-=iSpace
	# 	else:
	# 		return iStack-iLeft		
	
	# def canAllAdd2Package(self,*tProps):#道具是否可以全部放进包裹。检查了能叠加的情况，希望没有写错
	# 	if not tProps:
	# 		return True	

	# 	iEmptyPosAmount=0
	# 	dPropsStack={}
	# 	for iPos in self.__getPosGroup():
	# 		if iPos not in self.dPosMapProps:
	# 			iEmptyPosAmount+=1
	# 		else:
	# 			oProps=self.dPosMapProps[iPos]
	# 			for oItem in lProps:
	# 				if oItem.no()!=oProps.no():
	# 					continue
	# 				if oProps.stack()>=oProps.maxStack():
	# 					continue
	# 				if not oProps.canAutoCombine():
	# 					continue
	# 				if oProps in dPropsStack:
	# 					iStack=dPropsStack.get(oProps)
	# 				else:
	# 					iStack=oProps.stack()
	# 				if oItem.stack()+iStack>oProps.maxStack():
	# 					continue
	# 				#走到这里说明可以进行叠加了
	# 				dPropsStack[oProps]=iStack+oItem.stack()
	# 				iPropsNum-=1#需要放在空位置的道具数量变小了
	# 		if iEmptyPosAmount<iPropsNum:
	# 			return False
		
	# 	return True				
		
	def onBorn(self,*tArgs,**dArgs):#override
		pass

	# def _posComparer(self,iPropId1,iPropId2):
	# 	iWearPos1=self.getItem(iPropId1).wearPos()
	# 	iWearPos2=self.getItem(iPropId2).wearPos()
	# 	if iWearPos1==iWearPos2:
	# 		return 0
	# 	return 1 if iWearPos1>iWearPos2 else -1 #从小到大

	# def _levelComparer(self,iPropId1,iPropId2):
	# 	iUseLv1=self.getItem(iPropId1).level
	# 	iUseLv2=self.getItem(iPropId2).level
	# 	if iUseLv1==iUseLv2:
	# 		return 0
	# 	return 1 if iUseLv1<iUseLv2 else -1 #从大到小

	# def _colorComparer(self,iPropId1,iPropId2):
	# 	iColor1=self.getItem(iPropId1).color()
	# 	iColor2=self.getItem(iPropId2).color()
	# 	if iColor1==iColor2:
	# 		return 0
	# 	return 1 if iColor1<iColor2 else -1

	# def _baseFightComparer(self,iPropId1,iPropId2):
	# 	iBaseFight1=self.getItem(iPropId1).baseFight()
	# 	iBaseFight2=self.getItem(iPropId2).baseFight()
	# 	if iBaseFight1==iBaseFight2:
	# 		return 0
	# 	return 1 if iBaseFight1<iBaseFight2 else -1

	# def _enhanceComparer(self,iPropId1,iPropId2):
	# 	iEnhanceLv1=self.getItem(iPropId1).enhanceLv()
	# 	iEnhanceLv2=self.getItem(iPropId2).enhanceLv()
	# 	if iEnhanceLv1==iEnhanceLv2:
	# 		return 0
	# 	return 1 if iEnhanceLv1<iEnhanceLv2 else -1

	# def _starComparer(self,iPropId1,iPropId2):
	# 	iStarLv1=self.getItem(iPropId1).starLv()
	# 	iStarLv2=self.getItem(iPropId2).starLv()
	# 	if iStarLv1==iStarLv2:
	# 		return 0
	# 	return 1 if iStarLv1<iStarLv2 else -1

	# def _stackComparer(self,iPropId1,iPropId2):
	# 	iStack1=self.getItem(iPropId1).stack()
	# 	iStack2=self.getItem(iPropId2).stack()
	# 	if iStack1==iStack2:
	# 		return 0
	# 	return 1 if iStack1<iStack2 else -1

	# def _fightComparer(self,iPropId1,iPropId2):
	# 	iFightAbility1=self.getItem(iPropId1).calcFightAbility()
	# 	iFightAbility2=self.getItem(iPropId2).calcFightAbility()
	# 	if iFightAbility1==iFightAbility2:
	# 		return 0
	# 	return 1 if iFightAbility1<iFightAbility2 else -1

	# def _kindComparer(self,iPropId1,iPropId2):
	# 	iKind1=self.getItem(iPropId1).kind()
	# 	iKind2=self.getItem(iPropId2).kind()
	# 	if iKind1==iKind2:
	# 		return 0
	# 	return 1 if iKind1>iKind2 else -1

	# def _gemComparer(self,iPropId1,iPropId2):
	# 	oProp1=self.getItem(iPropId1)
	# 	oProp2=self.getItem(iPropId2)
	# 	return props.gem.compareGem(oProp1,oProp2)


def getEquipMsg(iRoleId):
	oPropsCtn=gKeeper.getObjFromDB(factory.NO_ROW_RETURN_NONE,iRoleId)
	msg=package_pb2.propsList()	
	
	for oProp in oPropsCtn.getWearEquipGroup():
		msg.props.extend([oProp.getMsg4Package(*oProp.MSG_FIRST)])
	return msg

import productKeeper
import factoryConcrete
import misc
import jitKeeper
import config

#用于查看离线玩家的包裹/装备信息.一段时间后不访问,自动从容器上移除
if 'gKeeper' not in globals():
	KEEP_SECOND=30 if config.IS_INNER_SERVER else 60*5
	# gKeeper=productKeeper.cJITproductKeeper(factoryConcrete.propsCtnFtr,KEEP_SECOND)	临时屏蔽,测试jitKeeper
	gKeeper=jitKeeper.cJITproductKeeper(factoryConcrete.propsCtnFtr)

import math
import copy
import sql
import props
import log
import c
import u
import mainService
import role

import factory
import findSort
import message
import props_pb2
from common import *
from props.defines import *




