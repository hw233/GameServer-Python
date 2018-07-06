#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import block.singleton
import misc
import config

if config.IS_INNER_SERVER:
	DURATION=24*60 #架上持续时间(分钟)
else:
	DURATION=24*60 #架上持续时间(分钟)

FEE=1000 #挂单手续费(元宝)
DIAMOND_TAX_RATE,GOLD_TAX_RATE=5,10  #元宝/元宝税率(百分点)
EXCHANGE_TIME_MAX=5 #每天交易次数上限
GEAR_AMOUNT=4 #档位数量,(盘口显示卖单n档,买单n档)
#钻石交易所
class cExchange(block.singleton.cSingleton):
	def __init__(self):#override
		block.singleton.cSingleton.__init__(self,'钻石交易所','diamondExchange')
		self.dBuyOrderByOrderId={} #买盘 {买单id:{'price':价钱,'amount':购买数量,start':挂单时间,'duration':持续时间,'ownerId':主人id}}
		self.dBuyOrderByRoleId={} #买盘 {玩家id:set<买单id,买单id,买单id,买单id,买单id>}
		self.dBuyOrderByPrice={} #买盘 {价格:deque<买单id,买单id,买单id,买单id>}

		self.dSellOrderByOrderId={} #卖盘 {卖单id:{'price':价钱,'amount':出售数量,start':挂单时间,'duration':持续时间,'ownerId':主人id}}
		self.dSellOrderByRoleId={} #卖盘 {玩家id:set<卖单id,卖单id,卖单id,卖单id,卖单id>}
		self.dSellOrderByPrice={} #卖盘 {价格:deque<卖单id,卖单id,卖单id,卖单id>}

		self.lOrderByTime=[] #订单id列表,按超时时间排序,买盘与卖盘都在一起.[订单id,订单id,订单id,订单id,订单id]

		self.oTimerMng=timer.cTimerMng()#定时器,撤消订单用
		self.uTimerId=0

		self.iLastOrderId=0 #订单id,不存盘
		self.bClosed=False #是否临时关闭钻石交易所

	def getBuyOrderAmountByRoleId(self,iRoleId):#某玩家的买单数量(暂时没用上这个函数)
		return len(self.dBuyOrderByRoleId.get(iRoleId,()))

	def getSellOrderAmountByRoleId(self,iRoleId):#某玩家的卖单数量(暂时没用上这个函数)
		return len(self.dSellOrderByRoleId.get(iRoleId,()))

	def addBuyOrder(self,iRoleId,iPrice,iAmount,iStrike,iStart,iDuration,bCheckTimer):#增加买单
		dOrder={'ownerId':iRoleId,'price':iPrice,'amount':iAmount,'start':iStart,'duration':iDuration}
		if iStrike>0:#已成交数量
			dOrder['strike']=iStrike
		iOrderId=self.genOrderId()
		self.dBuyOrderByOrderId[iOrderId]=dOrder

		self.dBuyOrderByRoleId.setdefault(iRoleId,set()).add(iOrderId)
		self.dBuyOrderByPrice.setdefault(iPrice,collections.deque()).append(iOrderId)
		iIndex=findSort.binaryInsertRight(self.lOrderByTime,iOrderId,self.downShelfMinuteComparer)
		if iIndex==0 and bCheckTimer:#撤单时间要更早,更新定时器
			self.__updateTimer()

	def addSellOrder(self,iRoleId,iPrice,iAmount,iStrike,iStart,iDuration,bCheckTimer):#增加卖单
		dOrder={'ownerId':iRoleId,'price':iPrice,'amount':iAmount,'start':iStart,'duration':iDuration}
		if iStrike>0:#已成交数量
			dOrder['strike']=iStrike

		iOrderId=self.genOrderId()
		self.dSellOrderByOrderId[iOrderId]=dOrder

		self.dSellOrderByRoleId.setdefault(iRoleId,set()).add(iOrderId)
		self.dSellOrderByPrice.setdefault(iPrice,collections.deque()).append(iOrderId)
		iIndex=findSort.binaryInsertRight(self.lOrderByTime,iOrderId,self.downShelfMinuteComparer)
		if iIndex==0:#撤单时间要更早,更新定时器
			self.__updateTimer()

	def removeOrder(self,iOrderId):#移除一个订单信息,买单与卖单都用这个函数移
		#先移按时间排序的数据结构
		iIndex1=findSort.binarySearchLeft(self.lOrderByTime,iOrderId,self.downShelfMinuteComparer)
		iIndex2=findSort.binarySearchRight(self.lOrderByTime,iOrderId,self.downShelfMinuteComparer)
		for iIndex in xrange(iIndex1,iIndex2):#这个区间的订单超时时间是相同的,只能按订单id再遍历一下
			if self.lOrderByTime[iIndex]==iOrderId:
				self.lOrderByTime.pop(iIndex)
				break
		else:
			raise Exception,'不可能找不到的,哪里数据不一致了吗?'
		#检查是不是卖单,是则移
		dOrder=self.dSellOrderByOrderId.pop(iOrderId,None)
		if dOrder:
			iOwnerId,iPrice=dOrder['ownerId'],dOrder['price']
			self.dSellOrderByRoleId[iOwnerId].discard(iOrderId)
			if not self.dSellOrderByRoleId[iOwnerId]:
				self.dSellOrderByRoleId.pop(iOwnerId,None)

			self.dSellOrderByPrice[iPrice].remove(iOrderId)#弹掉这个价位的最早的挂单 popleft
			if not self.dSellOrderByPrice[iPrice]:#这一价位的卖单全部成交了
				self.dSellOrderByPrice.pop(iPrice,None)#清掉这一档位的数据
		#检查是不是买单,是则移
		dOrder=self.dBuyOrderByOrderId.pop(iOrderId,None)
		if dOrder:
			iOwnerId,iPrice=dOrder['ownerId'],dOrder['price']
			self.dBuyOrderByRoleId[iOwnerId].discard(iOrderId)
			if not self.dBuyOrderByRoleId[iOwnerId]:
				self.dBuyOrderByRoleId.pop(iOwnerId,None)

			self.dBuyOrderByPrice[iPrice].remove(iOrderId)#弹掉这个价位的最早的挂单(popleft)
			if not self.dBuyOrderByPrice[iPrice]:#这一价位的买单全部被成交了
				self.dBuyOrderByPrice.pop(iPrice,None)#清掉这一档位的数据

	def downShelfMinuteComparer(self,iOrderId1,iOrderId2):#撤单时间比较器,从小到大排序(从早到晚排)
		iDownShelf1=self.getDownShelfMinute(iOrderId1)
		iDownShelf2=self.getDownShelfMinute(iOrderId2)
		if iDownShelf1==iDownShelf2:
			return 0
		return 1 if iDownShelf1>iDownShelf2 else -1

	def getDownShelfMinute(self,iOrderId):#取得某订单的撤单时间(分钟序号)
		dOrder=self.dBuyOrderByOrderId.get(iOrderId) or self.dSellOrderByOrderId.get(iOrderId)
		return dOrder['start']+dOrder['duration']

	def __updateTimer(self):#更新定时器
		if self.uTimerId:#先删除已注册的定时器
			self.oTimerMng.cancel(self.uTimerId)
			self.uTimerId=0
		if not self.lOrderByTime:#交易中心没有订单了,不需要定时器来取消订单
			return
		iOrderId=self.lOrderByTime[0] #最早应该撤单的订单id
		iNowMinute=timeU.getMinuteNo()
		iDownShelfMinute=self.getDownShelfMinute(iOrderId)
		if iNowMinute>=iDownShelfMinute:#已经超时,立马撤单
			self.__downShelf()
		else:
			fDelay=(iDownShelfMinute-iNowMinute)*60 #分钟转为秒
			self.uTimerId=self.oTimerMng.run(self.__downShelf,fDelay)#起一个更早的定时器

	def __downShelf(self):#撤单时间到,定时器触发
		self.uTimerId=0 #标志没有定时器了
		if self.bClosed:#交易所关闭了,中止自动撤单
			return
		if misc.gbMaintain:#服务器进入维护状态了,不再撤单
			return
		if not self.lOrderByTime:#没有挂单了,不需要撤单处理
			return
		iCurMinuteNo=timeU.getMinuteNo()
		for iIndex,iOrderId in enumerate(self.lOrderByTime):
			if iCurMinuteNo<self.getDownShelfMinute(iOrderId):#还没有超时
				break
		else:#全部都超时了
			iIndex+=1 #pass the end
		#[0,iIndex)都是超时要撤消的单
		for iOrderId in self.lOrderByTime[:iIndex]:#这些都是超时了的,一次性撤单多个.
			dOrder=self.dBuyOrderByOrderId.get(iOrderId)#撤单处理，发到用户邮箱
			if dOrder:#不知是买单还是卖单,要判断才知道
				iAmount=dOrder['amount']
				iStrike=dOrder.get('strike',0)
				iPrice=dOrder['price']
				iRoleId=dOrder['ownerId']
				if iStrike<=0:#全部没有成交
					sTitle='购买钻石超时撤单'
					sContent='你在交易中心挂单以{}价格购买{}钻石,超时未能成交,现在返还{}元宝给你'.format(iPrice,iAmount,iPrice*iAmount)
					mail.sendSysMail(iRoleId,sTitle,sContent,None,(c.GLOD,iPrice*iAmount))
				else:#部分成交
					iHangAmount=iAmount+iStrike #原来挂单的数量
					iTaxDiamond=iStrike*DIAMOND_TAX_RATE/100
					if iTaxDiamond<=0:
						iTaxDiamond=1
					iIncomeDiamond=iStrike-iTaxDiamond
					sTitle='购买钻石交割'
					sContent='你在交易中心挂单以{}价格购买{}钻石,实际成交{}钻石,扣除税费{}钻石,现在给给你{}钻石,并返还尚未成交的{}元宝'.format(iPrice,iHangAmount,iStrike,iTaxDiamond,iIncomeDiamond,iPrice*iAmount)
					mail.sendSysMail(iRoleId,sTitle,sContent,None,(c.GLOD,iPrice*iAmount),(c.DIAMOND,iIncomeDiamond))

			dOrder=self.dSellOrderByOrderId.get(iOrderId)
			if dOrder:#不知是买单还是卖单,要判断才知道
				iAmount=dOrder['amount']
				iStrike=dOrder.get('strike',0)
				iPrice=dOrder['price']
				iRoleId=dOrder['ownerId']

				if iStrike<=0:#全部没有成交
					sTitle='出售钻石超时撤单'
					sContent='你在交易中心挂单以{}价格出售{}钻石,超时超时未能成交,现在返还{}钻石给你'.format(iPrice,iAmount,iAmount)
					mail.sendSysMail(iRoleId,sTitle,sContent,None,(c.DIAMOND,iAmount))
				else:#部分成交
					iHangAmount=iAmount+iStrike #原来挂单的数量
					iTaxGold=iPrice*iStrike*GOLD_TAX_RATE/100
					if iTaxGold<=0:
						iTaxGold=1
					iIncomeGold=iPrice*iStrike-iTaxGold
					sTitle='出售钻石交割'
					sContent='你在交易中心挂单以{}单价出售{}钻石,实际成交{}钻石,扣除税费{}元宝,现在给给你{}元宝,并返还尚未成交的{}钻石'.format(iPrice,iHangAmount,iStrike,iTaxGold,iIncomeGold,iAmount)
					mail.sendSysMail(iRoleId,sTitle,sContent,None,(c.GOLD,iIncomeGold),(c.DIAMOND,iAmount))

			self.removeOrder(iOrderId)

		self.__updateTimer()#启动下一个定时器

	def isClose(self):
		return self.bClosed

	def close(self):
		if self.uTimerId:#删除已注册的定时器,停止自动撤单
			self.oTimerMng.cancel(self.uTimerId)
			self.uTimerId=0
		self.bClosed=True
		self.markDirty()

	def open(self):
		self.__updateTimer()#启动定时器,开启定时撤单
		self.bClosed=False
		self.markDirty()

	#稍晚需提供全部撤单的接口,合区时全部挂单退回到主人的邮箱里,简化合区的复杂性.
	def onBorn(self):#override
		#开新区时,是否需要挂一些伪单,当作引导玩家,引导开盘价??
		pass

	def genOrderId(self):#订单id,不存盘,(买与卖的id都不冲突)
		self.iLastOrderId+=1
		return self.iLastOrderId

	def getBuyOrderAmountByPrice(self,iPrice):#获得某一个档位上的总钻石数量
		deqOrder=self.dBuyOrderByPrice.get(iPrice)
		if not deqOrder:
			return 0
		iAmount=0
		for iOrderId in deqOrder:
			iAmount+=self.dBuyOrderByOrderId[iOrderId]['amount']
		return iAmount

	def getSellOrderAmountByPrice(self,iPrice):#获得某一个档位上的总钻石数量
		deqOrder=self.dSellOrderByPrice.get(iPrice)
		if not deqOrder:
			return 0
		iAmount=0
		for iOrderId in deqOrder:
			iAmount+=self.dSellOrderByOrderId[iOrderId]['amount']
		return iAmount

	def getQuotationMsg(self):#获得钻石行情信息(盘口)
		quotationMsg=exchange_pb2.quotation()
		#卖单价格从低到高,显示最低价格n档的单
		lPrice=self.dSellOrderByPrice.keys()
		lPrice.sort()

		for i in xrange(GEAR_AMOUNT-1,-1,-1):#发给客户端时要按从高价到低价.
			gearMsg=quotationMsg.gearInfo.add()
			gearMsg.iGear=i+1 #档位,1:卖单一档,2:卖单二档,3:卖单三档 ...
			if i<len(lPrice):
				gearMsg.iPrice,gearMsg.iAmount=lPrice[i],self.getSellOrderAmountByPrice(lPrice[i])
			else:
				gearMsg.iPrice,gearMsg.iAmount=0,0 #客户端显示要做特殊处理

		#买单价格从高到低,显示最高价格n档的单
		lPrice=self.dBuyOrderByPrice.keys()
		lPrice.sort(None,None,True)
		for i in xrange(GEAR_AMOUNT):
			gearMsg=quotationMsg.gearInfo.add()
			gearMsg.iGear=-(i+1) #-1:买单一档,-2:买单二档,-3:买单三档 ...
			if i<len(lPrice):
				gearMsg.iPrice,gearMsg.iAmount=lPrice[i],self.getBuyOrderAmountByPrice(lPrice[i])
			else:
				gearMsg.iPrice,gearMsg.iAmount=0,0 #客户端显示要做特殊处理
		return quotationMsg

	def load(self,dData):#override
		block.singleton.cSingleton.load(self,dData)
		self.bClosed=bool(dData.pop('close',0))
		iDuration=DURATION
		for sFlag in ('b','s'):
			for t in dData.pop(sFlag,[]):
				if len(t)==4:#一点也没有成交的单子
					iPrice,iAmount,iStart,iOwnerId=t
					iStrike=0
				else:#单子没有全部成交,只成交了一部分
					iPrice,iAmount,iStart,iOwnerId,iStrike=t
				if sFlag=='b':#买单
					self.addBuyOrder(iOwnerId,iPrice,iAmount,iStrike,iStart,iDuration,False)
				else:#'s' 卖单
					self.addSellOrder(iOwnerId,iPrice,iAmount,iStrike,iStart,iDuration,False)
		self.__updateTimer()#load完后,启动定时器撤消超时订单

	def save(self):#override
		dData=block.singleton.cSingleton.save(self)
		if self.bClosed:
			dData['close']=int(self.bClosed)#转换成1,节省存储空间
		for sKey,dOrderByOrderId in (('b',self.dBuyOrderByOrderId),('s',self.dSellOrderByOrderId)):
			l=[]
			for iOrderId,d in dOrderByOrderId.iteritems():
				if d.get('strike',0)>0:#有部分成交了
					t=d['price'],d['amount'],d['start'],d['ownerId'],d['strike']#,d['duration'] #架上持续时间不存盘
				else:
					t=d['price'],d['amount'],d['start'],d['ownerId']#,d['duration'] #架上持续时间不存盘
				l.append(t)
			if l:
				dData[sKey]=l
		return dData

	def canBuyAmount(self,iOffer,iAmount):#返回可买数量
		lKeys=self.dSellOrderByPrice.keys()
		lKeys.sort()#升序
		iCan=0
		for iPrice in lKeys:
			if iOffer<iPrice:#出价低,没人愿意卖给你
				return iCan
			for iOrderId in self.dSellOrderByPrice[iPrice]:
				iCan+=self.dSellOrderByOrderId[iOrderId]['amount']
				if iCan>=iAmount:#足够了
				 	return iCan
		return iCan

	def canSellAmount(self,iOffer,iAmount):#返回可卖数量
		lKeys=self.dBuyOrderByPrice.keys()
		lKeys.sort(None,None,True)#降序,价格优先,出价格高的买家优先成交
		iCan=0
		for iPrice in lKeys:
			if iOffer>iPrice:#要价高于买家意愿,没人愿意买你的
				return iCan
			for iOrderId in self.dBuyOrderByPrice[iPrice]:
				iCan+=self.dBuyOrderByOrderId[iOrderId]['amount']
				if iCan>=iAmount:#足够了
					return iCan
		return iCan

	def buyDiamond(self,ep,who,iOffer,iTryBuyAmount,iDuration):#购买钻石
		iRoleId=who.id
		lKeys=self.dSellOrderByPrice.keys()
		lKeys.sort()#升序,价格优先,出价低的卖家优先成交
		iLeft=iTryBuyAmount #尚未成交的钻石个数
		iTotalGold=0 #总成交金额(元宝)
		for iPrice in lKeys:
			if iOffer<iPrice:#剩下的单都是不愿意卖给你的了
				break
			if not self.dSellOrderByPrice[iPrice]:#竟然没有单,一般不可能
				continue
			for iOrderId in tuple(self.dSellOrderByPrice[iPrice]):#时间优先,相同价格的情况下,先挂单的卖家优先成交
				dOrder=self.dSellOrderByOrderId[iOrderId]
				iOwnerId,iAmount=dOrder['ownerId'],dOrder['amount']
				iStrikePrice=iPrice #成交价
				if iLeft>=iAmount:#这一个卖单全部买下
					iStrikeAmount=iAmount #本卖单成交数量
					self.removeOrder(iOrderId)
				elif iLeft<iAmount:#这一单只有一部分被买下,因为买够数了
					dOrder['amount']-=iLeft
					dOrder['strike']=iLeft #记录已成交数量,本单全部卖出时再一次性发邮件给卖家
					iStrikeAmount=iLeft #本卖单成交数量
				
				iStrikeGold=iStrikePrice*iStrikeAmount
				
				if iLeft>=iAmount:#本单被卖完了,#用邮件寄钱(元宝)给卖家
					iAllGold=dOrder.get('strike',0)+iStrikeGold #如果是被拆单了,需要加起来
					iTaxGold=iAllGold*GOLD_TAX_RATE/100 #税费
					if iTaxGold<=0:#税费至少要扣1
						iTaxGold=1
					iIncomeGold=iAllGold-iTaxGold #实际收入
					sContent='您在交易中心以单价{}总价{}卖出{}个钻石,扣除税费{}元宝,获得{}元宝'.format(iStrikePrice,iAllGold,iStrikeAmount,iTaxGold,iIncomeGold)
					iHisStrike=dOrder.get('strike',0)
					mail.sendSysMail(iOwnerId,'出售钻石收入',sContent,None,(c.GOLD,iIncomeGold))#

				iTotalGold+=iStrikeGold
				iLeft-=iStrikeAmount
				if iLeft==0:#买够了,没有goto语句,只能单层跳出
					break
			else:
				pass
			#for end
			if iLeft==0:#买够了,没有goto语句,再次跳出
				break
		else:#中途就跳出了,可能是买够了,也可能是价格不合适未能成交,未能全部成交.
			pass
		#for end
		self.markDirty()

		iRealBuyAmount=iTryBuyAmount-iLeft#实际成交的钻石个数
		iTaxDiamond=iRealBuyAmount*DIAMOND_TAX_RATE/100 #买回来的钻石也要扣税
		if iTaxDiamond<=0:
			iTaxDiamond=1
		iRealDiamond=iRealBuyAmount-iTaxDiamond #实际要给玩家的钻石数

		if iLeft<iTryBuyAmount:#有成交
			who.addTradeCash(-iTotalGold,'从交易中心购买钻石')#先扣
			who.addDiamond(iRealDiamond,'从交易中心购买钻石')#再给

		if iLeft>0:#没有全部成交,剩下的转为挂买单
			self.addBuyOrder(iRoleId,iOffer,iLeft,0,timeU.getMinuteNo(),iDuration,True)
		if iLeft==0:
			ep.rpcModalDialog('全部成交,购买了{}个钻石,花费了{}个元宝,平均每钻石用了{}元宝,扣除税费{}钻石'.format(iRealBuyAmount,iTotalGold,iTotalGold/iRealBuyAmount,iTaxDiamond))
		elif iRealBuyAmount>0:
			ep.rpcModalDialog('部分成交,购买了{}个钻石,花费了{}个元宝,平均每钻石用了{}元宝,扣除税费{}钻石,仍有{}个钻石单价{}转为挂买单等待成交.'.format(iRealBuyAmount,iTotalGold,iTotalGold/iRealBuyAmount,iTaxDiamond,iLeft,iOffer))
		else:#没有成交
			ep.rpcModalDialog('没有成交,有{}个钻石单价{}转为挂买单等待成交.'.format(iLeft,iOffer))
		
	def sellDiamond(self,ep,who,iOffer,iTrySellAmount,iDuration):#出售钻石
		iRoleId=who.id
		lKeys=self.dBuyOrderByPrice.keys()
		lKeys.sort(None,None,True)#降序,价格优先,出价高的买家优先成交
		iLeft=iTrySellAmount #尚未成交的钻石个数
		iTotalGold=0 #总成交金额(元宝)
		for iPrice in lKeys:
			if iOffer>iPrice:#你要价高,剩下的单都是不愿意买你的钻石了
				break
			if not self.dBuyOrderByPrice[iPrice]:#竟然没有单,一般不可能
				continue
			for iOrderId in tuple(self.dBuyOrderByPrice[iPrice]):#时间优先,相同价格的情况下,先挂单的买家优先成交
				dOrder=self.dBuyOrderByOrderId[iOrderId]
				iOwnerId,iAmount=dOrder['ownerId'],dOrder['amount']
				iStrikePrice=iPrice #(iOffer+iPrice)/2 #成交价 (别一种方式是以买家价格成交,理解成卖家手误输低了价格.)
				if iLeft>=iAmount:#这一个卖单全部买下
					iStrikeAmount=iAmount #本卖单成交数量
					self.removeOrder(iOrderId)
				elif iLeft<iAmount:#这一单只有一部分被买下,因为买够数了
					dOrder['amount']-=iLeft
					dOrder['strike']=iLeft #记录已成交数量,本单全部买到时再一次性发邮件给买家
					iStrikeAmount=iLeft #本卖单成交数量
				#用邮件寄货物(钻石)给买家
				iStrikeGold=iStrikePrice*iStrikeAmount

				if iLeft>=iAmount:#本单被买完了,#用邮件寄货(钻石)给卖家
					iAllDiamond=dOrder.get('strike',0)+iStrikeAmount #如果是被拆单了,需要加起来
					iTaxDiamond=iAllDiamond*DIAMOND_TAX_RATE/100
					if iTaxDiamond<=0:#税费至少是1钻石
						iTaxDiamond=1
					iIncomeDiamond=iAllDiamond-iTaxDiamond #实际买家所得钻石					
					sContent='您在交易中心以单价{}总价{}买到{}个钻石,扣除税费{}钻石,获得{}钻石'.format(iStrikePrice,iStrikeGold,iStrikeAmount,iTaxDiamond,iIncomeDiamond)
					mail.sendSysMail(iOwnerId,'购买到的钻石',sContent,None,(c.DURATION,iIncomeDiamond))#

				iTotalGold+=iStrikeGold
				iLeft-=iStrikeAmount
				if iLeft==0:#卖完了,没有goto语句,只能单层跳出
					break
			else:
				pass
			#for end
			if iLeft==0:#卖完了,没有goto语句,再次跳出
				break
		else:#中途就跳出了,可能是卖完了,也可能是价格不合适未能成交或未能全部成交.
			pass
		#for end
		self.markDirty()
		iTaxGold=iTotalGold*GOLD_TAX_RATE/100
		if iTaxGold<=0:
			iTaxGold=1
		iRealGold=iTotalGold-iTaxGold
		iRealSellAmount=iTrySellAmount-iLeft#实际成交的钻石个数
		if iLeft<iTrySellAmount:#有成交
			who.addDiamond(-iRealSellAmount,'卖钻石到交易中心所扣')#先扣钻石
			who.addTradeCash(iRealGold,'卖钻石到交易中心所得')#再给元宝

		if iLeft>0:#没有全部成交,剩下的转为挂卖单
			self.addSellOrder(iRoleId,iOffer,iLeft,0,timeU.getMinuteNo(),iDuration,True)
		if iLeft==0:
			ep.rpcModalDialog('全部成交,出售了{}个钻石,得到了{}个元宝,扣除税费{}元宝,平均每钻石换到了{}元宝'.format(iRealSellAmount,iRealGold,iTaxGold,iTotalGold/iRealSellAmount))
		elif iRealSellAmount>0:
			ep.rpcModalDialog('部分成交,出售了{}个钻石,得到了{}个元宝,扣除税费{}元宝,平均每钻石换到了{}元宝,还有{}个钻石单价{}转为挂卖单等待成交.'.format(iRealSellAmount,iRealGold,iTaxGold,iTotalGold/iRealSellAmount,iLeft,iOffer))
		else:#没有成交
			ep.rpcModalDialog('没有成交,有{}个钻石单价{}转为挂卖单等待出售.'.format(iLeft,iOffer))

	def getMyOrderMsg(self,ep,who):#我的订单msg
		iRoleId=who.id
		myOrderMsg=exchange_pb2.myOrder()

		for iOrderId in self.dBuyOrderByRoleId.get(iRoleId,[]):
			dOrder=self.dBuyOrderByOrderId[iOrderId]

			orderMsg=myOrderMsg.orderInfo.add()			
			orderMsg.iOrderId=iOrderId
			orderMsg.iPrice=dOrder['price']
			orderMsg.iAmount=dOrder['amount']+dOrder.get('strike',0)
			orderMsg.iType=1
			orderMsg.sTime=timeU.minuteNo2str(dOrder['start']+dOrder['duration'])

		for iOrderId in self.dSellOrderByRoleId.get(iRoleId,[]):
			dOrder=self.dSellOrderByOrderId[iOrderId]

			orderMsg=myOrderMsg.orderInfo.add()			
			orderMsg.iOrderId=iOrderId
			orderMsg.iPrice=dOrder['price']
			orderMsg.iAmount=dOrder['amount']+dOrder.get('strike',0)
			orderMsg.iType=2
			orderMsg.sTime=timeU.minuteNo2str(dOrder['start']+dOrder['duration'])	

		return myOrderMsg

	def cancelOrder(self,ep,who,iOrderId):#取消我的订单
		iRoleId=who.id
		dOrder=self.dBuyOrderByOrderId.get(iOrderId,None)# or
		if dOrder:
			iOwnerId,iPrice,iAmount,iStrike=dOrder['ownerId'],dOrder['price'],dOrder['amount'],dOrder.get('strike',0)
			self.removeOrder(iOrderId)
			who.addTradeCash(iPrice*iAmount,'交易中心撤单')#未成交的,返还元宝,玩家主动操作的,直接给,不进邮箱
			if iStrike>0:
				iTaxDiamond=iStrike*DIAMOND_TAX_RATE/100
				if iTaxDiamond<=0:
					iTaxDiamond=1
				iIncomeDiamond=iStrike-iTaxDiamond
				who.addDiamond(iIncomeDiamond,'交易中心成交')
		else:
			dOrder=self.dSellOrderByOrderId.get(iOrderId,None)
			if dOrder:
				iOwnerId,iPrice,iAmount,iStrike=dOrder['ownerId'],dOrder['price'],dOrder['amount'],dOrder.get('strike',0)
				self.removeOrder(iOrderId)
				who.addDiamond(iAmount,'钻石交易中心撤单')#未成交的,返还钻石,玩家主动操作的,直接给,不进邮箱
				if iStrike>0:
					iTaxGold=iPrice*iStrike*GOLD_TAX_RATE/100
					if iTaxGold<=0:
						iTaxGold=1
					iIncomeGold=iPrice*iStrike-iTaxGold
					who.addTradeCash(iIncomeGold,'交易中心成交')
		if dOrder:
			ep.rpcTips('撤单成功.')
			return True
		ep.rpcTips('撤单失败.')	
		return False

