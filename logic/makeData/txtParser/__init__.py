# -*-coding:utf-8-*-
# 作者:马昭@曹县闫店楼镇
# 文本文件分析器
from common import *

class cTxtParser(object):
	def __init__(self, sVarName, sSrcPath, ignore=False):
		self.sVarName = sVarName
		self.sSrcPath = sSrcPath
		self.ignore = ignore  # 忽略文件是否存在
		self.sTextName = sSrcPath[sSrcPath.rfind('/') + 1:]  # 出错时好提示相应的sl文件名

		#+-*/|^&()%>><<~ ** //
		self.expre = re.compile(r'[\+\-\*/\|\^&\(\)%>><<~]{1,2}') #分割表达式
		self.numre = re.compile(r'[\d]{1,}')	#判断一个字符串是否为全部数字

	def getVarName(self):  # 数据结构的变量名
		return self.sVarName

	def getParseTxt(self):  # 数据结构的内容
		raise NotImplementedError
	
	def formatData(self, sText, iFormat):
		'''格式化数据
		'''
		sText = sText.strip()

		# 猜测顺序是有讲究的
		if iFormat & makeData.D:  # 互斥的,说了是什么就是什么
			return '{{{}}}'.format(sText)
		elif iFormat & makeData.L:  # 互斥的,说了是什么就是什么
			return '[{}]'.format(sText)
		elif iFormat & makeData.T:  # 互斥的,说了是什么就是什么
			if sText == '' or sText.rfind(',') == len(sText) - 1:  # 没有元素,或最后面有逗号了
				return '({})'.format(sText)
			else:
				return '({},)'.format(sText)
		elif iFormat & makeData.S:
			if "\"" in sText or "'" in sText:
				return '"""%s"""' % sText
			return '"%s"' % sText
		elif iFormat & makeData.E:  #
			lStr = self.expre.split(sText)
			lPara = []
			for s in lStr:
				#判断是否为纯数字
				if s != "" and not self.numre.search(s):
					lPara.append(s)
			lPara = list(set(lPara))	#参数去重
			fun = "lambda {}:{}".format(','.join(lPara), sText)
			eval(fun)  # 检查一下语法
			return fun
		elif len(sText) == 0:
			return ""

		# 根据内容判断
		
		if isNumber(sText):  # 数字
			return sText
		
		r = isDict(sText)  # 字典
		if r:
			if r == 2:
				sText = "{%s}" % sText
			return sText
		
		r = isTuple(sText) # 元组
		if r:
			if r == 2:
				sText = "(%s)" % sText
			return sText
		
		r = isList(sText)  # 列表
		if r:
			if r == 2:
				sText = "[%s]" % sText
			return sText
		
		return '\"%s\"' % sText  # 只能当字符串了
	
	def formatDataByTitle(self, titleName, val, fmt):
		'''根据标题格式化数据
		'''
		if not val:
			return ""
		if hasattr(self, "maker"):
			valNew = self.maker.formatDataByTitle(self, titleName, val, fmt)
			if valNew != None:
				return valNew
		return self.formatData(val, fmt)
	
	def checkFormat(self, sText, iFormat):
		if sText.count('\"') % 2 or sText.count('\'') % 2:
			return "数据单引号或双引号不成对"
		if iFormat & makeData.M:  # 但是属于must填的
			return "不能为空"
		
		return None

	# 返回一个从txt生成的2维list
	def parseTxtTo2dGroup(self):
		try:
			fSrc = open(self.sSrcPath, 'r')  # codecs.open(self.sSrcPath,'r','utf-8')
		except Exception:
			if self.ignore:
				return []
			raise Exception, '找不到 {}'.format(self.sSrcPath)

		lResult = []
		try:
			for iRow, sLineTxt in enumerate(fSrc):
				if iRow == 0 and sLineTxt[:3] == codecs.BOM_UTF8:  # 去掉utf8的文件头
					sLineTxt = sLineTxt[3:]
				
				sLineTxt = sLineTxt.strip('\n')
				sLineTxt = sLineTxt.strip('\r')
				if sLineTxt.count('\t') == len(sLineTxt):  # 一行全是\t
					continue
				if not sLineTxt:
					continue
				# if sLineTxt.startswith('#'):#遇到注释了
				# 	continue

				lTemp = []
				lVal = sLineTxt.split('\t')
				# if len(lVal)>len(self.lFieldFormat):
				# 	raise Exception,'{}文件的列数({})>导表程序的列数({})'.format(self.sTextName,len(lVal),len(self.lFieldFormat))
				# elif len(lVal)<len(self.lFieldFormat):
				# 	raise Exception,'{}文件的列数({})<导表程序的列数({})'.format(self.sTextName,len(lVal),len(self.lFieldFormat))
				if iRow == 0:  # 第1行的注释,要解析表头
					lTitle, lFieldFormat = parseTitle(lVal)
					lResult.append(lTitle)  # 只把title插入
					continue

				for iCol, sVal in enumerate(lVal):
					sTitle = lTitle[iCol] # 标题
					iFormat = lFieldFormat[iCol]
					result = self.checkFormat(sVal, iFormat)
					if result:
						raise Exception, "{}表{}行{}列<{}>:{}".format(self.sTextName, iRow + 1, sTitle, sVal, result)
					sVal = self.formatDataByTitle(sTitle, sVal, iFormat)
					lTemp.append(sVal)

				lResult.append(lTemp)
			return lResult
		finally:
			fSrc.close()
			
	def parseTxtTo2Dict(self):
		'''返回二维字典
		'''
		try:
			f = open(self.sSrcPath, "r")
		except Exception:
			if self.ignore:
				return []
			raise Exception("找不到导表:%s" % self.sSrcPath)

		if hasattr(self, "excelMulti"): # excel表单元格内多行
			lineList = self.transTxtListByMulti(f)
		else:
			lineList = self.transTxtList(f)

		dataList = []
		titleList = []
		formatList = []

		try:
			for rowIdx, valList in enumerate(lineList):
				if rowIdx == 0: # 表头
					titleList, formatList = parseTitle(valList)
					continue
				
				data = {}
				for col, val in enumerate(valList):
					titleName = titleList[col] # 标题
					fmt = formatList[col] # 格式
					result = self.checkFormat(val, fmt)
					if result:
						raise Exception, '{}表{}行{}列<{}>:{}'.format(self.sTextName, rowIdx + 1, titleName, val, result)
					if hasattr(self, "customFormatData"):
						val = self.customFormatData(titleName, val, fmt)
					data[titleName] = val

				dataList.append(data)
		finally:
			f.close()
			
		return dataList
	
	def transTxtList(self, txt):
		'''转换文本
		'''
		txtList = []
		if isinstance(txt, str):
			txtList = txt.split("\n")
		else:
			f = txt
			txtList = f.readlines()
		
		lineList = []
		for rowIdx, line in enumerate(txtList):
			if rowIdx == 0 and line[:3] == codecs.BOM_UTF8:  # 去掉utf8的文件头
				line = line[3:]

			line = line.strip()
			if not line: # 空行
				continue
			lineList.append(line.split("\t"))
				
		return lineList
	
	def transTxtListByMulti(self, txt):
		'''转换excel表单元格有多行的文本
		'''
		txtList = []
		if isinstance(txt, str):
			txtList = txt.split("\n")
		else:
			f = txt
			txtList = f.readlines()
		
		lineList = []
		valList = []
		tmpList = [] # 特殊列的字符串
		for rowIdx, line in enumerate(txtList):
			if rowIdx == 0 and line[:3] == codecs.BOM_UTF8:  # 去掉utf8的文件头
				line = line[3:]

			line = line.strip()
			if not line: # 空行
				continue
	
			for val in line.split("\t"):
				if val.startswith("\""): # 特殊列开始
					tmpList.append(val[1:])
				elif tmpList:
					if val.endswith("\""): # 特殊列结束
						tmpList.append(val[:-1])
						valList.append("||".join(tmpList))
						tmpList = []
					else:
						tmpList.append(val)
				else:
					valList.append(val)
	
			if not tmpList:
				lineList.append(valList)
				valList = []
				
		return lineList

	# 生成一个字典
	def makeDict(self, lKeys, lValues, bIsNewLine=False, iElementIndent=1):  # iElementIndent元素缩进tab个数
		if len(lKeys) == 0 and len(lValues) == 0:
			return '{}'

		# 数据value列不够就补一些空
		for i in xrange(len(lKeys) - len(lValues)):
			lValues.append('')
		# key列少于value列就无视多余的数据列
		lTemp = []
		for i, sKey in enumerate(lKeys):
			try:
				eval(sKey)
			except Exception:
				sKey = '\"%s\"' % sKey
			val = lValues[i]
			if len(val) == 0:
				continue
			lTemp.append('%s:%s' % (sKey, val))
		if bIsNewLine:
			sEndTab = '\t' * (iElementIndent - 1)  # 字典结束符}缩进的tab串
			sElmTab = sEndTab + '\t'  # 元素缩进的tab串
			return '{\n%s' % sElmTab + (',\n%s' % sElmTab).join(lTemp) + ',\n%s}' % sEndTab
		else:
			return '{' + ','.join(lTemp) + '}'

	def makeTuple(self, lItems, bIsNewLine=False, iElementIndent=1):  # iElementIndent元素缩进tab个数
		if bIsNewLine:
			sEndTab = '\t' * (iElementIndent - 1)  # list结束符]缩进的tab串
			sElmTab = sEndTab + '\t'  # 元素缩进的tab串
			return '(\n%s' % sElmTab + (',\n%s' % sElmTab).join(lItems) + ',\n%s)' % sEndTab
		else:
			# 只有一个元素时,tuple的括号会被误解析为是运算符,所以要元素末尾要加逗号
			if len(lItems) == 1:
				return '(' + lItems[0] + ',)'
			else:
				return '(' + ','.join(lItems) + ')'

	def makeList(self, lItems, bIsNewLine=False, iElementIndent=1):  # iElementIndent元素缩进tab个数
		if bIsNewLine:
			sEndTab = '\t' * (iElementIndent - 1)  # 元组结束符)缩进的tab串
			sElmTab = sEndTab + '\t'  # 元素缩进的tab串
			return '[\n%s' % sElmTab + (',\n%s' % sElmTab).join(lItems) + ',\n%s]' % sEndTab
		else:
			return '[' + ','.join(lItems) + ']'

	def isLastInGroup(self, lLines, iCurRow, iCurCol):  # 在当前组中,是否是最后一个key
		if iCurRow + 1 >= len(lLines):  # 已经是整个表最最后一行了,当然是最后一条key了
			return True

		if iCurCol > 0 and self.isLastInGroup(lLines, iCurRow, iCurCol - 1):  # 如果父组都结束了,就不需要当前key与下一个key比较了
			return True

		sCur = lLines[iCurRow][iCurCol]  # 当前行的某列key
		sNext = lLines[iCurRow + 1][iCurCol]  # 下一行的某列key
		if sCur and not sNext:  # 上一行填了key,下一行没有填key,则说明当前行不是本组中最后一个key
			return False
		elif not sCur and sNext:  # 当前行策划没有填,但是下一行策划有填,说明当前行是本组中最后一个key了
			return True
		elif not sCur and not sNext:  # 当前行策划没有填,下一行策划也没有填,说明是当前行不是本组中最后一条key.
			return False
		else:  # sCur and sNext:#当前行与下一行策划都填了,就看填的内容是不是相同的来决定了
			return sCur != sNext

