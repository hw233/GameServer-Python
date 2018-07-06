#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import pst
import controller
import block
import multiField
import product

#账号的json数据
class cAccountJSON(block.cBlock,pst.cEasyPersist):
	def __init__(self,shellObj,sUserSource,sAccount):#override
		block.cBlock.__init__(self,'账号json数据',sUserSource,sAccount)
		pst.cEasyPersist.__init__(self,shellObj._dirtyEventHandler)#数据有变化就通知到外壳对象去
		self.shellObj=weakref.proxy(shellObj)
		self.sUserSource,self.sAccount=sUserSource,sAccount
		self.setIsStm(sql.ACCOUNT_JSON_INSERT).setUdStm(sql.ACCOUNT_JSON_UPDATE)
		self.setDlStm(sql.ACCOUNT_JSON_DELETE).setSlStm(sql.ACCOUNT_JSON_SELECT)

		self.hour=cCycHourInAccount(2,shellObj._dirtyEventHandler)#小时变量
		self.day=cCycDayInAccount(2,shellObj._dirtyEventHandler)#天变量
		self.week=cCycWeekInAccount(2,shellObj._dirtyEventHandler)#周变量
		self.month=cCycMonthInAccount(2,shellObj._dirtyEventHandler)#月变量
		self.lDiamondLog=[]

	def addDiamondLog(self,sLog):#元宝变化的日志,充值,消耗,赠送
		#时间,点数,剩余点数,项目,角色/途径
		t=timeU.getStamp(),sLog #哪个角色进行操作的?
		self.lDiamondLog.append(t)
		self.markDirty()

	def load(self,dData):#override
		pst.cEasyPersist.load(self,dData)
		self.hour.load(dData.pop('h',{}))
		self.day.load(dData.pop('d',{}))
		self.week.load(dData.pop('w',{}))
		self.month.load(dData.pop('m',{}))
		self.lDiamondLog=dData.pop('diamondLog',[])
		
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
		if self.lDiamondLog:
			dData['diamondLog']=self.lDiamondLog
		return dData

		
#一个属性占一列的账号数据
class cAccountMultiField(multiField.cMultiField):
	def __init__(self,shellObj,sUserSource,sAccount):#override
		self.tWatchNames=('iDiamond','iVipLv','iVipExp')
		multiField.cMultiField.__init__(self,'账号多列数据块',sUserSource,sAccount)
		self.shellObj=weakref.proxy(shellObj)
		self.sUserSource,self.sAccount=sUserSource,sAccount
		self.setIsStm(sql.ACCOUNT_MULTI_FIELD_INSERT).setDlStm(sql.ACCOUNT_MULTI_FIELD_DELETE)
		self.setUdStm(sql.ACCOUNT_MULTI_FIELD_UPDATE).setSlStm(sql.ACCOUNT_MULTI_FIELD_SELECT)
		#需要被存盘的成员变量初始值全部设为None,因为父类检查数据是否发生变化是依赖于发生变化的变量原来的值是否是None
		self.iDiamond,self.iVipLv,self.iVipExp=0,0,0 #0,0,0

	def _getWatchNames(self):#override
		return self.tWatchNames

	def _dirtyEventHandler(self):#override
		self.shellObj._dirtyEventHandler()#数据有变化就通知到外壳对象去

	def _getValuesTuple4Update(self):#override
		return self.iDiamond,self.iVipLv,self.iVipExp

	def _setValuesAfterSelect(self,*tValues):#override
		self.iDiamond,self.iVipLv,self.iVipExp=tValues

	def _setSelectNoRecordsetDefaultValues(self,*itNoRowInsertValues):#override
		self.iDiamond,self.iVipLv,self.iVipExp=itNoRowInsertValues[2:]#与sql.ACCOUNT_MULTI_FIELD_INSERT相关,前2个是用户来源与账号

	def _getSelectRecordsetFieldCount(self):#override
		return 3

