#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#
import gevent.greenlet
import endPoint
#发生异常时能够发送信息给操作者(内服用)

class cGreenlet(gevent.greenlet.Greenlet):
	def __init__(self,iEndPointId,*tArgs,**dArgs):#override
		super(cGreenlet,self).__init__(*tArgs,**dArgs)
		gGreenletMng.addObj(self)
		self.iEndPointId=iEndPointId
		self.sName='无名'

	def epId(self):
		return self.iEndPointId

	@property
	def name(self):
		return self.sName
	
	@name.setter
	def name(self, name):
		self.sName = name

	@classmethod
	def spawn(cls,func,*tArgs,**dArgs):#override		
		iEndPointId=getattr(gevent.getcurrent(),'iEndPointId',0)
		return cls.spawnWithChnId(iEndPointId,func,*tArgs,**dArgs)

	@classmethod
	def spawnWithChnId(cls,iEndPointId,func,*tArgs,**dArgs):
		func,=u.makeWeakFunc(func) #若是func是成员函数,要对func建立弱引用,不能意外延长对象生命期		
		curJob=gevent.getcurrent()
		newJob=super(cGreenlet,cls).spawn(iEndPointId,func,*tArgs,**dArgs)#这里只能使用super语法才能达到目的		
		newJob.iRequestId=getattr(curJob,'iRequestId',0)
		#newJob.iEndPointId=getattr(curJob,'iEndPointId',0)
		return newJob
		
		#使用父类的spawn方法,和cGreenlet,点号语法无法做到
		#下面两种做法都不对
		#return cls.spawn(iEndPointId,func,*tArgs,**dArgs)#调用的方法错了,调用了上面的spawn方法,参数cls是对的
		#return gevent.greenlet.Greenlet.spawn(iEndPointId,func,*tArgs,**dArgs)#调用了父类的方法对了,但是参数错了,期望参数是cls
		
		#super(cGreenlet,cls)得到一个很奇怪的对象,就可以实现调用父类的方法,使用当前class
	def _report_error(self,exc_info):#override		
		etype,value,tb=exc_info
		sMessage=str(value.message) if value.message else str(value)
		if sMessage.startswith('%$%'):
			sMessage=sMessage[len('%$%'):]			
		else:
			value.message='%$%'+sMessage #加上特殊标识,方便在linux下grep

		if isinstance(value,endPoint.cParseStringError):#是反序列化网络包出错
			pass #通知内部员工,可能有黑客修改网络包.并且要记log,要有开关可以停止记log
			
		if not isinstance(value,gevent.GreenletExit) and self.iEndPointId!=0 and config.SHOW_EXCEPTION:
			ep=mainService.gEndPointKeeper.getObj(self.iEndPointId)
			if ep:#根据channel id发错误信息到客户端				
				sExcept=traceback.format_exc()[-512:]#最多只显示512个字符
				if etype==PlannerError:
					sTitle='策划数据出错,请截图发到群里通知策划'
				else:
					sTitle='服务端出错,请截图发到群里通知服务端程序员'
				#message.message(ep.iRoleId,sExcept)
				if etype==Exception:
					sText='{}'.format(sExcept)
				else:
					sText='{},{}'.format(etype.__name__,sExcept)
				
				ep.rpcModalDialog(sText,sTitle)
		return super(cGreenlet,self)._report_error((etype,value,tb))


import timer
import u
import message

if 'gGreenletMng' not in globals():
	gGreenletMng=u.cWeakRefManager()#用于跟踪统计协程

import traceback
import c
import misc
import config
import log
import mainService