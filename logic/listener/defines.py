# -*- coding: utf-8 -*-

#===============================================================================
# 检查触发条件
#===============================================================================
operatorList = (
	"<=", ">=", "!=", "==",
	"<", ">",
)

def checkCondition(who, conditionStr, **kwargs):
	'''检查条件
	'''
	exList = splitCondition(conditionStr)
	exLeft, oprt, exRight = exList # 左表达式,操作符,右表达式
	resultLeft = doExpression(who, exLeft, **kwargs) # 左表达式结果
	resultRight = doExpression(who, exRight, **kwargs) # 右表达式结果
	exStr = "%s %s %s" % (resultLeft, oprt, resultRight)
	return eval(exStr)
	
def splitCondition(conditionStr):
	'''分离条件
	'''
	for oprt in operatorList:
		if oprt in conditionStr:
			exLeft, exRight = conditionStr.split(oprt)
			return exLeft, oprt, exRight
	raise Exception("分离条件时，条件的格式错误:%s" % conditionStr)

def doExpression(who, exStr, **kwargs):
	'''执行表达式
	'''
	handlerName, args = splitHandlerNameAndArgs(exStr)
	func = expressionHandlerList.get(handlerName)
	if func:
		result = func(who, *args, **kwargs)
	else:
		result = exStr

	if isinstance(result, str):
		if isInteger(result):
			result = int(result)
		elif isFloat(result):
			result = float(result)
		else:
			result = "'%s'" % result

	return result
	
def splitHandlerNameAndArgs(exStr):
	'''分离出处理器名和参数
	'''
	m = re.match("(\S+)\((\S+)\)", exStr)
	if m:
		name = m.group(1)
		args = []
		for arg in m.group(2).split(","):
			if isInteger(arg):
				arg = int(arg)
			elif isFloat(arg):
				arg = float(arg)
			args.append(arg)
	else:
		name = exStr
		args = []
	return name, args


#===============================================================================
# 条件检查表达式对应的处理函数
#===============================================================================

def getRoleLevel(who, *args, **kwargs):
	'''获取角色等级
	'''
	if "level" in kwargs:
		return kwargs["level"]
	return who.level

def getPetLevel(who, *args, **kwargs):
	'''获取宠物等级
	'''
	if "level" in kwargs:
		return kwargs["level"]

	if "petId" in kwargs:
		petObj = who.petCtn.getItem(kwargs["petId"])
		if petObj:
			return petObj.level

	return 0

def getAllSchoolSkillLevel(who, *args, **kwargs):
	'''所有门派技能等级
	'''
	levelList = []
	import skillSchData
	for skillId in skillSchData.getOpenSchSkill(who.school, who.level):
		level = who.querySkillLevel(skillId)
		levelList.append(level)
		
	if not levelList:
		return 0
	return min(levelList)

def getGender(who, *args, **kwargs):
	'''获取性别
	'''
	import role.defines
	if who.gender == role.defines.MALE:
		return "男"
	return "女"

def hasTaskType(who, taskId, **kwargs):
	'''拥有任务类型
	'''
	if task.hasTask(who, taskId):
		return 1
	return 0

def hasTitle(who, titleId, **kwargs):
	'''拥有称谓
	'''
	if who.titleCtn.getItem(titleId):
		return 1
	return 0

def hasAchv(who, achvId, **kwargs):
	'''拥有成就
	'''
	if who.achCtn.getItem(achvId):
		return 1
	return 0

def getPropsNo(who, *args, **kwargs):
	'''物品编号
	'''
	return kwargs.get("propsNo", 0)

def getBuddyNo(who, *args, **kwargs):
	'''伙伴编号
	'''
	return kwargs.get("buddyNo", 0)

def getPrice(who, *args, **kwargs):
	'''单价
	'''
	return kwargs.get("price", 0)


def isRare(who, *args, **kwargs):
	'''珍品
	'''
	propsId = kwargs.get("propsId", 0)
	propsObj = who.getProps(propsId)
	if propsObj and propsObj.isRare():
		return 1
	return 0

def recastIsRare(who, *args, **kwargs):
	'''装备重铸后是否为珍品
	'''
	return kwargs.get("recastIsRare", 0)

