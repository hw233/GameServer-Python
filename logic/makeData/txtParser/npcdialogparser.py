#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#npc对白表分析器
class cTxtParser(makeData.txtParser.cTxtParser):
	#override
	def getParseTxt(self):
		lKeyList1=[]
		lValList1=[]
		lKeyList2=[]
		lValList2=[]
		sTemp=''
		lTemp=[]
		sKey0=sKey1=''
		lLines=self.parseTxtTo2dGroup()


		for iRow,lLine in enumerate(lLines):
			lTemp.append(lLine[2].strip('\"'))#去掉头尾的双引号

			if lLine[1]!='':
				sKey1=lLine[1]

			if self.isLastInGroup(lLines,iRow,1):
				if len(lTemp)==1:#不跨行的用双引号
					sTemp="\"%s\""%lTemp[0]
				else:#跨行的用3个双引号
					sTemp="\"\"\"%s\"\"\""%(LINE_SEP.join(lTemp),)
				lKeyList1.append(sKey1)
				lValList1.append(sTemp)
				lTemp=[]

			if lLine[0]!="":
				sKey0=lLine[0]
			if self.isLastInGroup(lLines,iRow,0):
				lKeyList2.append(sKey0)
				sTemp=self.makeDict(lKeyList1,lValList1,True,2)
				lValList2.append(sTemp)
				lKeyList1=[]
				lValList1=[]

		return self.makeDict(lKeyList2,lValList2,True,1)
	
from makeData.defines import *