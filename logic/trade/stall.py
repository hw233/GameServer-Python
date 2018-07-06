#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import block.singleton
import misc
import config
import pst

DURATION = 24*60*60 #上架时间 一天

INIT_COUNT = 8 #初始摊位数

SELL_ING  = 1 #上架中
SELL_OUT = 2  #已过期

#摆摊交易中心
class cExchange(block.singleton.cSingleton):
	def __init__(self):#override
		block.singleton.cSingleton.__init__(self,'摆摊交易中心','stallTrade')
		self.goodsList = {} #物品列表 
		self.goodsListByTime = []  #时间排序
		self.goodsListByType = {}  #物品分类排序  {商品的编号:[物品Id]}
		self.goodsListByRoleId = {}  #物品玩家排序  {玩家Id:摊位obj}
		self.oTimerMng = timer.cTimerMng()#定时器,下架物品用
		self.uTimerId = 0
		self.lastId = 0

	def __updateTimer(self):#更新定时器
		if self.uTimerId:#先删除已注册的定时器
			self.oTimerMng.cancel(self.uTimerId)
			self.uTimerId=0
		if not self.goodsListByTime:#物品交易中心没有物品了,不需要定时器来下架物品
			return
		goodsId=self.goodsListByTime[0] #最早应该下架的物品id

		nowSeconds=getSecond()
		downShelfSeconds=self.getDownShelfTime(goodsId)
		if nowSeconds>=downShelfSeconds:#已经超时,立马下架
			self.__downShelf()
		else:
			delay=downShelfSeconds-nowSeconds#分钟转为秒
			self.uTimerId=self.oTimerMng.run(self.__downShelf,delay)#起一个更早的定时器

	def __downShelf(self):#下架时间到,定时器触发
		self.uTimerId=0 #标志没有定时器了
		if not self.goodsListByTime:#没有商品了,不需要下架处理
			return
		nowSeconds=getSecond()
		for iIndex,goodsId in enumerate(self.goodsListByTime):
			if nowSeconds<self.getDownShelfTime(goodsId):#还没有超时
				break
		else:#全部都超时了
			iIndex+=1 #pass the end
		#[0,iIndex)都是超时要下架的单
		for goodsId in self.goodsListByTime[:iIndex]:#这些都是超时了的,一次性下架多个.
			dGoods=self.goodsList[goodsId]

			self.removeGoods(goodsId)

		self.__updateTimer()#启动下一个定时器

	def __genId(self):#生成每个商品的唯一id,保证合区也不会冲突
		self.markDirty()
		self.lastId=u.guIdWithPostfix(config.ZONE_NO,self.lastId,True)
		#todo:检查生成的id是否已经被占用
		return self.lastId

	#稍晚需提供全部下架的接口,合区时全部的物品退回到主人的邮箱里,简化合区的复杂性.

	def addGoods(self,iRoleId,obj,price,start=0,itemNo=0,status=SELL_ING,bNewGoods=True):#增加一个物品(也增加各种索引表)
		goodsId=self.__genId()
		if not start:
			start=getSecond()
		if not itemNo:
			itemNo=self.getFreeItem(iRoleId)

		dGoods={}
		dGoods['obj']=obj
		dGoods['price']=price
		dGoods['start']=start
		dGoods['ownerId']=iRoleId
		dGoods['itemNo']=itemNo
		dGoods["status"]=status

		self.goodsList[goodsId]=dGoods #要先加到主表上去,下面几个二分插入都依赖于这个主表
		# to do添加玩家物品索引
		
		if status == SELL_ING:#上架中的 物品才要加到其他列表中
			goodsType = trade.getGoodsNo(obj)
			#物品价格索引，按类型分别存放
			lId=self.goodsListByType.setdefault(goodsType,[])
			findSort.binaryInsertRight(lId,goodsId,self.__priceComparer,self.__timeComparer)
			findSort.binaryInsertRight(self.goodsListByTime,goodsId,self.__timeComparer)
		self.addRoleItem(iRoleId,itemNo,goodsId)

		if bNewGoods:
			self.__updateTimer()
		self.markDirty()

	def removeGoods(self,goodsId,bTimeOut=True):#移除物品(也移除索引表相应的物品信息)
		dGoods=self.goodsList[goodsId]

		#-------------------------------
		goodsType = trade.getGoodsNo(dGoods['obj'])

		if dGoods["status"] == SELL_ING:
			goodsIdList=self.goodsListByType.get(goodsType,[])
			iIndex1=findSort.binarySearchLeft(goodsIdList,goodsId,self.__priceComparer)
			iIndex2=findSort.binarySearchRight(goodsIdList,goodsId,self.__priceComparer)
			for iIndex in xrange(iIndex1,iIndex2):#这个区间的物品价格是相同的,只能按物品id再遍历一下
				if goodsIdList[iIndex]==goodsId:
					goodsIdList.pop(iIndex)
					break
			else:
				raise Exception,'不可能找不到的,哪里数据不一致了吗?'

			#-------------------------------
			iIndex1=findSort.binarySearchLeft(self.goodsListByTime,goodsId,self.__timeComparer)
			iIndex2=findSort.binarySearchRight(self.goodsListByTime,goodsId,self.__timeComparer)
			for iIndex in xrange(iIndex1,iIndex2):#这个区间的物品下架时间是相同的,只能按物品id再遍历一下
				if self.goodsListByTime[iIndex]==goodsId:
					self.goodsListByTime.pop(iIndex)
					break
			else:
				raise Exception,'不可能找不到的,哪里数据不一致了吗?'
		#-------------------------------
		if not bTimeOut: #非超时才要移除
			self.removeRoleItem(dGoods["ownerId"],dGoods["itemNo"])
			self.goodsList.pop(goodsId,None)#这个要放在最后,因为上面几个移除依赖于这个数据结构
		else:
			dGoods["status"]=SELL_OUT
		self.markDirty()
		return dGoods

	def __priceComparer(self,goodsId1,goodsId2):#物品价格比较器,排序用
		if goodsId1 not in self.goodsList or goodsId2 not in self.goodsList:
			return 0 #避免抛异常,找不到就认为相同就好了 (在查询结果中再次筛选时,可能某个物品已被购买或下架)
		iPrice1=self.goodsList[goodsId1]['price']
		iPrice2=self.goodsList[goodsId2]['price']
		if iPrice1==iPrice2:
			return 0
		return 1 if iPrice1>iPrice2 else -1

	def __timeComparer(self,goodsId1,goodsId2):#时间比较器,从小到大排序(从早到晚排)
		if goodsId1 not in self.goodsList or goodsId2 not in self.goodsList:
			return 0 #避免抛异常,找不到就认为相同就好了 (在查询结果中再次筛选时,可能某个物品已被购买或下架)
		iStart1=self.getDownShelfTime(goodsId1)
		iStart2=self.getDownShelfTime(goodsId2)
		if iStart1==iStart2:
			return 0
		return 1 if iStart1>iStart2 else -1

	def getDownShelfTime(self,goodsId):
		return self.goodsList[goodsId]["start"]+DURATION

	def onBorn(self):#override
		pass

	def load(self,dData):#override
		block.singleton.cSingleton.load(self,dData)

		for iRoleId,dItems in dData.pop('items',{}).iteritems():
			itemObj=cStallItem(iRoleId)
			itemObj.load(dItems)
			self.goodsListByRoleId[iRoleId]=itemObj

		for tGoods in dData.pop('goods',[]):
			uData,iPrice,iStart,itemNo,iStatus,iOwnerId=tGoods
			if isinstance(uData,tuple):
				iPropsNo,dPropsData=uData
			else:
				iPropsNo,dPropsData=uData,{}
			obj=props.createAndLoad(iPropsNo,dPropsData)
			self.addGoods(iOwnerId,obj,iPrice,iStart,itemNo,iStatus,False)
		self.__updateTimer()

	def save(self):#override
		dData=block.singleton.cSingleton.save(self)
		
		lGoods=[]
		for dGoods in self.goodsList.itervalues():
			obj=dGoods['obj']
			dPropsData=obj.save()
			if dPropsData:
				uData=obj.no(),dPropsData
			else:
				uData=obj.no()
			tGoods=uData,dGoods['price'],dGoods['start'],dGoods['itemNo'],dGoods["status"],dGoods['ownerId']
			lGoods.append(tGoods)
		dData['goods']=lGoods

		dItems={}
		for itemObj in self.goodsListByRoleId.itervalues():
			d=itemObj.save()
			if d:
				dItems[itemObj.iRoleId]=d
		dData['items']=dItems

		return dData

	def addRoleItem(self,iRoleId,itemNo,goodsId):
		itemObj = self.goodsListByRoleId.get(iRoleId)
		if not itemObj:
			itemObj = self.addStallItem(iRoleId)

		itemObj.addGoods(itemNo,goodsId)

	def removeRoleItem(self,iRoleId,itemNo):
		itemObj = self.goodsListByRoleId.get(iRoleId)
		if not itemObj:
			return
		itemObj.removeGoods(itemNo)
		if not itemObj.priceList and not itemObj.goodsList and itemObj.count==INIT_COUNT:
			self.goodsListByRoleId.pop(iRoleId)

	def getFreeItem(self,iRoleId):
		itemObj = self.goodsListByRoleId.get(iRoleId)
		if not itemObj:
			return 1
		for i in xrange(1,itemObj.count+1):
			if i not in itemObj.priceList and i not in itemObj.goodsList:
				return i

		return 0

	def addStack(self,goodsId,stack):
		goodsObj = self.getGoodsObj(goodsId)
		if not goodsObj:
			return
		stack = goodsObj.stack()-stack
		if stack < 0:
			return
		goodsObj.setStack(stack)
		self.markDirty()
		if stack == 0:
			return self.removeGoods(goodsId,False)
		return self.goodsList[goodsId]

	def getGoodsObj(self,goodsId):
		dGoods = self.goodsList.get(goodsId,{})
		return dGoods.get("obj",None)

	def getGoodsPrice(self,goodsId):
		dGoods = self.goodsList.get(goodsId,{})
		return dGoods.get("price",0)

	def getGoodsSeller(self,goodsId):
		dGoods = self.goodsList.get(goodsId,{})
		return dGoods.get("ownerId",0)

	def getStallItemCount(self,iRoleId):
		if iRoleId not in self.goodsListByRoleId:
			return INIT_COUNT
		itemObj = self.goodsListByRoleId[iRoleId]
		return itemObj.count

	def getGoodsItemNo(self,goodsId):
		dGoods = self.goodsList.get(goodsId,{})
		return dGoods.get("itemNo",0)

	def addStallItem(self,iRoleId):
		itemObj = cStallItem(iRoleId)
		itemObj.eDirtyEvent+=self._dirtyEventHandler
		self.goodsListByRoleId[iRoleId] = itemObj		
		return itemObj

	def getGoodListByType(self, goodsType):
		return self.goodsListByType.get(goodsType,[])

	def getGoodCountByType(self, goodsType):
		lst = self.goodsListByType.get(goodsType,[])
		return len(lst)

	def hasProps(self, goodsNo):
		if goodsNo <= 1000000 and self.getGoodCountByType(goodsNo):
			return goodsNo
		if goodsNo > 1000000:
			propsNo = goodsNo%1000000
			lst = tradeGoodsData.gdQualityProps[propsNo]
			lst.sort()
			index = lst.index(goodsNo)
			minGoods = self.getMinPriceGoods(lst[index:])
			if not minGoods:
				minGoods = self.getMinPriceGoods(lst[:index])
			return minGoods

		return 0

	def getMinPriceGoods(self,lst):
		minPrice = 0
		minGoods = 0
		for goodsNo in lst:
			goodsList = self.getGoodListByType(goodsNo)
			if not goodsList:
				continue
			price = self.getGoodsPrice(goodsList[0])
			if not minPrice or price < minPrice:
				minPrice = price
				minGoods = goodsNo
		return minGoods

	def checkCanStall(self):
		'''检查是否可以出售（用于策划导表后删除物品）
		'''
		for goodsType,goodsList in self.goodsListByType.iteritems():
			if goodsType in tradeGoodsData.gdTradeCashGoods:
				continue
			#策划导表后该物品不能出售了，要下架放到玩家邮箱
			for stallId in list(goodsList):
				dGoods = self.removeGoods(stallId,False)
				roleId = dGoods["ownerId"]
				propsObjList = [dGoods["obj"]]
				mail.sendSysMail(roleId,"交易中心","因商品调整，此物品无法继续摆摊出售。",propsObjList)