#把两个不同的账号对象拼装成一个大账号对象
#理论上同一个区的一个账号下的多个角色可以同时在线.但我们只允许一个
class cAccount(product.cProduct,controller.cController):
	def __init__(self,sUserSource,sAccount):#override
		product.cProduct.__init__(self,'账号混合数据',sUserSource,sAccount)
		self.accountJson=cAccountJSON(self,sUserSource,sAccount)
		self.accountMf=cAccountMultiField(self,sUserSource,sAccount)
		self.sUserSource,self.sAccount=sUserSource,sAccount
		self.lRoleList=[]#按角色创建顺序存放id列表[iRoleId1,iRoleId2,...]
		self.dRoleList={}#角色列表
		self.iPlayingRoleId=0#当前在线角色
		self.sLoginAppId=self.sRegisterAppId=''
		self.iOStype=0 #操作系统类型
		self.sIP='' #ip地址
		self.iDisConnectStamp=0#最后断线时间

	def _dirtyEventHandler(self):
		factoryConcrete.accountFtr.schedule2tail4save(self.sUserSource,self.sAccount)
		
	def userSourceAccount(self):#返回元组
		return self.sUserSource,self.sAccount

	def osType(self):#客户端操作系统类型
		return  self.iOStype

	def setIP(self,sIP):#设置ip地址
		self.sIP=sIP

	def setOStype(self,iOStype):
		self.iOStype=iOStype

	def setPlayingRoleId(self,iRoleId):		
		self.iPlayingRoleId=iRoleId

	def playingRoleId(self):
		return self.iPlayingRoleId
	
	def isStaff(self):#是否内部员工
		return cfg.staff.isStaff(self.sUserSource,self.sAccount)
		
	def setRegisterAppId(self,sRegisterAppId):#战法牧账号的注册途径
		self.sRegisterAppId=sRegisterAppId
		
	def setLoginAppId(self,sLoginAppId):#本次登录用的客户端包标识(也叫登录子渠道)
		self.sLoginAppId=sLoginAppId			
		
	def _deleteFromDB(self):#override
		self.accountJson._deleteFromDB()
		self.accountMf._deleteFromDB()

	def _saveToDB(self):#override
		b1=self.accountJson._saveToDB()
		b2=self.accountMf._saveToDB()
		return b1 and b2

	def _loadFromDB(self):#override
		b1=self.accountJson._loadFromDB()
		b2=self.accountMf._loadFromDB()
		
		rs=db4ms.gConnectionPool.query(sql.ROLE_LIST,self.sUserSource,self.sAccount)
		for iRoleId,sName,iSchool,iLv,iAspect in rs.rows:
			iFashionDress=1
			iWeapShape=1
			iWeapEffect=1
			iEquipStar=1
			iDegree=1
			self.addRoleInfo(iRoleId,sName,iSchool,iLv,iWeapShape,iWeapEffect,iFashionDress,iEquipStar,iDegree)#前两位存武器特,后两位存武器外观
			# if sName:
			# 	self.addRoleName(iRoleId,sName)
		return b1 and b2

	def _insertToDB(self,*itNoRowInsertValues,**dData):#override
		gevent.spawn(u.cFunctor(self.accountJson._insertToDB),self.sUserSource,self.sAccount)
		gevent.spawn(u.cFunctor(self.accountMf._insertToDB),*itNoRowInsertValues)
		#self.bNewCreate=True

	def hasRoleId(self,iRoleId):
		return iRoleId in self.dRoleList
		
	def addRoleInfo(self,iRoleId,sName,iSchool,iLv,iWeapShape,iWeapEffect,iFashionDress,iEquipStar,iDegree):
		self.lRoleList.append(iRoleId)
		self.dRoleList[iRoleId]={'name':sName,"school":iSchool,'lv':iLv, 'wp':iWeapShape,'we':iWeapEffect,'fd':iFashionDress,'es':iEquipStar,'dgr':iDegree}

	def addTestRole(self,iRoleId):
		self.dRoleList[iRoleId]={'name':'莫当真','lv':99,"school":1}		

	def updateRoleStatus(self,iRoleId):
		if self.hasRoleId(iRoleId):
			self.lRoleList.remove(iRoleId)
			self.dRoleList.pop(iRoleId,None)
			db4ms.gConnectionPool.query('update role_multi_field1 set status=-1 where roleId={}',iRoleId)
	
	def roleAmount(self,iLv=0):#返回等级>=iLv的角色数量
		return len([dValues for dValues in self.dRoleList.itervalues() if dValues['lv']>=iLv])
	
	def setLv(self,iRoleId,iLv):#角色升级后,需要修改帐号对象的角色数据,否然切换角色时看到的角色数据是过时的
		self.dRoleList[iRoleId]['lv']=iLv

	def roleLv(self,iRoleId):
		return self.dRoleList[iRoleId]['lv']

	def disConnectedEventHandler(self,ep):
		print '帐号对象disConnectedEventHandler:{},{}'.format(self.sUserSource,self.sAccount)
		#gKeeper.removeObj(self.sUserSource,self.sAccount)		
		log.log('loginLogout','({},{})账号断线了.活跃角色:{},所有角色{}'.format(self.sUserSource,self.sAccount,self.iPlayingRoleId,self.lRoleList))		
		self.iDisConnectStamp=timeU.getStamp()
		#这里有bug,要遍历此账号下的全部角色是否在role.gKeeper
		if self.iPlayingRoleId==c.INVALID:#该账号下没有角色在线,账号对象即时删除.(有角色在线的,账号对象踢除由role.py的gTimingWheel负责)
			gKeeper.removeObj(self.sUserSource,self.sAccount)

	def onReLogin(self):
		print '帐号对象onReLogin:{},{}'.format(self.sUserSource,self.sAccount)
		log.log('loginLogout','({},{})账号重连了'.format(self.sUserSource,self.sAccount))		
		self.iDisConnectStamp=0 #重置最后断线时间戳	

	def log4report(self,sLogName,**dExtra):
		try:
			dBase={}
			dBase['t']=timeU.stamp2str() #时间
			dBase['ser']=config.ZONE_ID #区id
			dBase['os']=self.osType() #客户端操作系统类型
			#self.sUserSource #用户来源(xx说不用记录,他那边可以根据登录子渠道反推出来)
			dBase['ep']=self.sLoginAppId #当前登录所用客户端标识(登录子渠道)
			dBase['uid']=self.sAccount #uid,用户账号
			dBase['ip']=self.sIP #ip

			dBase.update(dExtra)#基础信息补上额外信息
			log.log(sLogName,'{}'.format(json.dumps(dBase)))
		except Exception:
			misc.logException()
			
	def isRobot(self):
		'''是否机器人账号
		'''
		return self.accountJson.fetch("robot")

