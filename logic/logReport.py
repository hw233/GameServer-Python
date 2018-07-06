#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇


class cLogReport(object):
	def __init__(self):
		self.timerMng=timer.cTimerMng()#定时器
		self.iTimerId = 0

		#self.sQueryUserSource='select distinct(userSource) from account_multi_field'	#查询所有的渠道
		#查询指定渠道的各个等级段的人数
		self.sQueryLvCount='select userSource,lv,count(*) from role_multi_field1 group by userSource,lv'	
		#指定渠道下账号总数
		self.sQueryActCount='select userSource,count(*) from account_multi_field group by userSource'  		
		#查询空账号总数
		self.sQueryEpAct='select userSource,count(*) from account_multi_field where userSource+account not in (select userSource+account from role_multi_field1 group by userSource,account) group by userSource'		
		#每个渠道下当日新增账号数量
		self.sQueryNewAct='select  userSource,count(*) from account_multi_field where TO_DAYS(curdate())=TO_DAYS(createTime) group by userSource'
		#当日新增账号中无角色账号数量
		self.sQueryNewEpAct='select userSource,count(*) from account_multi_field where TO_DAYS(curdate())=TO_DAYS(createTime) and userSource+account not in (select userSource+account from role_multi_field1 group by userSource,account) group by userSource'
		#查询当日新增账号等级人数分布
		self.sQueryNewActLvCount='select userSource,lv,count(*) from role_multi_field1 where  userSource+account in(select  userSource+account from account_multi_field where TO_DAYS(curdate())=TO_DAYS(createTime)) group by userSource,lv'

	def doStatistics(self):
		if 0==self.iTimerId:
			return
		self.timerMng.cancel(self.iTimerId)
		self.iTimerId=0

		#以下都不检查查询结果是否为空
		lLvCount=db4ms.gConnectionPool.query(self.sQueryLvCount).rows	#[(渠道,等级,总数), (渠道,等级,总数)]
		if not lLvCount:	#lLvCount为空,则表示整个数据库没数据,所以直接return
			log.log('logReportError','请注意,当前数据库无数据')
			return
		lActCount=db4ms.gConnectionPool.query(self.sQueryActCount).rows	#[(渠道, 账号总数)]
		lEpAct=db4ms.gConnectionPool.query(self.sQueryEpAct).rows		#[(渠道, 空账号总数)]

		lNewAct=db4ms.gConnectionPool.query(self.sQueryNewAct).rows	#[(渠道, 新增账号数量)]
		lNewEpAct=db4ms.gConnectionPool.query(self.sQueryNewEpAct).rows	#[(渠道, 当日新增的空账号数量)]
		lNewActLvCount=db4ms.gConnectionPool.query(self.sQueryNewActLvCount).rows	#[(渠道, 等级, 总数)]

		self.__logStatDist(lActCount, lEpAct, lLvCount)
		self.__logStatDist(lNewAct, lNewEpAct, lNewActLvCount)


	#记录每日角色等级区间分布
	def __logStatDist(self, lActCount, lEpAct, lLvCount):
		if not lActCount:
			return

		dLvCount={}	#{渠道:{等级:总数}}
		for tData in lLvCount:
			dLvCount.setdefault(tData[0],{})[tData[1]]=tData[2]
		dActCount={}	#{渠道,账号总数}
		for tData in lActCount:
			dActCount[tData[0]]=tData[1]
		dEpActCount={}	#{渠道;空账号总数}
		for tData in lEpAct:
			dEpActCount[tData[0]]=tData[1]

		for iUserSource in dActCount:
			dLogResult={'t':timeU.stamp2str(), 'no':1}
			dLogResult['ep'] = iUserSource	#渠道
			dLogResult['ta'] = dActCount.get(iUserSource, 0)	#账号总数
			dLogResult['ea'] = dEpActCount.get(iUserSource, 0)	#空账号总数
			dLogResult['rlvdist'] = dLvCount.get(iUserSource, {})	#等级分布
			try:
				log.log('statistics','{}'.format(json.dumps(dLogResult)))	#此处的渠道数量比较少,所以直接写入文件
				 													#如渠道数比较多的话,考虑做个缓存将多条数据一起写入文件
			except Exception:
				misc.logException()

	def __logAccount4report(self, oAccount,sLogName,**dExtra):
		try:
			dBase={}
			dBase['t']=timeU.stamp2str() #时间
			dBase['ser']=config.ZONE_ID #区id
			dBase['os']=oAccount.osType() #客户端操作系统类型
			#self.sUserSource #用户来源(xx说不用记录,他那边可以根据登录子渠道反推出来)
			dBase['ep']=oAccount.sLoginAppId #当前登录所用客户端标识(登录子渠道)
			dBase['uid']=oAccount.sAccount #uid,用户账号
			dBase['ip']=oAccount.sIP #ip
			dBase.update(dExtra)#基础信息补上额外信息
			log.log(sLogName,'{}'.format(json.dumps(dBase)))
		except Exception:
			misc.logException()

	def __logRole4report(self, oRole,sLogName,**dExtra):
		try:
			dBase={}
			dBase['t']=timeU.stamp2str() #时间
			dBase['ser']=config.ZONE_ID #区id
			dBase['rid']=oRole.iRoleId #角色id
			dBase['rn']=oRole.name #角色名字
			dBase["school"]=oRole.school #角色职业
			oAcnt=oRole.accountObj
			dBase['os']=oAcnt.osType() #客户端操作系统类型
			#oRole.sUserSource #用户来源(xx说不用记录,他那边可以根据登录子渠道反推出来)
			dBase['ep']=oAcnt.sLoginAppId #当前登录所用客户端标识(登录子渠道)
			dBase['uid']=oRole.sAccount #uid,用户账号		
			
			dBase.update(dExtra)#基础信息补上额外信息
			log.log(sLogName,'{}'.format(json.dumps(dBase)))
		except Exception:
			misc.logException()

	def logCreateRole(self, oRole):#创建角色
		self.__logRole4report(oRole, 'visit', no=2)
	
	def logAccountLogin(self, oAccount):#账号登陆
		if getattr(oAccount, 'bNewCreate', False):
			self.__logAccount4report(oAccount, 'visit', no=1)	#记录账号创建日志

		self.__logAccount4report(oAccount, 'visit', no=3)

	def logRoleLogin(self, oRole):#角色登陆
		self.__logRole4report(oRole, 'visit', no=4, act=1, ot=0)

	def logRoleLogout(self, oRole):#角色登出
		iCurrStamp=timeU.getStamp()
		iOt=iCurrStamp-getattr(oRole,'iLoginStamp', iCurrStamp)
		self.__logRole4report(oRole, 'visit', no=4, act=2, ot=iOt)

	# def logAccountCreate(self, oAccount):#创建账号
	# 	self.__logAccount4report(oAccount, 'log_report/account_create', no=1)


	#开启定时器
	def preStatistics(self,iYear,iMonth,iDay,iHour,iWeek):
		if iHour==PRE_HOUR:	#
			self.iTimerId=self.timerMng.run(self.doStatistics, DEALY_SECOND)
			# self.sDistLogName='statistics/statistics{}-{}-{}'.format(iYear, iMonth, iDay)	#log文件名

def init():#启动服务器时初始化
	global gLogReporter
	gLogReporter=cLogReport()
	#timerEvent.geNewHour+=gLogReporter.preStatistics

PRE_HOUR=23	#开启定时器的时间
DEALY_SECOND=50 * 60#

import misc
import log
import timeU
import copy
import json
import timerEvent
import db4ms
import account
import role
import timer
import config