def handleClose(oldFunc):#作用是,捕捉到任何异常都关闭钻石交易所,防止bug造成的影响扩散
	def newFunc(self,ep,who,reqMsg):
		if misc.gbMaintain:#服务器进入维护状态,不允许操作
			return
		if gExchange.isClose():# and not config.IS_INNER_SERVER:#只有生产环境才生效.
			ep.rpcTips('钻石交易所临时关闭.')
			return False
		try:
			return oldFunc(self,ep,who,reqMsg)
		except Exception:
			gExchange.close()
			log.log('diamondExchange','钻石交易所抛异常,临时关闭')
			raise
	return newFunc

import terminal_main_pb2
import endPoint
#交易所服务
class cService(terminal_main_pb2.terminal2main):
	@endPoint.result
	@handleClose
	def rpcBuyDiamond(self,ep,who,reqMsg):return rpcBuyDiamond(self,ep,who,reqMsg)#购买钻石

	@endPoint.result
	@handleClose
	def rpcSellDiamond(self,ep,who,reqMsg):return rpcSellDiamond(self,ep,who,reqMsg)#出售钻石

	@endPoint.result
	@handleClose
	def rpcEquipUnBind(self,ep,who,reqMsg):return rpcEquipUnBind(self,ep,who,reqMsg)#装备解绑

	@endPoint.result
	@handleClose
	def rpcLookQuotation(self,ep,who,reqMsg):return rpcLookQuotation(self,ep,who,reqMsg)#查看钻石行情

	@endPoint.result
	@handleClose
	def rpcLookMyOrder(self,ep,who,reqMsg):return rpcLookMyOrder(self,ep,who,reqMsg)#查看我的订单

	@endPoint.result
	@handleClose
	def rpcCancelOrder(self,ep,who,reqMsg):return rpcCancelOrder(self,ep,who,reqMsg)#撤消订单


