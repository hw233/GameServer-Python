#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import singleton
import misc
import config

if config.IS_INNER_SERVER:
	DURATION=24*60 #架上持续时间(分钟)
else:
	DURATION=24*60 #架上持续时间(分钟)

HISTORY_AMOUNT=10 #保留物品历史价格个数

FEE=1000 #物品上架手续费(元宝)
GOLD_TAX_RATE=10  #卖家获得元宝后扣税的税率(百分点)
PAGE_AMOUNT=10 #每页显示的条数.

#物品交易中心
class cExchange(singleton.cSingleton):
	def __init__(self):#override
		singleton.cSingleton.__init__(self,'道具交易所','propsExchange')
		self.bClose=False
		self.dSellOrderByPropsId={}#物品id:{'obj':物品对象,'price':价钱,'start':挂单时间,'duration':持续时间,'ownerId':主人id}
		self.dSellOrderByPrice={} #物品面板id(类别id):[物品id,物品id,物品id,物品id] #按价格排序		
		self.dOrderByUseLv={} #物品面板id(类别id):[物品id,物品id,物品id,物品id] #按使用等级排序
		self.dSellOrderByRoleId={} #玩家id:set<物品id,物品id,物品id,物品id,物品id>
		self.lSellOrderByTime=[] #里面全是物品id(按下架时间从早到晚排序) #本想使用双端队列collections.deque(),但是不支持pop(index)
		self.dHistory={} #每样物品的最近10件历史价格
		self.oTimerMng=timer.cTimerMng()#定时器,下架物品用
		self.uTimerId=0

	def addHistoryPrice(self,iPropsNo,iPrice,iAmount):#增加成交记录
		deq=self.dHistory.setdefault(iPropsNo,collections.deque())
		deq.append((iPrice,iAmount))
		while len(deq)>HISTORY_AMOUNT:#多了就弹掉,只保留部分历史记录
			deq.popleft()

	def historyAvgPrice(self,iPropsNo):#计算某物品的历史均价		
		i,j=0,0
		for iPrice,iAmount in self.dHistory.get(iPropsNo,()):
			i+=iPrice
			j+=iAmount
		return i/j if j else 0

	def __updateTimer(self):#更新定时器
		if self.uTimerId:#先删除已注册的定时器
			self.oTimerMng.cancel(self.uTimerId)
			self.uTimerId=0
		if not self.lSellOrderByTime:#物品交易中心没有物品了,不需要定时器来下架物品
			return
		iPropsId=self.lSellOrderByTime[0] #最早应该下架的物品id

		iNowMinute=timeU.getMinuteNo()
		iDownShelfMinute=self.getDownShelfTime(iPropsId)
		if iNowMinute>=iDownShelfMinute:#已经超时,立马下架
			self.__downShelf()
		else:
			fDelay=(iDownShelfMinute-iNowMinute)*60#分钟转为秒
			self.uTimerId=self.oTimerMng.run(self.__downShelf,fDelay)#起一个更早的定时器

	def __downShelf(self):#下架时间到,定时器触发
		self.uTimerId=0 #标志没有定时器了
		if self.bClose:#交易所关闭了,中止物品的自动下架
			return
		if misc.gbMaintain:#服务器进入维护状态了,不下架物品
			return
		if not self.lSellOrderByTime:#没有商品了,不需要下架处理
			return
		iCurMinuteNo=timeU.getMinuteNo()
		for iIndex,iPropsId in enumerate(self.lSellOrderByTime):
			if iCurMinuteNo<self.getDownShelfTime(iPropsId):#还没有超时
				break
		else:#全部都超时了
			iIndex+=1 #pass the end
		#[0,iIndex)都是超时要下架的单
		for iPropsId in self.lSellOrderByTime[:iIndex]:#这些都是超时了的,一次性下架多个.
			dGoods=self.dSellOrderByPropsId[iPropsId]

			#下架处理，物品发到用户邮箱
			self.removeGoods(iPropsId)#,'超时下架该物品'
			obj=dGoods['obj']
			iRoleId=dGoods['ownerId']
			log.log('propsExchange','下架时间到了,{}拍卖的物品{}({})下架了'.format(iRoleId,obj.name,obj.dumpsWithNo()))
			log.log('ddic/propsExchange','\t{}\t{}\t{}\t{}'.format(iRoleId,obj.name,dGoods['price'],'超时自动下架'))
			sTitle='交易中心超时下架物品{}'.format(obj.name)
			sContent='交易中心超时下架物品{}'.format(obj.name)
			mail.sendSysMail(iRoleId,sTitle,sContent,None,obj)

		self.__updateTimer()#启动下一个定时器

	def close(self):
		if self.uTimerId:#删除已注册的定时器,停止下架
			self.oTimerMng.cancel(self.uTimerId)
			self.uTimerId=0
		self.bClose=True
		self.markDirty()#关闭后，最后存盘。

	def isClose(self):
		return self.bClose

	def open(self):
		self.__updateTimer()#启动定时器,下架物品
		self.bClose=False
		self.markDirty()

	#稍晚需提供全部下架的接口,合区时全部的物品退回到主人的邮箱里,简化合区的复杂性.

	def addGoods(self,iRoleId,obj,iPrice,iStart,iDuration,bAddNewGoods):#增加一个物品(也增加各种索引表)
		iPropsId=obj.id

		dGoods={}
		dGoods['obj']=obj
		dGoods['price']=iPrice
		dGoods['start']=iStart #上架时间,分钟序号
		dGoods['duration']=iDuration #分钟
		dGoods['ownerId']=iRoleId

		self.dSellOrderByPropsId[iPropsId]=dGoods #要先加到主表上去,下面几个二分插入都依赖于这个主表
		#添加玩家物品索引
		self.dSellOrderByRoleId.setdefault(iRoleId,set()).add(iPropsId)
		
		iPanel=getPanel(obj)#如果返回0,说明是不准再上架此物品了,但启服时从数据库load回来时有这种物品,只能等着超时下架或主动下架,别人是没办法买你的东西的了
		#物品价格索引，按类型分别存放
		lId=self.dSellOrderByPrice.setdefault(iPanel,[])
		findSort.binaryInsertRight(lId,iPropsId,self.priceComparer)
		
		#物品使用等级索引，按类型分别存放
		lId=self.dOrderByUseLv.setdefault(iPanel,[])
		findSort.binaryInsertRight(lId,iPropsId,self.levelComparer)
		
		#物品id列表,按时间排序
		iIndex=findSort.binaryInsertRight(self.lSellOrderByTime,iPropsId,self.downShelfTimeComparer)
		if iIndex==0 and bAddNewGoods:#更新定时器
			self.__updateTimer()
		
		if bAddNewGoods:
			self.markDirty()

	def removeGoods(self,iPropsId):#移除物品(也移除索引表相应的物品信息)
		dGoods=self.dSellOrderByPropsId[iPropsId]
		iRoleId=dGoods['ownerId']

		self.dSellOrderByRoleId[iRoleId].discard(iPropsId)
		if not self.dSellOrderByRoleId[iRoleId]:#空set就pop掉
			self.dSellOrderByRoleId.pop(iRoleId,None)
		#-------------------------------
		iPanel=getPanel(dGoods['obj'])

		lPropsId=self.dSellOrderByPrice[iPanel]
		iIndex1=findSort.binarySearchLeft(lPropsId,iPropsId,self.priceComparer)
		iIndex2=findSort.binarySearchRight(lPropsId,iPropsId,self.priceComparer)
		for iIndex in xrange(iIndex1,iIndex2):#这个区间的物品价格是相同的,只能按物品id再遍历一下
			if lPropsId[iIndex]==iPropsId:
				lPropsId.pop(iIndex)
				break
		else:
			raise Exception,'不可能找不到的,哪里数据不一致了吗?'
		#-------------------------------
		lPropsId=self.dOrderByUseLv.get(iPanel,None)
		if lPropsId:
			iIndex1=findSort.binarySearchLeft(lPropsId,iPropsId,self.levelComparer)#,self.propsIdComparer
			iIndex2=findSort.binarySearchRight(lPropsId,iPropsId,self.levelComparer)
			for iIndex in xrange(iIndex1,iIndex2):#这个区间的装备使用等级是相同的,只能按物品id再遍历一下
				if lPropsId[iIndex]==iPropsId:
					lPropsId.pop(iIndex)
					break
			else:
				raise Exception,'不可能找不到的,哪里数据不一致了吗?'
		#-------------------------------
		iIndex1=findSort.binarySearchLeft(self.lSellOrderByTime,iPropsId,self.downShelfTimeComparer)
		iIndex2=findSort.binarySearchRight(self.lSellOrderByTime,iPropsId,self.downShelfTimeComparer)
		for iIndex in xrange(iIndex1,iIndex2):#这个区间的物品下架时间是相同的,只能按物品id再遍历一下
			if self.lSellOrderByTime[iIndex]==iPropsId:
				self.lSellOrderByTime.pop(iIndex)
				break
		else:
			raise Exception,'不可能找不到的,哪里数据不一致了吗?'
		#-------------------------------
		self.dSellOrderByPropsId.pop(iPropsId,None)#这个要放在最后,因为上面几个移除依赖于这个数据结构
		self.markDirty()
		return dGoods

	def levelComparer(self,iPropsId1,iPropsId2):#装备使用等级比较器,排序用
		if iPropsId1 not in self.dSellOrderByPropsId or iPropsId2 not in self.dSellOrderByPropsId:
			return 0 #避免抛异常,找不到就认为相同就好了 (在查询结果中再次筛选时,可能某个物品已被购买或下架)				
		iUseLv1=self.dSellOrderByPropsId[iPropsId1]['obj'].level
		iUseLv2=self.dSellOrderByPropsId[iPropsId2]['obj'].level
		if iUseLv1==iUseLv2:
			return 0
		return 1 if iUseLv1>iUseLv2 else -1

	def priceComparer(self,iPropsId1,iPropsId2):#物品价格比较器,排序用
		if iPropsId1 not in self.dSellOrderByPropsId or iPropsId2 not in self.dSellOrderByPropsId:
			return 0 #避免抛异常,找不到就认为相同就好了 (在查询结果中再次筛选时,可能某个物品已被购买或下架)
		iPrice1=self.dSellOrderByPropsId[iPropsId1]['price']
		iPrice2=self.dSellOrderByPropsId[iPropsId2]['price']
		if iPrice1==iPrice2:
			return 0
		return 1 if iPrice1>iPrice2 else -1

	def downShelfTimeComparer(self,iPropsId1,iPropsId2):#下架时间比较器,从小到大排序(从早到晚排)
		iDownShelf1=self.getDownShelfTime(iPropsId1)
		iDownShelf2=self.getDownShelfTime(iPropsId2)
		if iDownShelf1==iDownShelf2:
			return 0
		return 1 if iDownShelf1>iDownShelf2 else -1

	def getDownShelfTime(self,iPropsId):#取得某物品的下架时间(分钟序号)
		dGoods=self.dSellOrderByPropsId[iPropsId]
		return dGoods['duration']+dGoods['start']

	def onBorn(self):#override
		pass

	def load(self,dData):#override
		singleton.cSingleton.load(self,dData)
		self.bClose=bool(dData.pop('close',0))

		self.dHistory=dData.pop('his',{})#历史成交记录
		if self.dHistory:
			for iPropNo,l in self.dHistory.iteritems():
				self.dHistory[iPropNo]=collections.deque(l)#把存盘的list转为双端队列

		for tGoods in dData.pop('goods',[]):
			uData,iPrice,iStart,iDuration,iOwnerId=tGoods
			iDuration=DURATION #目前,全部物品的上架持续时间是相同的,所以没有存盘
			if isinstance(uData,tuple):
				iPropsNo,dPropsData=uData
			else:
				iPropsNo,dPropsData=uData,{}
			obj=props.createAndLoad(iPropsNo,dPropsData)
			self.addGoods(iOwnerId,obj,iPrice,iStart,iDuration,False)
		self.__updateTimer()#load完成后,启动定时器下架物品

	def save(self):#override
		dData=singleton.cSingleton.save(self)
		if self.bClose:
			dData['close']=int(self.bClose)#转换成1,节省存储空间
		
		if self.dHistory:#历史成交记录,因json不支持双端队列,要转成list来存储
			dTemp={}
			for iPropsNo,deq in self.dHistory.iteritems():
				dTemp[iPropsNo]=list(deq)
			dData['his']=dTemp

		lGoods=[]
		for dGoods in self.dSellOrderByPropsId.itervalues():
			obj=dGoods['obj']
			dPropsData=obj.save()
			if dPropsData:
				uData=obj.no(),dPropsData
			else:
				uData=obj.no()
			tGoods=uData,dGoods['price'],dGoods['start'],dGoods['duration'],dGoods['ownerId']
			lGoods.append(tGoods)
		dData['goods']=lGoods
		return dData

	def getStartStopStep(self,lPropsId,bAsc,iPage):
		iLen=len(lPropsId)
		if bAsc:#升序			
			iStart=PAGE_AMOUNT*iPage
			iStop=PAGE_AMOUNT*(iPage+1)
			iStop=iStop if iStop<iLen else iLen
			iStep=1 
		else:#降序
			iStart=iLen-1-PAGE_AMOUNT*iPage
			iStop=iLen-1-PAGE_AMOUNT*(iPage+1)
			iStop=iStop if iStop>=-1 else -1
			iStep=-1
		return iStart,iStop,iStep

	def getOtherQuotationMsg(self,iPanel,iTotal,lPropsId):#非装备行情信息
		propsMsgList=auction_pb2.goodsList()
		propsMsgList.iTab=iPanel
		propsMsgList.iMsgType=MSG_NORMAL
		propsMsgList.iMaxPage=(iTotal+PAGE_AMOUNT-1)/PAGE_AMOUNT
		for iPropsId in lPropsId:
			propsMsg=self.getOtherMsg4quotation(iPropsId)
			propsMsgList.sSerialized.append(propsMsg.SerializeToString())
		return propsMsgList

	def getOtherMsg4quotation(self,iPropsId):#非装备某一行数据
		dGoods=self.dSellOrderByPropsId[iPropsId]
		obj=dGoods['obj']
		propsMsg=auction_pb2.normalInfo()
		propsMsg.iPrice=dGoods['price']
		propsMsg.iPropsId=iPropsId
		propsMsg.sName=obj.name
		propsMsg.iStack=obj.stack()
		propsMsg.iPropsIcon=obj.icon()
		propsMsg.iUseLv=obj.level
		return propsMsg

	def getEquipQuotationMsg(self,iPanel,iTotal,lPropsId):#装备行情信息
		propsMsgList=auction_pb2.goodsList()
		propsMsgList.iTab=iPanel
		propsMsgList.iMsgType=MSG_EQUIP
		propsMsgList.iMaxPage=(iTotal+PAGE_AMOUNT-1)/PAGE_AMOUNT
		for iPropsId in lPropsId:			
			propsMsg=self.getEquipMsg4quotation(iPropsId)
			propsMsgList.sSerialized.append(propsMsg.SerializeToString())
		return propsMsgList

	def getEquipMsg4quotation(self,iPropsId):#装备的某一行数据
		dGoods=self.dSellOrderByPropsId[iPropsId]
		obj=dGoods['obj']
		propsMsg=auction_pb2.equipInfo()
		propsMsg.iPrice=dGoods['price']
		propsMsg.iPropsId=iPropsId
		propsMsg.sName=obj.name
		propsMsg.iPropsIcon=obj.icon()
		propsMsg.iUseLv=obj.level
		propsMsg.iQuality=obj.quality()
		propsMsg.iDegree = obj.degree() 
		propsMsg.iStrengThenLv=obj.enhanceLv()
		propsMsg.iColor=obj.color()
		return propsMsg

	def getQuotationByPanel(self,iPanel,iOrderBy,bAsc,iPage):#查看某一类型的卖品行情(某一面板上的物品)
		if iOrderBy==auction_pb2.PRICE:#按价格索引查看
			lPropsId=self.dSellOrderByPrice.get(iPanel,[])
		else: #iOrderBy==auction_pb2.USE_LV按使用等级排序查看
			lPropsId=self.dOrderByUseLv.get(iPanel,[])
		iStart,iStop,iStep=self.getStartStopStep(lPropsId,bAsc,iPage)
		#当前页的物品id
		lCurPagePropsId=[lPropsId[iIndex] for iIndex in xrange(iStart,iStop,iStep)]
		
		iMsgType=getMsgType(iPanel)
		if iMsgType==MSG_EQUIP:#是装备道具
			return self.getEquipQuotationMsg(iPanel,len(lPropsId),lCurPagePropsId)			
		else:#是普通道具
			return self.getOtherQuotationMsg(iPanel,len(lPropsId),lCurPagePropsId)

	def getMyGoods(self,iRoleId):#查看我的架上物品
		sPropsId=self.dSellOrderByRoleId.get(iRoleId,[])
		if not sPropsId:
			return None
		goodsListMsg=auction_pb2.myGoodsList()
		for iPropsId in sPropsId:
			dGoods=self.dSellOrderByPropsId[iPropsId]
			obj=dGoods['obj']
			propsMsg=goodsListMsg.goodsInfo.add()
			propsMsg.iPropsId=iPropsId
			propsMsg.iPropsIcon=obj.icon()
			propsMsg.sName=obj.name
			propsMsg.iPrice=dGoods['price']
			propsMsg.iStack=obj.stack()
			propsMsg.iColor=obj.color() if obj.uiType()==c.PROPS_EQUIP else 0
		return goodsListMsg

	def getPropsById(self,iPropsId):#某一个物品的对象
		dGoods=self.dSellOrderByPropsId.get(iPropsId)
		if not dGoods:
			return None
		return dGoods['obj']

	def getGoodsInfo(self,iPropsId):#用物品id获取某个卖单的信息
		return self.dSellOrderByPropsId.get(iPropsId)

	def searchEquip(self,who,iSchool,iWearPos,lUseLv,lColor,lQuality):#搜索装备
		iPanel=getPanelsByProWearPos(iSchool,iWearPos)
		propsMsgList=auction_pb2.goodsList()
		propsMsgList.iTab=0 #搜索结果都用0
		propsMsgList.iMsgType=MSG_EQUIP
		lPropsId=self.dSellOrderByPrice.get(iPanel,[])
		
		lSearchReult=[]
		for iPropsId in lPropsId:
			dGoods=self.dSellOrderByPropsId[iPropsId]
			oProps=dGoods['obj']
			iUseLv,iColor,iQuality=oProps.level,oProps.color(),oProps.quality()
			if lUseLv and iUseLv not in lUseLv:
				continue
			if lColor and iColor not in lColor:
				continue
			if lQuality and iQuality not in lQuality:
				continue
			lSearchReult.append(iPropsId)
			propsMsg=self.getEquipMsg4quotation(iPropsId)			
			propsMsgList.sSerialized.append(propsMsg.SerializeToString())

		propsMsgList.iMaxPage=(len(lSearchReult)+PAGE_AMOUNT-1)/PAGE_AMOUNT
		return propsMsgList,lSearchReult

	def searchGem(self,who,iPanel,lUseLv):#搜索宝石
		tGemNo=gdPanelMapGemNo[iPanel]
		tGemNo=[tGemNo[iIndex-1] for iIndex in lUseLv]
		
		propsMsgList=auction_pb2.goodsList()
		propsMsgList.iTab=0 #搜索结果都用0
		propsMsgList.iMsgType=MSG_NORMAL
		lPropsId=self.dSellOrderByPrice.get(iPanel,[])
		
		lSearchReult=[]
		for iPropsId in lPropsId:
			dGoods=self.dSellOrderByPropsId[iPropsId]
			oProps=dGoods['obj']
			if tGemNo and oProps.no() not in tGemNo:
				continue
			lSearchReult.append(iPropsId)
			propsMsg=self.getOtherMsg4quotation(iPropsId)
			propsMsgList.sSerialized.append(propsMsg.SerializeToString())
		propsMsgList.iMaxPage=(len(lSearchReult)+PAGE_AMOUNT-1)/PAGE_AMOUNT
		return propsMsgList,lSearchReult

	def searchOtherByKeyword(self,who,sKeyword):#用关键字搜索其他
		propsMsgList=auction_pb2.goodsList()
		propsMsgList.iTab=0 #搜索结果都用0
		propsMsgList.iMsgType=MSG_NORMAL				
		lSearchReult=[]
		for iPanel,lPropsId in self.dSellOrderByPrice.iteritems():			
			if iPanel!=OTHER:
				continue
			for iPropsId in lPropsId:
				dGoods=self.dSellOrderByPropsId[iPropsId]
				oProps=dGoods['obj']				
				if sKeyword	not in oProps.name:
					continue				
				lSearchReult.append(iPropsId)	
				propsMsg=self.getOtherMsg4quotation(iPropsId)
				propsMsgList.sSerialized.append(propsMsg.SerializeToString())							
		
		propsMsgList.iMaxPage=(len(lSearchReult)+PAGE_AMOUNT-1)/PAGE_AMOUNT
		return propsMsgList,lSearchReult

