#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
'''角色相关指令

指令的target是玩家(最后一个参数是一个角色id,你不填就是你当前登录的角色)
'''
#测试指令

import instruction

#本文件中的指令操作对象都是与玩家相关的,所以最后一个参数必须是who


#每一个指令后面的who必然不为None,只是为了符合

fightInfo = {
	1001:(
		{"类型":1,"名称":"强盗","造型":"1111(1,1,1,1,1)","能力编号":"1002","数量":"1","技能":(1311,1321,1323,),"精通技能":1321,"阵法编号":1001,"AI集":"攻击集"},
		{"类型":0,"名称":"邪魔帮手","造型":"3008(0,1,0,0,0)","染色":"0,2,0,0,0","能力编号":"1001","数量":"1","技能":(5401,)},
		{"类型":0,"名称":"杀手","造型":"1111(1,1,1,1,1)","能力编号":"1001","数量":"2","技能":(5102,5103,)},
	),
# 	1002:(
# 		{"类型":1,"名称":"女飞贼","造型":"1111(1,1,1,1,1)","能力编号":"1002","数量":"1","技能":(5401,),"阵法编号":1003},
# 		{"类型":0,"名称":"帮凶","造型":"1111(1,1,1,1,1)","能力编号":"1001","数量":"1","技能":(1112,)},
# 		{"类型":0,"名称":"路过的","造型":"1111(1,1,1,1,1)","能力编号":"1001","数量":"2","技能":(5401,)},
# 		{"类型":0,"名称":"凑热闹的","造型":"1111(1,1,1,1,1)","能力编号":"1001","数量":"2","技能":(5401,)},
# 	),
# 	1003:(
# 		{"类型":1,"名称":"男少侠","造型":"1111(1,1,1,1,1)","能力编号":"1003","数量":"1","技能":(1111,)},
# 		{"类型":0,"名称":"女少侠","造型":"1111(1,1,1,1,1)","能力编号":"1003","数量":"1","技能":(5401,)},
# 	),
}

