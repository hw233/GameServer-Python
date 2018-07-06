#-*-coding:utf-8-*-
#称号
if "gTitleList" not in globals():
	gTitleList = {}

def create(iNo):
	if iNo not in titleData.gdData:
		raise Exception,'不存在编号为{}的称号.'.format(iNo)
	return title.object.cTitle(iNo)

def newTitle(who, iNo, **dArgs):
	obj = create(iNo)
	# 检查角色身上有无同组的称号，有则替换
	oTitle = hasTitleGroup(who, iNo)
	if oTitle:
		removeTitle(who, oTitle.id, True)
	obj.onBorn(who, **dArgs)
	# 将称号加进角色称号容器
	if who.titleCtn.addItem(obj):
		common.writeLog("title/new", "%d new title %d" % (who.id, iNo))
		who.reCalcAttr()#重新计算人物属性
		message.tips(who, "成功获得称谓#C02{}#n".format(obj.name))
		#获得新称谓时同时帮玩家使用
		bRet = who.titleCtn.putOnTitle(iNo)
		if bRet:
			who.endPoint.rpcTitleUpdate(iNo)
			who.attrChange("title", "titleEffect")
			message.tips(who, "设置称谓成功")
		return obj
	else:
		sReason = "加入容器时出错了"
		if not obj.isActive():
			sReason = "此称号已过了真实有效期"
		common.writeLog("title/new", "%d new title %d failed(%s)" % (who.id, iNo, sReason))
		del obj
		return None

def removeTitle(who, titleId, bReplaced=False):
	'''移除称号
	'''
	oTitle = who.titleCtn.getItem(titleId)
	if not oTitle:
		return
	who.titleCtn.removeTitle(oTitle, bReplaced)
	if not bReplaced:
		who.reCalcAttr()#重新计算人物属性
	common.writeLog("title/remove", "%d remove title %d" % (who.id, titleId))

def hasTitle(who, titleId):
	'''玩家是否拥有指定编号的称谓
	'''
	titleObj = who.titleCtn.getItem(titleId)
	return titleObj


def hasTitleGroup(who, titleId):
	'''玩家是否拥有指定称谓编号组内的称谓
	'''
	titleObj = getTitle(titleId)
	groupId = titleObj.groupId

	for titleObj in who.titleCtn.getAllValues():
		if titleObj.groupId == groupId:
			return titleObj
	return None

def getTitle(titleId):
	'''获取缓存中的称号
	'''
	global gTitleList
	if titleId not in gTitleList:
		titleObj = create(titleId)
		if titleObj:
			gTitleList[titleId] = titleObj
	return gTitleList.get(titleId)

import titleData
import title.object
import common
import message