def getPanelsByProWearPos(iSchool,iWearPos):#装备面板编号
	if iWearPos==c.EQUIP_WEAPON:#是武器
		return iWearPos*10+iSchool
	return iWearPos

#各种宝石所在面板
STAGE1_PANEL,STAGE2_PANEL,STAGE3_PANEL,STAGE4_PANEL,STAGE5_PANEL=21,22,23,24,25 #这是与客户端约定好的
gdPanelMapGemNo={
	STAGE1_PANEL:(110,111,112,113,114),
	STAGE2_PANEL:(120,121,122,123,124),
	STAGE3_PANEL:(130,131,132,133,134),
	STAGE4_PANEL:(140,141,142,143,144),
	STAGE5_PANEL:(150,151,152,153,154),
}
gdGemNoMapPanel={}
for iPanel,tNo in gdPanelMapGemNo.iteritems():
	for iNo in tNo:
		gdGemNoMapPanel[iNo]=iPanel

OTHER=101

def getPanel(obj):#根据物品的分类,展现在哪个面板(与客户端约定好了的),返回0表示不知往哪里放好.
	if isinstance(obj,props.equip.cProps):#装备
		iWearPos=obj.wearPos()
		if iWearPos==c.EQUIP_WEAPON:#是武器,要区分职业的
			return iWearPos*10+obj.school
		return iWearPos #以装备孔作面板标识
	elif isinstance(obj,props.gem.cProps):#宝石
		return gdGemNoMapPanel.get(obj.no(),0)
	else:#其他道具(暂时是任意物品都可以上架)
		return OTHER

