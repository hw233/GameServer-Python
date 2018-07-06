#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import makeData.txtParser.configparser

#配置型分析器,字典内嵌字典
class cTxtParser(makeData.txtParser.configparser.cTxtParser):

	def transEffect(self,effectListStr):
		if not effectListStr:
			return ""

		effectListStr = transApplyList(effectListStr, False, 0)
		return "{%s}" % effectListStr

	def formatDataByTitle(self, titleName, val, fmt):
		'''根据标题格式化数据
		'''
		if titleName == "效果":
			return self.transEffect(val)
		return self.formatData(val, fmt)

from makeData.defines import *
import re

