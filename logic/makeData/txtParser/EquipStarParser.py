#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#称号标签表分析器
class cTxtParser(makeData.txtParser.cTxtParser):
	#override
	def getParseTxt(self):
		lKeyList1=[]
		lValList1=[]
		lKeyList2=[]
		lValList2=[]
		lKeyList3=[]
		lValList3=[]
		sKey0=""
		tFieldName=("Icon","StarAttr","SuccessRatio","NeedCost")
		lLines=self.parseTxtTo2dGroup()

		for iRow,lLine in enumerate(lLines):
			for iIndex,uValue in enumerate(lLine):
				if iIndex == 0 and uValue != "":
					sKey0=uValue
				elif iIndex == 1:
					lKeyList2.append(uValue)
				else:
					lKeyList3.append(tFieldName[iIndex-2])
					lValList3.append(uValue)
				if iIndex == len(lLine)-1:
					sTemp3=self.makeDict(lKeyList3,lValList3,False,2)
					lKeyList3=[]
					lValList3=[]
					lValList2.append(sTemp3)

			if self.isLastInGroup(lLines,iRow,0):
				sTemp=self.makeDict(lKeyList2,lValList2,True,2)
				lKeyList1.append(sKey0)
				lValList1.append(sTemp)
				lKeyList2=[]
				lValList2=[]

		return self.makeDict(lKeyList1,lValList1,True,1)