def getMsgType(iPanel):#行情列表类型,分普通道具,装备道具.各种行情列表列个数与列名是不相同的.
	if iPanel>=101 or iPanel in gdPanelMapGemNo:
		return MSG_NORMAL #普通道具
	return MSG_EQUIP #装备道具

def init():#启服时调用,从数据库中加载
	global gExchange
	gExchange=cExchange()
	if not gExchange._loadFromDB():
		gExchange._insertToDB(*gExchange.getPriKey())

def handleClose(oldFunc):#作用是,捕捉到任何异常都关闭物品交易中心,防止bug造成的影响扩散
	def newFunc(self,ep,who,reqMsg):
		if misc.gbMaintain:#服务器进入维护状态,不允许操作
			return
		if gExchange.isClose():# and not config.IS_INNER_SERVER:#只有生产环境才生效.
			ep.rpcTips('物品交易中心临时关闭.')
			return
		try:
			return oldFunc(self,ep,who,reqMsg)
		except Exception:
			gExchange.close()
			log.log('propsExchange','物品交易中心抛异常,临时关闭')
			raise
	return newFunc

import terminal_main_pb2
import endPoint

#物品交易服务
class cService(terminal_main_pb2.terminal2main):
	@endPoint.result
	@handleClose
	def rpcAuctionUp(self,ep,who,reqMsg):return rpcAuctionUp(self,ep,who,reqMsg)#上架物品

	@endPoint.result
	@handleClose
	def rpcAuctionDown(self,ep,who,reqMsg):return rpcAuctionDown(self,ep,who,reqMsg)#下架物品

	@endPoint.result
	@handleClose
	def rpcAuctionLookByType(self,ep,who,reqMsg):return rpcAuctionLookByType(self,ep,who,reqMsg)#按类型查看物品

	@endPoint.result
	@handleClose
	def rpcAuctionBuy(self,ep,who,reqMsg):return rpcAuctionBuy(self,ep,who,reqMsg)#购买物品

	@endPoint.result
	@handleClose
	def rpcAuctionLookMy(self,ep,who,reqMsg):return rpcAuctionLookMy(self,ep,who,reqMsg)#查看我上架的物品

	@endPoint.result
	@handleClose
	def rpcAuctionLookOnly(self,ep,who,reqMsg):return rpcAuctionLookOnly(self,ep,who,reqMsg)#

	@endPoint.result
	@handleClose
	def rpcAuctionLook(self,ep,who,reqMsg):return rpcAuctionLook(self,ep,who,reqMsg)#

	@endPoint.result
	@handleClose
	def rpcAuctionSearch(self,ep,who,reqMsg):return rpcAuctionSearch(self,ep,who,reqMsg)#搜索物品

