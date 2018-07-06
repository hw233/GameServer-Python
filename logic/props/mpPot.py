#-*-coding:utf-8-*-
import props.object

class cProps(props.object.cProps):
	def use(self,who):#override
		iAdd=self.getConfig('universal1',0)
		if not isinstance(iAdd,(int,long,float)):
			raise Exception,'MP药的"通用字段1"必须是一个整数或小数形式的百分数.'
		if isinstance(iAdd,float) and iAdd>1:
			raise Exception,'MP药的百分数不能大于1'
		
		if hasattr(who, "eatAmount"):
			eatAmount = who.eatAmount
			del who.eatAmount
		else:
			eatAmount = 1
		
		if hasattr(who, "isSpoil"):
			isSpoil = who.isSpoil
			del who.isSpoil
		else:
			isSpoil = False

		for i in xrange(eatAmount):
			if who.mp==who.mpMax:
				message.tips(who, '真气值已达上限')
				return False
			if not isSpoil:
				who.propsCtn.addStack(self,-1)
			if isinstance(iAdd,float):
				iAdd=int(iAdd*who.hpMax)
			who.addMp(iAdd)
		return True
	
import message