class cStallItem(pst.cEasyPersist):
	'''摆摊摊位
	'''
	def __init__(self,iRoleId):
		pst.cEasyPersist. __init__(self)
		self.iRoleId = iRoleId
		self.count = INIT_COUNT
		self.priceList = {}
		self.goodsList = {}

	def addGoods(self,iNo, goodsId):
		self.goodsList[iNo] = goodsId

	def removeGoods(self,iNo):
		return self.goodsList.pop(iNo,0)

	def getPriceAll(self):
		iPriceAll = 0
		for iPrice in self.priceList.itervalues():
			iPriceAll += iPrice

		return iPriceAll

	def addPrice(self,iNo, price):
		self.priceList[iNo] = self.priceList.get(iNo,0) + price
		self.markDirty()

	def removePrice(self,iNo):
		self.markDirty()
		return self.priceList.pop(iNo,0)

	def addCount(self,iValue):
		self.count += iValue
		self.markDirty()

	def save(self):
		dData = pst.cEasyPersist.save(self)
		if self.count != INIT_COUNT:
			dData["ct"] = self.count
		if self.priceList:
			dData["pl"] = self.priceList
		return dData

	def load(self,dData):
		pst.cEasyPersist.load(self,dData)
		self.count = dData.pop("ct",INIT_COUNT)
		self.priceList = dData.pop("pl",{})

from common import *
import collections
import copy
import gevent
import c
import u
import props
import props.equip
import props.gem
import findSort
import log
import role
import mail
import misc
import auction_pb2
import timer
import timeU
import trade
import tradeGoodsData