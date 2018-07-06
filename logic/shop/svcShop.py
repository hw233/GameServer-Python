#-*-coding:utf-8-*-
import terminal_main_pb2
import endPoint

if 'gbIsClosed' not in globals():
	gbIsClosed=False #商店是否关闭

def handleClose(oldFunc):
	def newFunc(self,ep,who,reqMsg):
		global gbIsClosed
		if gbIsClosed:# and not config.IS_INNER_SERVER:#只有生产环境才生效.
			ep.rpcTips('商店临时关闭.')
			return
		try:
			return oldFunc(self,ep,who,reqMsg)
		except Exception:			
			gbIsClosed=True #发生异常,关闭商店
			log.log('shop','商店抛异常,临时关闭')
			raise
	return newFunc

class cService(terminal_main_pb2.terminal2main):
	@endPoint.result
	@handleClose
	def rpcServerShopGoods(self,ep,who,reqMsg):return rpcServerShopGoods(self,ep,who,reqMsg) #请求商城数据
	@endPoint.result
	@handleClose
	def rpcServerBugGoods(self,ep,who,reqMsg):return rpcServerBugGoods(self,ep,who,reqMsg) #购买物品
	
	@endPoint.result
	def rpcBuyRest(self,ep,who,reqMsg):return rpcBuyRest(self,ep,who,reqMsg)	#购买体力
	@endPoint.result
	def rpcBuyGold(self,ep,who,reqMsg):return rpcBuyGold(self,ep,who,reqMsg)	#购买元宝

#购买120点体力消耗钻石表  {次数:消耗值},默认为200
gdBuyRestCost = {
	1 : 50, 
	2 : 100,
	3 : 100
}
ADD_REST, ACQU_COST = 120, 200	#增加体力,默认消耗钻石数

def rpcBuyRest(self,ep,who,reqMsg):#购买体力
	doBuyRest(ep, who)

def doBuyRest(ep, who):
	if who.rest()>=role.REST_OVER_MAX:
		ep.rpcTips('体力已达上限')
		return
	iBuyRestTimes = who.day.fetch('buyRest', 0)+1
	if iBuyRestTimes > vip.helper.buyRestTime(who):
		misc.rechargeTips(who,ep, '今日可购买次数已经用完。提升VIP等级可增加购买次数')
		return
	iCost = 400
	if iBuyRestTimes <= 3:
		iCost = 50
	elif iBuyRestTimes <= 6:
		iCost = 100
	elif iBuyRestTimes <= 9:
		iCost = 200
	#iCost = gdBuyRestCost.get(iBuyRestTimes, ACQU_COST)
	sRestText = '是否消耗 钻石x{},增加{}点体力'.format(iCost, ADD_REST)
	bFail,oMsg=ep.rpcConfirmBox(sTitle='购买体力',sContent=sRestText,sSelect='Q_购买Q_取消')
	if bFail or oMsg.iValue!=0:
		return
	if who.diamond < iCost:
		misc.rechargeTips(who, ep)
		return
	who.addDiamond(-iCost,'购买体力消耗')
	who.addRest(ADD_REST,'钻石购买','体力增加120点',True)	
	who.day.add('buyRest',1)

def rpcBuyGold(self,ep,who,reqMsg):#购买元宝
	iBuyGoldAmount = 10000
	misc.buyGold(who,ep, iBuyGoldAmount, '消耗{}钻石购买{}元宝'.format(iBuyGoldAmount/c.DIAMOND_GOLD_RATIO, iBuyGoldAmount))
	# bFail,oMsg=ep.rpcConfirmBox(sTitle='购买元宝',sContent='消耗20钻石购买10000元宝',sSelect='Q_确定Q_取消')
	# if bFail or oMsg.iValue!=0:
	# 	return	
	# if who.diamond < 20:
	# 	misc.rechargeTips(who, ep)
	# 	return 
	# who.addDiamond(-20,'购买元宝消耗')
	# who.addTradeCash(10000,'钻石购买')	

#请求商城数据,默认发第一页的数据过去
def rpcServerShopGoods(self,ep,who,reqMsg):
	iCurrPage=reqMsg.iPage
	iTabNo=reqMsg.iTabNo
	openShopUI(ep,who,iTabNo,iCurrPage)

