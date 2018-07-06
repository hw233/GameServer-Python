# -*- coding: utf-8 -*-

import block.singleton
import pst

class cCashTradeCenter(block.singleton.cSingleton):
	'''银币交易中心
	'''
	def __init__(self,sChineseName,sName):#override
		block.singleton.cSingleton.__init__(self,sChineseName,sName)
		self.dKeyMapItem = {}

	def init(self):
		lst = []
		for goodsNo in self.dKeyMapItem:
			if goodsNo not in tradeGoodsData.gdCashGoods:
				lst.append(goodsNo)
		for goodsNo in lst:
			self.dKeyMapItem.pop(goodsNo)
		for goodsNo in tradeGoodsData.gdCashGoods:
			obj = self.newItem(goodsNo)
			self.addItem(obj)
		self.markDirty()

	def getItemListBysid(self,sid):
		if sid not in tradeGoodsData.gdCashGoodsList:
			return []

		return tradeGoodsData.gdCashGoodsList[sid]

	def getItem(self,iKey):#根据键值获取子项
		return self.dKeyMapItem.get(iKey,None)

	def addItem(self,obj):
		if obj.key in self.dKeyMapItem:
			return
		self.dKeyMapItem[obj.key] = obj
		obj.eDirtyEvent+=self._dirtyEventHandler

	def save(self):
		dData = block.singleton.cSingleton.save(self)
		dItem = {}
		for goodsNo,obj in self.dKeyMapItem.iteritems():
			dItem[goodsNo] = obj.save()

		dData["item"] = dItem
		return dData

	def load(self,dData):
		block.singleton.cSingleton.load(self,dData)
		for goodsNo,goodsData in dData.pop("item").iteritems():
			obj = self.newItem(goodsNo)
			obj.load(goodsData)
			self.addItem(obj)

	def update(self):
		for obj in self.dKeyMapItem.itervalues():
			obj.update()
		self.markDirty()

	def newItem(self,goodsNo):
		return cCashGoods(goodsNo)

class cTradeCashTradeCenter(cCashTradeCenter):
	'''元宝交易中心
	'''
	def init(self):
		lst = []
		for goodsNo in self.dKeyMapItem:
			if goodsNo not in tradeGoodsData.gdTradeCashGoods:
				lst.append(goodsNo)
		for goodsNo in lst:
			self.dKeyMapItem.pop(goodsNo)
		for goodsNo in tradeGoodsData.gdTradeCashGoods:
			obj = self.newItem(goodsNo)
			self.addItem(obj)
		self.markDirty()

	def getItemListBysid(self,sid):
		if sid not in tradeGoodsData.gdTradeCashGoodsList:
			return []

		return tradeGoodsData.gdTradeCashGoodsList[sid]

	def newItem(self,goodsNo):
		return cTradeCashGoods(goodsNo)