def rpcAuctionUp(self,ep,who,reqMsg):#上架物品,以后还会收交易税
	iPropsId,iAmount=reqMsg.iPropsId,reqMsg.iAmount
	iPrice=reqMsg.iPrice
	#iDuration=reqMsg.iDuration #超时时间(暂时物品的超时时间是相同的,不提供差异性)
	iDuration=DURATION #24小时(分钟为单位)
	if iAmount<=0 or iPrice<=0:#外挂在搞鬼
		return False
	obj=who.propsCtn.getItem(iPropsId)
	if not obj:#没有这个物品(可能还是外挂)
		return False
	if obj.stack()<iAmount:#你此物品没那么多(可能还是外挂)
		return False
	iPanel=getPanel(obj)
	if iPanel==0:#这个物品不知往哪放
		ep.rpcTips('{}不能上架出售.'.format(obj.name))
		return False

	if obj.isBind():
		ep.rpcTips('{}是绑定的,不可以上架.'.format(obj.name))
		return False
	if who.gold<FEE:
		ep.rpcTips('您不足{}手续费.'.format(FEE))
		return False
	#if config.IS_INNER_SERVER:
	#	ep.rpcTips('内服提示:上架{}分钟后自动下架'.format(iDuration))
	who.addTradeCash(-FEE,'交易中心上架物品手续费')
	who.propsCtn.addStack(obj,-iAmount)#扣除
	oProps=props.fork(obj,iAmount)#分裂所要的数量出来
	log.log('propsExchange','{}把物品{}({})已{}价格放上拍卖场'.format(who.name,obj.name,obj.dumpsWithNo(),iPrice))
	log.log('ddic/propsExchange', '\t{}\t{}\t{}\t{}'.format(who.id,obj.name,iPrice,'上架'))
	gExchange.addGoods(who.id,oProps,iPrice,timeU.getMinuteNo(),iDuration,True)
	return True