def openShopUI(ep,who,iTabNo,iCurrPage):
	lAllGoodsNo=shopData.groudGdData.get(iTabNo)
	if not lAllGoodsNo:
		return
	iStart=(iCurrPage-1)*c.SHOP_PAGE_NUM
	iEnd=iStart+c.SHOP_PAGE_NUM
	lResult=lAllGoodsNo[iStart:iEnd]
	goodsList=shop_pb2.goodsList()
	goodsList.iTabNo=iTabNo
	for iSeq in lResult:
		item=goodsList.list.add()
		item.iNo=iSeq #商品序号
		iPropsNo=shopData.getConfig(iSeq,'propsno') #物品编号
		item.sNo=shopData.getConfig(iSeq, 'sNo', '')	#物品字符串编号
		module=propsData
		if iPropsNo >=10000:
			module=equipData
		iLimit=shopData.getConfig(iSeq,'limit') #产品购买上限
		iVipLv=shopData.getConfig(iSeq,'viplv') #vip等级
		iCurrency=shopData.getConfig(iSeq,'currency')
		item.iIcon=module.getConfig(iPropsNo,'icon')
		item.sName=module.getConfig(iPropsNo,'name')
		if iLimit==-1:#无限制,客户端不显示
			item.iNum=iLimit
		else:	
			item.iNum=iLimit-who.day.fetch('shop',{}).get(iSeq,0) #今天剩余购买个数
		item.sDesc='描述:'+shopData.getConfig(iSeq,'desc')
		item.iVipLv=iVipLv
		item.iPrice=shopData.getConfig(iSeq,'price')
		item.iCurrencyType=iCurrency

		iVIPlv=shopData.getConfig(iSeq,'viplv')
		if iVIPlv:
			item.sCondiction.append('vip等级{}级'.format(iVIPlv))
#		item.sCondiction.append('假数据:vip2级')
#		item.sCondiction.append('角色等级10')

	ep.rpcClientShopGoods(goodsList)
	print goodsList

#购买物品
def rpcServerBugGoods(self,ep,who,reqMsg):
	if gbIsClosed:
		ep.rpcTips('商店临时关闭.')
		return False
	iAmount=reqMsg.iAmount
	if iAmount<=0:#外挂
		return False
	iSeq=reqMsg.iNo #序号,不是物品编号
	iCurrency=shopData.getConfig(iSeq,'currency') #货币类型
	iPrice=shopData.getConfig(iSeq,'price')#单价
	iPropsNo=shopData.getConfig(iSeq,'propsno')#物品编号

	oProp=props.getCacheProps(iPropsNo)
	iMaxAdd=who.propsCtn.calcMaxAdd(iPropsNo,iAmount)	#
	if iMaxAdd:
		ep.rpcTips('包裹空间最大能装{}个{}'.format(iMaxAdd,oProp.name))
		return False
	
	iSumPrice=iAmount*iPrice #总价	
	iLimit=shopData.getConfig(iSeq,'limit')#限制购买个数


	if iLimit>=0:#-1表示无限制购买
		dShop=who.day.fetch('shop',{})
		iRemain=iLimit-dShop.get(iSeq,0)		
		if iAmount>iRemain:
			oProps=props.getCacheProps(iPropsNo)
			if iRemain<=0:
				ep.rpcTips('您今天不能再购买{}.'.format(oProps.name))
			else:
				ep.rpcTips('今天只能再购买{}个{}.'.format(iRemain,oProps.name))
			return False
		dShop[iSeq]=dShop.get(iSeq,0)+iAmount
		who.day.set('shop',dShop)

	if iCurrency==c.CURRENCY_YXB:
		if who.gold<iSumPrice:
			#检查游戏币是否足够
			misc.buyGold(who,ep, iSumPrice-who.gold)
			return False
		who.addTradeCash(-iSumPrice,'购买商品')
	else:
		if who.diamond<iSumPrice:			
			ep.rpcTips('钻石不足,无法购买')
			return False
		who.addDiamond(-iSumPrice,'购买商品')

	iMaxStack=oProp.maxStack()
	iCounter=int(math.ceil(iAmount/float(iMaxStack)))
	
	#放物品进入玩家的包裹
	# oProps=props.new(iPropsNo)  #如果有初始化参数由策划配置
	# oProps.setStack(iAmount) #数量
	# who.propsCtn.launchProps(oProps,'购买商品')

	who.propsCtn.clearRecEquip()	#清空上一次新获取装备的缓存
	for i in xrange(iCounter):
		oProp=props.new(iPropsNo)
		iStack=iMaxStack if i<iCounter-1 else iAmount-iMaxStack*i
		oProp.setStack(iStack)
		who.propsCtn.launchProps(oProp,'购买商品')
	recEquip.upRecEquip(who, '商城')	#查看是否新获得比当前穿戴装备更好的装备,若有则提示角色穿戴
	
	return True


import c
import u
import propsData
import props
import equipData
import math
import log
import role
import misc
import config