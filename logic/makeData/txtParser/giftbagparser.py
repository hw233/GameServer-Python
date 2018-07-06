#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser.multiparser

#配置型分析器,字典内嵌字典
class cTxtParser(makeData.txtParser.multiparser.cTxtParser):

	def transEffect(self,effect):
		if not effect:
			return ''
		sEffect = ""
		for data in effect.split(","):
			k,v = data.split(":")
			sEffect += "\"%s\":%d," % (k,int(v))
		return "{"+sEffect[:-1]+"}"

	def formatDataByTitle(self, titleName, val, fmt):
		'''根据标题格式化数据
		'''
		if titleName == "效果":
			return self.transEffect(val)
		return self.formatData(val, fmt)

import re

