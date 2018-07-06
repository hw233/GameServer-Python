#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#公共模块


import timeU
import c
import u
import keeper

#支持以下5种格式
"""
道具编号
[道具编号]
[道具编号,(参数1,参数2,参数n)]
[道具编号,{'参数名1':值1,'参数名2':值2,'参数名n':值n}]
[道具编号,(参数1,参数2,参数n),{'参数名1':值1,'参数名2':值2,'参数名n':值n}]

"""
def parseItemInfo(uInfo):#解析投放道具的类型与参数
	if isinstance(uInfo,list):
		if not 0<len(uInfo)<=3:
			raise Exception,'道具信息是list时,必须符合 0<元素个数<=3.{}'.format(uInfo)
		if len(uInfo)==1:
			iNo,tArgs,dArgs=uInfo[0],(),{}
		elif len(uInfo)==2:
			if isinstance(uInfo[1],tuple):#元组
				iNo,tArgs,dArgs=uInfo[0],uInfo[1],{}
			elif isinstance(uInfo[1],dict):#字典
				iNo,tArgs,dArgs=uInfo[0],(),uInfo[1]
			else:
				raise Exception,'参数是列表时,列表的第二个元素必须是元组或字典.{}'.format(uInfo)
		else:
			iNo,tArgs,dArgs=uInfo
	elif isinstance(uInfo,(int,str)):
		iNo,tArgs,dArgs=uInfo,(),{}
	else:
		raise Exception,'资源类型参数不对.{}'.format(uInfo)
	return iNo,tArgs,dArgs

if 'gbOnce' not in globals():
	gbOnce=True
	gsProgressStartTime=timeU.stamp2str()#进程启动时间
	if 'mainService' in SYS_ARGV:
		gbMaintain=False #系统是否处于停服维护状态.

def logException(sExtra='',iSkip=0):#比u.py模块的logException更强大,会向客户端弹窗口显示异常.
	etype,value=sys.exc_type,sys.exc_value#提前拿出value.message,因为u.logException会修改value.message
	sMessage=str(value.message) if value.message else str(value)
	u.logException(sExtra,iSkip)
	if not config.SHOW_EXCEPTION:
		return
	job=gevent.getcurrent()
	iEndPointId=getattr(job,'iEndPointId',0)
	if iEndPointId==0:
		return
	ep=mainService.gEndPointKeeper.getObj(iEndPointId)
	if not ep:
		return

	if etype!=Exception:
		sTips='{}:{}'.format(etype.__name__,sMessage)
	else:
		sTips='{}'.format(sMessage)
	ep.rpcModalDialog(sTips,'请告知后端程序员')

def zoneName():#测试环境才有用,生产环境不用理
	return getattr(config,'ZONE_NAME','未知服务器')	

#把两个字典合并,如果有相同key的话,把value相加
def addTwoDict(dict1,dict2):#好像没啥用,,暂时留着吧
	d={}
	for uKey,uValue in dict1.iteritems():
		if not isinstance(uValue,(int,long)):
			raise Exception,'value必须是int或者long才能调用该接口'
		if uKey in dict2:
			d[uKey]=dict2[uKey]+uValue
		else:
			d[uKey]=uValue
	for uKey,uValue in dict2.iteritems():
		if not isinstance(uValue,(int,long)):
			raise Exception,'value必须是int或者long才能调用该接口'
		if uKey not in d:
			d[uKey]=uValue
	return d

#假的ep,调用rpcXXX时不用判断ep的有效性,简化代码
class cDummyEndPoint(object):
	def __getattr__(self,sPropName):#找不到属性时,会执行这个函数
		if sPropName.startswith('rpc') or sPropName == 'send':
			return lambda *tArgs,**dArgs:(True,None)
		else:
			raise Exception,'获取ep访问其{}属性时要先判断ep的有效性.'.format(sPropName)

	def __nonzero__(self):#用if obj判断时,返回结果为假
		return False

#当ep为None时,返回一个dummy,可以不判断真假直接调用rpcXXXX,简化写代码
class cEndPointKeeper(keeper.cKeeper):
	def getObj(self,*tPriKey):#override 返回proxy
		obj=keeper.cKeeper.getObj(self,*tPriKey)
		if not obj:
			obj=cDummyEndPoint()
		return obj

class cEndPointProxyManager(u.cKeyMapProxy):
	def getProxy(self,*tPriKey):#override 循环引用也会导致总是能get出有效的proxy,
		oProxy=u.cKeyMapProxy.getProxy(self,*tPriKey)
		if oProxy:
			ep=self._getEndPoint(oProxy.epId())
			if not ep:#主引用中都没有找到,说明找到的是循环引用中的对象
				#要不要在这里打破循环引用呢??
				if config.IS_INNER_SERVER:#外网不记log,量太大了
					sText='主键{}相关联的endPoint在主引用管理器中不存在,endPoint实例发生循环引用了'.format(tPriKey)				
					log.log('warning',sText)
					print sText
				return cDummyEndPoint()
			if ep.this()!=oProxy.this():#
				sText='主键{}相关联的endPoint和主引用管理器中的endPoint不是同一个,关系错乱了'.format(tPriKey)
				#if config.IS_INNER_SERVER:
				raise Exception,sText
				#else:
				#log.log('warning',sText)
				return cDummyEndPoint()
			return oProxy		
		return cDummyEndPoint()		

	def _getEndPoint(self,iEndPointId):
		raise NotImplementedError,'请在子类实现'

import config
import sys
import os
import gevent

import log
import random
import u
import rand
import timeU
import endPoint
import mainService
import props
import config
import role
import math
