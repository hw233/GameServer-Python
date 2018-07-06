#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#对白表分析器
class cTxtParser(makeData.txtParser.cTxtParser):
	#override
	def getParseTxt(self):
		lKeyList=[]
		lValList=[]
		lLines=self.parseTxtTo2dGroup()
		sKey0=""
		lTemp=[]
		for iRow,lLine in enumerate(lLines):
			lTemp.append(lLine[1].strip("\""))

			if lLine[0]!="":
				sKey0=lLine[0]

			if self.isLastInGroup(lLines,iRow,0):
				if len(lTemp)==1:#不跨行的用双引号
					sTemp="\"%s\""%(LINE_SEP.join(lTemp),)
				else:#跨行的用3个双引号
					sTemp="\"\"\"%s\"\"\""%(LINE_SEP.join(lTemp),)
				lKeyList.append(sKey0)
				lValList.append(sTemp)
				lTemp=[]
		return self.makeDict(lKeyList,lValList,True)
	
from makeData.defines import *
