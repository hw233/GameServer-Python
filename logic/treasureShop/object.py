#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import block.singleton
import config
import pst

TIME_SHOW = 4*60*60  #公示时间 4小时
TIME_SELL = 7*24*60*60 #上架时间 七天
TIME_CHECK = 1*24*60*60 #审核 一天
TIME_STOP = 4 * 60 * 60 #停市期 4小时

SELL_BORAD = 1  #出售板
SHOW_BORAD = 2  #公示板

SELL_ING  = 1 #上架中
SELL_SHOW = 2  #公示
SELL_OUT = 3  #已过期
SELL_CHECK = 4 #审核
SELL_MONEY = 5 #提现

ITEM_COUNT = 8 #摊位数

#珍品阁
class cTreasureShop(block.singleton.cSingleton):
	def __init__(self):#override
		block.singleton.cSingleton.__init__(self,'珍品阁','treasureShop')
		self.goodsList = {} #物品列表 
		self.goodsListByRoleId = {}  #物品玩家排序  {玩家Id:摊位obj}
		self.goodsListByTime = []  #商品时间排序
		self.goodsListByType = {SELL_BORAD:{},SHOW_BORAD:{}}  #商品分类排序  {状态:{商品的编号:[商品Id]}
		self.attentionListByRole = {SELL_BORAD:{},SHOW_BORAD:{}}  #玩家关注 {状态:{roleId:[商品id]}}
		self.priceList = {} #价格列表，玩家可以提取的金额。{玩家Id:价格}
		self.oTimerMng = timer.cTimerMng()#定时器,下架物品用
		self.uTimerId = 0

	def __updateTimer(self):#更新定时器
		if self.uTimerId:#先删除已注册的定时器
			self.oTimerMng.cancel(self.uTimerId)
			self.uTimerId=0
		if not self.goodsListByTime:#物品交易中心没有物品了,不需要定时器来下架物品
			return
		iStallId=self.goodsListByTime[0] #最早应该下架的物品id

		nowSeconds=getSecond()
		downTime=self.getDownTime(iStallId)
		if nowSeconds>=downTime:#已经超时,立马下架
			self.__timeOut()
		else:
			delay=downTime-nowSeconds
			self.uTimerId=self.oTimerMng.run(self.__timeOut,delay)#起一个更早的定时器

	def __timeOut(self):#时间到,定时器触发
		self.uTimerId=0 #标志没有定时器了
		if not self.goodsListByTime:#没有商品了,不需要下架处理
			return
		nowSeconds=getSecond()
		for iIndex,iStallId in enumerate(self.goodsListByTime):
			if nowSeconds<self.getDownTime(iStallId):#还没有超时
				break
		else:#全部都超时了
			iIndex+=1 #pass the end
		#[0,iIndex)都是超时要下架的单
		for iStallId in self.goodsListByTime[:iIndex]:#这些都是超时了的,一次性下架多个.
			dGoods = self.goodsList[iStallId]
			if dGoods["status"] == SELL_ING:
				self.updateStatus(iStallId,SELL_OUT)
			elif dGoods["status"] == SELL_SHOW:
				self.updateStatus(iStallId,SELL_ING)
			else:
				self.updateStatus(iStallId,SELL_MONEY)

		self.__updateTimer()#启动下一个定时器

	def __genId(self):#生成每个商品的唯一id,保证合区也不会冲突
		self.markDirty()
		global giId
		giId=u.guIdWithPostfix(config.ZONE_NO,giId,True)
		#todo:检查生成的id是否已经被占用
		return giId

	def addGoods(self,iRoleId,obj,iPrice,lAttention,iStart=0,iTtemId=0,iStatus=SELL_SHOW,bNewGoods=True):#增加一个物品(也增加各种索引表)
		iStallId=self.__genId()
		if not iStart:
			iStart=self.getStartTime()
		if not iTtemId:
			iTtemId=self.getFreeItemId(iRoleId)

		dGoods={}
		dGoods['obj']=obj
		dGoods['price']=iPrice
		dGoods['start']=iStart
		dGoods['ownerId']=iRoleId
		dGoods['itemId']=iTtemId
		dGoods["status"]=iStatus
		dGoods["attention"]=lAttention

		self.goodsList[iStallId]=dGoods #要先加到主表上去,下面几个二分插入都依赖于这个主表
		# to do添加玩家物品索引
		
		if iStatus in (SELL_ING,SELL_SHOW) : #上架中的 物品才要加到其他列表中
			iGoodsType = treasureShop.getGoodsNo(dGoods["obj"])
			listByType = self.goodsListByType[iStatus]
			#物品价格索引，按类型分别存放
			lId=listByType.setdefault(iGoodsType,[])
			findSort.binaryInsertRight(lId,iStallId,self.__priceComparer,self.__timeComparer)
			findSort.binaryInsertRight(self.goodsListByTime,iStallId,self.__timeComparer)

			for iAttRoleId in lAttention:
				lst = self.attentionListByRole[iStatus].setdefault(iAttRoleId,[])
				lst.append(iStallId)

		if iStatus == SELL_CHECK:
			findSort.binaryInsertRight(self.goodsListByTime,iStallId,self.__timeComparer)		

		if iStatus == SELL_MONEY:
			self.priceList[iRoleId] = self.priceList.get(iRoleId,0) + iPrice

		dGoodsByRole = self.goodsListByRoleId.setdefault(iRoleId,{})
		dGoodsByRole[iTtemId] = iStallId

		if bNewGoods:
			self.__updateTimer()
			self.markDirty()

		return iStallId

	def removeGoods(self,iStallId):#移除物品(也移除索引表相应的物品信息)
		dGoods=self.goodsList[iStallId]

		#-------------------------------
		iGoodsType = treasureShop.getGoodsNo(dGoods["obj"])
		iStatus = dGoods["status"]

		if iStatus in (SELL_ING,SELL_SHOW): #只有在出售或者公示期的才会移除。
			self.removeGoodsFromTypeList(iStatus,iGoodsType,iStallId)
			self.removeGoodsFromTimeList(iStallId)
			self.removeGoodsFromAttentionList(iStallId)

		self.removeGoodsFromRoleList(dGoods["ownerId"],dGoods["itemId"])
		if iStatus == SELL_MONEY:
			iRoleId = dGoods["ownerId"]
			iPrice = self.priceList[iRoleId] - dGoods["price"]
			if not iPrice:
				self.priceList.pop(iRoleId)
			else:
				self.priceList[iRoleId] = iPrice

		self.goodsList.pop(iStallId,None)#这个要放在最后,因为上面几个移除依赖于这个数据结构

		self.markDirty()
		return dGoods

	def updateStatus(self, iStallId, iStatus):
		'''更新状态
		'''
		dGoods = self.goodsList.get(iStallId)
		if not dGoods:
			return
		oldStatus = dGoods["status"]
		if iStatus == SELL_ING:
			self.removeGoods(iStallId)
			self.addGoods(dGoods["ownerId"],dGoods["obj"],dGoods["price"],dGoods["attention"],iStatus=SELL_ING,bNewGoods=False)
		elif iStatus == SELL_OUT:
			iGoodsType = treasureShop.getGoodsNo(dGoods["obj"])
			self.removeGoodsFromTypeList(oldStatus,iGoodsType,iStallId)
			self.removeGoodsFromTimeList(iStallId)
			self.removeGoodsFromAttentionList(iStallId)
			dGoods["status"] = SELL_OUT
		elif iStatus == SELL_CHECK:
			iGoodsType = treasureShop.getGoodsNo(dGoods["obj"])
			self.removeGoodsFromTypeList(oldStatus,iGoodsType,iStallId)
			self.removeGoodsFromTimeList(iStallId)
			self.removeGoodsFromAttentionList(iStallId)
			iPrice = dGoods["price"]
			dGoods["price"] = int(iPrice*(1-treasureShopData.gdTreasureShopData[iGoodsType]["税率"]))
			dGoods["status"] = SELL_CHECK
			dGoods["start"] = getSecond()
			findSort.binaryInsertRight(self.goodsListByTime,iStallId,self.__timeComparer)
		elif iStatus == SELL_MONEY:		
			self.removeGoodsFromTimeList(iStallId)
			dGoods["status"] = SELL_MONEY
			iRoleId = dGoods["ownerId"]
			self.priceList[iRoleId] = self.priceList.get(iRoleId,0) + dGoods["price"]
			treasureShop.service.sendMailToSeller(dGoods)
			who = getRole(iRoleId)
			if who:
				who.endPoint.rpcTSItemListMod(self.priceList[iRoleId])

		self.markDirty()

	def removeGoodsFromTypeList(self, iStatus, iGoodsType, iStallId):
		'''从分类列表移除
		'''
		listByType = self.goodsListByType[iStatus]
		lId=listByType.get(iGoodsType,[])
		iIndex1=findSort.binarySearchLeft(lId,iStallId,self.__priceComparer)
		iIndex2=findSort.binarySearchRight(lId,iStallId,self.__priceComparer)
		for iIndex in xrange(iIndex1,iIndex2):#这个区间的物品价格是相同的,只能按物品id再遍历一下
			if lId[iIndex]==iStallId:
				lId.pop(iIndex)
				break
		else:
			raise Exception,'不可能找不到的,哪里数据不一致了吗?'

	def removeGoodsFromTimeList(self, iStallId):
		'''从时间列表移除
		'''
		iIndex1=findSort.binarySearchLeft(self.goodsListByTime,iStallId,self.__timeComparer)
		iIndex2=findSort.binarySearchRight(self.goodsListByTime,iStallId,self.__timeComparer)
		for iIndex in xrange(iIndex1,iIndex2):#这个区间的物品下架时间是相同的,只能按物品id再遍历一下
			if self.goodsListByTime[iIndex]==iStallId:
				self.goodsListByTime.pop(iIndex)
				break
		else:
			raise Exception,'不可能找不到的,哪里数据不一致了吗?'

	def removeGoodsFromAttentionList(self, iStallId):
		'''从关注列表移除
		'''
		dGoods = self.goodsList[iStallId]
		iStatus = dGoods["status"]
		for iAttRoleId in dGoods["attention"]:
			lst = self.attentionListByRole[iStatus][iAttRoleId]
			if iStallId in lst:
				lst.remove(iStallId)

	def __priceComparer(self,iStallId1,iStallId2):#物品价格比较器,排序用
		if iStallId1 not in self.goodsList or iStallId2 not in self.goodsList:
			return 0 #避免抛异常,找不到就认为相同就好了 (在查询结果中再次筛选时,可能某个物品已被购买或下架)
		iPrice1=self.goodsList[iStallId1]['price']
		iPrice2=self.goodsList[iStallId2]['price']
		if iPrice1==iPrice2:
			return 0
		return 1 if iPrice1>iPrice2 else -1

	def __timeComparer(self,iStallId1,iStallId2):#时间比较器,从小到大排序(从早到晚排)
		if iStallId1 not in self.goodsList or iStallId2 not in self.goodsList:
			return 0 #避免抛异常,找不到就认为相同就好了 (在查询结果中再次筛选时,可能某个物品已被购买或下架)
		iStart1=self.getDownTime(iStallId1)
		iStart2=self.getDownTime(iStallId2)
		if iStart1==iStart2:
			return 0
		return 1 if iStart1>iStart2 else -1

	def getStartTime(self):
		iNow = getSecond()
		iHour = getDatePart(iNow,"hour")
		if 20 <= iHour < 24:
			return iNow + TIME_STOP
		elif 0 <= iHour < 4:
			return self.getOpenShowTime(iNow)

		return iNow

	def getShowTime(self, iStallId, iNow):
		dGoods = self.getGoods(iStallId)
		if dGoods:
			iStatus = dGoods["status"]
			if iStatus != SELL_SHOW:
				return self.getDownTime(iStallId) - iNow
			nowHour = getDatePart(iNow,"hour")
			if 0 <= nowHour < 4:
				iNow = self.getOpenShowTime(iNow)
			elif 20 <= nowHour < 24:
				if dGoods["start"] > iNow:
					iNow = iNow + TIME_STOP
			return min(self.getDownTime(iStallId) - iNow,TIME_SHOW)

		return 0

	def getDownTime(self,iStallId):
		dGoods = self.goodsList[iStallId]
		if dGoods["status"] == SELL_ING:
			iDurationTime = TIME_SELL
		elif dGoods["status"] == SELL_SHOW:
			iDurationTime = TIME_SHOW
		else:
			iDurationTime = TIME_CHECK
		return dGoods["start"]+iDurationTime

	def getOpenShowTime(self, iNow):
		'''获得开启公示期的时间
		'''
		import time
		t=time.localtime(iNow)
		return int(time.mktime((t[0],t[1],t[2],4,0,0,0,0,t[8])))

	def onBorn(self):#override
		pass

	def load(self,dData):#override
		block.singleton.cSingleton.load(self,dData)

		for dGoods in dData.pop('goods',[]):
			uData = dGoods["obj"]
			if isinstance(uData,tuple):
				iPropsNo,dPropsData=uData
			else:
				iPropsNo,dPropsData=uData,{}
			obj=props.createAndLoad(iPropsNo,dPropsData)
			self.addGoods(dGoods["ownerId"],obj,dGoods["price"],dGoods["attention"],dGoods["start"],dGoods["itemId"],dGoods["status"],False)
		self.__updateTimer()

	def save(self):#override
		dData=block.singleton.cSingleton.save(self)
		
		lGoods=[]
		for dGoods in self.goodsList.itervalues():
			d = {}
			d.update(dGoods)
			obj = d.pop("obj")
			dPropsData=obj.save()
			if dPropsData:
				uData=obj.no(),dPropsData
			else:
				uData=obj.no()
			d["obj"] = uData
			lGoods.append(d)
		dData['goods']=lGoods

		return dData

	def getGoodList(self, iStatus, iGoodsType):
		'''获得商品列表
		'''
		if iStatus not in self.goodsListByType or iGoodsType not in self.goodsListByType[iStatus]:
			return []
		return self.goodsListByType[iStatus][iGoodsType]

	def getGoods(self, iStallId):
		'''获得商品
		'''
		if iStallId not in self.goodsList:
			return {}
		return self.goodsList[iStallId]

	def hasGoods(self, iStallId):
		dGoods = self.goodsList.get(iStallId)
		if not dGoods:
			return {}
		if dGoods["status"] not in (SELL_ING,SELL_SHOW):
			return {}
		return dGoods

	def getAttentionList(self, iStatus, iRoleId):
		'''获得关注列表
		'''
		lstByRoleId = self.attentionListByRole[iStatus]
		if iRoleId not in lstByRoleId:
			return []

		return lstByRoleId[iRoleId]

	def getRoleItem(self, iRoleId):
		'''获得玩家摊位
		'''
		if iRoleId not in self.goodsListByRoleId:
			return {}
		return self.goodsListByRoleId.get(iRoleId)

	def getPrice(self, iRoleId):
		'''获得玩家可提现金
		'''
		if iRoleId not in self.priceList:
			return 0
		return self.priceList[iRoleId]

	def removeGoodsFromRoleList(self, iRoleId, iTtemId):
		dGoodsByRole = self.goodsListByRoleId.get(iRoleId)
		if not dGoodsByRole or iTtemId not in dGoodsByRole:
			return
		dGoodsByRole.pop(iTtemId)
		if not dGoodsByRole:
			self.goodsListByRoleId.pop(iRoleId)

	def getFreeItemId(self,iRoleId):
		dGoodsByRole = self.goodsListByRoleId.get(iRoleId,{})
		
		for i in xrange(1,ITEM_COUNT+1):
			if i not in dGoodsByRole:
				return i

		return 0

	def setAttention(self, iRoleId, iStallId, isAttention):
		dGoods = self.goodsList[iStallId]
		lst = self.attentionListByRole[dGoods["status"]].setdefault(iRoleId,[])
		if isAttention and iStallId not in lst:
			dGoods["attention"].append(iRoleId)
			lst.append(iStallId)
			message.tips(iRoleId,"关注成功")
		elif not isAttention and iStallId in lst:
			dGoods["attention"].remove(iRoleId)
			lst.remove(iStallId)
			message.tips(iRoleId,"取消关注成功")
		self.markDirty()


