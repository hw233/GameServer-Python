#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
'''内存相关的指令
'''

import types
#-----------------------------
def gcEnable(ep):
	gc.enable()	
	ep.rpcTips('打开GC成功')

def gcDisable(ep):
	gc.disable()	
	ep.rpcTips('关闭GC成功')

def gcCollect(ep):
	gc.collect()	
	ep.rpcModalDialog('收集垃圾OK')

def gcStatus(ep):
	if gc.isenabled():
		ep.rpcModalDialog('GC当前处于打开状态')
	else:
		ep.rpcModalDialog('GC当前处于关闭状态')

def debugCollect(ep,bIsLog=False):
	iBefore=len(gc.garbage)
	gc.set_debug(gc.DEBUG_LEAK)
	gc.collect()
	gc.set_debug(0)
	iAfter=len(gc.garbage)
	ep.rpcModalDialog('收集前已有{}垃圾,收集后共有{}垃圾,本次收集到{}个垃圾',iBefore,iAfter,iAfter-iBefore)
	if gc.garbage and bIsLog:
		log.log('garbage','{}'%gc.garbage)

def removeGarbage(ep):
	iLen=len(gc.garbage)
	#gc.garbage=[] 不能这么做,这样只是换了个容器,只能一个一个地pop出来并打破循环.
	while  gc.garbage:
		obj=gc.garbage.pop()
		try:
			if hasattr(obj,'__del__'):
				obj.__del__()
			elif hasattr(obj,'__dict__'):
				for sName in obj.__dict__.keys():					
					obj.__dict__.pop(sName, None)#pop掉obj的每一个属性
		except Exception:
			u.logException()
	ep.rpcModalDialog('清空了gc.garbage中的{}垃圾'.format(iLen))

#若是有循环引用,且循环链中的对象有重写了__del__,在collect之后,一定会被移到gc.garbage里面.
#若是有循环引用,且有设置DEBUG_LEAK,在collect之后,一定会被移到gc.garbage里面.


#----------------------------------------------
def referrers(ep,sClassName,bIsLog=False):
	l=[]
	for obj in gc.get_objects():
		sName=type(obj).__name__
		if sName==sClassName:
			l.extend(gc.get_referrers(obj))
	if l and bIsLog:
		log.log(sClassName+'Referrers','\n'.join(l))
	ep.rpcModalDialog('执行完毕')

def objAmount(ep):
	ep.rpcModalDialog('共有{}个对象'.format(len(gc.get_objects())))

def logObjAmount(ep):
	d={}
	for obj in gc.get_objects():
		sName=type(obj).__name__
		d[sName]=d.get(sName,0)+1
	log.log('objAmount','{}'.format(d))	
	ep.rpcTips('统计对象个数ok')

def dumpMemory(ep):
	sFile = 'spartaMemory'
	meliae.scanner.dump_all_objects(sFile)	
	ep.rpcTips('dump内存成功')

def analyzeMemory(ep):
	sFile = 'spartaMemory'
	obj_mgr = meliae.loader.load(sFile, using_json=None, show_prog=False, collapse=True)
	obj_mgr.remove_expensive_references()
	summarize = obj_mgr.summarize()
	log.log('analyzeMemory','{}'.format(ummarize))

def refMem(ep):
	sFile = 'spartaMemory'
	obj_mgr = meliae.loader.load(sFile, using_json=None, show_prog=False, collapse=True)
	p = obj_mgr.get_all('CPlayer')#列表
	log.log('RefIt','{}'%p[0].c)	#引用谁
	log.log('ItRef','{}'%p[0].p)	#谁引用



import gc
import time
#import gevent
import c
import u
import log
import resume
import misc
#import meliae
#import meliae.scanner
#import meliae.loader


