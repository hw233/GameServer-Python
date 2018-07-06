#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

#py文件生成器
class cPyMaker(object):
	def __init__(self,sDstPath='',*tParser,**dArgs):
		self.sDstPath=sDstPath
		self.tParser = []
		self.addParser(*tParser)
		tFlags=dArgs.get('flag')
		if tFlags:
			self.sBeginFlag=tFlags[0]
			self.sEndFlag=tFlags[1]
		else:
			self.sBeginFlag='#导表开始'
			self.sEndFlag='#导表结束'	
			
	def addParser(self, *parserList):
		for parserObj in parserList:
			parserObj.maker = weakref.proxy(self)
			self.tParser.append(parserObj)

	def getParserGroup(self):
		return self.tParser
	
	def getParserByName(self, name):
		'''根据名称获取文本分析器
		'''
		for parser in self.tParser:
			if parser.getVarName() == name:
				return parser
		return None

	def getDstPath(self):
		return self.sDstPath
	
	def formatDataByTitle(self, parser, titleName, val, fmt):
		return None

	def getBeWriteTxt(self):
		list=[]
		for ps in self.getParserGroup():
			list.append(ps.getVarName()+'='+ps.getParseTxt())
		lineSep = LINE_SEP * 2
		return lineSep.join(list)

	def makeToPyFile(self):
		if not self.getParserGroup():#一个解析器也没有
			raise Exception,'没有文本解析器'
		sTemp=self.getBeWriteTxt()
		sPath=self.getDstPath()
		sFlag1,sFlag2=self.sBeginFlag,self.sEndFlag
		if not os.path.exists(sPath):
			sTemp='''#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
'''+sFlag1+LINE_SEP+sTemp+LINE_SEP+sFlag2
		else:
			fDst=open(sPath,'rb')#读
			sOri=fDst.read()
			iBegin=sOri.find(sFlag1)
			iEnd=sOri.find(sFlag2)
			if iBegin==-1:
				fDst.close()
				raise Exception,'错误,{}没有导表开始标志 {}'.format(sPath,sFlag1)
			if iEnd==-1:
				fDst.close()
				raise Exception,'错误,{}没有导表结束标志 {}'.format(sPath,sFlag2)
			if iBegin>iEnd:
				fDst.close()
				raise Exception,'错误,导表开始,结束标志位置反了 {}'.format(sPath)

			iBegin+=len(sFlag1)
			sTemp=sOri[:iBegin]+LINE_SEP+sTemp+LINE_SEP+sOri[iEnd:]
			fDst.close()
		fDst=open(sPath,'wb')#写
		fDst.seek(0,0)
		fDst.write(sTemp)
		fDst.close()


import weakref
import os.path
import u
import log
from makeData.defines import *
