#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#配置型分析器,字典内嵌字典
class cTxtParser(makeData.txtParser.cTxtParser):
	
	def getParseTxt(self):#override
		dataList = self.parseTxtTo2dGroup()
		if not dataList:
			return "{\n}"

		lKeyList=[]
		lValList=[]
		dValList={}
		count=0
		for iRow,lLine in enumerate(dataList):
			if iRow==0:#title栏
				lKeyList=lLine
				continue
			for count,uValue in enumerate(lLine):
				if uValue:
					lst = dValList.setdefault(count,[])
					lst.append(uValue)

		for iRow in range(0,count+1):
			lst = dValList[iRow]
			sTemp = self.makeList(lst,False)
			lValList.append(sTemp)

		return self.makeDict(lKeyList,lValList,True)

import u