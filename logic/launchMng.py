#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import launchData

#投放管理器(按权重投放)

#全部奖励结果信息都在self.dLaunchResult了
#{	玩家id:{物品编号:数量,物品编号:数量,物品编号:数量},	玩家id:{物品编号:数量,物品编号:数量,物品编号:数量},	玩家id:{物品编号:数量,物品编号:数量,物品编号:数量},	玩家id:{物品编号:数量,物品编号:数量,物品编号:数量},	玩家id:{物品编号:数量,物品编号:数量,物品编号:数量},}

class cLaunchMng(object):
	def __init__(self,sLogReason='',dLaunchData=launchData.gdData):
		self.sLogReason=sLogReason
		self.dLaunchData=dLaunchData
		self.dLaunchResult={}

	def resultInfo(self):#奖励结果信息,写log用
		return self.dLaunchResult

	def clearResult(self):
		self.dLaunchResult={}

	def __getLaunchTuple(self,iGroupNo):#返回具体某奖励编号的tuple		
		d=self._getLaunchTable()
		if iGroupNo not in d:
			raise Exception,'投放表没有编号为{}的奖励'.format(iGroupNo)
		return d[iGroupNo]

	def _getLaunchTable(self):#哪个数据表
		return self.dLaunchData

	def __randomLaunchInfo(self,iGroupNo):#随机出投放信息,返回dict,具体的奖励信息
		tInfo=self.__getLaunchTuple(iGroupNo)
		idx=self.__randomLaunchIdx(iGroupNo)
		return tInfo[idx]

	def __randomLaunchIdx(self,iGroupNo):#按权重抽取一个索引
		tInfo=self.__getLaunchTuple(iGroupNo)
		iTotal=0
		dWeight={}
		#计算总权重
		for i,dLaunchInfo in enumerate(tInfo):
			dWeight[i]=dLaunchInfo['weight']
			iTotal+=dLaunchInfo['weight']
		iIdx=rand.randomKey(dWeight,iTotal)
		return iIdx

	def getLaunchInfoByGroupNoIndex(self,iGroupNo,iIndex,who,*tArgs,**dArgs):#取得某一组某一行的投放信息
		tInfo=self.__getLaunchTuple(iGroupNo)
		if not 0<=iIndex<len(tInfo):
			raise Exception,'{}组有{}个元素,索引{}越界'.format(iGroupNo,len(tInfo),iIndex)
		return self.parseInfo(tInfo[iIndex],who,*tArgs,**dArgs)

	def __callLambda(self,func,who,iPropsNo,*tArgs,**dArgs):
		lParameter=[]
		for sVarName in func.func_code.co_varnames:
			lParameter.append(self._getValueByVarName(sVarName,who,iPropsNo,*tArgs,**dArgs))
		return func(*lParameter)		
		
	def _getValueByVarName(self,sVarName,who,iPropsNo,*tArgs,**dArgs):#可能子类需要override
		if sVarName=='roleLv' or sVarName=='lv':
			return who.level
		else:
			raise Exception,'策划填的变量{}无法解析.'.format(sVarName)

	def parseSchool(self,uItemInfo,who,*tArgs,**dArgs): #解析职业
		if isinstance(uItemInfo,dict):
			return uItemInfo.get(who.school)
		return 	uItemInfo

	def parseInfo(self,dLaunchInfo,who,*tArgs,**dArgs):
		uAmount,sAnnounce,uItemInfo,bIsBind=dLaunchInfo['amount'],dLaunchInfo.get('announce',''),dLaunchInfo['item'],dLaunchInfo['isBind']
		uItemInfo=self.parseSchool(uItemInfo,who,*tArgs,**dArgs)
		iPropsNo,tPropsArgs,dPropsArgs=misc.parseItemInfo(uItemInfo)#物品编号,参数
		if type(uAmount)==types.FunctionType:#数量
			iAmount=self.__callLambda(uAmount,who,iPropsNo,*tArgs,**dArgs)#数量用函数算出来
		elif isinstance(uAmount,int):
			iAmount=uAmount
		else:
			raise Exception,'资源数量不对.{}'.format(uAmount)
		return iPropsNo,tPropsArgs,dPropsArgs,iAmount,bIsBind,sAnnounce

	#多选一,返回一个一个物品编号和数量
	def launchByGroupNo(self,who,iGroupNo,sLogReason='',sTips='',*tArgs,**dArgs):
		if not sLogReason:
			sLogReason=self.sLogReason
		dLaunchInfo=self.__randomLaunchInfo(iGroupNo)

		iPropsNo,tPropsArgs,dPropsArgs,iAmount,bIsBind,sAnnounce=self.parseInfo(dLaunchInfo,who,*tArgs,**dArgs)
		if iPropsNo==0 or iAmount==0:#没有命中
			return 0,0
		launch.launchBySpecify(who,iPropsNo,iAmount,tPropsArgs,dPropsArgs,bIsBind,sLogReason,sTips,sAnnounce)

		dInfo=self.dLaunchResult.setdefault(iRoleId,{})
		dInfo[iPropsNo]=dInfo.get(iPropsNo,0)+iAmount
		return iPropsNo,iAmount

	# def transString(self,iRoleId,sText):
	# 	if not iRoleId:
	# 		return sText
	# 	who=role.gKeeper.getObj(iRoleId)
	# 	if who:
	# 		sText=sText.replace('$ROLENAME',who.Name())

	# 	dInfo=self.dLaunchResult.get(iRoleId,{})
	# 	if not dInfo:
	# 		return sText
	# 	if 9000 in dInfo:
	# 		sText=sText.replace('$EXP','%d'%dInfo[9000])
	# 	if 9001 in dInfo:
	# 		sText=sText.replace('$GOLD','%d'%dInfo[9001])
	# 	if 9002 in dInfo:
	# 		sText=sText.replace('$DIAMOND','%d'%dInfo[9002])
	# 	if iRoleId in dInfo:
	# 		sText=sText.replace('$ITEMNAME',dInfo[iRoleId])
	# 	if iRoleId in dInfo:
	# 		sText=sText.replace('$ITEMAMOUNT','%d'%dInfo[iRoleId])
	# 	if iRoleId in dInfo:
	# 		sText=sText.replace('$PRESTIGE','%d'%dInfo[iRoleId])
	# 	if iRoleId in dInfo:
	# 		sText=sText.replace('$ENERGY','%d'%dInfo[iRoleId])
	# 	return sText

import types

import launch
import u
import misc
import rand
import props
import role
import random
import c
import log
import mainService