def rpcLookQuotation(self,ep,who,reqMsg):#查看钻石行情
	ep.rpcQuotation(gExchange.getQuotationMsg())

def rpcBuyDiamond(self,ep,who,reqMsg):#购买钻石
	iPrice=reqMsg.iPrice
	iAmount=reqMsg.iAmount
	iDuration=DURATION
	if iPrice<=0 or iAmount<=0:#外挂
		return False
	#价格太低,低于跌停板,不允许
	
	#if iPrice%1000:
	#	ep.rpcTips('价格必须是1000的整数倍.')
	#	return False
	if iAmount%10:
		ep.rpcTips('购买数量必须必须是10的整数倍.')
		return False
	iExchangeTime=who.day.fetch('exchangeTime',0)
	if iExchangeTime>=EXCHANGE_TIME_MAX:
		ep.rpcTips('对不起，一天最多只能交易{}次'.format(EXCHANGE_TIME_MAX))
		return False
	who.day.add('exchangeTime',1)
	if who.gold<iPrice*iAmount+FEE:#实际有可能是够钱的,因为玩家可能填高价了,但是市场价可能是低的
		ep.rpcTips('您的钱不足以购买{}个钻石.'.format(iAmount))
		return False
	#if config.IS_INNER_SERVER:
	#	ep.rpcTips('内服提示:挂单{}分钟后自动撤单'.format(iDuration))
	#1.全部可以即时成交
	#2.全部不能成交,变为挂买单
	#3.部分可以成交,部分挂买单
	#判断交易次数
	who.addTradeCash(-FEE,'交易中心挂单手续费','扣除了挂单手续费{}元宝.')
	gExchange.buyDiamond(ep,who,iPrice,iAmount,iDuration)	
	return True

