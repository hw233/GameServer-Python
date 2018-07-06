#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import pst
import block

class cGoldCoin(block.cBlock,pst.cEasyPersist):
	def __init__(self,iRoleId):#override
		block.cBlock.__init__(self,'玩家元宝数据',iRoleId)
		pst.cEasyPersist.__init__(self,self._dirtyEventHandler)#
		
		self.iRoleId=iRoleId
		self.setIsStm(sql.GOLD_COIN_INSERT)
		self.setDlStm(sql.GOLD_COIN_DELETE)
		self.setUdStm(sql.GOLD_COIN_UPDATE)
		self.setSlStm(sql.GOLD_COIN_SELECT)

		self.hour=cCycHourInGoldCoin(1,self._dirtyEventHandler)#小时变量
		self.day=cCycDayInGoldCoin(1,self._dirtyEventHandler)#天变量
		self.week=cCycWeekInGoldCoin(1,self._dirtyEventHandler)#周变量
		self.month=cCycMonthInGoldCoin(1,self._dirtyEventHandler)#月变量
		self.lGoldLog=[]

	def _dirtyEventHandler(self):
		factoryConcrete.goldCoinFtr.schedule2tail4save(self.iRoleId)

	def addGoldLog(self,sLog):#元宝变化的日志,充值,消耗,赠送
		#时间,点数,剩余点数,项目,角色/途径
		t=timeU.getStamp(),sLog #哪个角色进行操作的?
		self.lGoldLog.append(t)
		self.markDirty()

	def load(self,dData):#override
		pst.cEasyPersist.load(self,dData)
		self.hour.load(dData.pop('h',{}))
		self.day.load(dData.pop('d',{}))
		self.week.load(dData.pop('w',{}))
		self.month.load(dData.pop('m',{}))
		self.lGoldLog=dData.pop('goldLog',[])
		
	def save(self):#override
		dData=pst.cEasyPersist.save(self)
		dHour=self.hour.save()
		if dHour:
			dData['h']=dHour
		dDay=self.day.save()
		if dDay:
			dData['d']=dDay
		dWeek=self.week.save()
		if dWeek:
			dData['w']=dWeek
		dMonth=self.month.save()
		if dMonth:
			dData['m']=dMonth
		if self.lGoldLog:
			dData['goldLog']=self.lGoldLog
		return dData


def getObj(iRoleId):
	return gGoldCoinKeeper.getObj(iRoleId)


#import productKeeper
import factoryConcrete
import jitKeeper
import u

if 'gbOnce' not in globals():
	gbOnce=True
	
	if 'mainService' in SYS_ARGV:		
		gGoldCoinKeeper=jitKeeper.cJITproductKeeper(factoryConcrete.goldCoinFtr)
	

#import gevent
import weakref
import c
import u
import misc
import log
import config
import cycleData

#起几个别名,方便统计内存对象
class cCycHourInGoldCoin(cycleData.cCycHour):pass
class cCycDayInGoldCoin(cycleData.cCycDay):pass	
class cCycWeekInGoldCoin(cycleData.cCycWeek):pass	
class cCycMonthInGoldCoin(cycleData.cCycMonth):pass



#import json

# import factoryConcrete
# import sql

# import db4ms
# import endPoint

# import cycleData
# import instruction
# import timeU
# import cfg.staff
# import mainService
# import block.sysActive
# import factory

# import role



