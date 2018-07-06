#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#公共模块,不为某一个服务或某一个游戏

def recursiveEncode(obj,sTargetCode='utf-8'):#递归地把unicode转成utf-8
	if isinstance(obj, dict):
		return {recursiveEncode(key): recursiveEncode(value) for key, value in obj.iteritems()}
	elif isinstance(obj, list):
		return [recursiveEncode(element) for element in obj]
	elif isinstance(obj, unicode):
		return obj.encode(sTargetCode)
	else:
		return obj
		
def makeWeakFunc(*tFuncs):#解出带弱引用指针的functor
	if not tFuncs:
		raise Exception,'至少请传一个参数'
	lTemp=[]
	for func in tFuncs:
		if type(func) not in (types.FunctionType,cFunctor):
			func=cFunctor(func)#cFunctor有存储弱引用的功效.
		lTemp.append(func)#即使传None过来也会原样返回None
	return lTemp
	
def parseCallable(func):#分解函数,使用弱引用可以不增加引用计数
	if type(func) in (types.FunctionType,cFunctor):#全局函数 或 是一个子functor
		return func,None
	elif type(func)==types.MethodType:#实例方法 或 类方法
		if func.im_self:
			return func.im_func,weakref.ref(func.im_self)
		else:
			return func.im_func,None
	else:
		raise Exception,'未知的callable'

#函数对象(仿函数),C++中也有此概念
#作用有二,1.闭包 2.生成弱引用的函数指针
#不要研究此版本，此版本较复杂一点点，直接看下面那个已被注释掉的CFunctor,对使用者来说功能是一模一样的
class cFunctor(object):
	def __init__(self,func,*tArgs,**dArgs):
		#被打包的函数处理
		self.func,self.wr=parseCallable(func)
		for obj in tArgs:
			if type(obj)==weakref.ProxyType:
				raise Exception,'你要存储对象的id,不要存对象本身.'
		for obj in dArgs.itervalues():
			if type(obj)==weakref.ProxyType:
				raise Exception,'你要存储对象的id,不要存对象本身.'
		self.tArgs=tArgs
		self.dArgs=dArgs

	def __call__(self,*tArgs,**dArgs):#重载()运算符
		if self.dArgs and dArgs:#复制出新的dict,不要修改原来的dict
			dTempArgs=dArgs.copy()
			dTempArgs.update(self.dArgs)#合并两个个字典
		elif self.dArgs:
			dTempArgs=self.dArgs
		elif dArgs:
			dTempArgs=dArgs
		else:
			dTempArgs={}
		if not self.wr:
			return self.func(*(tArgs+self.tArgs ),**dTempArgs)
		elif self.wr():
			return self.func(self.wr(),*(tArgs+self.tArgs ),**dTempArgs)

	def isValid(self):#是否还可以调用
		if not self.wr:#全局函数或类方法总是有效的
			return True
		return self.wr()#实例方法,取决于相关实例是否活着

	def __repr__(self):#调试用的
		return self.funcCode()

	def innerFuncObj(self):
		return self.getFuncObj(self.func)

	@staticmethod
	def getFuncObj(callObj):
		while callObj and isinstance(callObj,cFunctor):
			callObj=callObj.func

		if type(callObj)==types.MethodType:
			return callObj.im_func.func_code
		return callObj

	def funcName(self):#调试用的
		func=self.innerFuncObj()
		if func:
			return '{}'.format(func.func_name)
		return '{}'.format(func)

	def funcCode(self):#调试用的
		func=self.innerFuncObj()
		if func:
			return '{}'.format(func.func_code)
		return '{}'.format(func)


"""
简化版的函数对象(仿函数)
这个版本不够完美,保存一个函数指针时会增加引用计数,上面那个版本使用弱引用则不会增加引用计数
class cFunctor(object):
	def __init__(self,func,*tArgs,**dArgs):
		self.func=func
		self.tArgs=tArgs
		self.dArgs=dArgs
	def __call__(self,*tArgs,**dArgs):
		if self.dArgs and dArgs:
			dTempArgs=dArgs.copy()
			dTempArgs.update(self.dArgs)
		elif self.dArgs:
			dTempArgs=self.dArgs
		elif dArgs:
			dTempArgs=dArgs
		else:
			dTempArgs={}
		return self.func(*(tArgs+self.tArgs),**dTempArgs)
"""