def rpcSellDiamond(self,ep,who,reqMsg):#出售钻石
	iPrice=reqMsg.iPrice
	iAmount=reqMsg.iAmount
	iDuration=DURATION
	if iPrice<=0 or iAmount<=0:#外挂
		return False
	#价格太高,高于涨停板,不允许
	#if iPrice%1000:
	#	ep.rpcTips('价格必须是1000的整数倍.')
	#	return False
	if iAmount%10:
		ep.rpcTips('出售钻石的数量必须必须是10的整数倍.')
		return False
	if who.diamond<iAmount:
		ep.rpcTips('您没有这么多钻石可以出售.')
		return False
	#检查交易次数
	iExchangeTime=who.day.fetch('exchangeTime',0)
	if iExchangeTime>=EXCHANGE_TIME_MAX:
		ep.rpcTips('对不起，一天最多只能交易{}次'.format(EXCHANGE_TIME_MAX))
		return False
	if who.gold<FEE:
		ep.rpcTips('您连{}元宝手续费都没有.'.format(FEE))
		return False
	#if config.IS_INNER_SERVER:
	#	ep.rpcTips('内服提示:挂单{}分钟后自动撤单'.format(iDuration))
	who.addTradeCash(-FEE,'交易中心挂单手续费','扣除了挂单手续费{}元宝.')
	gExchange.sellDiamond(ep,who,iPrice,iAmount,iDuration)
	return True

