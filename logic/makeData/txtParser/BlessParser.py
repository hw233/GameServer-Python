#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#奖励表分析器
class cTxtParser(makeData.txtParser.cTxtParser):

	#override
	def getParseTxt(self):
		tFieldName=("WishWord",)
		lKey0=[]
		lVal0=[]
		lKey1=[]
		lVal1=[]
		lTupleItem=[]
		lLines=self.parseTxtTo2dGroup()
		sKey0=""

		for iRow,lLine in enumerate(lLines):
			sTemp=self.makeDict(tFieldName,lLine[2:],False)
			lTupleItem.append(sTemp)

			if lLine[1]!="":
				sKey1=lLine[1]
			if self.isLastInGroup(lLines,iRow,1):
				sTemp=self.makeTuple(lTupleItem,True,2)
				lKey1.append(sKey1)
				lVal1.append(sTemp)

				lTupleItem=[]

			if lLine[0]!="":
				sKey0=lLine[0]
			if self.isLastInGroup(lLines,iRow,0):
				sTemp=self.makeDict(lKey1,lVal1,True,1)
				lKey1=[]
				lVal1=[]
				lKey0.append(sKey0)
				lVal0.append(sTemp)

		return self.makeDict(lKey0,lVal0,True,1)





