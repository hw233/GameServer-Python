#-*-coding:utf-8-*-
#作者:叶伟龙@龙川县赤光镇

#对象管理器

#key映射obj
#作用是当调用getObj拿到是proxy
#确保obj的ownership是属于这个keeper,不会发生ownership转移或被共享
class cKeeper(object):
	def __init__(self):
		self.dProxy={}#实例的代理
		self.dObjs={}#实例的强引用



	def getObj(self,*tPriKey):#返回proxy
		if not tPriKey:
			raise ValueError,'请提供主键.'	
		return self.dProxy.get(tPriKey)

	def addObj(self,obj,*tPriKey):
		if not tPriKey:
			raise ValueError,'请提供主键.'
		if tPriKey in self.dObjs:
			return
			#raise Exception,'{}为key的对象已在管理器中了{}.'.format(tPriKey,obj)
		self.dProxy[tPriKey]=weakref.proxy(obj)
		self.dObjs[tPriKey]=obj

	def removeObj(self,*tPriKey):
		if not tPriKey:
			raise ValueError,'请提供主键.'
		#下面两句有顺序的,先从proxy弹出,避免从dObjs弹出进引起的析构函数访问dProxy里面的元素,
		#引起ReferenceError: weakly-referenced object no longer exists			
		self.dProxy.pop(tPriKey,None)
		self.dObjs.pop(tPriKey,None)

	def removeAllObj(self):
		self.dProxy={}
		self.dObjs={}
				
	def amount(self):
		return len(self.dObjs)

	def getItems(self):
		return self.dProxy.items()

	def getKeys(self):
		return self.dProxy.keys()

	def getValues(self):
		return self.dProxy.values()

	def getIterItems(self):
		return self.dProxy.iteritems()

	def getIterKeys(self):
		return self.dProxy.iterkeys()

	def getIterValues(self):
		return self.dProxy.itervalues()
import weakref
import log
import u