#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import pst
import block

#玩家周期数据
class cCycDataBlock(block.cBlock):
	def __init__(self,iRoleId):#override
		self.iRoleId=iRoleId
		block.cBlock.__init__(self,'玩家周期数据',iRoleId)
		self.setIsStm(sql.CYCLE_INSERT)
		self.setDlStm(sql.CYCLE_DELETE)
		self.setUdStm(sql.CYCLE_UPDATE)
		self.setSlStm(sql.CYCLE_SELECT)

		self.hour=cycleData.cCycHour(24,self._dirtyEventHandler)#小时变量
		self.day=cycleData.cCycDay(10,self._dirtyEventHandler)#天变量
		self.week=cycleData.cCycWeek(5,self._dirtyEventHandler)#周变量
		self.month=cycleData.cCycMonth(3,self._dirtyEventHandler)#月变量
		self.cycDataMerge=pst.cMergePersist({'h':self.hour,'d':self.day,'w':self.week,'m':self.month})

	def getPstObj(self):#override
		return self.cycDataMerge

	def _dirtyEventHandler(self):
		factoryConcrete.cycFtr.schedule2tail4save(self.iRoleId)

import factoryConcrete		
import productKeeper
import misc
import config
import jitKeeper
#用于查看离线玩家的cycData,一段时间后自动删除
if 'gKeeper' not in globals():
	KEEP_SECOND=30 if config.IS_INNER_SERVER else 60*5
	# gKeeper=productKeeper.cJITproductKeeper(factoryConcrete.cycFtr,KEEP_SECOND) 临时屏蔽,测试jitKeeper
	gKeeper=jitKeeper.cJITproductKeeper(factoryConcrete.cycFtr)


import sql
import cycleData