#事件(观察者模式)
class cEvent(object):
	def clearObserver(self):#清空监听的函数
		self.lEventHandler=[]#事件响应函数,即是一堆函数指针

	#返回观察者数量
	def observerCount(self):
		return len(self.lEventHandler)

	def contain(self,handler):#是否在观察者列表中
		tHandler=parseCallable(handler)
		return tHandler in self.lEventHandler

	def clearDead(self):#删掉死亡的观察者
		for i in xrange(len(self.lEventHandler)-1,-1,-1):#从后往前pop,才不会有跳跃行为
			handler,wr=self.lEventHandler[i]
			if wr and not wr():#是实例方法,但是观察者已死
				self.lEventHandler.pop(i)

	def __init__(self):
	    self.lEventHandler=[]

	def __iadd__(self,handler):#增加观察者		重载+=运算符		
		self.clearDead()#顺便尝试清理死掉的事件响应函数
		tHandler=parseCallable(handler)
		if tHandler in self.lEventHandler:
			raise Exception,'事件响应函数已经存在于观察者列表中了'
		self.lEventHandler.append(tHandler)
		return self

	def __isub__(self,handler):#减少观察者		重载-=运算符
		self.clearDead()#顺便尝试清理死掉的事件响应函数
		tHandler=parseCallable(handler)
		for i in xrange(len(self.lEventHandler)-1,-1,-1):#从后往前pop,才不会有跳跃行为
			if self.lEventHandler[i]==tHandler:
				self.lEventHandler.pop(i)		
		return self

	#触发事件
	#重载()运算符
	def __call__(self,*tArgs,**dArgs):
		bRet=bHasDead=False
		#lDeadIdx=[]
		#改为使用切片,因为要复制一份list,防止在遍历过程中某个事件的行为影响到其他的事件
		for iIdx,tHandler in enumerate(self.lEventHandler[:]):
			handler,wr=tHandler
			try:
				if not wr:
					bRet=handler(*tArgs,**dArgs)
				elif wr():
					bRet=handler(wr(),*tArgs,**dArgs)
				else:
					bHasDead=True
					#lDeadIdx.append(iIdx)#已死亡的观察者,记录下来他的索引,要清理掉
				if bRet:#上一个事件处理函数返回True则停止执行剩下的事件响应函数
					break
			except Exception:
				logException()

		if bHasDead:
			self.clearDead()
		# for i in xrange(len(lDeadIdx)-1,-1,-1):#正式删掉死亡的观察者,从后往前pop,才不会有跳跃行为
		# 	iIdx=lDeadIdx[i]
		# 	self.lEventHandler.pop(iIdx)#
		return bRet

#用来记录某个函数执行所花时间
def LogPacketCost(fStamp,func,iNeedLog=20):
	iCost=(time.time()-fStamp)*1000
	if iCost<iNeedLog:
		return
	if isinstance(func,cFunctor):
		sLogName,sLogText=func.FuncName(),func.funcCode()
	else:
	 	sLogName,sLogText=func.func_name,func.func_code
	#print 'sLogName,sLogText,iCost>>>',sLogName,sLogText,iCost
	log.log('%s.log'%sLogName,'cost %d\t%s '%(iCost,sLogText))



#获得i有多少个十进制位
def decimalCarry(i):
	if type(i)==float:
		raise Exception,'不得是浮点型'
	if i==0:
		return 1
	iCnt=0
	while i:
		iCnt+=1
		i/=10
	return iCnt

#生成带服务器编号信息作后缀的唯一id.这样合区也不怕数据键值相同
#在iBase进行加1,bBaseHasPostfix表示iBase是否本身是否带有后缀
#return	唯一id(当前服序号（可变长）+服务器编号（可变长）+服务器编号长度（1位））
def guIdWithPostfix(iNo,iBase=0,bBaseHasPostfix=False):
	iDecCarry=decimalCarry(iNo)
	iMod=10**(iDecCarry+1)
	iPostfix=iNo*10+iDecCarry
	if bBaseHasPostfix:
		iPrefix=(iBase/iMod+1)
	else:
		iPrefix=iBase+1
	return iPrefix*iMod+iPostfix

