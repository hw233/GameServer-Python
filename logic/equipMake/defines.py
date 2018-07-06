# -*- coding: utf-8 -*-

giMakePropNo = 241001	#打造符
giTailorPropNo = 241101	#裁缝符
giAlchemistPropNo = 241201	#炼金符

glAllMakePropsNo = []		#所有打造符物品编号
glAllTailorPropsNo = []		#所有裁缝符物品编号
glAllAlchemistPropsNo = []	#所有炼金符物品编号

for i in xrange(11):
	glAllMakePropsNo.append(giMakePropNo+i)
	glAllTailorPropsNo.append(giTailorPropNo+i)
	glAllAlchemistPropsNo.append(giAlchemistPropNo+i)

def getUpPropsNo(iPropNo):
	'''重铸向下兼容的功能
	'''
	if iPropNo in glAllMakePropsNo:
		return glAllMakePropsNo[glAllMakePropsNo.index(iPropNo):]

	if iPropNo in glAllTailorPropsNo:
		return glAllTailorPropsNo[glAllTailorPropsNo.index(iPropNo):]

	if iPropNo in glAllAlchemistPropsNo:
		return glAllAlchemistPropsNo[glAllAlchemistPropsNo.index(iPropNo):]

	return []

