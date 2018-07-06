#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

def beforeLogin(who, bReLogin):
	#在checkDayNo之前调用，拿到上次登录的天编号
	tougheningExp.beforeLogin(who, bReLogin)
	who.checkDayNo()
	if who.fetch("newbie"):
		onNewbie(who)
	if not bReLogin: # 执行离线处理
		offlineHandler.executeHandler(who)
	resume.addLinkMan(who)

def onLogin(who,bReLogin):
	if bReLogin:
		teamObj = who.getTeamObj()
		if teamObj:
			teamObj.reEnter(who)
	else:
		pass # 策划要求下线不再回队伍
# 		teamId = who.fetch("teamId")
# 		if teamId:
# 			who.delete("teamId")
# 			teamObj = team.getTeam(teamId)
# 			if teamObj:
# 				teamObj.setOnline(who)

	who.delete("offlineTime")
	role.addToLevelList(who)
	activity.onLogin(who, bReLogin)
	task.onLogin(who, bReLogin)
	state.onLogin(who, bReLogin)
	openLevel.checkExpRatio(who,True)
	role.roleConfig.checkForceUnlockTime(who)
	role.service.rpcSecurityLockMsg(who)
	signIn.onLogin(who, bReLogin)
	collect.onLogin(who, bReLogin)
	guild.updateMemberInfo(who)
	guide.onLogin(who, bReLogin)
	treasureShop.onLogin(who)
	trade.onLogin(who)
	resume.onLogin(who)
	friend.onLogin(who,bReLogin)
	if who.inWar():
		who.war.reEnter(who.warrior)
		
	# if task.offlineTask.inOfflineTask(who):
	# 	task.offlineTask.quitOfflineTask(who, False)
			

def onNewbie(who):
	'''新人
	'''
	who.delete("newbie")
	who.newbie = True

	skill.upgrade.checkSchSkillOpen(who) # 默认开启职业基础技能
	#task.newTask(who,None,40120)  #自动领取主线任务
	#task.newTask(who,None,40200)  #自动领取主线任务
	# 测试送宠物

	#注释这段表示不带任何异兽
	'''
	fightPet = None
	for petId in [1001, 1009]:
		petObj = pet.new(petId, 0)
		pet.addPet(who, petObj)
		who.petCtn.setCarry(petObj, True) # 先携带，然后才能参战
		if petId == 1009:
			fightPet = petObj
	if fightPet:
		who.petCtn.setFighter(fightPet, True)
	'''
	#注释这段表示不带任何装备
	#props.equip.sendEquipForNewbie(who)
	#activity.center.sendDoublePointForNewBie(who)
	#注释这段表示不带任何助战
	#buddy.sendBuddyForNewbie(who)

	# for newbie test beging
	props.sendPropsForNewbie(who)
	#注释这段表示原增加的龙纹玉为0
	#who.addMoneyCash(1000, "newbie test", None)
	# for newbie test end
	who.hp = who.hpMax
	who.mp = who.mpMax
	who.addHuoli(300, "newbie test", None)
	who.reserveHp = 0	#10000
	who.reserveMp = 0	#10000
	state.addState(who, 102)
	state.addState(who, 103)
	who.attrChange("hp","mp","huoli","reserveHp","reserveMp")
	
	sceneId, x, y, d = newRoleBornData.getPos(who.school)
	who.sceneId = sceneId
	who.x = x
	who.y = y

	if who.isRobot():
		onNewbieForRobot(who)
		
def onNewbieForRobot(who):
	data = robotData.getRandAttrData()
	school = data["门派"]
	shapeList = data["造型"]
	shape = shapeList[rand(len(shapeList))]
	levelList = data["等级"]
	level = levelList[rand(len(levelList))]
	sceneList = data["场景"]
	sceneId = sceneList[rand(len(sceneList))]
	x, y = scene.randSpace(sceneId)
	
	who.set("school", school)
	who.set("shape", shape)
	who.set("shapeParts", role.defines.randShapeParts(shape))
	who.sceneId = sceneId
	who.x = x
	who.y = y
	
	level = level + rand(10)
	for i in xrange(level):
		who.exp += who.expNext
		who.upLevel()

def onNewbieAfterLogin(who):
	if not hasattr(who, "newbie"):
		return
	del who.newbie

	if not task.hasTask(who, 40200):
		task.newTask(who, None, 40200)

def onOffline(who):
	'''玩家下线时
	'''
	activity.onOffline(who)

from common import *
import skill.upgrade
import props.equip
import pet
import task
import activity
import block.numenBag
import state
import robotData
import scene
import role
import openLevel
import role.service
import role.roleConfig
import task.offlineTask
import signIn
import collect
import offlineHandler
import guild
import guide
import activity.center
import buddy
import treasureShop
import trade
import resume
import friend
import newRoleBornData
import tougheningExp