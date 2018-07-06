#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import terminal_main_pb2
import endPoint

#称号服务
class cService(terminal_main_pb2.terminal2main):
	@endPoint.result
	def rpcFightTitleList(self,ep,who,reqMsg): return rpcFightTitleList(self,ep,who,reqMsg)#请求战力称号面板

	@endPoint.result
	def rpcActiveTitle(self,ep,who,reqMsg):#激活称号(穿上)
		flag = False
		iTitleNo=reqMsg.iValue
		if iTitleNo in titleData.gdData:
			flag = who.titleCtn.putOnTitle(iTitleNo)
			who.titleCtn.rpcRefreshTitleList(ep)
		if flag:
			who.reCalcAttr() ##更新
		#print("==================> rpcActiveTitle", flag)
		return flag

	@endPoint.result
	def rpcInActiveTitle(self,ep,who,reqMsg):#停止使用称号（脱掉）
		flag = False
		iTitleNo=reqMsg.iValue
		if iTitleNo in titleData.gdData:
			flag = who.titleCtn.takeOffTitle(iTitleNo)
			who.titleCtn.rpcRefreshTitleList(ep)
		if flag:
			who.reCalcAttr() ##更新
		#print("==================> rpcInActiveTitle", flag)
		return flag

def rpcFightTitleList(self,ep,who,reqMsg):
	who.titleCtn.rpcRefreshTitleList(ep)
	return
	oFightTitle=who.titleCtn.getItem(c.FIGHT_TITLE)
	iMyFight=who.fightAbility()
	iMaxFight=oFightTitle.fight() if oFightTitle else 0
	oFightTitleList=title_pb2.fightTitleList()
	for iFight in titleData.glFight:
		iFightNo=titleData.gdMsgByFight.get(iFight)
		dValue=titleData.gdData.get(iFightNo)
		oTitle=oFightTitleList.title.add()
		oTitle.name=dValue.get('name')
		oTitle.icon=dValue.get('icon')
		oTitle.bigIcon=dValue.get('bigIcon')
		oTitle.bAchieve=iMaxFight>=iFight
		oTitle.fight=iFight
	return oFightTitleList



import sys
import os
import u
import log
import c
import time
import role
import title
import gevent
import props
import factoryConcrete

import factory
import titleData
import title_pb2