#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#买与卖货物价格表分析器
class cTxtParser(makeData.txtParser.cTxtParser):
	#override
	def getParseTxt(self):
		lKey=[]
		lVal=[]
		lKey2=[]
		lVal2=[]
		sKey0=""

		lLines=self.parseTxtTo2dGroup()

		for iRow,lLine in enumerate(lLines):
			lKey.append(lLine[1])
			lVal.append(lLine[2])

			if lLine[0]!="":
				sKey0=lLine[0]

			if self.isLastInGroup(lLines,iRow,0):
				lKey2.append(sKey0)
				sTemp=self.makeDict(lKey,lVal,True,2)
				lVal2.append(sTemp)
				lKey=[]
				lVal=[]

		return self.makeDict(lKey2,lVal2,True,1)