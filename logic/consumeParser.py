#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

#需要扣除的物品,包括虚拟物品,即经验,绑钻,元宝,钻石,竞技点等
#传入的参数有如下面
#{101:850,145:lambda roleLv,guildLv:roleLv*guildLv+800}

import codeParser

#扣除器
class cNeedConsume(codeParser.cCodeParser):
	def needConsumeStr(self,sSeparator=',',bInclude=True):#sSeparator各需求物品中间的分隔符,bInclude是否包含虚拟物品
		l=[]
		for iNo,v in self.dItem.iteritems():
			if iNo in c.VIR_ITEM:#是虚拟道具
				if not bInclude:
					continue
				else:
					sName=c.VIR_ITEM.get(iNo,'未知')
			else:
				obj=props.getCacheProps(iNo)				
				sName=obj.name if obj else '{}'.format(iNo)
		
			l.append('{}×{}'.format(sName,v))
		return sSeparator.join(l)

	def needConsumeIcon(self,bInclude=True):
		l=[]
		for iNo,v in self.dItem.iteritems():
			if iNo in c.VIR_ITEM:
				if not bInclude:
					continue
				else:
					iIcon=c.VIR_ICON.get(iNo,0)
			else:
				obj=props.getCacheProps(iNo)
				iIcon=obj.icon() if obj else 0

			l.append(iIcon)
		return l

	def needConsumeAmount(self,bInclude=True):
		l=[]
		for iNo,v in self.dItem.iteritems():
			l.append(v)

		return l

	#执行扣除
	#sTips	传None就不会有扣除提示
	#sFailSeparator	多条不满足的条件之间的连接符,传None则发现一个条件不满足时,立即返回单条错误原因
	def doConsume(self,who,sLogReason,sTips='',sFailSeparator=','):
		sFailReason=self.checkAll(who,sFailSeparator)
		if sFailReason!='':#有条件没有达到
			return sFailReason

		for iNo,iAmount in self.dItem.iteritems():
			if iNo in c.VIR_ITEM:#虚拟道具
				who.addVirtualTool(iNo,-iAmount,sLogReason,sTips)
			else:#真实的道具
				who.propsCtn.subtractPropsByNo(iNo,iAmount,sLogReason,sTips)
		return ''

	#判断是否满足条件,#返回为不满足的条件的字符串提示信息
	def checkAll(self,who,sFailSeparator=','):#sFailSeparator==None时遇到第1个失败时则返回
		l=[]
		for iNo,v in self.dItem.iteritems():
			sFailReason=self._checkProps(who,iNo,v)
			if sFailReason:
				if sFailSeparator==None:
					return sFailReason
				else:
					l.append(sFailReason)
		return sFailSeparator.join(l)

	def _checkProps(self,who,iNo,iAmount):#检查单独一项条件是否达到,不达到则返回字符串描述,空字串表示达到条件.
		if iAmount==0:
			return ''
		if iNo in c.VIR_ITEM:#虚拟道具
			if iNo==c.EXP:#经验
				if who.exp()<iAmount:
					return '经验不足{}'.format(iAmount)
			elif iNo==c.GOLD:#元宝
				if who.gold<iAmount:
					return '元宝不足{}'.format(iAmount)
			elif iNo==c.DIAMOND:#钻石
				if who.diamond<iAmount:
					return '钻石不足{}'.format(iAmount)
			elif iNo==c.VOUCHER:#绑钻
				if who.voucher()<iAmount:
					return '绑钻不足{}'.format(iAmount)
			else:
				raise Exception,'漏写代码支持虚拟物品编号{}'.format(iNo)
		else:
			iTotal=0
			for oProps in who.propsCtn.getPropsGroupByNo(iNo):#扫描整个包裹
				iTotal+=oProps.stack()
				if iTotal>=iAmount:
					return ''
			else:#数量不足
				obj=props.getCacheProps(iNo)
				sName=obj.name if obj else '{}'.format(iNo)				
				return '{}不足{}'.format(sName,iAmount)

		return ''
	
	#def enoughDiamond(self,who):#判断钻石是否满足
	#	return who.diamond>=self.dItem.get(9002,0)

import types
import u
import props
import c