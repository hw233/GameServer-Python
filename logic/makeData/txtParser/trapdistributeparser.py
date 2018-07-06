#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#怪物,机关分布表分析器
class cTxtParser(makeData.txtParser.cTxtParser):
	#override
	def getParseTxt(self):
		lKeyList1=[]
		lValList1=[]
		lKeyList2=[]
		lValList2=[]
		lKeyList3=[]
		lValList3=[]
		lTemp=[]
		sKey0=sKey1=sTemp=""

		lLines=self.parseTxtTo2dGroup()
		for iRow,lLine in enumerate(lLines):
			sTemp=self.makeTuple(lLine[2:5],False)
			lKeyList1.append(sTemp)
			lValList1.append(lLine[5])
			if lLine[1]!="":
				sKey1=lLine[1]

			if self.isLastInGroup(lLines,iRow,1):
				sTemp=self.makeDict(lKeyList1,lValList1,True,3)
				lKeyList1=[]
				lValList1=[]
				lKeyList2.append(sKey1)
				lValList2.append(sTemp)

			if lLine[0]!="":
				sKey0=lLine[0]
			if self.isLastInGroup(lLines,iRow,0):
				sTemp=self.makeDict(lKeyList2,lValList2,True,2)
				lKeyList2=[]
				lValList2=[]
				lKeyList3.append(sKey0)
				lValList3.append(sTemp)
		return self.makeDict(lKeyList3,lValList3,True,1)