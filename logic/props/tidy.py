# -*- coding: utf-8 -*-
'''整理相关
'''

def sortList(propList, reverse=False):
	'''物品排序
	'''
	propList.sort(key=_sortKey, reverse=reverse)
	return propList

def _sortKey(obj):
	lst = []
	if hasattr(obj, "level"):
		lst.append(obj.level)
	if hasattr(obj, "quality"):
		lst.append(obj.quality)
	if hasattr(obj, "score"):
		lst.append(obj.getScore())
	lst.append(-obj.id)
	return lst