#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#
import gevent.pool
import endPointWithoutSocket

class cMSplayerEP(endPointWithoutSocket.cEndPointWithoutSocket):
	def __init__(self,*tArgs,**dArgs):#override
		endPointWithoutSocket.cEndPointWithoutSocket.__init__(self,*tArgs,**dArgs)
		self.iRoleId=0
		self.sUserSource=self.sAccount=''
		self.bGranted=False #是否已经通过账号密码验证
		self.iTempGroup=instruction.FAKE
		self.iCreateStamp=timeU.getStamp()#创建时间
		self.iAssociativeGateServiceId=0	
	
	@property
	def accountObj(self):#关联的账号对象
		return account.gKeeper.getObj(self.sUserSource,self.sAccount)

	@property
	def roleObj(self):#关联的角色对象
		return role.gKeeper.getObj(self.iRoleId)

	def group(self):#所属gm权限组
		if config.IS_INNER_SERVER:#测试服人人都是admin
			return instruction.ADMIN
		if self.iTempGroup!=instruction.FAKE:#临时权限,角色下线后消失.
			return self.iTempGroup			
		return cfg.gm.group(self.sUserSource,self.sAccount)

	def setGranted(self):
		self.bGranted=True
	
	def roleId(self):
		return self.iRoleId
	
	def selfDescription(self):#override 自描述
		sBase=endPointWithoutSocket.cEndPointWithoutSocket.selfDescription(self)
		if self.iRoleId!=0:
			return '{},角色id={}'.format(sBase,self.iRoleId)
		elif self.sUserSource or self.sAccount:
			return '{},账号源={},账号={}'.format(sBase,self.sUserSource,self.sAccount)
		else:
			return sBase

	def setAssociativeRole(self,who):#为endPoint设置关联的角色
		self.resetAssociativeRole() #先重置一下再说
		self.iRoleId=who.id
		self.eDisConnected+=who.disConnectedEventHandler #endPoint断线要通知到角色
		mainService.gRoleIdMapEndPoint.addObj(self,self.iRoleId)
		
	def setAssociativeAccount(self,oAccount):#为endPoint设置关联的账号
		self.resetAssociativeAccount() #先重置一下再说
		self.sUserSource,self.sAccount=oAccount.userSourceAccount()
		self.eDisConnected+=oAccount.disConnectedEventHandler #endPoint断线要通知到账号对象
		mainService.gAccountMapEndPoint.addObj(self,self.sUserSource,self.sAccount)

	def resetAssociativeRole(self):#重置,不再关联角色
		if 0==self.iRoleId:
			return
		who=role.gKeeper.getObj(self.iRoleId)
		if who:
			self.eDisConnected-=who.disConnectedEventHandler
		mainService.gRoleIdMapEndPoint.removeProxy(self.iRoleId)

		self.iRoleId=0

	def resetAssociativeAccount(self):#重置,不再关联账号
		if self.sUserSource=='' and self.sAccount=='':
			return
		oAccount=account.gKeeper.getObj(self.sUserSource,self.sAccount)
		if oAccount:
			self.eDisConnected-=oAccount.disConnectedEventHandler
		mainService.gAccountMapEndPoint.removeProxy(self.sUserSource,self.sAccount)		
		self.sUserSource,self.sAccount='',''

	def copyFrom(self,ep):#override(目前这个函数没啥用)
		endPointWithoutSocket.cEndPointWithoutSocket.copy(self,ep)
		self.bGranted=ep.bGranted
		self.iRoleId=ep.iRoleId
		self.sAccount=ep.sAccount
		self.sUserSource=ep.sUserSource

	#根据不同方法名取得不同的对象,若是返回假值,表示没有通过授权
	#这里return的对象必须是controller子类的实例
	def _getControllerForDealRequest(self,sMethodName,iReqId):#override 获取ctrl,在处理对端的请求时
		self.iLastRequest=timeU.getMinuteNo()
		if not self.bGranted and (sMethodName not in gsEndPointMethodName):
			# return '未通过验证,不允许调用{}.'.format(sMethodName)	
			return '您已离线,请重新登录'
		
		if sMethodName in gsEndPointMethodName:
			return self
		elif sMethodName in gsAccountMethodName:
			oAccount=self.accountObj
			return oAccount if oAccount else '非法请求，请重新登陆.[找不到账号对象]'
		else:#gsRoleMethodName
			oRole=self.roleObj
			#临时代码,记录最后一次请求时间戳
			if oRole:
				oRole.iLastRequest=timeU.getStamp()
			return oRole if oRole else '非法请求，请重新登陆.[找不到角色对象]'
	
	def _workerJobProc(self,fRecvStamp,req):#override,在异常信息中加上角色id
		try:
			endPointWithoutSocket.cEndPointWithoutSocket._workerJobProc(self,fRecvStamp,req)
		except Exception:
			value=sys.exc_value
			sMessage=str(value.message) if value.message else str(value)
			if self.iRoleId!=c.INVALID:
				value.message=sMessage+';角色id={},服务器={}'.format(self.iRoleId,misc.zoneName())
				#u.reRaise('角色id={}.'.format(self.iRoleId))
			elif self.sUserSource or self.sAccount:
				value.message=sMessage+';账号源={},账号={},服务器={}'.format(self.sUserSource,self.sAccount,misc.zoneName())
				#u.reRaise('账号源={},账号={}.'.format(self.sUserSource,self.sAccount))			
			raise

	def _spawn(self,*tArgs,**dArgs):#override
		return myGreenlet.cGreenlet.spawnWithChnId(self.iEndPointId,*tArgs,**dArgs)

	def _getPool(self):#override
		return cPool(self.iEndPointId,500,myGreenlet.cGreenlet)#协程池,限制最大并发数

	def _onDisConnected(self):#override
		#从keeper中移除endPoint时要判断是不是自己		
		oEndPoint=mainService.gEndPointKeeper.getObj(self.epId())
		#log.log('_onDisConnected', 'epId:{},keeper.getObj:{}, id地址:{}'.format(self.epId(), bool(oEndPoint), id(self.this())==id(oEndPoint.this()) if oEndPoint else 0 ))
		if oEndPoint and oEndPoint.this()==self.this():
			
			mainService.gEndPointKeeper.removeObj(self.epId())
		elif oEndPoint:
			print '哈哈,被我找到了,请通知马昭.....'
			import traceback
			traceback.print_stack()
		endPointWithoutSocket.cEndPointWithoutSocket._onDisConnected(self)

	def setAssociativeGateServiceId(self,iAssociativeGateServiceId):
		self.iAssociativeGateServiceId=iAssociativeGateServiceId

	def associativeGateServiceId(self):
		return self.iAssociativeGateServiceId

	def _getEP2send(self):#override
		#if self.iAssociativeGateServiceId==0:
		#	raise Exception,'没有设置用来发送数据的通道.'
		return client4gate.getGateEp4ms()
		

	def _nextRequestId(self): #override
		self.iLastRequestId = u.guIdWithPostfix(backEnd_pb2.MAIN_SERVICE,self.iLastRequestId,True)
		return self.iLastRequestId

class cPool(gevent.pool.Pool):#协程池,记录着endPoint id
	def __init__(self,iEndPointId,iSize,greenletClass):#override
		self.iEndPointId=iEndPointId
		gevent.pool.Pool.__init__(self,iSize,greenletClass)

	def spawn(self,*tArgs,**dArgs):#override
		return gevent.pool.Pool.spawn(self,self.iEndPointId,*tArgs,**dArgs)

gsEndPointMethodName=(#这里的rpc都返回endPoint实例
'rpcAccountLogin','rpcReconnect','rpcRobotLogin'
)
gsAccountMethodName=(#这里的rpc都返回账号实例
'rpcRoleLogin','rpcDelRole','rpcCreateRole','rpcRandomName','rpcSwitchRole','rpcAccountLogOut',
)
gsRoleMethodName=(#这里的rpc都返回角色实例(不写这里也行,else部分,若是不在上面的就认为在这里)
)

import u

if 'gbOnce' not in globals():
	gbOnce=True
	

import weakref
import sys
import c
import misc
import log
import account
import role
import cfg.gm
import mainService
import myGreenlet
import instruction
import timeU
import client4gate
import config
import backEnd
import backEnd_pb2