def rpcAuctionDown(self,ep,who,reqMsg):#下架物品
	iPropsId=reqMsg.iValue
	dGoods=gExchange.getGoodsInfo(iPropsId)
	if not dGoods:#可能被别人购买掉了,或被定时器下架了
		return False
	if dGoods['ownerId']!=who.id:#不是你的物品，你不可以下架！
		return False	
	obj=props.fork(dGoods['obj'])
	gExchange.removeGoods(iPropsId)
	#如果不检查包裹并阻止,若是包裹不足,物品会下架到邮箱中.
	log.log('propsExchange','{}下架物品{},{}'.format(who.id,obj.name,obj.dumpsWithNo()))
	log.log('ddic/propsExchange','\t{}\t{}\t{}\t{}'.format(iRoleId,obj.name,dGoods['price'],'玩家主动下架'))
	who.propsCtn.launchProps(obj,'交易中心下架物品{}'.format(obj.name))
	return True

def rpcAuctionLookByType(self,ep,who,reqMsg):#查看某一类型的卖品的行情(某一面板上的物品)
	iPanel=reqMsg.iPropsType
	bAsc=reqMsg.bAsc #降序
	iOrderBy=reqMsg.iOrderBy #排序依据
	iPage=reqMsg.iPage #第n页(从0开始)
	if iOrderBy not in (1,2):
		ep.rpcTips('客户端上传的iOrderBy是{},我只接受1或2.'.format(iOrderBy))
		return
	if iPage<0:
		return
	print 'iPanel={},bAsc={},iOrderBy={},iPage={}'.format(iPanel,bAsc,iOrderBy,iPage)
	if iPanel!=0:#在默认的分类面板上筛选
		respMsg=gExchange.getQuotationByPanel(iPanel,iOrderBy,bAsc,iPage)
		ep.rpcAuctionGoodsList(respMsg)
	else:#在搜索结果中再次筛选,注意:有些道具已经被卖掉/下架了
		iSearchType,lSearchResult=getattr(who,'searchResult',(0,0))
		if not iSearchType:
			return
		if iOrderBy==auction_pb2.PRICE:#按价格再次排序
			lSearchResult.sort(gExchange.priceComparer)
		elif iOrderBy==auction_pb2.USE_LV:#按使用等级再次排序
			lSearchResult.sort(gExchange.levelComparer)

		iStart,iStop,iStep=gExchange.getStartStopStep(lSearchResult,bAsc,iPage)
		#当前页的物品id
		lCurPagePropsId=[lSearchResult[iIndex] for iIndex in xrange(iStart,iStop,iStep)]		
		
		if iSearchType==SEARCH_RESULT_EQUIP:#是装备道具
			respMsg=gExchange.getEquipQuotationMsg(iPanel,len(lSearchResult),lCurPagePropsId)
		else:#是普通道具
			respMsg=gExchange.getOtherQuotationMsg(iPanel,len(lSearchResult),lCurPagePropsId)
		ep.rpcAuctionGoodsList(respMsg)

