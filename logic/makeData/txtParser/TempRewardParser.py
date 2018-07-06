#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#兑换表分析器
class cTxtParser(makeData.txtParser.cTxtParser):
	#override
	def getParseTxt(self):
		lKeyList1=[]
		lValList1=[]
		lKeyList2=[]
		lValList2=[]
		lKeyList3=[]
		lValList3=[]
		sKey0,sKey1="",""
		tFieldName=("Reward","Freeze","Title","Content")
		lLines=self.parseTxtTo2dGroup()

		for iRow,lLine in enumerate(lLines):
			sTemp=self.makeDict(tFieldName,lLine[3:],False,4)
			lKeyList3.append(lLine[2])
			lValList3.append(sTemp)


			if lLine[1]!="":
				sKey1=lLine[1]

			if self.isLastInGroup(lLines,iRow,1):
				sTemp=self.makeDict(lKeyList3,lValList3,True,3)
				lKeyList3=[]
				lValList3=[]
				lKeyList2.append(sKey1)
				lValList2.append(sTemp)

			if lLine[0]!="":
				sKey0=lLine[0]
			if self.isLastInGroup(lLines,iRow,0):
				sTemp=self.makeDict(lKeyList2,lValList2,True,2)
				lKeyList2=[]
				lValList2=[]
				lKeyList1.append(sKey0)
				lValList1.append(sTemp)

		return self.makeDict(lKeyList1,lValList1,True,1)