#根据唯一id把所带的编号信息解出来
def getNoByguId(iId):
	iDecCarry = iId%10
	iMod=10**(iDecCarry+1)
	iPostfix = iId%iMod
	return iPostfix/10

#把嵌套的list,tuple,set等等可迭代类型全部展开
def expand(it):
	for item in it:
		if isinstance(item, collections.Iterable):
			for o in item:
				yield o
		else:
			yield item

def formatLocals(dLocals):
	l=[]
	for k,v in dLocals.iteritems():
		l.append('{}\t= {}'.format(k,v))
	return '\n'+'\n'.join(l)

gsSeparator1='= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =\n'
gsSeparator2='- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n'
#日志记录异常,往stderr上写
def logException(sExtra='',iSkip=0):
	etype,value,tb=sys.exc_info()
	sMessage=str(value.message) if value.message else str(value)
	value.message='%$%'+sMessage #加上特殊标识,方便在linux下grep

	if etype==None and value==None and tb==None:#根本没有异常
		return
	#把之前的调用栈也弄出来
	lLine=traceback.format_list(traceback.extract_stack())[iSkip:-2]#[]#
	sText1=''.join(lLine)
	sText2=traceback.format_exc()#traceback.print_exc()	
	if sExtra:
		sTextAll='{}{}{}{}{}'.format(gsSeparator1,sText1,gsSeparator2,sText2,sExtra)#u.py 
	else:
		sTextAll='{}{}{}{}'.format(gsSeparator1,sText1,gsSeparator2,sText2)
	sys.stderr.write(sTextAll)

#重新抛出异常
#sText	异常提示信息
def reRaise(sText,exceptionType=None):	
	etype,value=sys.exc_type,sys.exc_value
	sMessage=value.message if value.message else str(value) #umysql.SQLError 竟然value.message是空串,但是str(value)又可以拿得到	
	if exceptionType is None:		
		raise etype,'{};{}'.format(sText,sMessage),sys.exc_traceback
	else:
		raise exceptionType,'{};{}:{}'.format(sText,etype.__name__,sMessage),sys.exc_traceback

#在windows下要把uft8转成gbk,linux则原样返回uft8
def trans(sUTF8Text):#即将废掉	
	return sUTF8Text

def trans2gbk(sUTF8Text):#即将废掉
	return sUTF8Text

def trans2utf8(sGBKtext):#
	if platform.system().upper()=='WINDOWS':
		try:
			return sGBKtext.decode('gbk').encode('utf-8')
		except Exception:			
			raise
	return sGBKtext

#获得递归字典里面的val
#例：DictInnerVal({"x":{"y":1}},"x","y") == 1
def dictInnerVal(dDict,*tKey):
	for key in tKey:
		dDict=dDict[key]
	return dDict

def transMsg(oMsg):#默认的msg每个域用换行分隔,改成逗号分隔.
	return '{}'.format(oMsg).replace('\n',',')

#检查dDict深度是否超过iDepth,即是多少级的字典
def dictDepthIsOver(dDict,iDepth):
	if type(dDict)!=types.DictType:
		raise Exception,'dDict参数必须是字典.'
	if iDepth<=1:
		return True
	for k,v in dDict.iteritems():
		if type(v)==types.DictType:
			if DictDepthIsOver(v,iDepth-1):
				return True
	return False

#键映射代理(只做关联,不影响obj的生命期,obj是其他地方持有的.内部存储的只是proxy)
#这个类可以简化dProxy清理工作,因为捕捉了析构行为
class cKeyMapProxy(object):
	def __init__(self):
		self.dProxy={}

	def amount(self):
		return len(self.dProxy)

	def getAll(self):
		return self.dProxy

	def getProxy(self,*tKey):
		#因为有可能同一个对象绑定了多个析构函数,obj被销毁之后,本类的__deleter还没有调用前,有其他地方的析构函数访问了getProxy
		#导致出现ReferenceError: weakly-referenced object no longer exists
		#所以在这里提前检查proxy是否有效,无效则返回None出去
		oPrx=self.dProxy.get(tKey)
		try:
			if oPrx:
				pass
			return oPrx
		except Exception:
			return None
		 

	def addObj(self,obj,*tKey):
		if not tKey:
			raise Exception,'必须提供主键.'
		if type(obj)==weakref.ProxyType:
			if not hasattr(obj,'this'):
				raise Exception,'必须实现this成员函数,函数返回一个self即可.'
			obj=obj.this()

		self.dProxy[tKey]=weakref.proxy(obj,cFunctor(self.__deleter,tKey))

	def removeProxy(self,*tKey):#移除掉(一般靠析构函数自动移除,但是发生循环引用就要依靠手动调用此函数)
		self.dProxy.pop(tKey,None)

	def __deleter(self,prx,tKey):		
		if id(prx)!=id(self.dProxy.get(tKey)):#用id来判断是不是同一个proxy,避免异常 ReferenceError: weakly-referenced object no longer exists				
			return
		self.dProxy.pop(tKey,None)

