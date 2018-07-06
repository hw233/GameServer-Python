#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#已经作废
#场景固定怪物分析器
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
			lKey2.append(self.makeTuple(lLine[1:-1],False))
			lVal2.append(lLine[-1])

			if lLine[0]!="":
				sKey0=lLine[0]

			if self.isLastInGroup(lLines,iRow,0):
				lKey.append(sKey0)
				lVal.append(self.makeDict(lKey2,lVal2,True,2))
				lKey2=[]
				lVal2=[]

		return self.makeDict(lKey,lVal,True,1)