ableInfo = {
	1001:{"等级":"1","生命":"B*1","真气":"B*1","物理伤害":"B*0.5","法术伤害":"B*0.5","物理防御":"B*0.4","法术防御":"B*0.4","速度":"B*0.4","治疗强度":"B*0.4","封印命中":"B*0.4","抵抗封印":"B*0.4","物理抗性":5,"法术抗性":5,"攻击修炼":5,"物防修炼":5,"法防修炼":5,"物理暴击":10,"物理抗暴":10,"法术暴击":10,"法术抗暴":10},
	1002:{"等级":"10+1","生命":"B*1","真气":"B*1","物理伤害":"B*0.6","法术伤害":"B*0.6","物理防御":"B*0.5","法术防御":"B*0.5","速度":"B*0.6","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
	1003:{"等级":"1+2","生命":"B*1","真气":"B*1","物理伤害":"B*0.6","法术伤害":"B*0.6","物理防御":"B*0.5","法术防御":"B*0.5","速度":"B*0.6","物理抗性":0,"法术抗性":0,"攻击修炼":0,"物防修炼":0,"法防修炼":0},
}

lineupInfo = {
	1001:{"阵法":1,"等级":3,"阵眼":1,"被动技能":(5801,5802,5803,)},
	1002:{"阵法":2,"等级":4,"阵眼":2,"被动技能":(5801,5802,5803,)},
	1003:{"阵法":3,"等级":5},
}

def fight(ep, target=None):
	'''战斗
	'''
	if target.inWar():
		ep.rpcTips("目标已经在战斗了")
		return
	
	fightIdx = shuffleList(fightInfo.keys())[0]
	
# 	target.set("level",50)
# 	target.setSkill(1111, target.level)
# 	target.reCalcAttr()
# 	target.phyDam = 500
# 	target.magDam = 500
# 	target.hp = target.hpMax = 999
# 	target.mp = target.mpMax = 999
	warObj = war.warctrl.createCommonWar(target, fightIdx, fightInfo[fightIdx], ableInfo, lineupInfo)
	ep.rpcTips("战斗开始")
	
def halt(ep, isWin=False, target=None):
	'''结束战斗
	'''
	if not target.inWar():
		ep.rpcTips("目标不在战斗中")
		return
	
	w = target.warrior
	warObj = w.war
	
# 	if hasattr(warObj, "doneEnd"): # 卡机了
# 		try:
# 			for side in warObj.teamList:
# 				for w in warObj.teamList[side].values():
# 					warObj.kickWarrior(w)
# 		except:
# 			warObj._rpcWarEnd(w)
# 			target.leaveWar()
# 		return
	
	if isWin:
		winner = w.side
	else:
		winner = w.side^1
	warObj.winner = winner
	warObj.isEnd = True
	
# 	if not warObj.timerMgr.hasTimer(): # 卡机了
# 		warObj.end()
	warObj.end()
	
	ep.rpcTips("结束战斗")
	
def win(ep, target=None):
	'''战斗胜利
	'''
	halt(ep, True, target)
	
def fail(ep, target=None):
	'''战斗失败
	'''
	halt(ep, False, target)
	
def setskill(ep, skId, lv, target=None):
	'''设置技能
	'''
	skObj = skill.get(skId)
	if not skObj:
		ep.rpcTips("不存在此技能:%s" % skId)
		return
	target.setSkill(skId, lv)
	target.reCalcAttr()
	ep.rpcTips("成功设置%s等级为%d" % (skObj.name, lv))
	
def showskill(ep, target=None):
	'''显示指定或所有技能
	'''
	if target.skillCtn.itemCount() == 0:
		ep.rpcTips("目标身上没有任何技能")
		return
	
	txtList = []
	for skObj in target.skillCtn.getAllValues():
		txtList.append("%d/%s 等级:%d" % (skObj.id, skObj.name,skObj.level))
	ep.rpcModalDialog("\n".join(txtList))

def clearskill(ep, target=None):
	'''清除身上所有技能
	'''
	target.skillCtn.clearAll()
	target.reCalcAttr()
	ep.rpcTips("OK")

@instruction.properties(sn='npc')
def newNpc(ep,npcIdx,sceneId=0,x=0,y=0,target=None):#新造一个npc
	'新造一个npc，参数：npc编号，场景编号，[x]，[y]；短指令：npc'
	if not sceneId:
		sceneId=target.sceneId
		x=target.x
		y=target.y
	oScene=scene.getScene(sceneId)
	if not oScene:
		ep.rpcTips('编号为{}的场景不存在'.format(sceneId))
		return
	if not x:
		x=333
	if not y:
		y=333

	import npc.object
	if npcIdx == 20:
		npcObj = npc.object.NpcBase()
		npcObj.idx = npcIdx
	elif npcIdx < 100: # 测试npc
		npcObj = npc.newByType(npcIdx)
		npcObj.idx = npcIdx
	else: # 固定npc
		npcObj = npc.newByIdx(npcIdx)
	scene.switchSceneForNpc(npcObj, sceneId, x, y, 0)
	if npcObj.name:
		ep.rpcTips('克隆了一个{}'.format(npcObj.name))
	else:
		ep.rpcTips('克隆了一个npc')

import taskData


import ujson

def newTask(ep,iNo,target=None):
	'添加任务到角色，参数：任务编号，[角色id]'
	oTask=task.new(iNo,target)
	target.taskCtn.addItem(oTask)
	ep.rpcTips('玩家{}激活任务{}!'.format(target.name,oTask.name))

def delTask(ep,iNo,target=None):
	oTask=task.new(iNo,target)
	target.taskCtn.removeItem(oTask)
	ep.rpcTips('dasfas')

def addtradecash(ep,iAmount,target=None):
	'增加角色游戏币，参数：游戏币数，[角色id]'
	target.addTradeCash(iAmount,'instruction')
	ep.rpcTips("OK")


def addcash(ep,iVal,target=None):
	'''增加现金
	'''
	target.addCash(iVal,"instruction")
	ep.rpcTips("OK")

def addhuoli(ep,iVal,target=None):
	'''增加活力
	'''
	target.addHuoli(iVal, "instruction")
	ep.rpcTips("OK")

def addactpoint(ep, iVal, target=None):
	'''增加活跃点
	'''
	target.addActPoint(iVal)
	ep.rpcTips("OK")

def addschoolpoint(ep,iVal,target=None):
	'''增加门贡
	'''
	target.addSchoolPoint(iVal, "instruction")
	ep.rpcTips("OK")
	
def addguildpoint(ep,iVal,target=None):
	'''增加帮贡
	'''
	target.addGuildPoint(iVal, "instruction")
	ep.rpcTips("OK")

def addholidaypoint(ep,iVal,target=None):
	'''增加节日积分
	'''
	target.addHolidayPoint(iVal, "instruction")
	ep.rpcTips("OK")

def addmasterpoint(ep,iVal,target=None):
	'''增加良师值
	'''
	target.addMasterPoint(iVal, "instruction")
	ep.rpcTips("OK")

def addpkpoint(ep,iVal,target=None):
	'''增加武勋值
	'''
	target.addPKPoint(iVal, "instruction")
	ep.rpcTips("OK")

def addhelppoint(ep,iVal,target=None):
	'''增加侠义值
	'''
	target.addHelpPoint(iVal, "instruction")
	ep.rpcTips("OK")

def addflowerpoint(ep,iVal,target=None):
	'''增加献花积分
	'''
	target.addFlowerPoint(iVal, "instruction")
	ep.rpcTips("OK")

def adddemonpoint(ep, iVal, target=None):
	'''增加除魔积分
	'''
	target.addDemonPoint(iVal, "instruction")
	ep.rpcTips("OK")

def addanima(ep, iVal, target=None):
	'''增加灵气
	'''
	target.alchemyCtn.addAnima(iVal)
	ep.rpcTips("OK")
	ep.rpcAnimaMod(target.alchemyCtn.getAnima())

def adddiamond(ep,iAmount,target=None):
	'增加角色所在账号钻石，参数：钻石数量，[角色id]'
	if target.diamond+iAmount>2**31-1:
		ep.rpcTips('数值过大，请重新输入')
		return
	target.addDiamond(iAmount,'instruction')
	ep.rpcTips("OK")

def addmoneycash(ep,iAmount,target=None):
	'''增加或减少龙纹玉
	'''
	target.addMoneyCash(iAmount,'instruction')

def addexp(ep,iAdd,target=None):
	'''增加经验
	'''
	target.addExp(iAdd,'instruction')
	ep.rpcTips("OK")
	
def uplevel(ep,iCnt=1,target=None):
	'''升级
	'''
	iCnt = max(iCnt - target.level,0)
	if not iCnt:
		return
	for i in xrange(iCnt):
		target.exp += target.expNext
		target.upLevel()
	import openLevel
	openLevel.checkExpRatio(target)
	ep.rpcTips("%s的等级升级为%d" % (target.name, target.level))

def addhp(ep,iAdd,target=None):
	'增加角色HP，参数：HP，[角色id]'
	target.addHP(iAdd)
	ep.rpcTips("OK")
	
def addmp(ep,iAdd,target=None):
	'增加角色MP，参数：MP，[角色id]'
	target.addMP(iAdd)
	ep.rpcTips("OK")
	
def addsp(ep,iAdd,target=None):
	'增加角色愤怒，参数：愤怒值，[角色id]'
	target.addSP(iAdd)
	ep.rpcTips("OK")

@instruction.properties(sn='np')
def newProps(ep,iNo,iAmount=1,target=None):
	'添加物品，参数：物品编号，[数量]，[角色id]；短指令：np'
	oProp=props.new(iNo)
	iMaxStack=oProp.maxStack()
	# iCounter=int(math.ceil(iAmount/float(iMaxStack)))
	# for i in xrange(iCounter):
	launch.launchBySpecify(target,iNo,iAmount,False,sLogReason='指令',sTips=None)
	ep.rpcTips("OK")
	# ep.rpcTips('玩家{}获得克隆物品{}({})!'.format(target.id,oProp.name,oProp.id))

def setequiplife(ep,equipId,iValue,target=None): 
	'''设置耐久度
	'''
	oEquip = target.equipCtn.getItem(equipId)
	if not oEquip:
		oEquip = target.propsCtn.getItem(equipId)
		if not oEquip:
			return
	oEquip.set("life",iValue)
	if oEquip.isWear():
		target.endPoint.rpcModEquip(oEquip.getMsg4Item(target.equipCtn,"life","addon"))
	else:
		target.endPoint.rpcModProps(oEquip.getMsg4Package(target.propsCtn,'life','addon'))
	message.tips(target,"设置{}耐久为->{}".format(oEquip.name,iValue))

def setequipskill(ep,equipId,iValue,target=None):
	'''设置特技特效
	'''
	oEquip = target.propsCtn.getItem(equipId)
	if not oEquip:
		oEquip = target.equipCtn.getItem(equipId)
		if not oEquip:
			return
		oEquip.cancelSetup(target)
	if iValue < 4000: #特效	
		oEquip.set("spEffect",iValue)
	else:
		oEquip.set("spSkill",iValue)
	if oEquip.isWear():
		target.endPoint.rpcModEquip(oEquip.getMsg4Item(target.equipCtn,"spSkill","spEffect"))
		oEquip.setup(target)
		target.reCalcAttr()
	else:
		target.endPoint.rpcModProps(oEquip.getMsg4Package(target.propsCtn,"spSkill","spEffect"))
	message.tips(target,"设置{}特技/特效为->{}".format(oEquip.name,iValue))

@instruction.properties(sn='sp')
def showProps(ep,target=None):
	'''查看物品
	'''
	txtList = []
	txtList.append("穿着装备")
	for obj in target.equipCtn.getAllValues():
		txtList.append("id:%s 装备:%s " % (obj.id, obj.name))
	txtList.append("背包装备")
	for obj in target.propsCtn.getAllValues():
		sKind = "装备" if obj.kind == props.defines.ITEM_EQUIP else "物品"
		txtList.append("id:%s %s:%s " % (obj.id, sKind, obj.name))
	message.dialog(target, "\n".join(txtList))

@instruction.properties(sn='cp')
def clearPackage(ep,target=None):#清空包裹
	for oProps in list(target.propsCtn.getAllValues()):
		target.propsCtn.removeItem(oProps)
	ep.rpcTips('操作成功')

def full(ep,target=None):#满血,满蓝,满..
	'HP、MP等状态补满，参数：[角色id]'
	target.addHP(target.hpMax)
	target.addMP(target.mpMax)
	target.addSP(target.spMax)
	
	petObj = target.petCtn.getFighter()
	if petObj:
		petObj.addHP(petObj.hpMax)
		petObj.addMP(petObj.mpMax)
	
	if target.inWar():
		warObj = target.war
		w = target.warrior
		w.addHP(w.getHPMax())
		w.addMP(w.getMPMax())
		w.addSP(w.spMax)
		w.addFuWen(w.fuwenMax)
		
		sw = warObj.getWarrior(w.petIdx)
		if sw:
			sw.addHP(sw.getHPMax())
			sw.addMP(sw.getMPMax())
		
	ep.rpcTips("OK")

@instruction.properties(sn='go')
def goto(ep,sceneId,x=0,y=0,target=None):
	'设置角色坐标，参数：[场景编号]，[x]，[y]，[角色id]；短指令：go'
	if sceneId == 0:
		sceneId = target.sceneId
	scene.tryTransfer(target.id, sceneId, x, y)
	
@instruction.properties(sn='gotorole')
def gotoRole(ep, roleId, target=None):
	obj = getRole(roleId)
	if not obj:
		ep.rpcTips("目标不在线")
		return
	scene.tryTransfer(target.id, obj.sceneId, obj.x, obj.y)

@instruction.properties(sn='get')
def getvalue(ep,sAttr,target=None):
	'''获取角色属性
	'''
	func=getattr(target,"get%s" % toTitle(sAttr), None)
	if func:
		val=func()
	elif hasattr(target,sAttr):
		val=getattr(target,sAttr)
		if callable(val):
			val=val()
	else:
		func = getattr(target, "is%s" % toTitle(sAttr), None)
		if func:
			val = func()
		else:
			val = target.fetch(sAttr,None)

	if ep:
		ep.rpcTips('角色{}的{}={}'.format(target.id,sAttr,val))
	return val

@instruction.properties(sn='set')
def setvalue(ep,sAttr,uValue,target=None):
	'设置角色属性，参数：属性名，属性值，[角色id]'
	if sAttr=='iTempAuthLv':
		ep.rpcTips('不允许改此属性')
		return
	func = getattr(target, "set%s" % toTitle(sAttr), None)
	if func:
		uOriVal = getvalue(None, sAttr, target)
		func(uValue)
	elif sAttr in ("name", "school"):
		uOriVal = getattr(target, sAttr)
		setattr(target, sAttr, uValue)
	elif sAttr in ("shape", "level"):
		uOriVal = target.fetch(sAttr)
		target.set(sAttr, uValue)
	elif hasattr(target,sAttr):
		uOriVal=getattr(target,sAttr)
		if callable(uOriVal):
			ep.rpcTips('变量名{}错误,与函数同名了'.format(sAttr))
			return
		setattr(target,sAttr,uValue)
	else:
		uOriVal=target.fetch(sAttr,None)
		target.set(sAttr,uValue)
	ep.rpcTips('{}值{}->{}'.format(sAttr,uOriVal,uValue))
	
	if sAttr in ('level',):#有联动效果的属性(比如升了角色等级,对应的战斗属性也要相应提高.)
		target.reCalcAttr(False)

	#设置完属性后,还得刷新到客户端去.
	try:
		target.attrChange(sAttr)
	except:
		pass

@instruction.properties(sn='rp')
def rolePos(ep,target=None):
	'查看角色位置，参数：[角色id]；短指令：rp'
	ep.rpcTips('{},{},{}'.format(target.sceneNo,target.x,target.y))


type2Cycle = {
  "m": "month",
  "w": "week",
  "d": "day",
  "h": "hour",
}

#只用于内服作测试用,生产环境太危险了
@instruction.properties(sn='clearcyc')
def clearCycle(ep,sType=None,target=None):
	'清除角色周期数据，参数：[周期类型],[角色id]；短指令：clearcyc'
	if sType:
		obj = getattr(target, type2Cycle[sType])
		obj.clear()
		ep.rpcTips("清除成功")
		return
	content = '''你要清除你身上的什么周期数据?
Q小时数据
Q天数据
Q周数据
Q月数据
Q我什么都不想,逗你玩而已'''
	message.selectBoxByArgsNew(target, responseClearCycle, content)
		
def responseClearCycle(who, selectNo):
	if selectNo==1:
		who.hour.clear()
	elif selectNo==2:
		who.day.clear()
	elif selectNo==3:
		who.week.clear()
	elif selectNo==4:
		who.month.clear()
	else:
		return
	who.endPoint.rpcTips('清除成功')

@instruction.properties(sn='delcyc')
def delCycle(ep,sType,sKey,target=None):
	'清除角色某周期当前数据，参数：周期类型(m、w、d、h)，属性名，[角色id]'
	obj = getattr(target, type2Cycle[sType])
	obj.delete(sKey)
	ep.rpcTips("删除周期数据{}成功".format(sKey))

@instruction.properties(sn='showcyc')
def showCycle(ep,sType,target=None):
	'''查看某周期数据，只支持显示当天的，历史数据不予显示
	'''
	obj = getattr(target, type2Cycle[sType])
	# msg =  obj.save()
	msg = obj.dData.get(obj.getCycleNo(), {})
	message.dialog(target, str(msg))
	
def cleardayall(ep,target=None):
	'''清空玩家身上所有天变量数据
	'''
	target.day.clear()
	for petObj in target.petCtn.getAllValues():
		petObj.day.clear()
	ep.rpcTips('清除成功')

def clearweekall(ep,target=None):
	'''清空玩家身上所有周变量数据
	'''
	target.week.clear()
	ep.rpcTips('清除成功')

@instruction.properties(sn="setcyc")
def setCycle(ep, sType, sKey, uValue, target=None):
	'''设置角色某周期当前数据，参数：周期类型(m\w\d\h)，属性名, 属性值
	'''
	obj = getattr(target, type2Cycle[sType])
	obj.set(sKey, uValue)
	ep.rpcTips("设置成功")

def addFriend(ep,iRoleId,target=None):
	'添加好友，参数：被添加角色id，[添加角色id]'
	if target.friendCtn.getItem(iRoleId):
		ep.rpcTips('已经有id为{}的好友了'.format(iRoleId))
		return
	obj=friend.new(iRoleId,target)
	target.friendCtn.addItem(obj)
	ep.rpcTips('加了{}为好友'.format(iRoleId))

@instruction.properties(sn='super')	
def superman(ep, target=None):
	'''变成超人
	'''
	target.hp = target.hpMax = 99999
	target.mp = target.mpMax = 99999
	target.phyDam = 99999
	target.magDam = 99999
	target.phyDef = 99999
	target.magDef = 99999
	target.spe = 99999
	ep.rpcTips("OK，你暂时变成超人了")

def addtask(ep, taskId, target=None):
	if task.hasTask(target, taskId):
		ep.rpcTips("已有%s任务" % taskId)
		return
	
	taskObj = task.create(taskId)
	if isinstance(taskObj, task.object.TeamTask) and not target.inTeam():
		ep.rpcTips("你没有队伍，无法增加组队任务")
		return
	
	task.newTask(target, None, taskId)
	ep.rpcTips("成功添加%s任务" % taskId)
	
def cleartask(ep, taskId=0, target=None):
	if taskId:
		taskObj = task.hasTask(target, taskId)
		if taskObj:
			task.removeTask(target, taskObj.id)
			ep.rpcTips("成功清除任务%d" % taskId)
		else:
			ep.rpcTips("你身上没有此类任务")
		return
	
	taskList = []
	for taskId in target.taskCtn.getAllKeys():
		taskList.append(taskId)
		
	teamObj = target.inTeam()
	if teamObj:
		for taskId in teamObj.taskCtn.getAllKeys():
			taskList.append(taskId)
		
	for taskId in taskList:
		task.removeTask(target, taskId)
	ep.rpcTips("成功清除全部任务")

def clearpt(ep, target=None):
	'''清空宠物任务数据
	'''
	target.taskCtn.delete("petCom")
	ep.rpcTips("成功清除清空宠物任务数据")
	
# def showlineup(ep, target=None):
# 	'''显示所有阵法
# 	'''
# 	txtList = []
# 	for lineupObj in target.lineupCtn.getAllValues():
# 		txtList.append("%s: 编号%d 等级%d 经验%d " % (lineupObj.name, lineupObj.id, lineupObj.level, lineupObj.getExp()));
# 	
# 	if txtList:
# 		ep.rpcModalDialog("\n".join(txtList))
# 	else:
# 		ep.rpcTips("没有任何阵法")
# 		
# def setlineup(ep, lineupId, level, target=None):
# 	'''设置阵法等级
# 	'''
# 	target.lineupCtn.setLevel(lineupId, level)
# 	ep.rpcTips("OK")
# 		
# def addlineupexp(ep, lineupId, val, target=None):
# 	'''增加阵法经验
# 	'''
# 	lineupObj = target.lineupCtn.getItem(lineupId)
# 	if not lineupObj:
# 		lineupObj = target.lineupCtn.setLevel(lineupId, 1)
# 	target.lineupCtn.addExp(lineupId, val)
# 	ep.rpcTips("OK")

@instruction.properties(sn='addlineup')
def addLineup(ep, lineupId, level, target=None):
	'''增加阵法
	'''
	if level > 0:
		lineupObj = target.lineupCtn.getItem(lineupId)
		if lineupObj:
			lineupObj = target.lineupCtn.setLevel(lineupId, level)
		else:
			lineupObj = target.lineupCtn.setLevel(lineupId, level)
			eyeNo = lineupId
			eyeObj = lineup.addEye(target, eyeNo)
			lineupObj.setEyeObj(eyeObj)
		
		target.buddyCtn.setLineup(target.buddyCtn.currentIdx, lineupObj.id)
		ep.rpcTips("增加阵法成功")
	else:
		target.lineupCtn.setLevel(lineupId, level)
		target.buddyCtn.setLineup(target.buddyCtn.currentIdx, 0)
		ep.rpcTips("删除阵法成功")
	
def addbuff(ep, bfId, bout=5, target=None):
	if not target.inWar():
		ep.rpcTips("你不在战斗中")
		return
	buff.addOrReplace(target.warrior, bfId, bout, target.warrior)
	
def removebuff(ep, bfId, target=None):
	if not target.inWar():
		ep.rpcTips("你不在战斗中")
		return
	buff.remove(target.warrior, bfId)
	
def removebuffall(ep, target=None):
	if not target.inWar():
		ep.rpcTips("你不在战斗中")
		return
	w = target.warrior
	for lst in w.buffList.valus():
		for bfObj in lst:
			buff.remove(w, bfObj.id)
			
def follow(ep, targetId=0, target=None):
	'''跟踪玩家或取消跟踪
	'''
	who = target
	
	if targetId == 0: # 取消跟踪
		who.stopTimer("follow")
		ep.rpcTips("成功取消跟踪")
		return
	
	targetObj = getRole(targetId)
	if not targetObj:
		ep.rpcTips("对方不在线")
		return
	
	_follow(targetId, who.id)

def setalchemytime(ep, propsNo, time, target=None):
	'''设置炼丹时间
	'''
	time = getSecond()-(60*60*4-time)
	alchemy = target.alchemyCtn.getAlchemy(propsNo)
	if alchemy:
		alchemy.set("time",time)
	else:
		alchemy = target.alchemyCtn.addAlchemy(propsNo)
		alchemy.set("cnt",2)
		alchemy.set("time",time)
	ep.rpcTips("设置炼丹时间成功")
	import alchemy.service
	alchemy.service.sendAlchemy(target)

def _follow(targetId, pid):
	who = getRole(pid)
	targetObj = getRole(targetId)
	if not who:
		return
	if not targetObj:
		message.tips(who, "对方已下线")
		return
	
	if not scene.isNearBy(who, targetObj, 20):
		if not scene.tryTransfer(who, targetObj.sceneId, targetObj.x, targetObj.y):
			return
		message.tips(who, "正在跟踪玩家%s[%d]" % (targetObj.name, targetId))
	who.startTimer(functor(_follow, targetId, who.id), 3, "follow")
	
def addTitle(ep, titleId, target=None):
	'''增加称谓
	'''
	title.newTitle(target, titleId)
	
def removeTitle(ep, titleId, target=None):
	'''移除称谓
	'''
	title.removeTitle(target, titleId)

@instruction.properties(sn='removenpc')
def removeNpc(ep, npcIdx=0, target=None):
	if npcIdx:
		npcObj = npc.getNpcByIdx(npcIdx)
	else:
		npcId = getattr(target, "lastNpcId", None)
		if not npcId:
			return
		npcObj = npc.getNpc(npcId)

	if not npcObj:
		return

	sceneObj = scene.getScene(npcObj.sceneId)
	if sceneObj:
		sceneObj.removeEntity(npcObj)


def goodsinfo(ep, goodsType, goodsNo, target=None):
	tradeCenterObj = trade.getTradeCenter(goodsType)
	if not tradeCenterObj:
		return

	goodsObj = tradeCenterObj.getItem(goodsNo)
	if not goodsObj:
		message.tips(target,"商品编号错误")
		return

	txtList = []
	txtList.append("实际基础价格:%0.2f" % goodsObj.getPrice())
	txtList.append("波动价格和:%0.2f" % goodsObj.getWavePrice())
	txtList.append("变更数量:%d" % goodsObj.getWaveCount())
	txtList.append("刷新实际基础价格:%0.2f" % goodsObj.getFlushPrice())
	txtList.append("涨幅:%0.4f" % goodsObj.getRose())

	message.dialog(target, "\n".join(txtList))

def setgoods(ep, goodsType, goodsNo, setType, value, target=None):
	tradeCenterObj = trade.getTradeCenter(goodsType)
	if not tradeCenterObj:
		message.tips(target,"商店类型错误")
		return

	goodsObj = tradeCenterObj.getItem(goodsNo)
	if not goodsObj:
		message.tips(target,"商品编号错误")
		return

	if setType == 1:
		goodsObj.setPrice(value)
	elif setType == 2:
		goodsObj.setWavePrice(value)
	elif setType == 3:
		goodsObj.setWaveCount(value)
	elif setType == 4:
		goodsObj.setFlushPrice(value)

	message.tips(target, "设置成功")

def updategoods(ep, target=None):
	trade.gCashTradeCenter.update()
	trade.gTradeCashTradeCenter.update()
	message.tips(target, "刷新成功")

def resetgoods(ep, goodsType, goodsNo, target=None):
	'''重置商品
	'''
	tradeCenterObj = trade.getTradeCenter(goodsType)
	if not tradeCenterObj:
		message.tips(target,"商店类型错误")
		return

	goodsObj = tradeCenterObj.getItem(goodsNo)
	if not goodsObj:
		message.tips(target,"商品编号错误")
		return

	goodsObj.reset()
	message.tips(target, "重置成功")


def setstallitemtime(ep, itemNo, time, target=None):
	'''设置摊位剩余时间
	'''
	itemObj = trade.gStall.goodsListByRoleId[target.id]
	stallId = itemObj.goodsList[itemNo]
	dGoods=trade.gStall.removeGoods(stallId,False)

	start = getSecond()+time-trade.stall.DURATION
	trade.gStall.addGoods(target.id,dGoods["obj"],dGoods["price"],start,itemNo)
	message.tips(target, "设置成功")

def showstalltime(ep, itemNo, target=None):
	'''查看摆摊剩余时间
	'''
	itemObj = trade.gStall.goodsListByRoleId[target.id]
	stallId = itemObj.goodsList[itemNo]
	dGoods=trade.gStall.goodsList[stallId]
	if dGoods["status"] == 2:
		tips = "已经过期"
	else:
		second = dGoods["start"]+trade.stall.DURATION-getSecond()
		sTime = "%d秒" % second
		if second >= 60:
			minute = second/60
			sTime = "%d分" % minute
			if minute >= 60:
				hour,mte = minute/60,minute%60
				sTime = "%d小时%d分" % (hour,mte)
		tips = "剩余摆摊时间%s" % sTime

	txtList = []
	txtList.append(tips)
	message.dialog(target, "\n".join(txtList))

def setstalltime(ep, propsId, day, target=None):
	'''设置摆摊交易时间
	'''
	propsObj = target.propsCtn.getItem(propsId)
	if not propsObj:
		message.tips(target,"物品Id输错了")
		return
	dayNo = getDayNo() + day - 7
	propsObj.set("stall",dayNo)
	target.endPoint.rpcDelProps(propsId)
	target.endPoint.rpcAddProps(propsObj.getMsg4Package(target.propsCtn,*propsObj.MSG_ALL))
	message.tips(target, "设置成功")

def addguildfund(ep, fund, target=None):
	'''增加帮派资金
	'''
	oGuild = target.getGuildObj()
	if not oGuild:
		message.tips(target, "你还没有帮派")
		return
	oGuild.addFund(fund)

def addeye(ep, eyeNo, target=None):
	lineup.addEye(target, eyeNo)

def addtestgoods(ep, goodsNo=0,target=None):
	'''增加测试商品
	'''
	if goodsNo:
		goodsObj = trade.gTradeCashTradeCenter.getItem(goodsNo)
		lst = [goodsObj]
	else:
		lst = trade.gTradeCashTradeCenter.dKeyMapItem.values()
	for goodsObj in lst:
		goodsNo = goodsObj.getPropsNo()
		args = goodsObj.getPropsArgs()
		price = int(goodsObj.getSellPrice())
		for i in xrange(10):
			obj = props.new(goodsNo,**args)
			trade.gStall.addGoods(1010101011,obj,price)
	message.tips(target,"增加测试商品成功")

def removetestgoods(ep, goodsNo=0,target=None):
	'''移除测试商品
	'''

	for goodsId,dGoods in trade.gStall.goodsList.items():
		if dGoods["ownerId"] == 1010101011:
			if goodsNo and goodsNo != trade.getGoodsNo(dGoods["obj"]):
				continue
			trade.gStall.removeGoods(goodsId,False)
	message.tips(target,"移除测试商品成功")

def addtstestgoods(ep, goodsNo=0,target=None):
	'''增加珍品阁商品
	'''
	lst = []
	if goodsNo:
		if not 200020 <= goodsNo <= 200029:
			goodsObj = props.new(goodsNo)
		else:
			goodsObj = lineup.createEye(goodsNo)
		lst = [goodsObj]
	else:
		import treasureShopData
		for goodsNo in treasureShopData.gdTreasureShopData:
			if not 200020 <= goodsNo <= 200029:
				goodsObj = props.new(goodsNo)
			else:
				pass
				goodsObj = lineup.createEyeByNo(goodsNo%200020 + 1)
			lst.append(goodsObj)
	for goodsObj in lst:
		import treasureShop
		import treasureShop.service
		for i in xrange(10):
			import block.sysActive
			if not 200020 <= goodsObj.no() <= 200029:
				goodsObj.onBorn()
			else:
				goodsObj = lineup.createEyeByNo(goodsObj.getNo())
			goodsObjFork = treasureShop.service.getGoodsFork(goodsObj)
			treasureShop.gTreasureShop.addGoods(1010101011,goodsObjFork,1000,[],iStatus=1)
	message.tips(target,"增加珍品阁商品成功")

def removetstestgoods(ep, goodsNo=0,target=None):
	'''移除珍品阁商品
	'''
	for goodsId,dGoods in treasureShop.gTreasureShop.goodsList.items():
		if dGoods["ownerId"] == 1010101011:
			if goodsNo and goodsNo != treasureShop.getGoodsNo(dGoods["obj"]):
				continue
			treasureShop.gTreasureShop.removeGoods(goodsId)

	message.tips(target,"移除珍品阁商品成功")

def clearflfail(ep, target=None):
	'''清空试炼幻境失败次数
	'''
	target.day.delete("flFail")
	message.tips(target,"清空试炼幻境失败次数成功")
	
def achvShow(ep, targetId=0, target=None):
	'''显示成就列表
	'''
	if targetId:
		targetObj = getRole(targetId)
		if not targetObj:
			ep.rpcTips("找不到玩家:%s" % targetId)
			return
	else:
		targetObj = target
	
	txtList = []
	for achvObj in targetObj.achvCtn.getAllValues():
		if achvObj.isDone():
			state = "已达成"
		else:
			state = "未达成"
		txtList.append("%s %s %s" % (achvObj.id, achvObj.name, state))
		
	if not txtList:
		ep.rpcTips("目标身上没有任何成就")
		return
	ep.rpcModalDialog("\n".join(txtList))
	
def achvDone(ep, achvId, targetId=0, target=None):
	'''达成成就
	'''
	if targetId:
		targetObj = getRole(targetId)
		if not targetObj:
			ep.rpcTips("找不到玩家:%s" % targetId)
			return
	else:
		targetObj = target

	if targetObj.achvCtn.getItem(achvId):
		ep.rpcTips("已有该成就")
		return
	achvObj = achv.createAchv(achvId)
	targetObj.achvCtn.addItem(achvObj)
	achvObj.setDone()
	ep.rpcTips("达成成就:%s" % achvId)
	
def achvAddProgress(ep, achvId, val, targetId=0, target=None):
	'''增加成就进度
	'''
	if targetId:
		targetObj = getRole(targetId)
		if not targetObj:
			ep.rpcTips("找不到玩家:%s" % targetId)
			return
	else:
		targetObj = target

	achvObj = targetObj.achvCtn.getItem(achvId)
	if not achvObj:
		achvObj = achv.createAchv(achvId)
		targetObj.achvCtn.addItem(achvObj)
	achvObj.tryAddProgress(val)
	ep.rpcTips("增加%s成就进度:%s" % (achvId, val))
	
def achvDoneCondition(ep, achvId, conditionVal, targetId=0, target=None):
	'''达成成就条件
	'''
	if targetId:
		targetObj = getRole(targetId)
		if not targetObj:
			ep.rpcTips("找不到玩家:%s" % targetId)
			return
	else:
		targetObj = target

	achvObj = targetObj.achvCtn.getItem(achvId)
	if not achvObj:
		achvObj = achv.createAchv(achvId)
		targetObj.achvCtn.addItem(achvObj)
	achvObj.doneCondition(conditionVal)
	ep.rpcTips("达成%s成就条件:%s" % (achvId, conditionVal))
	
def achvBreakProgress(ep, achvId, targetId=0, target=None):
	'''中断成就进度
	'''
	if targetId:
		targetObj = getRole(targetId)
		if not targetObj:
			ep.rpcTips("找不到玩家:%s" % targetId)
			return
	else:
		targetObj = target

	achvObj = targetObj.achvCtn.getItem(achvId)
	if not achvObj:
		ep.rpcTips("没有该成就")
		return
	achvObj.setBreak(True)
	achvObj.delete("progressTmp")
	ep.rpcTips("中断%s成就进度成功" % achvId)
		

def showtsid(ep,target=None):
	'''查看珍品阁商品id
	'''
	d = {
		1:"上架中",
		2:"公示期",
		3:"已过期",
		4:"审核",
		5:"提现",
	}
	txtList = []
	data = treasureShop.gTreasureShop.getRoleItem(target.id)
	if not data:
		txtList.append("没卖东西，在耍我吧")
	else:
		for iStallId in data.itervalues():
			dGoods = treasureShop.gTreasureShop.getGoods(iStallId)
			obj = dGoods["obj"]
			sMsg = "摊位id:{},价格:{},名字:{},状态:{}".format(iStallId,dGoods["price"],obj.name,d[dGoods["status"]])
			txtList.append(sMsg)

	message.dialog(target, "\n".join(txtList))

def settstime(ep,iStallId,iTime,target=None):
	'''修改珍品阁珍品时间
	'''
	dGoods = treasureShop.gTreasureShop.getGoods(iStallId)
	if not dGoods:
		return
	iRoleId = dGoods["ownerId"]
	obj = dGoods["obj"]
	iPrice = dGoods["price"]
	lAttention = dGoods["attention"]
	iTeamId = dGoods["itemId"]
	iStatus = dGoods["status"]
	if iStatus == 1:
		iDuration =  7*24*60*60
	elif iStatus == 2:
		iDuration =  4*60*60
	elif iStatus == 4:
		iDuration =  1*24*60*60
		treasureShop.gTreasureShop.removeGoodsFromTimeList(iStallId)
	else:
		message.tips(target,"别搞我啊,提现/过期的还设置什么时间")
		return
	iStart = (getSecond() + iTime) - iDuration
	treasureShop.gTreasureShop.removeGoods(iStallId)
	iStallId = treasureShop.gTreasureShop.addGoods(iRoleId,obj,iPrice,lAttention,iStart,iTeamId,iStatus)
	message.tips(target,"修改珍品阁时间成功，商品摆摊id改为%d"%iStallId)

def addbuddy(ep, iBuddyNo, target=None):
	import buddy
	buddyObj = target.buddyCtn.getItem(iBuddyNo)
	if buddyObj:
		message.tips(target,"已经拥有此伙伴")
		return
	buddy.add(target,iBuddyNo)

def clearstar(ep, target=None):
	'''清除杀星奖励次数成功
	'''
	target.day.delete("starKill")
	target.day.delete("starKindKill")
	message.tips(target,"清除杀星奖励次数成功")

def killallstar(ep, target=None):
	'''杀死所有星
	'''
	import activity
	actObj = activity.getActivity("star")
	actObj.removeAllNpc()
	message.tips(target,"杀死所有星成功")

def sendSysMsg(ep, content, target=None):
	import friend
	friend.sendSysMsg(target.id,str(content))

def setfribuddytime(ep, iFriendId, iTime,target=None):
	oFriBuddy = target.buddyCtn.getFriendBuddy(iFriendId)
	if not oFriBuddy:
		message.tips(target,"你没有租借该好友的伙伴")
		return
	oFriBuddy.oTimerMng.cancel(oFriBuddy.uTimerId)
	oFriBuddy.set("endTime",getSecond()+iTime)
	oFriBuddy.startTimer()
	message.tips(target,"设置成功")
		
def delbuddy(ep, iBuddyNo, target=None):
	oBuddy = target.buddyCtn.getItem(iBuddyNo)
	if not oBuddy:
		message.tips(target,"你并没有该伙伴")
		return

	for iBattleNo,lBuddy in target.buddyCtn.buddyList.iteritems():
			if iBuddyNo not in lBuddy:
				continue
			index = lBuddy.index(iBuddyNo)
			target.buddyCtn.downBattle(iBattleNo,index)
			target.buddyCtn.rpcDownBattle(iBattleNo,index)

	target.buddyCtn.removeItem(oBuddy)
	message.tips(target,"清除伙伴成功")

from common import *
import math
import gevent
import instruction
import role.roleHelper
import types
import scene
import c
import misc
import u
import log
import role
import friend
import resume
import props
import task
import mainService
import buff
import factory
import pet
import war.warctrl
import message
import skill
import npc
import team
import launch
import props.equip
import props.defines
import title
import trade
import trade.stall
import lineup
import achv
import block.sysActive
import treasureShop