#-*-coding:utf-8-*-
import props.object

class cProps(props.object.cProps):
	def use(self,who):#override
		iAdd=self.getConfig('universal1',0)
		if not isinstance(iAdd,(int,long)):
			raise Exception,'体力丹的"通用字段1"必须是一个整数.'
		
		if hasattr(who, "eatAmount"):
			eatAmount = who.eatAmount
			del who.eatAmount
		else:
			eatAmount = 1

		for i in xrange(eatAmount):
			if who.rest()>=role.REST_OVER_MAX:
				message.tips(who, '当前体力已达上限')
				return False
			if message.confirmBox(who, "增加#C07{}点#n活力?\nQ取消\nQ使用") != 2:
				return False
			
			who.propsCtn.addStack(self,-1)
			message.tips(who, '活力增加#C04{}#n点'.format(who.addRest(iAdd,self.name,bOverMax=True)))
			# iCurrRest,iMaxRest=who.rest(),who.maxRest()
			# if iCurrRest==iMaxRest:
		# 		ep.rpcTips('体力已达到最大值')
		# 		return False
		# 	if iCurrRest+iAdd>iMaxRest:
		# 		iRealAdd=iMaxRest-iCurrRest
		# 		bFail,oMsg=ep.rpcConfirmBox(sTitle='使用物品',sContent='使用物品将会恢复{}点体力,剩余{}点将不会产生作用,是否使用?'.format(iRealAdd,iAdd-iRealAdd),sSelect='Q_确定Q_取消')
		# 		if bFail or oMsg.iValue!=0:
			# 		return
			# 	iAdd=iRealAdd
		# 	who.propsCtn.addStack(self,-1)
		# 	ep.rpcTips('恢复体力{}点'.format(who.addRest(iAdd,self.name)))

		return True

import role
import message