#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

import props.object
class cProps(props.object.cProps):
	
	@property
	def kind(self):
		return ITEM_BOX
	
	# def __init__(self,iNo):
	# 	props.object.cProps.__init__(self,iNo)
	# 	self.lItems=[] #投放物品

	# def save(self):
	# 	dData=props.object.cProps.save(self)
	# 	if self.lItems:
	# 		dData['item']=self.lItems
	# 	return dData

	# def load(self,dData):
	# 	props.object.cProps.load(self,dData)
	# 	self.lItems=dData.pop('item',[])

	# def canAutoCombine(self):
	# 	return True

	def use(self,who):#override
		if who.level<self.level:
			message.tips(who, '等级不足')
			return False
		lNo=self.getConfig('universal1')
		if not isinstance(lNo,list):
			raise Exception,'宝箱{}propsData配置项universal1数据类型不是list'.format(self.no())
	
		who.propsCtn.addStack(self,-1)
		oLaunchMng=launchMng.cLaunchMngNew('宝箱{}'.format(self.no()),giftLaunchData.gdData) #难道我发放道具都要create cLaunchMng对象？
		for iGroupNo in lNo:#解析投放物品
			lLaunchProps=oLaunchMng.launch(who,iGroupNo)
			for (iPropsNo,iAmount,tPropsArgs,dPropsArgs,bIsBind,sAnnounce) in lLaunchProps:
				oLaunchMng.launchBySpecify(who,iPropsNo,iAmount,tPropsArgs,dPropsArgs,bIsBind,sAnnounce=sAnnounce)

		return True
		# if not self.lItems:		
		# 	for iGroupNo in lNo:#解析投放物品
		# 		iPropsNo,tPropsArgs,dPropsArgs,iAmount,bIsBind,sAnnounce=oLaunchMng.calcLaunchByGroupNo(who,iGroupNo)
		# 		if iPropsNo:
		# 			self.lItems.append((iPropsNo,tPropsArgs,dPropsArgs,iAmount,bIsBind,sAnnounce))

		# 	if not self.lItems:
		# 		raise Exception,'宝箱{}({})什么东西也没开出来,是不是数据配错了?'.format(self.name,self.no())

		# lProps=[]	#生成投放物品
		# for (iPropsNo,tPropsArgs,dPropsArgs,iAmount,bIsBind,sAnnounce) in self.lItems:
		# 	if iPropsNo in c.VIR_ITEM:
		# 		continue
		# 	if iAmount==1:
		# 		oProp=props.getCacheProps(iPropsNo)
		# 	else:
		# 		oProp=props.new(iNo)
		# 		oProp.setStack(iAmount)
		# 	lProps.append(oProp)

		# if who.propsCtn.canAllAdd2Package(*lProps):#判断包裹空间是否足够并投放物品
		# 	who.propsCtn.addStack(self,-1)
		# 	for (iPropsNo,tPropsArgs,dPropsArgs,iAmount,bIsBind,sAnnounce) in self.lItems:
		# 		oLaunchMng.launchBySpecify(who,iPropsNo,tPropsArgs,dPropsArgs,iAmount,bIsBind,sLogReason=self.name,sTips='',sAnnounce=sAnnounce)
		# 	self.lItems=[]
		# 	self.markDirty()
		# else:
		# 	ep=mainService.getEndPointByRoleId(who.id)
		# 	if ep:
		# 		ep.rpcTips('背包空间不足')

		# print "split-----------launch --------- Drop----------"
		# oDropMng=dropMng.cDropMng('宝箱{}'.format(self.no())) #难道我发放道具都要create cLaunchMng对象？
		# for iGroupNo in lNo:
		# 	oDropMng.dropByGroupNo(who,iGroupNo)

	def _buttons(self):#override
		return [props_pb2.OPEN,]
		
from props.defines import *
import u
import c
import propsData
import dropMng
import launchMng
import props_pb2
import mainService
import message