def rpcLookMyOrder(self,ep,who,reqMsg):#查看我的挂单	
	msg=gExchange.getMyOrderMsg(ep,who)
	if len(msg.orderInfo)<=0:
		ep.rpcTips('您没有任何挂单.')
	return msg

def rpcCancelOrder(self,ep,who,reqMsg):#撤单
	pid = who.id
	iOrderId=reqMsg.iValue
	dOrder=gExchange.dBuyOrderByOrderId.get(iOrderId,{})
	if dOrder.get('strike',0)>0:		
		sText='''本买单已经成交{}元宝,尚有{}元宝等待成交,是否撤单?
Q是的,我要撤单
Q不,我继续等待交易'''.format(dOrder['strike'],dOrder['amount'])
		message.selectBoxNew(who, functor(responseCancelOrder, iOrderId), sText)
		
def responseCancelOrder(who, selectNo, iOrderId):
	if selectNo != 1:
		return
	dOrder=gExchange.dSellOrderByOrderId.get(iOrderId,{})
	if dOrder.get('strike',0)>0:
		sText='''本卖单已经成交{}元宝,尚有{}元宝等待成交,是否撤单?
Q是的,我要撤单
Q不,我继续等待交易'''.format(dOrder['strike'],dOrder['amount'])
		message.selectBoxNew(who, functor(responseCancelOrder2, iOrderId), sText)

def responseCancelOrder2(who, selectNo, iOrderId):
	return gExchange.cancelOrder(who.endPoint,who,iOrderId)

def init():
	global gExchange
	gExchange=cExchange()
	if not gExchange._loadFromDB():
		gExchange._insertToDB(*gExchange.getPriKey())

from common import *
import collections
import timer
import timeU
import props
import log
import c
import u
import mail
import findSort
import exchange_pb2
import message