def rpcAuctionLookMy(self,ep,who,reqMsg):#查看我的架上物品
	respMsg=gExchange.getMyGoods(who.id)
	if not respMsg:
		ep.rpcTips('您没有物品正在出售.')
		return
	ep.rpcAuctionMyGoodsList(respMsg)

def rpcAuctionLookOnly(self,ep,who,reqMsg):#查看自己拍卖物品详细信息(无对比)
	iPropsId=reqMsg.iValue
	dGoods=gExchange.getGoodsInfo(iPropsId)
	if not dGoods:#可能被别人抢购了,或被定时器下架了,或被主人下架了
		ep.rpcTips('物品已被卖出.')
		return
	oProps=gExchange.getPropsById(iPropsId)
	if oProps:
		ep.rpcSendPropsDetail(oProps.getMsg(*oProps.MSG_ALL))

def rpcAuctionLook(self,ep,who,reqMsg):#查看某个卖品的详细信息(有对比)
	iPropsId=reqMsg.iValue
	dGoods=gExchange.getGoodsInfo(iPropsId)
	if not dGoods:#可能被别人抢购了,或被定时器下架了,或被主人下架了
		ep.rpcTips('物品已被卖出.')
		return
	oProps=gExchange.getPropsById(iPropsId)
	if oProps:
		ep.rpcSendPropsDetail(oProps.getMsg(*oProps.MSG_ALL))
	if oProps.uiType()!=c.PROPS_EQUIP:
		return
	onWear=who.propsCtn.getPropsByPos(oProps.wearPos())#装备对比信息
	if onWear:
		ep.rpcSendPropsDetail(onWear.getMsg(*oProps.MSG_ALL))	

