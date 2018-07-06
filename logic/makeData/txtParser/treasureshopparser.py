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
		for iRow,lLine in enumerate(dataList):
			if iRow==0:#title栏
				lTitle=lLine
				continue
			if lLine[5] in lKeyList:
				raise PlannerError,'编号{}已经存在,请不要重复'.format(lLine[5])
			lKeyList.append(lLine[5])
			sTemp=self.makeDict(lTitle[6:],lLine[6:],False)
			lValList.append(sTemp)
		return self.makeDict(lKeyList,lValList,True)

import u