class cCashGoods(pst.cEasyPersist):
	'''银币商品
	'''
	def __init__(self,iNo):
		pst.cEasyPersist. __init__(self)
		self.iNo=iNo
		self.price=0
		self.flushPrice=0
		self.wavePrice=0
		self.waveCount=0

	def getType(self):
		return trade.TYPE_CASH

	def getPrice(self):
		'''基础价格
		'''
		if not self.price:
			return self.getConfig("基础价格")
		return self.price

	def setPrice(self, value):
		'''设置基础价格
		'''
		self.price = value
		self.markDirty()
	
	def getFlushPrice(self):
		'''刷新价格
		'''
		if not self.flushPrice:
			return self.getConfig("基础价格")
		return self.flushPrice

	def setFlushPrice(self, value):
		'''设置刷新价格
		'''
		self.flushPrice = value
		self.markDirty()

	def getWavePrice(self):
		'''波动价格总和
		'''
		return self.wavePrice

	def setWavePrice(self, value):
		'''设置波动价格总和
		'''
		self.wavePrice = value
		self.markDirty()
	
	def getWaveCount(self):
		'''波动数量
		'''
		return self.waveCount

	def setWaveCount(self, value):
		'''设置波动数量
		'''
		self.waveCount = value
		self.markDirty()

	def getRose(self):
		'''涨幅
		'''
		return (self.getPrice()-self.getFlushPrice())/self.getFlushPrice()

	def getBuyCount(self, who):
		'''本周购买数量
		'''
		return who.week.fetch("cbuy%d" % self.iNo)

	def addBuyCount(self, who, count):
		'''增加本周购买数量
		'''
		who.week.add("cbuy%d" % self.iNo,count)

	def getSellCount(self, who):
		'''本周出售数量
		'''
		return who.week.fetch("csell%d" % self.iNo)

	def addSellCount(self, who, count):
		'''增加本周出售数量
		'''
		who.week.add("csell%d" % self.iNo,count)

	def getBuyPrice(self, price=0):
		'''购买价格
		'''
		if not price:
			price = self.getPrice()
		minPrice = self.getConfig("基础价格") * self.getConfig("最小购买系数")
		return max(price * (1-self.getConfig("商店购买率")), minPrice)

	def getSellPrice(self, price=0):
		'''出售价格
		'''
		if not price:
			price = self.getPrice()
		return price * (1+self.getConfig("商店出售率"))

	def getPropsNo(self):
		'''货物编号
		'''
		return self.getConfig("商品编号")

	def getPropsArgs(self):
		'''货物额外参数
		'''
		if self.iNo > 100000:  #食品和药品有品质
			return {"quality":self.getConfig("显示等级")}
		return {}

	def getName(self):
		'''商品名称
		'''
		return self.getConfig("商品名称")

	def maxWeekBuy(self):
		'''每周限购数量
		'''
		return self.getConfig("每周限购")

	def maxWeekSell(self):
		'''每周限售数量
		'''
		return self.getConfig("每周限售")

	def maxStack(self):
		'''叠加上限
		'''
		return self.getConfig("叠加数量")

	def needWaveCount(self):
		'''所需波动数量
		'''
		return self.getConfig("波动数量")

	def needLevel(self):
		'''所需等级
		'''
		return self.getConfig("出现等级")

	def changeRange(self):
		'''变更幅度
		'''
		return self.getConfig("变更幅度")

	def minStallPrice(self):
		'''摆摊最低价格
		'''
		return int((1 - self.getConfig("商店出售率")) * self.getPrice())

	def maxStallPrice(self):
		'''摆摊最高价格
		'''
		return int((1 + self.getConfig("商店购买率")) * self.getPrice())

	def isLimitUp(self):
		'''是否涨停
		'''
		return self.getRose() >= self.getConfig("涨跌幅度")

	def isLimitDown(self):
		'''是否跌停
		'''
		return self.getRose() <= -self.getConfig("涨跌幅度")

	def taxRate(self):
		'''税率
		'''
		return self.getConfig("税率")

	def maxStallCount(self):
		'''最大摊位数
		'''
		return self.getConfig("最大摊位数")

	def wave(self):
		'''波动
		'''
		if hasattr(self,"newWavePrice"):
			self.wavePrice = round(self.newWavePrice,2)
			del self.newWavePrice
		if hasattr(self,"newWaveCount"):
			self.waveCount = self.newWaveCount
			del self.newWaveCount
		if hasattr(self,"newPrice"):
			self.price = round(self.newPrice,2)
			del self.newPrice
		self.markDirty()

	def waveByStall(self, price, count):
		'''摆摊波动
		'''
		waveCount = self.getWaveCount()
		wavePrice = self.getWavePrice()
		needWaveCount = self.needWaveCount()
		if not needWaveCount:
			return
		elif waveCount + count < needWaveCount:
			self.newWavePrice = wavePrice + count * price
			self.newWaveCount = waveCount + count
			self.wave()
			return

		basePrice = self.getPrice()
		while count:
			oldPriceCount = needWaveCount - waveCount
			newPriceCount = min(needWaveCount,count - oldPriceCount)
			oldPriceAll   = price * oldPriceCount
			newBasePrice  = ((oldPriceAll+wavePrice)/needWaveCount-basePrice) * self.changeRange() + basePrice #新的基础价格
			newPriceAll   = price * newPriceCount

			waveCount = newPriceCount
			wavePrice = newPriceAll
			basePrice = newBasePrice

			count -= oldPriceCount + newPriceCount

		self.newWavePrice = wavePrice
		self.newWaveCount = waveCount
		self.newPrice = basePrice
		self.wave()

	def update(self):
		'''更新
		'''
		self.wavePrice = 0
		self.waveCount = 0
		newPrice = self.getPrice() - (self.getPrice() - self.getConfig("基础价格")) * self.getConfig("每日回复")
		self.price = round(newPrice,2)
		self.flushPrice = self.price

	def reset(self):
		'''重置
		'''
		self.price = 0
		self.wavePrice = 0
		self.waveCount = 0
		self.flushPrice = 0
		self.markDirty()

	def save(self):
		dData = pst.cEasyPersist.save(self)
		if self.price:
			dData["price"] = self.price
		if self.flushPrice:
			dData["fprice"] = self.flushPrice
		if self.wavePrice:
			dData["wprice"] = self.wavePrice
		if self.waveCount:
			dData["wcount"] = self.waveCount
		return dData

	def load(self,dData):
		pst.cEasyPersist.load(self,dData)
		self.price = dData.pop("price",0)
		self.flushPrice = dData.pop("fprice",0)
		self.wavePrice = dData.pop("wprice",0)
		self.waveCount = dData.pop("wcount",0)

	@property
	def key(self):
	    return self.iNo

	def getConfig(self,sKey,uDefault=0):
		return tradeGoodsData.getCashGoods(self.iNo,sKey,uDefault)

class cTradeCashGoods(cCashGoods):
	'''元宝商品
	'''
	def getType(self):
		return trade.TYPE_TRADE_CASH

	def getConfig(self,sKey,uDefault=0):
		return tradeGoodsData.getTradeCashGoods(self.iNo,sKey,uDefault)

	def getBuyCount(self, who):
		return who.week.fetch("tcbuy%d" % self.iNo)

	def addBuyCount(self, who, count):
		who.week.add("tcbuy%d" % self.iNo,count)

	def getSellCount(self, who):
		return who.week.fetch("tcsell%d" % self.iNo)

	def addSellCount(self, who, count):
		who.week.add("tcsell%d" % self.iNo,count)

import trade
import tradeGoodsData