def existAccount(sUserSource,sAccount):#是否存在某个账号
	#先检查内存中有没有,没有再到数据库中查一下
	return factoryConcrete.accountFtr.getProductFromDB(factory.NO_ROW_RETURN_NONE,sUserSource,sAccount)

def get(sUserSource,sAccount):
	return gKeeper.getObj(sUserSource,sAccount)


import productKeeper
import factoryConcrete
import jitKeeper

class cProductkeeper(productKeeper.cProductkeeper):
	def removeObj(self,sUserSource,sAccount):#override
		return productKeeper.cProductkeeper.removeObj(self,sUserSource,sAccount)
import u

if 'gbOnce' not in globals():
	gbOnce=True
	
	if 'mainService' in SYS_ARGV:
		gKeeper=cProductkeeper(factoryConcrete.accountFtr)#在线的账号才放到这里

		#为了方便后台gm指令,所以此处加一个account的jitKeeper
		# gJitKeeper=productKeeper.cJITproductKeeper(factoryConcrete.accountFtr)	临时屏蔽,测试jitKeeper
		gJitKeeper=jitKeeper.cJITproductKeeper(factoryConcrete.accountFtr)
		
		
#-----------------------------------------------
#上面的都是单区内的账号信息,还应该有一个跨区的账号信息.数据存在登录服.
#-----------------------------------------------
import gevent
import weakref
import json

import factoryConcrete
import sql
import db4ms
import endPoint
import c
import u
import misc
import log
import cycleData
import instruction
import timeU
import cfg.staff
import mainService
import block.sysActive
import factory

import role
import config
#起几个别名,方便统计内存对象
class cCycHourInAccount(cycleData.cCycHour):pass
class cCycDayInAccount(cycleData.cCycDay):pass	
class cCycWeekInAccount(cycleData.cCycWeek):pass	
class cCycMonthInAccount(cycleData.cCycMonth):pass

