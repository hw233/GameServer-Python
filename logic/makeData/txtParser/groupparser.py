# -*- coding: utf-8 -*-
import makeData.txtParser

class cTxtParser(makeData.txtParser.cTxtParser):
	'''分组表
	'''

	def getParseTxt(self):
		dataList = self.parseTxtTo2Dict()
		if not dataList:
			return "{\n}"

		txtList = []
		for data in dataList:
			txtList.append("%s:%s," % (data["编号"], data["列表"]))
			
		dataStr = "\n".join(txtList)
		return "{\n%s\n}" % indent(dataStr, 1)

	def customFormatData(self, titleName, val, fmt):
		'''根据标题格式化数据
		'''
		if titleName == "列表":
			return "(%s,)" % val
		return self.formatData(val, fmt)
	
from makeData.defines import *
