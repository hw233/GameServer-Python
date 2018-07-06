#!/usr/bin/python
#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#递归地import全部模块,并自动调用各个py文件的 autoInit 函数.


#作废了,先保留别删吧
FUNC_NAME='autoInit'

def _dealFile(sPath,sPrefix):	
	sPath=sPath[len(sPrefix):]#去掉路径前缀
	if sPath.startswith(os.path.sep):#去得不干净
		sPath=sPath[1:]
	sPath=sPath.replace(os.path.sep,'.')

	if sPath.endswith('.__init__.py'):
		sMod=sPath[:-len('.__init__.py')]
	else:
		sMod=sPath[:-len('.py')]
	#if sMod!='init':
	mod=hotUpdate.importPath(sMod)
	return getattr(mod,FUNC_NAME,None)

def _dealDir(sDir,sPrefix):
	lInitFunc=[]
	for sSub in os.listdir(sDir):
		sNew=os.path.join(sDir,sSub)
		if os.path.isdir(sNew):
			l=_dealDir(sNew,sPrefix)
			lInitFunc.extend(l)
		elif os.path.isfile(sNew) and sNew.endswith('.py'):
			func=_dealFile(sNew,sPrefix)
			if func and func not in lInitFunc:
				lInitFunc.append(func)
	return lInitFunc


#外部是这样子用的
#initCall.importAndCall('logic')


def importAndCall(*tPaths):#启服时调用
	#全部模块预先import一遍,让各模块的全局代码运行一遍,各模块的全局变量即时生效
	for sPath in tPaths:
		if not os.path.exists(sPath):
			continue
		lInitFunc=_dealDir(sPath,sPath)
		for func in lInitFunc:
			#print 'func=',func.func_code
			func()

import os
import os.path
import hotUpdate			