def parseTitle(lVal):  # 解析excel的表头,即是第一行
	lTitel = []
	lFieldFormat = []
	for iCol, sVal in enumerate(lVal):
		iIdx = sVal.find('_')
		if iIdx == -1:
			sTitle = sVal
			iFormat = 0
		else:
			sTitle = sVal[:iIdx]
			iFormat = 0
			for s in sVal[iIdx + 1:].split('|'):
				i = getattr(makeData, s, 0)
				iFormat |= i
	
		lTitel.append(sTitle)
		lFieldFormat.append(iFormat)
	return lTitel, lFieldFormat

# def isInt(iRow,iCol,sText):
# 	try:
# 		int(sText)
# 	except Exception:
# 		return False
# 	return True

# def isFloat(iRow,iCol,sText):
# 	try:
# 		float(sText)
# 	except Exception:
# 		return False
# 	return True

# def isDict(iRow,iCol,sText):
# 	if sText[0]!='{' and sText[-1]!='}':
# 		return False
# 	checkTupleListDict(iRow,iCol,sText)
# 	return True

# def isList(iRow,iCol,sText):
# 	if sText[0]!='[' and sText[-1]!=']':
# 		sText='['+sText+']'
# 		return False
# 	checkTupleListDict(iRow,iCol,sText)
# 	return True