def rpcAuctionBuy(self,ep,who,reqMsg):#购买物品
	iRoleId=who.id
	iPropsId=reqMsg.iValue
	dGoods=gExchange.getGoodsInfo(iPropsId)
	if not dGoods:#可能被别人抢购了,或被定时器下架了,或被主人下架了
		ep.rpcTips('没有此出售物品')
		return False
	if who.id==dGoods['ownerId']:
		ep.rpcTips('你不能购买自己上架的物品.')
		return False

	iPrice=dGoods['price']#总价
	if who.gold<iPrice:#你钱不够,买不起啊！
		ep.rpcTips('你的钱不够，买不起！')
		return False
	obj=dGoods['obj']

	iAvgPrice=gExchange.historyAvgPrice(obj.no())
	if iAvgPrice!=0 and iPrice>iAvgPrice:
		sText='{}售价{}元宝,历史平均价是{}元宝,高出了{}元宝,是否继续购买?\nQ是\nQ否'.format(obj.name,iPrice,iAvgPrice,iPrice-iAvgPrice)
		bFail,uMsg=ep.rpcSelectBox(sText)
		if bFail or uMsg.iValue!=0:
			return False
		who=role.gKeeper.getObj(iRoleId)
		if not who:
			return False
		dGoods=gExchange.getGoodsInfo(iPropsId)
		if not dGoods:
			return False
		iPrice=dGoods['price']
		if who.gold<iPrice:
			return False
		obj=props.fork(dGoods['obj'])#分裂所要的数量出来

	#给买家扣除元宝,给买家发放物品,移除商品,再给卖家钱	
	who.addTradeCash(-iPrice,'交易中心购买物品{}'.format(obj.name))#扣买家钱
	who.propsCtn.launchProps(obj,'交易中心购买物品{}'.format(obj.name))
	gExchange.removeGoods(iPropsId)#移除商品,'玩家购买该物品'
	#通过邮箱给卖家钱
	iTaxGold=iPrice*GOLD_TAX_RATE/100 #税费
	if iTaxGold<=0:
		iTaxGold=1
	iIncomeGold=iPrice-iTaxGold #实际所得
	tItems=(c.GOLD, iIncomeGold)
	sTitle='交易中心出售{}'.format(obj.name)
	sContent='您在交易中心挂单出售{}以{}元宝成功卖出,扣除{}税金后得{}'.format(obj.name,iPrice,iTaxGold,iIncomeGold)
	mail.sendSysMail(dGoods['ownerId'],sTitle,sContent,None,tItems)
	log.log('propsExchange','{}已{}钱购买了{}的物品{}({})'.format(who.name,iPrice,dGoods['ownerId'],obj.name,obj.dumpsWithNo()))
	log.log('ddic/propsExchangeBuy','\t{}\t{}\t{}\t{}\t{}'.format(iRoleId,iPrice,dGoods['ownerId'],obj.no(),obj.name))
	gExchange.addHistoryPrice(obj.no(),iPrice,obj.stack())#记录历史
	return True

