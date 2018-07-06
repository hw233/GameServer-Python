#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser

#配置型分析器,元组
class cTxtParser(makeData.txtParser.cTxtParser):
	def getParseTxt(self):
		l=[]
		for index,lLine in enumerate(self.parseTxtTo2dGroup()):
			if index == 0:
				continue
			sName = lLine[0]
			if u'\xa0' in sName.decode("utf-8"):
				raise PlannerError,'{}加入空格'.format(sName)
			l.append(lLine[0])
		return self.makeTuple(l,True)