#交易板（投诉板）
class cReportBoard(block.singleton.cSingleton):
	def __init__(self):#override
		block.singleton.cSingleton.__init__(self,'珍品阁交易板','reportBoard')
		self.goodsList = {}  #物品列表
		self.goodsListByType = {}  #类型表
		self.goodsListByTime = []  #时间表
		self.reportList = {}  #投诉表
		self.oTimerMng = timer.cTimerMng()#定时器,下架物品用
		self.uTimerId = 0

	def __updateTimer(self):#更新定时器
		if self.uTimerId:#先删除已注册的定时器
			self.oTimerMng.cancel(self.uTimerId)
			self.uTimerId=0
		if not self.goodsListByTime:#物品交易中心没有物品了,不需要定时器来下架物品
			return
		iStallId=self.goodsListByTime[0] #最早应该下架的物品id

		nowSeconds=getSecond()
		downTime=self.getDownTime(iStallId)
		if nowSeconds>=downTime:#已经超时,立马下架
			self.__timeOut()
		else:
			delay=downTime-nowSeconds
			self.uTimerId=self.oTimerMng.run(self.__timeOut,delay)#起一个更早的定时器

	def __timeOut(self):#时间到,定时器触发
		self.uTimerId=0 #标志没有定时器了
		if not self.goodsListByTime:#没有商品了,不需要下架处理
			return
		nowSeconds=getSecond()
		for iIndex,iStallId in enumerate(self.goodsListByTime):
			if nowSeconds<self.getDownTime(iStallId):#还没有超时
				break
		else:#全部都超时了
			iIndex+=1 #pass the end
		#[0,iIndex)都是超时要下架的单
		for iStallId in self.goodsListByTime[:iIndex]:#这些都是超时了的,一次性下架多个.
			self.removeGoods(iStallId)

		self.__updateTimer()#启动下一个定时器

	def __genId(self):#生成每个商品的唯一id,保证合区也不会冲突
		self.markDirty()
		global giId
		giId=u.guIdWithPostfix(config.ZONE_NO,giId,True)
		#todo:检查生成的id是否已经被占用
		return giId

	def addGoods(self, iSellerId, obj, iPrice, iBuyerId, lValidReport, lInvalidReport, iStart=0, bNewGoods=True):
		iStallId=self.__genId()
		if not iStart:
			iStart = getSecond()

		dGoods = {}
		dGoods["sellerId"] = iSellerId
		dGoods["obj"] = obj
		dGoods["price"] = iPrice
		dGoods["buyerId"] = iBuyerId
		dGoods["start"] = iStart
		dGoods["vReport"] = lValidReport
		dGoods["ivReport"] = lInvalidReport

		self.goodsList[iStallId] = dGoods
		iGoodsType = treasureShop.getGoodsNo(dGoods["obj"])
		lId=self.goodsListByType.setdefault(iGoodsType,[])
		findSort.binaryInsertRight(lId,iStallId,self.__priceComparer,self.__timeComparer)
		findSort.binaryInsertRight(self.goodsListByTime,iStallId,self.__timeComparer)

		for iReporterId in lValidReport:
			lst = self.reportList.setdefault(iReporterId,[])
			lst.append(iStallId)

		for iReporterId in lInvalidReport:
			lst = self.reportList.setdefault(iReporterId,[])
			lst.append(iStallId)

		if bNewGoods:
			self.__updateTimer()

		self.markDirty()

	def removeGoods(self, iStallId):
		dGoods=self.goodsList[iStallId]
		iGoodsType = treasureShop.getGoodsNo(dGoods["obj"])
		goodsIdList=self.goodsListByType.get(iGoodsType,[])
		iIndex1=findSort.binarySearchLeft(goodsIdList,iStallId,self.__priceComparer)
		iIndex2=findSort.binarySearchRight(goodsIdList,iStallId,self.__priceComparer)
		for iIndex in xrange(iIndex1,iIndex2):#这个区间的物品价格是相同的,只能按物品id再遍历一下
			if goodsIdList[iIndex]==iStallId:
				goodsIdList.pop(iIndex)
				break
		else:
			raise Exception,'不可能找不到的,哪里数据不一致了吗?'

		#-------------------------------
		iIndex1=findSort.binarySearchLeft(self.goodsListByTime,iStallId,self.__timeComparer)
		iIndex2=findSort.binarySearchRight(self.goodsListByTime,iStallId,self.__timeComparer)
		for iIndex in xrange(iIndex1,iIndex2):#这个区间的物品下架时间是相同的,只能按物品id再遍历一下
			if self.goodsListByTime[iIndex]==iStallId:
				self.goodsListByTime.pop(iIndex)
				break
		else:
			raise Exception,'不可能找不到的,哪里数据不一致了吗?'

		for iReporterId in dGoods["vReport"]:
			self.reportList[iReporterId].remove(iStallId)

		for iReporterId in dGoods["ivReport"]:
			self.reportList[iReporterId].remove(iStallId)

		self.goodsList.pop(iStallId)
		self.markDirty()

	def __priceComparer(self,goodsId1,goodsId2):#物品价格比较器,排序用
		if goodsId1 not in self.goodsList or goodsId2 not in self.goodsList:
			return 0 #避免抛异常,找不到就认为相同就好了 (在查询结果中再次筛选时,可能某个物品已被购买或下架)
		iPrice1=self.goodsList[goodsId1]['price']
		iPrice2=self.goodsList[goodsId2]['price']
		if iPrice1==iPrice2:
			return 0
		return 1 if iPrice1>iPrice2 else -1

	def __timeComparer(self,iStallId1,iStallId2):#时间比较器,从小到大排序(从早到晚排)
		if iStallId1 not in self.goodsList or iStallId2 not in self.goodsList:
			return 0
		iStart1=self.getDownTime(iStallId1)
		iStart2=self.getDownTime(iStallId2)
		if iStart1==iStart2:
			return 0
		return 1 if iStart1>iStart2 else -1

	def getDownTime(self,iStallId):
		dGoods = self.goodsList[iStallId]

		return dGoods["start"]+7*24*60*60

	def load(self,dData):#override
		block.singleton.cSingleton.load(self,dData)

		for dGoods in dData.pop('goods',[]):
			uData = dGoods["obj"]
			if isinstance(uData,tuple):
				iPropsNo,dPropsData=uData
			else:
				iPropsNo,dPropsData=uData,{}
			obj=props.createAndLoad(iPropsNo,dPropsData)
			self.addGoods(dGoods["sellerId"],obj,dGoods["price"],dGoods["buyerId"],dGoods["vReport"],dGoods["ivReport"],dGoods["start"],False)
		self.__updateTimer()

	def save(self):#override
		dData=block.singleton.cSingleton.save(self)
		
		lGoods=[]
		for dGoods in self.goodsList.itervalues():
			d = {}
			d.update(dGoods)
			obj=d.pop("obj")
			dPropsData=obj.save()
			if dPropsData:
				uData=obj.no(),dPropsData
			else:
				uData=obj.no()
			d["obj"] = uData
			lGoods.append(d)
		dData['goods']=lGoods

		return dData

	def getGoodList(self,iGoodsId):
		if iGoodsId not in self.goodsListByType:
			return []

		return self.goodsListByType[iGoodsId]

	def getReportList(self, iRoleId):
		if iRoleId not in self.reportList:
			return []

		return self.reportList[iRoleId]

	def getGoods(self, iStallId):
		if iStallId not in self.goodsList:
			return {}

		return self.goodsList[iStallId]

	def addReport(self, iStallId, who):
		dGoods = self.goodsList[iStallId]
		iRoleId = who.id
		lst = self.reportList.setdefault(iRoleId,[])
		if iStallId not in lst:
			lst.append(iStallId)

		isVaild = self.isVaildReport(who)
		if isVaild:
			lValidReport = dGoods["vReport"]
			if iRoleId not in lValidReport:
				lValidReport.append(iRoleId)
			if len(lValidReport) == 10:
				obj = dGoods["obj"]
				writeLog("treasureShop/report","玩家{}的物品(id:{},name:{})被{}有效投诉" % (who.id,obj.id,obj.name,lValidReport))
		else:
			lInvalidReport = dGoods["ivReport"]
			if iRoleId not in lInvalidReport:
				lInvalidReport.append(iRoleId)

		self.markDirty()

	def isVaildReport(self, who):
		if who.fetch("reportAll") < 4:
			return 1

		return float(who.fetch("reportSuc"))/who.fetch("reportAll") >=0.75


from common import *
import message
import props
import findSort
import mail
import timer
import treasureShop
import treasureShop_pb2
import u
import lineup
import treasureShopData
import treasureShop.service

if 'gbOnce' not in globals():
	gbOnce=True
	
	if 'mainService' in SYS_ARGV:
		giId = 0