def getRealObj(obj):#从proxy中取得真实的obj
	if type(obj)==weakref.ProxyType:
		if not hasattr(obj,'this'):
			raise Exception,'必须实现this成员函数,函数返回一个self即可.'
		obj=obj.this()
	return obj

#用于统一管理监控实例,对象是没有key的.(obj的生命期不在这里管理,内部存储的只是弱引用,obj是其他地方持有的.)
#若是发生循环引用,这里的对象统计是不准确的
class cWeakRefManager(object):
	def __init__(self):
		self.sWeakRef=set()

	def amount(self):#总共个数
		return len(self.sWeakRef)

	def getAllWeakRef(self):#取得全部弱引用
		return self.sWeakRef

	def getAllObj(self):#取得全部对象
		for wr in self.sWeakRef:
			obj=wr()
			if obj:
				yield obj

	def addObj(self,obj):
		wr=weakref.ref(obj,cFunctor(self.__deleter))#循环引用自己的成员函数了(还是用cFunctor来避免循环吧)
		self.sWeakRef.add(wr)

	def removeWeakRef(self,wr):#移除掉
		self.sWeakRef.discard(wr)

	def __deleter(self,wr):
		self.sWeakRef.discard(wr)

#替换前后两端的空格(半角,全角)
#注意返回的值和实参不是同一个对象
#\x09: Tab
#\x20: 半角空格
#\xa1\xa1:全角空格
#\x0D\x0A :回车

def trim(sText):#修剪两端的空白字符(包括tab,半角空格,全角空格,回车换行...)
	if not isinstance(sText, basestring):
		return sText
	if not sText:
		return sText
	#正则
	pattern = re.compile('^(\x09|\x20|\x0D\x0A|\xa1\xa1)+|(\x09|\x20|\x0D\x0A|\xa1\xa1)+$')
	return pattern.sub('', sText)

#是否包含非法字符,任何玩家输入的都要用这个函数检查
def isInvalidText(*tArgs):#为什么禁止这些字符入库,原因查看sql.py后面的注释
	for sText in tArgs:		
		if '\'' in sText:
			return '\''
		if '"' in sText:
			return '"'
		if '\\' in sText:
			return '\\'
	return '' #空串表示合法

def callLambda(lambdaFunc,obj,*tArgs,**dArgs):
	lParameter=[]
	getValFunc=getattr(obj,'_getValueByVarName',None)
	if not getValFunc:
		raise Exception,'obj必须实现_getValueByVarName方法'
	for sVarName in lambdaFunc.func_code.co_varnames:
		lParameter.append(getValFunc(sVarName,*tArgs,**dArgs))
	return lambdaFunc(*lParameter)


def regDestructor(obj,func):#给obj注册析构函数
	oReal=getRealObj(obj)
	if type(func)==types.MethodType and func.im_self==oReal:
		raise Exception,'func不能是obj自身的成员函数'
	iHashVal=hash(oReal)

	def innerFunc(prx):
		gdProxy.pop(iHashVal,None)#从全局dict弹掉
		func()#执行析构		

	gdProxy[iHashVal]=weakref.proxy(oReal,innerFunc)

def transSocketMsg():#把windows下socket抛出的gbk错误转为utf8
	value=sys.exc_value
	sMessage=value.message if value.message else str(value)
	if platform.system().upper()=="WINDOWS":
		sMessage=sMessage.decode('gbk').encode('utf-8')
	return sMessage



import collections
import sys
import traceback
import weakref
import types
import random
import sys
import platform
import time
import log
import re

if 'gbOnce' not in globals():
	gbOnce=True
	
	gdProxy={}