# def isTuple(iRow,iCol,sText):
# 	if sText[0]!='(' and sText[-1]!=')':
# 		return False
# 	checkTupleListDict(iRow,iCol,sText)
# 	return True

# def checkTupleListDict(iRow,iCol,sText):#非法则返回错误原因
# 	if sText.count('{')!=sText.count('}'):
# 		raise Exception,'{}行{}列,{}花括号不匹配'.format(iRow+1,iCol+1)
# 	elif sText.count('[')!=sText.count(']'):
# 		raise Exception,'{}行{}列,[]方括号不匹配'.format(iRow+1,iCol+1)
# 	elif sText.count('(')!=sText.count(')'):
# 		raise Exception,'{}行{}列,()括弧不匹配'.format(iRow+1,iCol+1)
# 	try:
# 		eval(sText)
# 	except Exception:
# 		raise Exception,'{}行{}列,数据错误,{}'.format(iRow+1,iCol+1,sText)





# 是否需要用双引号括起来
# 本来可以用eval解决一切问题的.但是eval有bug,会崩服务器
# 怀疑是 eval('中文字符串时')引起的
# 为了安全多加了上面的很多过滤
# def needQuotationMark(sText):#已作废,但是别删除
# 	if len(sText)==0:
# 		return False
# 	if sText.isalpha():
# 		return True
# 	if sText.isdigit():
# 		return False
# 	try:
# 		float(sText)#是否是数值型
# 		return False
# 	except Exception:
# 		pass

# 	if sText[0] in ('{','(','[') and sText[-1] in ('}',')',']'):#tuple or list or dict
# 		return False
# 	try:
# 		if len(sText)!=len(unicode(sText,'gbk')):	#有中文在里面
# 			return True
# 	except Exception:
# 		return True

# 	try:
# 		eval(sText)
# 		return False
# 	except Exception:
# 		pass
# 	return True

from makeData.defines import *
import codecs
import makeData
import copy
import u
import os
import re
