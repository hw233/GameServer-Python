#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import primitive

def lockByEndPoint(oldFunc):#装饰器
	def newFunc(self,ep,obj,reqMsg):
		iEndPointId=ep.iEndPointId
		with primitive.cLockByKey(dLock4endPoint,iEndPointId):
			ep=mainService.gEndPointKeeper.getObj(iEndPointId)#阻塞之后,要重新检查对象的有效性
			if not ep:
				return
			return oldFunc(self,ep,obj,reqMsg)
	return newFunc


def lockByAccount(oldFunc):#装饰器
	def newFunc(self,ep,oAccount,reqMsg):
		sUserSource,sAccount=oAccount.userSourceAccount()
		with primitive.cLockByKey(dLock4account,(sUserSource,sAccount)):
			oAccount=account.gKeeper.getObj(sUserSource,sAccount)#阻塞之后,要重新检查对象的有效性
			if not oAccount:
				return
			return oldFunc(self,ep,oAccount,reqMsg)		
	return newFunc

def lockByRole(oldFunc):#装饰器
	def newFunc(self,ep,who,reqMsg):
		iRoleId=who.id
		with primitive.cLockByKey(dLock4role,iRoleId):
			who=role.gKeeper.getObj(iRoleId)#阻塞之后,要重新检查对象的有效性
			if not who:
				return
			return oldFunc(self,ep,who,reqMsg)		
	return newFunc

import account
import mainService
import role

if 'gbOnce' not in globals():
	gbOnce=True

	if 'mainService' in SYS_ARGV:
	
		dLock4account={}		
		dLock4endPoint={}
		dLock4role={}
