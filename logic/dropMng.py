#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#重写cLaunchMsg的几个方法就OK了！

class cDropMng(object):
	def __init__(self,sLogReason='',dDrop=None):
		self.sLogReason=sLogReason
		self.dDrop=dDrop
		self.dResultInfo={}

	def resultInfo(self):#奖励结果信息,写log用
		return self.dResultInfo

	def clearResult(self):
		self.dResultInfo={}

	def getDropTuple(self,iNo):#返回具体某奖励编号的tuple
		if self.dDrop:
			d=self.dDrop
		else:
			d=self.getDropTable()
		if iNo not in d:
			raise Exception,'投放表没有编号为{}的奖励'.format(iNo)
		return d[iNo]

	def getDropTable(self):
		return launchData.gdData

	def randomDropInfo(self,iGroupNo):#返回dict,具体的奖励信息
		tInfo=self.getDropTuple(iGroupNo)
		tIndexs=self.randomDropIndexs(iGroupNo)
		lInfo=[]
		for idx in tIndexs:
			lInfo.append(tInfo[idx])
		return tuple(lInfo)

	def randomDropIndexs(self,iGroupNo):#按权重抽取一个索引
		tInfo=self.getDropTuple(iGroupNo)
		lIndexs=[]
		for i,dDropInfo in enumerate(tInfo):
			numerator=dDropInfo['numerator']
			denominator=dDropInfo['denominator']
			if numerator>=random.randint(1,denominator):
				lIndexs.append(i)
		return tuple(lIndexs)

	def __callLambda(self,func,who,iNo,*tArgs,**dArgs):
		lParameter=[]
		for sVarName in func.func_code.co_varnames:
			lParameter.append(self._getValueByVarName(sVarName,who,iNo,*tArgs,**dArgs))
		return func(*lParameter)		
		
	def _getValueByVarName(self,sVarName,who,iNo,*tArgs,**dArgs):
		if sVarName=='roleLv':
			return 1
		elif sVarName=='roleLv':
			return 2
		else:
			raise Exception,'策划填的变量{}无法解析'.format(sVarName)

	#对外接口
	def dropByGroupNo(self,who,iGroupNo,sLogReason=''):
		if not sLogReason:
			sLogReason=self.sLogReason
		tDropInfo=self.randomDropInfo(iGroupNo)
		if not tDropInfo:
			return
		lRet=[]
		for dDropInfo in tDropInfo: 
			print dDropInfo
			uAmount,sAnnounce,uItemInfo,bIsBind=dDropInfo['amount'],dDropInfo.get('announce',''),dDropInfo['item'],dDropInfo['isBind']
			iNo,tArgs,dArgs=misc.parseItemInfo(uItemInfo)#物品编号,参数
			if type(uAmount)==types.FunctionType:#数量
				iAmount=self.__callLambda(uAmount,who,iNo,*tArgs,**dArgs)#数量用函数算出来
			elif isinstance(uAmount,int):
				iAmount=uAmount
			else:
				raise Exception,'资源数量不对.{}'.format(uAmount)
			if iNo==0 or iAmount==0:#没有命中
				return
			self.launchBySpecify(who,iNo,tArgs,dArgs,iAmount,bIsBind,sLogReason,'',sAnnounce)
			lRet.append((iNo,iAmount))
		return tuple(lRet)
		
	def launchBySpecify(self,who,iNo,tArgs,dArgs,iAmount,bIsBind,sLogReason='',sTips='',sAnnounce=''):#sTips传None就不会提示
		iRoleId=who.id
		if not sLogReason:
			sLogReason=self.sLogReason
		if iPropsNo in c.VIR_ITEM:#虚拟道具
			who.addVirtualTool(iNo,iAmount,sLogReason,sTips)
		else:#真实物品
			iTmp=iAmount
			while iAmount>0:
				oProps=props.new(iNo,*tArgs,**dArgs)
				iMaxStack=oProps.maxStack()
				if iAmount>iMaxStack:
					iRealStack=iMaxStack
				else:
					iRealStack=iAmount
				oProps.setStack(iRealStack)
				iAmount-=iRealStack
				if bIsBind and not oProps.isBind():
					oProps.bind(who.id)
				who.propsCtn.launchProps(oProps,self.sLogReason,sTips,dArgs.get('sAnnounce',''))
			iAmount=iTmp
		
		dInfo=self.dResultInfo.setdefault(iRoleId,{})
		dInfo[iNo]=dInfo.get(iNo,0)+iAmount

	def transString(self,iRoleId,sText):
		if not iRoleId:
			return sText
		who=role.gKeeper.getObj(iRoleId)
		if who:
			sText=sText.replace('$ROLENAME',who.Name())

		dInfo=self.dResultInfo.get(iRoleId,{})
		if not dInfo:
			return sText
		if 9000 in dInfo:
			sText=sText.replace('$EXP','%d'%dInfo[9000])
		if 9001 in dInfo:
			sText=sText.replace('$GOLD','%d'%dInfo[9001])
		if 9002 in dInfo:
			sText=sText.replace('$DIAMOND','%d'%dInfo[9002])
		if iRoleId in dInfo:
			sText=sText.replace('$ITEMNAME',dInfo[iRoleId])
		if iRoleId in dInfo:
			sText=sText.replace('$ITEMAMOUNT','%d'%dInfo[iRoleId])
		if iRoleId in dInfo:
			sText=sText.replace('$PRESTIGE','%d'%dInfo[iRoleId])
		if iRoleId in dInfo:
			sText=sText.replace('$ENERGY','%d'%dInfo[iRoleId])
		return sText

import types
import random
import launchData
import props
import misc
import u
import role