#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

#需要扣除/奖励的物品,包括虚拟物品,即经验,绑钻,元宝,钻石,竞技点等
#传入的参数有如下面
#{101:850,145:lambda roleLv,guildLv:roleLv*guildLv+800}

#策划代码解析器
class cCodeParser(object):
	def __init__(self,dItem,*tArgv,**dArgs):
		if not isinstance(dItem,dict):
			raise Exception,'cNeedConsume.__init__的dNeed参数必须是dict'
		self.dItem={}#要把策划填的表达式计算出来
		for iNo,iAmount in dItem.iteritems():
			if type(iAmount)==types.FunctionType:
				iAmount=self.__callLambda(iNo,iAmount,*tArgv,**dArgs)#计算表达式的值
			if iAmount<=0:
				continue
			self.dItem[iNo]=iAmount#把需要的数量记起来,稍候扣除

	def __callLambda(self,iNo,func,*tArgs,**dArgs):#计算表达式
		lParameter=[]
		for sVarName in func.func_code.co_varnames:
			lParameter.append(self._getValueByVarName(iNo,sVarName,*tArgs,**dArgs))
		return func(*lParameter)

	def _getValueByVarName(self,iNo,sVarName,*tArgs,**dArgs):
		raise NotImplementedError,'请在子类实现.'

	def props(self):#物品
		d={}
		for iNo,iAmount in self.dItem.iteritems():
			if iNo not in c.VIR_ITEM:
				d[iNo]=iAmount
		return d

	def diamond(self):#钻石
		return self.dItem.get(c.DIAMOND,0)

	def gold(self):#元宝
		return self.dItem.get(c.GOLD,0)

	def exp(self):#经验
		return self.dItem.get(c.EXP,0)

	def arenaPoint(self):#竞技点
		return self.dItem.get(c.ARENA_POINT,0)

	def voucher(self):#绑钻
		return self.dItem.get(c.VOUCHER,0)



import types
import u
import c