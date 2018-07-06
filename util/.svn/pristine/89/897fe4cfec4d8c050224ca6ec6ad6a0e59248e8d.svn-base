#-*-coding:utf-8-*-
#作者:叶伟龙@龙川县赤光镇

class configParser(object):
	def __init__(self,sPathName):
		self.cfps=ConfigParser.ConfigParser()
		if not os.path.exists(sPathName):
			raise Exception,'{}不存在'.format(sPathName)
		self.cfps.read(sPathName)
		self.sPathName=sPathName

	def __getattr__(self,sPropName):
		if hasattr(self,sPropName):
			return object.__getattribute__(self,sPropName)
		for sSection in self.cfps.sections():
			if self.cfps.has_option(sSection,sPropName):
				if sSection=='int':				
					uValue=self.cfps.getint(sSection,sPropName)
				elif sSection=='boolean':
					uValue=self.cfps.getboolean(sSection,sPropName)
				elif sSection=='float':
					uValue=self.cfps.getfloat(sSection,sPropName)
				else:#其他名字的section解析为字符串
					uValue=self.cfps.get(sSection,sPropName)			
				break
		else:
			sPathName=object.__getattribute__(self,'sPathName')
			raise Exception,'配置文件{}中不存在{}的字段'.format(sPathName,sPropName)
				
		setattr(self,sPropName,uValue)
		return uValue

import ConfigParser
import os.path
import u


#不要重新read配置文件,如果有重新读取配置文件的需求
#就重新生成一个configParser实例,会自动重新读



#以int,float,boolean为名的section会解析成对应的格式
#以其他名字的section则解析成字符串


'''

[int]
serverNo=5


[boolean]
flag=True ;true false TRUE ,tRUe,FalsE 各种大小写的都可以

[float]
pi=3.14159

;分号开头表示注释
;我是注释





'''