def rpcAuctionSearch(self,ep,who,reqMsg):
	if reqMsg.HasField('equipSearch'):#搜索装备
		msg=reqMsg.equipSearch
		respMsg,lResultPropsId=gExchange.searchEquip(who,msg.iSchool,msg.iWearPos,msg.useLv,msg.color,msg.quality)
		who.searchResult=SEARCH_RESULT_EQUIP,lResultPropsId #缓存搜索结果
		ep.rpcAuctionGoodsList(respMsg)		
	elif reqMsg.HasField('gemSearch'):#搜索宝石
		msg=reqMsg.gemSearch
		if msg.iKind not in gdPanelMapGemNo:
			return
		respMsg,lResultPropsId=gExchange.searchGem(who,msg.iKind,msg.lv)
		who.searchResult=SEARCH_RESULT_GEM,lResultPropsId #缓存搜索结果
		ep.rpcAuctionGoodsList(respMsg)
	elif reqMsg.HasField('otherSearch'):#按关键字模糊搜索物品
		sKeyword=reqMsg.otherSearch.sKeyword
		if not sKeyword:
			ep.rpcTips('请输入搜索关键字.')
			return
		respMsg,lResultPropsId=gExchange.searchOtherByKeyword(who,sKeyword)	
		who.searchResult=SEARCH_RESULT_OTHER,lResultPropsId
		ep.rpcAuctionGoodsList(respMsg)

#搜索结果类型
SEARCH_RESULT_GEM=1
SEARCH_RESULT_EQUIP=2
SEARCH_RESULT_OTHER=3

MSG_NORMAL=1 #普通道具
MSG_EQUIP=2 #装备

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