def getEquipSkillCount(who, *args, **kwargs):
	'''身上装备特技数
	'''
	count = 0
	for propsObj in who.equipCtn.getAllWearEquip():
		if propsObj.fetch("spSkill"):
			count += 1
	return count

def getTaskId(who, *args, **kwargs):
	'''任务编号
	'''
	return kwargs.get("taskId", 0)

def getTaskType(who, *args, **kwargs):
	'''任务类型
	'''
	return kwargs.get("taskType", 0)

def getEventName(who, *args, **kwargs):
	'''事件名
	'''
	return kwargs.get("eventName", "")

def getCashVal(who, *args, **kwargs):
	'''货币值
	'''
	return kwargs.get("cash", 0)

def getRank(who, *args, **kwargs):
	'''名次
	'''
	return kwargs.get("rank", 0)

expressionHandlerList = {
	"人物等级": getRoleLevel,
	"宠物等级": getPetLevel,
	"所有门派技能等级": getAllSchoolSkillLevel,

	"性别": getGender,

	"拥有任务类型": hasTaskType,
	"拥有称谓": hasTitle,
	"拥有成就": hasAchv,
	
	"物品编号": getPropsNo,
	"助战编号": getBuddyNo,
	"单价": getPrice,
	"珍品": isRare,
	"重铸后珍品": recastIsRare,
	"身上装备特技数": getEquipSkillCount,
	"任务编号": getTaskId,
	"任务类型": getTaskType,
	"事件名": getEventName,
	"货币值": getCashVal,
	"名次": getRank,
}




#===============================================================================
# 达成条件后触发的事件
#===============================================================================
def triggerEvent(who, eventStr, **kwargs):
	handlerName, args = splitHandlerNameAndArgs(eventStr)
	
	tmpArgs = args
	args = []
	for arg in tmpArgs:
		if isinstance(arg, str):
			func = expressionHandlerList.get(arg)
			if func:
				arg = func(who, **kwargs)
		args.append(arg)
		
	func = eventHandlerList.get(handlerName)
	if func:
		func(who, *args, **kwargs)
	else:
		raise Exception("触发事件时，找不到对应的处理函数:%s" % handlerName)


#===============================================================================
# 触发事件对应的处理函数
#===============================================================================

def taskGive(who, taskId, **kwargs):
	'''给予任务
	'''
	if "npcId" in kwargs:
		npcObj = getNpc(kwargs["npcId"])
	else:
		npcObj = None
	task.newTask(who, npcObj, taskId)
	
def titleGive(who, titleId, **kwargs):
	'''给予称谓
	'''
	title.newTitle(who, titleId)
	
def achvDone(who, achvId, **kwargs):
	'''达成成就
	'''
	if who.achvCtn.getItem(achvId):
		return
	achvObj = achv.createAchv(achvId)
	who.achvCtn.addItem(achvObj)
	achvObj.setDone()
	
def achvAddProgress(who, achvId, val, **kwargs):
	'''增加成就进度
	'''
	achvObj = who.achvCtn.getItem(achvId)
	if achvObj:
		if achvObj.isDone():
			return
	else:
		achvObj = achv.createAchv(achvId)
		who.achvCtn.addItem(achvObj)
	achvObj.tryAddProgress(val)
	
def achvDoneCondition(who, achvId, conditionVal, **kwargs):
	'''达成成就条件
	'''
	achvObj = who.achvCtn.getItem(achvId)
	if achvObj:
		if achvObj.isDone():
			return
	else:
		achvObj = achv.createAchv(achvId)
		who.achvCtn.addItem(achvObj)
	achvObj.doneCondition(conditionVal)
	
def achvBreakProgress(who, achvId, **kwargs):
	'''中断成就进度
	'''
	achvObj = who.achvCtn.getItem(achvId)
	if not achvObj:
		return
	if achvObj.isDone():
		return
	achvObj.setBreak(True)
	achvObj.delete("progressTmp")


eventHandlerList = {
	"给予任务": taskGive,
	"给予称谓": titleGive,
	"达成成就": achvDone,
	"增加成就进度": achvAddProgress,
	"达成成就条件": achvDoneCondition,
	"中断成就进度": achvBreakProgress,
}


from common import *
import re
import task
import title
import achv